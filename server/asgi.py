# import os
#
# from django.apps import apps
# from django.conf import settings
# from django.core.wsgi import get_wsgi_application
# from fastapi import FastAPI
# from fastapi.middleware.wsgi import WSGIMiddleware
# from starlette.middleware.cors import CORSMiddleware
#
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
# apps.populate(settings.INSTALLED_APPS)
#
# from api.router import api_router
#
#
# def get_application() -> FastAPI:
#     main_app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG, docs_url="/api/v0/docs")
#     main_app.add_middleware(
#         CORSMiddleware,
#         allow_origins=settings.ALLOWED_HOSTS or ["*"],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )
#     main_app.include_router(api_router, prefix="/api")
#     main_app.mount("", WSGIMiddleware(get_wsgi_application()))
#
#     return main_app
#
#
# app = get_application()
