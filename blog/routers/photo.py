from fastapi import APIRouter, Depends, status, HTTPException
from fastapi import FastAPI, File, UploadFile
import boto3

router = APIRouter(
    prefix='/user',
    tags=['photos']
)

S3_BUCKET_NAME = 'photo-db'

@router.post("/upload/")
async def upload_file(file: UploadFile):
    s3_client = boto3.client('s3')

    # Generate a unique key for the uploaded file in S3
    s3_key = f"uploads/{file.filename}"

    # Upload the file to S3
    s3_client.upload_fileobj(file.file, S3_BUCKET_NAME, s3_key)

    # Optionally, you can return the S3 URL of the uploaded file
    s3_url = f"https://{'photo-db'}.s3.amazonaws.com/{'arn:aws:s3:::photo-db'}"
    return {"s3_url": s3_url}