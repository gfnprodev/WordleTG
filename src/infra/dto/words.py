from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .category import CategoryDTO


@dataclass
class WordDTO:
    id: int
    word: str
    category_id: int
    category: Optional["CategoryDTO"] = None
