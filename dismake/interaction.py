from __future__ import annotations

from typing import Any, List, Optional, TYPE_CHECKING, Union
from fastapi import Request
from pydantic import BaseModel, validator

from .types import SnowFlake
from .models import Member, User, Guild, Channel


if TYPE_CHECKING:
    from .client import Bot
    from .commands import SlashCommand

__all__ = ("Interaction", "ApplicationCommandData", "ApplicationCommandOption")


class ResolvedData(BaseModel):
    users: Optional[Any]
    members: Optional[Any]
    channels: Optional[Any]
    roles: Optional[Any]
    messages: Optional[Any]
    attachments: Optional[Any]


class ApplicationCommandOption(BaseModel):
    name: str
    type: int
    value: Optional[Union[str, int, float, bool]]
    options: Optional[List[ApplicationCommandOption]]
    focused: bool = False


class ApplicationCommandData(BaseModel):
    id: SnowFlake
    name: str
    type: int
    resolved: Optional[ResolvedData]
    options: Optional[List[ApplicationCommandOption]]
    guild_id: Optional[SnowFlake]
    target_id: Optional[SnowFlake]


class MessageComponentData(BaseModel):
    custom_id: str
    component_type: int
    # values?*	array of select option values	values the user selected in a select menu component


class ModalSubmitData(BaseModel):
    custom_id: str
    # components	array of message components	the values submitted by the user


class Interaction(BaseModel):
    request: Request
    id: SnowFlake
    application_id: SnowFlake
    type: int
    guild_id: Optional[int]
    channel: Optional[Any]
    channel_id: Optional[SnowFlake]
    member: Optional[Member]
    user: Optional[User]
    token: str
    version: int
    message: Optional[Any]
    app_permissions: Optional[str]
    locale: Optional[str]
    guild_locale: Optional[str]

    @property
    def author(self) -> Union[Member, User]:
        if self.guild_id:
            assert self.member is not None
            return self.member
        assert self.user is not None
        return self.user

    
    @validator('channel')
    def validate_channel(cls, value: SnowFlake) -> Optional[Channel]:
        ...

    async def fetch_guild(self) -> Guild:
        assert self.guild_id is not None, "Guild id is none."
        return await self.bot.fetch_guild(self.guild_id)

    @property
    def bot(self) -> Bot:
        return self.request.app

    class Config:
        arbitrary_types_allowed = True
