from __future__ import annotations

import json
import logging
from typing import Optional

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from dismake.types.command import OptionType
from .command import SlashCommand, Option
from functools import wraps
from .api import API
from .types import (
    AsyncFunction,
    InteractionType,
    InteractionResponseType,
)
from .models import User


log = logging.getLogger("uvicorn")

__all__ = ("Bot",)


class Bot(FastAPI):
    def __init__(
        self,
        token: str,
        client_public_key: str,
        client_id: int,
        route: str = "/interactions",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self._client_id = client_id
        self._client_public_key = client_public_key
        self.verification_key = VerifyKey(bytes.fromhex(self._client_public_key))
        self._http = API(token=token, client_id=client_id)
        self._slash_commands: dict[str, SlashCommand] = {}
        self.add_route(path=route, route=self.handle_interactions, methods=["POST"])
        self.add_event_handler("startup", self._init)
        self.add_event_handler("startup", self._http.fetch_me)

    @property
    def user(self) -> User:
        return self._http._user

    @property
    def get_commands(self) -> Optional[list[SlashCommand]]:
        if self._slash_commands:
            return list(command for _, command in self._slash_commands.items())

    def verify_key(self, body: bytes, signature: str, timestamp: str):
        message = timestamp.encode() + body
        try:
            self.verification_key.verify(message, bytes.fromhex(signature))
            return True
        except BadSignatureError as e:
            log.error("Bad signature request.")
        except Exception as e:
            log.exception(e)
            return False

    async def handle_interactions(self, request: Request):
        signature = request.headers["X-Signature-Ed25519"]
        timestamp = request.headers["X-Signature-Timestamp"]

        if (
            signature is None
            or timestamp is None
            or not self.verify_key(await request.body(), signature, timestamp)
        ):
            return Response(content="Bad Signature", status_code=401)

        request_body = json.loads(await request.body())
        if request_body["type"] == InteractionType.PING:
            log.info("Successfully responded to discord.")
            return JSONResponse({"type": InteractionResponseType.PONG})
        elif request_body["type"] == InteractionType.APPLICATION_COMMAND:
            ...
        return JSONResponse({"type": InteractionResponseType.PONG})

    def command(
        self,
        name: str,
        description: Optional[str],
        options: Optional[list[Option]] = None,
    ):
        if name in self._slash_commands.keys():
            raise ValueError(
                f"{name!r} already registered as a slash command please use a different name."
            )

        command = SlashCommand(name=name, description=description)
        if options:
            for option in options:
                if (
                    option._type != OptionType.SUB_COMMAND
                    or option._type != OptionType.SUB_COMMAND_GROUP
                ):
                    command._options.append(option)

        def decorator(coro: AsyncFunction):
            @wraps(coro)
            def wrapper(*args, **kwargs):
                command.callback = coro
                self._slash_commands[command._name] = command
                return command

            return wrapper()

        return decorator

    async def _init(self):
        registered_commands = await self._http.get_global_commands()
        if self._slash_commands:
            if registered_commands:
                for name, command in self._slash_commands.items():
                    for registered_command in registered_commands:
                        if name == registered_command.name:
                            command.id = registered_command.id

    async def sync_commands(self, *, guild_id: Optional[int] = None):
        if not guild_id:
            res = await self._http.bulk_override_commands(
                [command for _, command in self._slash_commands.items()]
            )
            return res.json()
