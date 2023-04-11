from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .commands import SlashCommand
    from .interaction import Interaction

__all__ = (
    "DismakeException",
    "NotImplemented",
    "CommandInvokeError",
    "InteractionResponded",
    "InteractionNotResponded",
    "HouseError",
)


class DismakeException(Exception):
    """Base dismake exception."""


class NotImplemented(DismakeException):
    """Raise when a unknown command invoke."""


class CommandInvokeError(DismakeException):
    """TODO"""

    def __init__(self, command: SlashCommand, exception: Exception) -> None:
        self.command = command
        self.exception = exception
        super().__init__(f"Command {command.name!r} raised an exception: {exception}")


class InteractionResponded(DismakeException):
    def __init__(self, interaction: Interaction) -> None:
        self.interaction = interaction
        super().__init__(f"{interaction.id!r} Interaction already responded.")


class InteractionNotResponded(DismakeException):
    def __init__(self, interaction: Interaction) -> None:
        self.interaction = interaction
        super().__init__(f"{interaction.id!r} The interaction is not responded.")


class HouseError(DismakeException):
    """Base Exception for house."""
