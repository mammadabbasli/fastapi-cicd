from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import boto3
import io

app = FastAPI()

BUCKET_NAME = "fastapi-storage-az"
s3_client = boto3.client('s3', region_name='eu-north-1')

@app.get("/")
def read_root():
    return {"message": "FastAPI with S3!"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file to S3"""
    contents = await file.read()
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=file.filename,
        Body=contents
    )
    return {"message": f"Uploaded {file.filename} to S3"}

@app.get("/files")
def list_files():
    """List all files in S3 bucket"""
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    files = []
    if 'Contents' in response:
        files = [obj['Key'] for obj in response['Contents']]
    return {"files": files}

@app.get("/download/{filename}")
def download_file(filename: str):
    """Download a file from S3"""
    response = s3_client.get_object(Bucket=BUCKET_NAME, Key=filename)
    return StreamingResponse(
        io.BytesIO(response['Body'].read()),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.delete("/delete/{filename}")
def delete_file(filename: str):
    """Delete a file from S3"""
    s3_client.delete_object(Bucket=BUCKET_NAME, Key=filename)
    return {"message": f"Deleted {filename}"}
