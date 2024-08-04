from fastapi import FastAPI

from app.application.api.messages.routes import router as message_router


def create_app() -> FastAPI:
    app = FastAPI(
        title='Simple Kafka Chat',
        docs_url='/api/docs',
        debug=True
    )
    app.include_router(message_router, prefix='/chat', tags=['Chat'])

    return app
