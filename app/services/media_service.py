from fastapi import UploadFile
from app.core.database import s3_client, media_collection, settings
from app.core.config import settings

def get_all_media():
    """Fetch all media metadata from DB"""
    return list(media_collection.find().sort("_id", -1))

def get_media_stream(filename: str):
    """Get the raw file stream from S3"""
    file_obj = s3_client.get_object(Bucket=settings.S3_BUCKET, Key=filename)
    return file_obj['Body'], file_obj.get('ContentType', 'application/octet-stream')

def upload_media_item(file: UploadFile):
    """Upload to S3 and save metadata to Mongo"""
    try:
        # 1. Upload to S3
        s3_client.upload_fileobj(
            file.file,
            settings.S3_BUCKET,
            file.filename,
            ExtraArgs={'ContentType': file.content_type}
        )
        
        # 2. Save to Mongo
        media_data = {
            "filename": file.filename,
            "content_type": "video" if "video" in file.content_type else "image",
            "size": file.size
        }
        media_collection.insert_one(media_data)
        return True
    except Exception as e:
        print(f"Service Error: {e}")
        return False