import importlib.metadata
import os
from os import path
from typing import Union

from fastapi import FastAPI, Query, applications
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from funcaptcha_solver import funcaptcha, WhisperWebService

WHISPER_WEBSERVICE_ENDPOINT = os.getenv("WHISPER_WEBSERVICE_ENDPOINT", "http://localhost:9000/asr")

projectMetadata = importlib.metadata.metadata('funcaptcha-solver')
app = FastAPI(
    title=projectMetadata['Name'].title().replace('-', ' '),
    description=projectMetadata['Summary'],
    version=projectMetadata['Version'],
    contact={
        "url": projectMetadata['Home-page']
    },
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    license_info={
        "name": "MIT License",
        "url": projectMetadata['License']
    }
)

assets_path = os.getcwd() + "/swagger-ui-assets"
if path.exists(assets_path + "/swagger-ui.css") and path.exists(assets_path + "/swagger-ui-bundle.js"):
    app.mount("/assets", StaticFiles(directory=assets_path), name="static")


    def swagger_monkey_patch(*args, **kwargs):
        return get_swagger_ui_html(
            *args,
            **kwargs,
            swagger_favicon_url="",
            swagger_css_url="/assets/swagger-ui.css",
            swagger_js_url="/assets/swagger-ui-bundle.js",
        )


    applications.get_swagger_ui_html = swagger_monkey_patch


@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def index():
    return "/docs"


@app.post("/token", tags=["Endpoints"])
async def token(
        public_key: str = Query(description="FunCaptcha public key"),
        service_url: Union[str, None] = Query(default="https://roblox-api.arkoselabs.com", description="Some websites can have a custom service URL"),
        proxy: Union[str, None] = Query(default=None, description="A proxy to fetch the token, usually not required"),
        ssl_verify: bool = Query(default=True, description="Verify SSL Certificate"),
):
    proxies = None
    if proxy:
        proxies = {
            'https': proxy,
            'http': proxy,
        }

    return funcaptcha(
        public_key=public_key,
        site=service_url,
        transcriber=WhisperWebService(endpoint=WHISPER_WEBSERVICE_ENDPOINT),
        proxies=proxies,
        ssl_verify=ssl_verify,
    ).solve()
