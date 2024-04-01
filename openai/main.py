import openai as openai
from openai import OpenAI
from dotenv import load_dotenv
import os
from fastapi import FastAPI, Form, Request
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

openai = OpenAI(api_key=api_key)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
chat_response = []


@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "chat_response": chat_response})


chat_log = [
    {
        "role": "system",
        "content": "You are a Python tutor AI, completely dedicated to teaching users how to learn Python from scratch. Please provide clear instructions on Python concepts, best  practices, and syntax. Help create a path of learning for users to be able to create real-life, production-ready Python applications.",
    }]


@app.post("/", response_class=HTMLResponse)
async def chat(request: Request, user_input: Annotated[str, Form()]):
    chat_log.append({"role": "user", "content": user_input})
    chat_response.append(user_input)
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo", messages=chat_log, temperature=0.6
    )
    bot_response = response.choices[0].message.content
    chat_log.append({"role": "assistant", "content": bot_response})
    chat_response.append(bot_response)
    return templates.TemplateResponse("home.html", {"request": request, "chat_response": chat_response})


@app.get("/image", response_class=HTMLResponse)
async def image_page(request: Request):
    return templates.TemplateResponse("image.html", {"request": request})


@app.post("/image", response_class=HTMLResponse)
async def create_image(request: Request, user_input: Annotated[str, Form()]):
    response = openai.images.generate(
        prompt=user_input,
        n=1,
        size="512x512")
    image_url = response.data[0].url
    return templates.TemplateResponse("image.html", {"request": request, "image_url": image_url})
