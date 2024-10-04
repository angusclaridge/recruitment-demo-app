# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
import json
import urllib.parse
import boto3
import time
import requests
import uuid

print('Loading function')

s3 = boto3.client('s3')

transcribe = boto3.client('transcribe')

bedrock = boto3.client('bedrock')
bedrock_runtime = boto3.client(service_name = 'bedrock-runtime', region_name = 'eu-west-2')


dynamodb = boto3.resource('dynamodb')
table_name = 'Candidate'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    media_uri = f"s3://{bucket}/{key}"
    try:
        job_name = "TranscriptionJob" + str(context.aws_request_id)
        response = transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': media_uri},
            MediaFormat='m4a',  # Specify the format of the audio file
            LanguageCode='en-US',  # Change to the appropriate language code
        )
        
        while True:
            response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            status = response['TranscriptionJob']['TranscriptionJobStatus']
            
            if status in ['COMPLETED', 'FAILED']:
                break
            
            # Wait before polling again
            time.sleep(2)  # Wait for 2 seconds before checking again
        
        # Check if the job was successful
        if status == 'COMPLETED':
            transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
            transcript_response = requests.get(transcript_uri)
            transcript_json = transcript_response.json()
            transcription_text = transcript_json['results']['transcripts'][0]['transcript']
            
            model_id = 'amazon.titan-text-lite-v1'
            prompt = f"Extract the person's name and job requirements from this :\n\n{transcription_text}.\nPresent in the format \"Name: person's name\"\n\"Requirements: list of requirements\""
            body = json.dumps(
               {
                  "inputText": prompt, 
                  "textGenerationConfig": {
                      "maxTokenCount": 4096,
                      "stopSequences": [],
                      "temperature": 0.0,
                      "topP": 0.1
                  }
               }
            )
            response = bedrock_runtime.invoke_model(
               body=body, 
               modelId=model_id, 
               accept='application/json', 
               contentType='application/json'
            )
            
                
            response_body = json.loads(response.get('body').read())
             # The response from the model now mapped to the answer
            answer = response_body['results'][0]['outputText']
            
            candidate = {
                'candidate-key': str(uuid.uuid4()),
                "name": answer.split("Person: ")[1].split()[0].split("\\n")[0],
                "summary": answer.split("Requirements:")[1]
            }
            
            response = table.put_item(Item=candidate)
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Transcription job completed successfully',
                    'transcript_text': transcription_text,
                    'summary': answer
                })
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'message': 'Transcription job failed',
                    'error': response['TranscriptionJob']['FailureReason']
                })
            }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error starting transcription job',
                'error': str(e)
            })
        }
              
