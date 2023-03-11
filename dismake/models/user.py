from __future__ import annotations
from typing import Optional
from ..asset import Asset

from pydantic import BaseModel


__all__ = ("User",)

FLAGS_MAPPING = {
    1 << 0: "STAFF",
    1 << 1: "PARTNER",
    1 << 2: "HYPESQUAD",
    1 << 3: "BUG_HUNTER_LEVEL_1",
    1 << 6: "HYPESQUAD_ONLINE_HOUSE_1",
    1 << 7: "HYPESQUAD_ONLINE_HOUSE_2",
    1 << 8: "HYPESQUAD_ONLINE_HOUSE_3",
    1 << 9: "PREMIUM_EARLY_SUPPORTER",
    1 << 10: "TEAM_PSEUDO_USER",
    1 << 14: "BUG_HUNTER_LEVEL_2",
    1 << 16: "VERIFIED_BOT",
    1 << 17: "VERIFIED_DEVELOPER",
    1 << 18: "CERTIFIED_MODERATOR",
    1 << 19: "BOT_HTTP_INTERACTIONS",
    1 << 22: "ACTIVE_DEVELOPER",
}


class User(BaseModel):
    id: int
    username: str
    display_name: Optional[str]
    discriminator: int
    avatar: Optional[str]
    avatar_decoration: Optional[str]
    bot: bool
    bio: str
    system: Optional[bool]
    banner: Optional[str]
    ancent_color: Optional[int]
    locale: str
    verified: bool
    email: str | None
    flags: int
    premium_type: int
    public_flags: int

    @property
    def get_flags(self) -> Optional[list[str | None]]:
        _flag_names = list()
        for k, v in FLAGS_MAPPING.items():
            if k == self.flags:
                _flag_names.append(v)

        return _flag_names
    @property
    def display_avatar(self) -> Asset:
        return Asset.from_avatar(self.avatar, self)

class Member(User):
    ...