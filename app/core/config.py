from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URL: str = "mongodb://localhost:27017"
    DB_NAME: str = "gallery_db"
    
    S3_ENDPOINT: str = "http://localhost:9000"
    S3_ACCESS_KEY: str = "minioadmin"  # Change to your local key
    S3_SECRET_KEY: str = "minioadmin"  # Change to your local secret
    S3_BUCKET: str = "my-gallery-bucket"
    S3_REGION: str = "us-east-1"

    class Config:
        env_file = ".env"

settings = Settings()