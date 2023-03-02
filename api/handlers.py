from logging import getLogger
from hashing import Hasher

from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi import HTTPException

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import (
    UserCreate, UserShow, DeleteUserResponse,
    UpdatedUserResponse, UserUpdate
)
from db.dals import UserDAL
from db.session import get_db


logger = getLogger(__name__)

user_router = APIRouter()


async def _create_new_user(body: UserCreate, db) -> UserShow:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                name=body.name,
                surname=body.surname,
                email=body.email,
                hashed_password=Hasher.get_password_hash(body.password)
            )
            return UserShow(
                user_id=user.user_id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_active=user.is_active
            )


async def _get_user_by_id(user_id, db) -> Union[UserShow, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get_user_by_id(user_id)
            if user is not None:
                return UserShow(
                    user_id=user.user_id,
                    name=user.name,
                    surname=user.surname,
                    email=user.email,
                    is_active=user.is_active
                )


async def _update_user(body: UserUpdate, user_id: UUID, db) -> Union[UUID, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            updated_user_id = await user_dal.update_user(
                user_id, **body.dict(exclude_none=True)
            )
            return updated_user_id


async def _delete_user(user_id, db) -> Union[UUID, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            deleted_user_id = await user_dal.delete_user(
                user_id=user_id
            )
            return deleted_user_id


@user_router.post('/', response_model=UserShow)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> UserShow:
    try:
        return await _create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=400, detail="User with this email already exists.")


@user_router.delete('/', response_model=DeleteUserResponse)
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)) -> DeleteUserResponse:
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(status_code=404, detail="User with given credentials was not found.")
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


@user_router.get('/', response_model=UserShow)
async def get_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_db)) -> UserShow:
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User with given credentials was not found.")
    return user


@user_router.patch('/', response_model=UpdatedUserResponse)
async def update_user_by_id(
    user_id: UUID, body: UserUpdate, db: AsyncSession = Depends(get_db)
) -> UpdatedUserResponse:
    if body.dict(exclude_none=True) == {}:
        raise HTTPException(
            status_code=422, detail="At least one parameter should be provided."
        )
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User with given credentials was not found.")
    try:
        updated_user_id = await _update_user(body, user_id, db)
        return UpdatedUserResponse(updated_user_id=updated_user_id)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=400, detail="User with this email already exists.")
