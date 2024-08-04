from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from punq import Container

from app.application.api.chat.schemas import CreateChatRequestSchema, CreateChatResponseSchema
from app.application.schemas import ErrorSchema
from app.domain.entities.chat import Chat
from app.domain.exceptions.base import ApplicationException
from app.logic.commands.chat import CreateChatCommand
from app.logic.init import init_container
from app.logic.mediator import Mediator

router = APIRouter()


@router.post(
    path='',
    summary='Создает новый чат',
    description='Создает новый чат, если чат с таким названием существует, то возвращается 400 ошибка',
    response_model=CreateChatResponseSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {'model': CreateChatResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def create_chat_route(
        schema: CreateChatRequestSchema,
        container: Annotated[Container, Depends(init_container)]
):
    mediator: Mediator = container.resolve(Mediator)
    command = CreateChatCommand(title=schema.title)

    try:
        chats = await mediator.handle_command(command)
        chat: Chat = chats[0]
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    return CreateChatResponseSchema.from_entity(chat)
