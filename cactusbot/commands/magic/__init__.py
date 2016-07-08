"""Define custom magic commands."""

from .. import Command

from .command import Meta
from .quote import Quote
from .cube import Cube
from .temmie import Temmie
from .social import Social

COMMANDS = (Meta, Quote, Cube, Temmie, Social)

__all__ = ["Command", "Meta", "Quote", "Cube", "Temmie", "Social"]
