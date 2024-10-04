import React from 'react';
import { useDropzone } from 'react-dropzone';
import AWS from 'aws-sdk';
import { toast } from 'react-toastify';

const Dropzone = () => {
    // Configure AWS S3
    const s3 = new AWS.S3({
        accessKeyId: 'accessKey',
        secretAccessKey: 'secretAccessKey',
        region: 'eu-west-2',
    });

    const onDrop = (acceptedFiles) => {
        acceptedFiles.forEach((file) => {
            const params = {
                Bucket: 'recruitment-audio-files',
                Key: file.name,
                Body: file,
                ContentType: file.type,
            };

            s3.upload(params, (err, data) => {
                if (err) {
                    console.error("Error uploading file:", err);
                    toast.error("Error uploading file");
                } else {
                    console.log("Successfully uploaded file:", data);
                    toast.success("File uploaded successfully!");
                }
            });
        });
    };

    const { getRootProps, getInputProps } = useDropzone({ onDrop });

    return (
        <div {...getRootProps()} style={{ border: '2px dashed #cccccc', padding: '20px', textAlign: 'center' }}>
            <input {...getInputProps()} />
            <p>Drag & drop some files here, or click to select files</p>
        </div>
    );
};

export default Dropzone;
