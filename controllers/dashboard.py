from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.campaign import Campaign
from models.brand import Brand

router = APIRouter()

templates = Jinja2Templates(directory="./templates")

@router.get("/dashboard", name="dashboard", response_class=HTMLResponse)
def user(request: Request):
    if "user" in request.session:
        user = request.session["user"]
        campaigns = Campaign({}).get_all_by_user(user[0])
        brands = Brand({}).get_all_brands()
        return templates.TemplateResponse("dashboard.html", {
        "request": request, "brands": brands, "user_data": user, "campaigns": campaigns})
    else:
        return RedirectResponse("/login")
