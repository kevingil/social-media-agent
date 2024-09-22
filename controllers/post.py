from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.campaign import Media, Post, Campaign
from utils.agent.writter import WrittingAgent
from utils.agent.vision import VisionAgent

router = APIRouter()
templates = Jinja2Templates(directory="./templates")

# Create agent instance
writter = WrittingAgent()
vision = VisionAgent()
  
@router.post("/post/generate", name="generate_post", response_class=HTMLResponse)
async def generate_post(
    request: Request, campaign_id: int = Form(...), prompt: str = Form(...)
):
    # Get all media for the campaign
    media_query = Media({})
    all_media = media_query.get_all_by_campaign(campaign_id)

    # Delete all existing posts for the campaign to start over
    post = Post({})
    existing_posts = post.get_all_by_campaign(campaign_id)
    for existing_post in existing_posts:
        post.delete_post(existing_post['id'])

    # Create a post for each media
    for media in all_media:
        image_url = f"{media['key']}"
        target_platform = "Instagram"
        
        # AI description of the image
        if media['description'] == "":
            media_description = vision.describe_image(image_url)
            media_query.add_description(media['id'], media_description)
            print(f"MediaID: {media['id']}. using existing image description.")

        else: 
            media_description = media['description']
            print(f"MediaID: {media['id']}. using existing image description.")
            
        # Text generation
        campaign_data = Campaign({}).get_campaign(campaign_id)
        post_text = writter.generate_post(campaign_data, media_description)

        
        post_data = {
            "campaign_id": campaign_id,
            "post_date": "2022-01-01 00:00:00",
            "target_platform": target_platform,
            "media_id": media['id'],
            "text_content": post_text.content
        }
        
        new_post = Post(post_data)
        post_id = new_post.create_post()
        media['post_id'] = post_id 
        media_query.update_media(media['id'], post_id)
        
        
    # Update campaign with prompt 
    campaign_data = Campaign({}).get_campaign(campaign_id)
    campaign_data['user_prompt'] = prompt
    Campaign(campaign_data).update_campaign(campaign_id)
    post_list = post.get_all_by_campaign(campaign_id)

    # Render the updated media container
    return templates.TemplateResponse(
        "components/generate.html",
        {"request": request, "campaign_id": campaign_id, "post_list": post_list, "campaign_prompt": prompt},
    )
