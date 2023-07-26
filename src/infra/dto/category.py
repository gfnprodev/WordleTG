from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .words import WordDTO


@dataclass
class CategoryDTO:
    id: int
    name: str
    description: str
    words: list["WordDTO"] = field(default_factory=list)
