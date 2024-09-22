from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from models.user import User
from fastapi.templating import Jinja2Templates
from utils.auth import check_user

router = APIRouter()

templates = Jinja2Templates(directory="./templates")


@router.get("/", name="home", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/login", name="login", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", name="login", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = check_user(username, password)
    if user:
        request.session["user"] = user
        return RedirectResponse(url="/dashboard", status_code=302)
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid username or password"})
    
    
@router.get("/logout", name="logout", response_class=RedirectResponse)
def logout(request: Request):
    request.session.pop("user")
    return RedirectResponse(url="/", status_code=302)

@router.get("/signup", name="signup", response_class=HTMLResponse)
def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@router.post("/user-processing", response_class=RedirectResponse)
def user_processing(
    username: str = Form(),
    first_name: str = Form(),
    last_name: str = Form(),
    password: str = Form(),
):
    user_data = {
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "password": password,
    }

    user_db = User(user_data)
    user_db.create_user()

    return RedirectResponse("/login")
