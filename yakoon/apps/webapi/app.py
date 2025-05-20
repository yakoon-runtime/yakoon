# yakoon/app/webapi/app.py

from fastapi import FastAPI
from yakoon.apps.webapi.endpoints import command

app = FastAPI()
 

# Include routes
def init_routes():
    app.include_router(command.router, prefix="/command")

init_routes()

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "yakoon.apps.webapi.app:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=False)
    
    # http://127.0.0.1:8000/docs