from fastapi import Form

from main import app


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    ...


@app.post("/signup")
async def signup(username: str = Form(...), password: str = Form(...)):
    return {"message": f"Пользователь {username} зарегистрирован!"}