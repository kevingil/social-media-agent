from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.campaign import Campaign, Media, Post
from models.brand import Brand

router = APIRouter()

templates = Jinja2Templates(directory="./templates")

# For new campaigns
@router.get(
    "/dashboard/campaign/form", name="campaign_form", response_class=HTMLResponse
)
def campaign_form(request: Request):
    product_brands = Brand({}).get_all_brands()
    campaign = None
    return templates.TemplateResponse(
        "campaign_form.html", {"request": request, "campaign": campaign, "product_brands": product_brands}
    )

@router.post(
    "/dashboard/campaign/form",
    name="campaign_form_submit",
    response_class=RedirectResponse,
)
async def campaign_form_submit(
    request: Request,
    title: str = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...),
    product_brand_id: int = Form(...),
    objectives: str = Form(...),
    target_platforms: str = Form(...),
    target_audience: str = Form(...),
    key_messages: str = Form(...),
    hashtags: str = Form(None),
    user_prompt: str = Form(None),
    campaign_id: int = Form(None),
):
    campaign_data = {
        "title": title,
        "start_date": start_date,
        "end_date": end_date,
        "product_brand_id": product_brand_id,
        "objectives": objectives,
        "target_platforms": target_platforms,
        "target_audience": target_audience,
        "key_messages": key_messages,
        "hashtags": hashtags,
        "user_prompt": user_prompt,
        "user_id": request.session["user"][0],
    }
    
    if campaign_id:
        campaign = Campaign(campaign_data)
        campaign.update_campaign(campaign_id)
    else:
        campaign = Campaign(campaign_data)
        campaign.create_campaign()
        campaign_id = campaign.db.get_last_insert_id()
    
    return RedirectResponse(url=f"/dashboard/campaign/{campaign_id}", status_code=303)


@router.get(
    "/dashboard/campaign/{campaign_id}", name="campaign", response_class=HTMLResponse
)
def campaign(request: Request, campaign_id: int):
    campaign = Campaign({}).get_campaign(campaign_id)
    if campaign is None:
        return RedirectResponse("/dashboard")
    media_query = Media({})
    all_media = media_query.get_all_by_campaign(campaign_id)
    post_list = Post({}).get_all_by_campaign(campaign_id)
    product_brands = Brand({}).get_all_brands()

    return templates.TemplateResponse(
        "campaign.html",
        {
            "request": request,
            "campaign": campaign,
            "media_list": all_media,
            "post_list": post_list,
            "product_brands": product_brands
        },
    )


# For existing campaigns
@router.get(
    "/dashboard/campaign/form/{campaign_id}",
    name="campaign_form_edit",
    response_class=HTMLResponse,
)
def campaign_form_edit(request: Request, campaign_id: int):
    campaign = Campaign({}).get_campaign(campaign_id)
    if campaign is None:
        return RedirectResponse("/dashboard")
    product_brands = Brand({}).get_all_brands()

    return templates.TemplateResponse(
        "campaign_form.html", {"request": request, "campaign": campaign, "product_brands": product_brands}
    )


@router.post(
    "/dashboard/campaign/form/{campaign_id}",
    name="campaign_form_edit_submit",
    response_class=RedirectResponse,
)
async def campaign_form_edit_submit(
    request: Request,
    campaign_id: int,
    title: str = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...),
    product_brand_id: int = Form(...),
    objectives: str = Form(...),
    target_platforms: str = Form(...),
    target_audience: str = Form(...),
    key_messages: str = Form(...),
    hashtags: str = Form(None),
    user_prompt: str = Form(None)
):
    campaign_data = {
        "title": title,
        "start_date": start_date,
        "end_date": end_date,
        "product_brand_id": product_brand_id,
        "objectives": objectives,
        "target_platforms": target_platforms,
        "target_audience": target_audience,
        "key_messages": key_messages,
        "hashtags": hashtags,
        "user_prompt": user_prompt,
        "user_id": request.session["user"][0],
    }
    campaign = Campaign(campaign_data)
    campaign.update_campaign(campaign_id)
    return RedirectResponse(url=f"/dashboard/campaign/{campaign_id}", status_code=303)


@router.post(
    "/dashboard/campaign/form/{campaign_id}/delete",
    name="campaign_form_delete_submit",
    response_class=RedirectResponse,
)
async def campaign_form_delete_submit(request: Request, campaign_id: int):
    campaign_query = Campaign({})
    campaign_query.delete_campaign(campaign_id)
    return RedirectResponse(url=f"/dashboard", status_code=303)
