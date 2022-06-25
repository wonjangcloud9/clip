from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="view")


@app.get("/")
async def index():
    return {"response": "Hi"}


@app.get('/login', response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})
