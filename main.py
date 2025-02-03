from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
# , JSONResponse
from models.url import Url

from typing import Annotated, Union

from fastapi import FastAPI, Header
from fastapi import FastAPI, Form, Request, Header



url_link = Url(url="nie")

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})



@app.get("/url", response_class=HTMLResponse)
async def get_url(request: Request, hx_request: Annotated[Union[str, None], Header()] = None):
    if hx_request:
        return templates.TemplateResponse(
            request=request, name="urlshow.html", context={"url": url_link}
        )


@app.post("/url", response_class=HTMLResponse)
async def create_todo(request: Request, url: Annotated[str, Form()]):
    url_link.url = url
    return templates.TemplateResponse(
        request=request, name="urlshow.html", context={"url": url_link}
    )


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
