from fastapi import FastAPI
from src.routes.user_address_route import router as user_address_router
from container import Container


def create_app():
    app = FastAPI()
    container = Container()
    container.wire(["src.routes.user_address_route"])

    app.router.include_router(user_address_router)
    return app


app = create_app()
