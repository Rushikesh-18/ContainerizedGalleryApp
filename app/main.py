from fastapi import FastAPI
from app.routers import gallery
from app.core.database import ensure_bucket_exists

app = FastAPI(title="My Local Media Gallery")

# Initialize S3 Bucket on startup
@app.on_event("startup")
def startup_event():
    ensure_bucket_exists()

# Include our routes
app.include_router(gallery.router)

if __name__ == "__main__":
    import uvicorn
    # Run from the root directory: python -m app.main
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)