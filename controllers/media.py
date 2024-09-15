from fastapi import Request, Form, APIRouter, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.campaign import Media
from typing import List
import os

router = APIRouter()

templates = Jinja2Templates(directory="./templates")


@router.post("/media/upload", name="media_upload", response_class=HTMLResponse)
async def upload_media(
    request: Request, campaign_id: int = Form(...), files: List[UploadFile] = File(...)
):
    media_list = []
    os.makedirs("static/media", exist_ok=True)

    for file in files:
        # Generate a unique filename
        filename = f"{campaign_id}_{file.filename}"
        file_path = f"/static/media/{filename}"

        # Save the file
        with open(f".{file_path}", "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Create media entry
        media_data = {
            "key": file_path,
            "description": "",  
            "campaign_id": campaign_id,
        }

        media = Media(media_data)
        media.create_media()


    # Fetch all media for this campaign
    media_query = Media({})
    all_media = media_query.get_all_by_campaign(campaign_id)

    # Return the updated template
    return templates.TemplateResponse(
        "components/media.html",
        {"request": request, "campaign_id": campaign_id, "media_list": all_media},
    )
