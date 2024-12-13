from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Подключение папок для статических файлов и шаблонов
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/login")
async def post_login(username: str = Form(...), password: str = Form(...)):
    # Здесь будет проверка пользователя
    return {"message": f"Пользователь {username} вошёл!"}


@app.post("/register")
async def post_register(username: str = Form(...), password: str = Form(...)):
    # Здесь будет регистрация пользователя
    return {"message": f"Пользователь {username} зарегистрирован!"}