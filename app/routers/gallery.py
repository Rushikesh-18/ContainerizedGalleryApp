from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from typing import List

# Import our service logic
from app.services import media_service

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def view_gallery(request: Request):
    # Call Service
    media_docs = media_service.get_all_media()
    
    # Transform data for UI
    files = []
    for doc in media_docs:
        files.append({
            "name": doc["filename"],
            "url": f"/media/{doc['filename']}", # Points to the proxy route below
            "type": doc["content_type"]
        })
        
    return templates.TemplateResponse("index.html", {"request": request, "files": files})

@router.get("/media/{filename}")
async def stream_media(filename: str):
    try:
        # Call Service
        stream, content_type = media_service.get_media_stream(filename)
        return StreamingResponse(stream, media_type=content_type)
    except Exception:
        raise HTTPException(status_code=404, detail="File not found")

@router.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    for file in files:
        # Call Service
        success = media_service.upload_media_item(file)
        if not success:
            raise HTTPException(status_code=500, detail=f"Failed to upload {file.filename}")
            
    return HTMLResponse(content=f"<script>window.location.href = '/';</script>", status_code=200)