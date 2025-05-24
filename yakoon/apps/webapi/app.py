# yakoon/app/webapi/app.py

from fastapi import FastAPI

from yakoon.apps.webapi.tools.middleware import setup_CORS
from yakoon.apps.webapi.tools.routes import init_routes

app = FastAPI()
setup_CORS(app) 
init_routes(app)

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "yakoon.apps.webapi.app:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=False)
    
    # http://127.0.0.1:8000/docs