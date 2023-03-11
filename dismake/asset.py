from __future__ import annotations
from typing import Optional



__all__ = ("Asset",)

class Asset:
    BASE = 'https://cdn.discordapp.com'
    def __init__(self, *, url: str, key: str, animated: bool = False) -> None:
        self._url = url
        self._animated = animated
        self._key = key
    
    def __str__(self) -> str:
        return self._url

    

    @classmethod
    def from_avatar(cls, avatar_hash: Optional[str], user):
        if not avatar_hash:
            return cls(
                url=f"{cls.BASE}/embed/avatars/{user.discriminator}.png",
                animated=False,
                key=user.username
            )
        animated = avatar_hash.startswith("a_")
        format = 'gif' if animated else 'png'
        return cls(
            url=f"{cls.BASE}/avatars/{user.id}/{avatar_hash}.{format}/?size=1024",
            animated=animated,
            key=avatar_hash
        )