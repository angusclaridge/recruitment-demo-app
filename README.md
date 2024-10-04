Infra needed

2 x lambda, found in src/lambdas
For the speechToText one you'll need to create a lambda layer using recruitment-layer.zip (see [docs](https://docs.aws.amazon.com/lambda/latest/dg/chapter-layers.html))
Also add a trigger for the speechToText bucket from an s3 bucket
The speechToText summary will need to have a role attached which grants the following permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:CreateLogGroup",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "dynamodb:PutItem",
                "transcribe:*",
                "dynamodb:Scan",
                "s3:ListBucket",
                "bedrock:*"
            ],
            "Resource": "*"
        }
    ]
}
```

1 x api gateway in front of the fetchCandidates lambda -> then add the url for this api to the CandidatesTable component

1 x dynamoDB table

1 x s3 bucket (which triggers the speechToText lambda)

Enable the titan lite model in aws bedrock

1 x iam policy with permissions to upload to s3 - add secret keys to the front end env variables