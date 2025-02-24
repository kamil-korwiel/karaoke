from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
# , JSONResponse
from models.audio import Audio
from models.url import Url

from typing import Annotated, Union

from fastapi import FastAPI, Header
from fastapi import FastAPI, Form, Request, Header

from sqlmodel import create_engine , Session 

import os
from loguru import logger
from utility import download_video, check_url, init_db
from pathlib import Path

""" This is set up database """
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


init_db(engine,sqlite_file_name,sqlite_url)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

url_link = Url(url="")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})

@app.get("/download/")
async def download_file():
    with Session(engine) as session:
        audio_info = session.get(Audio,1)
    file_path = Path(audio_info.file_path)
    logger.debug(file_path)
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    return FileResponse(file_path,media_type="audio/wav", filename=audio_info.full_title)


# @app.get("/url", response_class=HTMLResponse)
# async def get_url(request: Request, hx_request: Annotated[Union[str, None], Header()] = None):
#     if hx_request:
#         return templates.TemplateResponse(
#             request=request, name="urlshow.html", context={"url": url_link}
#         )

# @app.post("/url", response_class=HTMLResponse)
# async def create_todo(request: Request, url: Annotated[str, Form()]):
#     if check_url(url):
#         download_video(logger,url)
    
#     return templates.TemplateResponse(
#         request=request, name="urlshow.html", context={"url": url_link}
#     )

@app.get("/audio", response_class=HTMLResponse)
async def get_audio(request: Request, hx_request: Annotated[Union[str, None], Header()] = None):
    with Session(engine) as session:
        audio_info = session.get(Audio,1)

    if hx_request:
        return templates.TemplateResponse(
            request=request, name="audio.html", context={ 'audio_info': audio_info }
        )
    

# @app.get("/audio_list", response_class=HTMLResponse)
# async def get_audio(request: Request, hx_request: Annotated[Union[str, None], Header()] = None):
#     # ? How to cashing out a data
#     with Session(engine) as session:
#         statement = select(Audio)
#         results = session.exec(statement)
    
#     if hx_request:
#         return templates.TemplateResponse(
#             request=request, name="audio.html"
#         )


# @app.put("/todos/{todo_id}", response_class=HTMLResponse)
# async def update_todo(request: Request, todo_id: str, text: Annotated[str, Form()]):
#     for index, todo in enumerate(todos):
#         if str(todo.id) == todo_id:
#             todo.text = text
#             break
#     return templates.TemplateResponse(
#         request=request, name="todos.html", context={"todos": todos}
#     )


# @app.post("/todos/{todo_id}/toggle", response_class=HTMLResponse)
# async def toggle_todo(request: Request, todo_id: str):
#     for index, todo in enumerate(todos):
#         if str(todo.id) == todo_id:
#             todos[index].done = not todos[index].done
#             break
#     return templates.TemplateResponse(
#         request=request, name="todos.html", context={"todos": todos}
#     )


# @app.post("/todos/{todo_id}/delete", response_class=HTMLResponse)
# async def delete_todo(request: Request, todo_id: str):
#     for index, todo in enumerate(todos):
#         if str(todo.id) == todo_id:
#             del todos[index]
#             break
#     return templates.TemplateResponse(
#         request=request, name="todos.html", context={"todos": todos}
#     )
