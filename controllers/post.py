from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.campaign import Media, Post
from typing import List
import os

router = APIRouter()

templates = Jinja2Templates(directory="./templates")


@router.post("/post/generate", name="generate_post", response_class=HTMLResponse)
async def generate_post(
    request: Request, campaign_id: int = Form(...), prompt: str = Form(...)
):
    # Get all media for the campaign
    media_query = Media({})  
    all_media = media_query.get_all_by_campaign(campaign_id)

    # Delete all existing posts for the campaign
    post = Post({})
    existing_posts = post.get_all_by_campaign(campaign_id)
    for existing_post in existing_posts:
        post.delete_post(existing_post['id'])

    # Create a test post object and create a post for each media
    for media in all_media:
        test_post_data = {
            "campaign_id": campaign_id,
            "date": "2022-01-01 00:00:00",
            "target_platform": "Instagram",
            "media_id": media['id'],
            "text_content": f"Test post for Instagram with prompt: {prompt}",
        }
        new_post = Post(test_post_data)
        new_post.create_post()
    
    post_list = post.get_all_by_campaign(campaign_id)

    # Render the updated media container
    return templates.TemplateResponse(
        "components/generate.html",
        {"request": request, "campaign_id": campaign_id, "post_list": post_list, "campaign_prompt": prompt},
    )
