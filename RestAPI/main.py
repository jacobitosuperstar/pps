"""
Fast API

Production and Planning Software.
"""
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from router import api_router


def main() -> FastAPI:
    app: FastAPI = FastAPI(
        title="Production & Planning Software",
        default_response_class=ORJSONResponse,
    )
    app.include_router(api_router)
    return app


app: FastAPI = main()


if __name__ == "__main__":
    main()
