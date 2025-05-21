
from yakoon.apps.webapi.endpoints import command

# Include routes
def init_routes(app):
    app.include_router(command.router, prefix="/command")
