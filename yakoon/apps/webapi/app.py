# yakoon/app/webapi/app.py

from fastapi import FastAPI
from yakoon.apps.webapi.endpoints import command

app = FastAPI()

# Include routes
def init_routes():
    app.include_router(command.router, prefix="/command")

init_routes()
