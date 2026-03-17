from dataclasses import dataclass
from typing import Any


@dataclass
class CellSnapshot:
    sheet: str
    cell_ref: str
    value: Any
    formula: str | None

    def to_dict(self) -> dict:
        return {
            "sheet": self.sheet,
            "cell_ref": self.cell_ref,
            "value": self.value,
            "formula": self.formula,
        }
