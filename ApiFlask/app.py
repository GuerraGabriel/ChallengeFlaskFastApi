from flask import Flask
from src.models.base import Base
from src.routes.user_address_route import blueprint as user_bp
from container import Container


def create_app():
    app = Flask(__name__)
    container = Container()
    sa_engine = container.sa_engine()
    Base.metadata.create_all(sa_engine)

    app.container = container
    app.register_blueprint(user_bp, url_prefix="/users")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
