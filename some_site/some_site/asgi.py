import os
from django.core.asgi import get_asgi_application
from blog.routers import api_router

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "some-site.settings")

django_asgi_app = get_asgi_application()

from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware

app = FastAPI()
app.mount("/api", WSGIMiddleware(django_asgi_app))

app.include_router(api_router)
   
uvicorn.run(app)