from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from punq import Container

from app.application.api.chat.schemas import (
    CreateChatSchema,
    CreateChatResponseSchema,
    CreateMessageSchema,
    CreateMessageResponseSchema,
)
from app.application.schemas import ErrorSchema
from app.domain.exceptions.base import ApplicationException
from app.logic.commands.chat import CreateChatCommand
from app.logic.commands.message import CreateMessageCommand
from app.logic.exceptions.chat import ChatNotFound
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
        schema: CreateChatSchema,
        container: Annotated[Container, Depends(init_container)]
):
    mediator: Mediator = container.resolve(Mediator)
    command = CreateChatCommand(title=schema.title)

    try:
        chat, *_ = await mediator.handle_command(command)
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    return CreateChatResponseSchema.from_entity(chat)


@router.post(
    path='/{chat_oid}/messages',
    status_code=status.HTTP_201_CREATED,
    summary='Добавляет новое сообщение в чат',
    description='Добавляет новое сообщение в чат',
    responses={
        status.HTTP_201_CREATED: {'model': CreateChatResponseSchema},
        status.HTTP_404_NOT_FOUND: {'model': ErrorSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
    response_model=CreateMessageResponseSchema
)
async def create_message_route(
        chat_oid: str,
        schema: CreateMessageSchema,
        container: Annotated[Container, Depends(init_container)]
):
    mediator: Mediator = container.resolve(Mediator)
    command = CreateMessageCommand(chat_oid=chat_oid, text=schema.text)

    try:
        message, *_ = await mediator.handle_command(command)
    except ChatNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    return CreateMessageResponseSchema.from_entity(message)
