"""
FastAPI

Production and Planning Software.
"""

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from router import api_router
from settings import settings
from database import DeclarativeBase, engine

def main() -> FastAPI:
    app = FastAPI(
        title="Production & Planning Software",
        default_response_class=ORJSONResponse,
    )
    app.include_router(api_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.backend_cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    DeclarativeBase.metadata.create_all(engine)
    return app

app: FastAPI = main()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    # uvicorn.run("main:app", host="localhost", port=8000, reload=True)
