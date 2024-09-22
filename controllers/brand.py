from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.brand import Brand

router = APIRouter()

templates = Jinja2Templates(directory="./templates")

@router.get("/dashboard/brands", name="brands", response_class=HTMLResponse)
def brands(request: Request):
    if "user" in request.session:
        user = request.session["user"]
        brands = Brand({}).get_all_brands()
        return templates.TemplateResponse("brands.html", {"request": request, "user_data": user, "brands": brands})
    else:
        return RedirectResponse("/login")

@router.get("/dashboard/brand/form", name="brand_form", response_class=HTMLResponse)
def brand_form(request: Request):
    brand = None
    return templates.TemplateResponse("brand_form.html", {"request": request, "brand": brand})

@router.post("/dashboard/brand/form", name="brand_form_submit", response_class=RedirectResponse)
async def brand_form_submit(
    request: Request,
    name: str = Form(...),
    type: str = Form(...),
    description: str = Form(...),
    industry: str = Form(...),
    website_url: str = Form(...),
    location: str = Form(...),
    target_audience: str = Form(...),
    mission_statement: str = Form(...),
    unique_selling_proposition: str = Form(...),
    competitors: str = Form(...),
    product_categories: str = Form(...),
    distribution_channels: str = Form(...),
    key_values: str = Form(...),
    brand_id: int = Form(None),
):
    brand_data = {
        "name": name,
        "type": type,
        "description": description,
        "industry": industry,
        "website_url": website_url,
        "location": location,
        "target_audience": target_audience,
        "mission_statement": mission_statement,
        "unique_selling_proposition": unique_selling_proposition,
        "competitors": competitors,
        "product_categories": product_categories,
        "distribution_channels": distribution_channels,
        "key_values": key_values,
    }
    if brand_id:
        brand = Brand(brand_data)
        brand.update_brand(brand_id)
    else:
        brand = Brand(brand_data)
        brand.create_brand()
        brand_id = brand.get_last_insert_id()
    return RedirectResponse(url=f"/dashboard/brand/{brand_id}", status_code=303)

@router.get("/dashboard/brand/{brand_id}", name="brand", response_class=HTMLResponse)
def brand(request: Request, brand_id: int):
    brand = Brand({}).get_brand(brand_id)
    if brand is None:
        return RedirectResponse("/dashboard/brands")
    return templates.TemplateResponse("brand.html", {"request": request, "brand": brand})

@router.get("/dashboard/brand/form/{brand_id}", name="brand_form_edit", response_class=HTMLResponse)
def brand_form_edit(request: Request, brand_id: int):
    brand = Brand({}).get_brand(brand_id)
    if brand is None:
        return RedirectResponse("/dashboard/brands")
    return templates.TemplateResponse("brand_form.html", {"request": request, "brand": brand})

@router.post("/dashboard/brand/form/{brand_id}", name="brand_form_edit_submit", response_class=RedirectResponse)
async def brand_form_edit_submit(
    request: Request,
    brand_id: int,
    name: str = Form(...),
    type: str = Form(...),
    description: str = Form(...),
    industry: str = Form(...),
    website_url: str = Form(...),
    location: str = Form(...),
    target_audience: str = Form(...),
    mission_statement: str = Form(...),
    unique_selling_proposition: str = Form(...),
    competitors: str = Form(...),
    product_categories: str = Form(...),
    distribution_channels: str = Form(...),
    key_values: str = Form(...),
):
    brand_data = {
        "name": name,
        "type": type,
        "description": description,
        "industry": industry,
        "website_url": website_url,
        "location": location,
        "target_audience": target_audience,
        "mission_statement": mission_statement,
        "unique_selling_proposition": unique_selling_proposition,
        "competitors": competitors,
        "product_categories": product_categories,
        "distribution_channels": distribution_channels,
        "key_values": key_values,
    }
    brand = Brand(brand_data)
    brand.update_brand(brand_id)
    return RedirectResponse(url=f"/dashboard/brand/{brand_id}", status_code=303)

@router.post("/dashboard/brand/form/{brand_id}/delete", name="brand_form_delete_submit", response_class=RedirectResponse)
async def brand_form_delete_submit(request: Request, brand_id: int):
    Brand({}).delete_brand(brand_id)
    return RedirectResponse(url="/dashboard/brands", status_code=303)
