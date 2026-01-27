
from yakoon.apps.webapi.app import run_web_api


if __name__ == "__main__":
    run_web_api("127.0.0.1", 8000, reload=False)