

from __future__ import annotations

from typing import Any
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class BaseDTO:
    pass





@dataclass
class CarawlerResultDTO(BaseDTO):
    result: dict[str, str]
    status: bool = field(default=True)

@dataclass
class ProcessorConfigDTO(BaseDTO):
    rules: dict[str, Any] = field(default_factory=dict)
    output: Path = field(default_factory=Path)

@dataclass
class thefewProcessorConfigDTO(ProcessorConfigDTO):
    output: Path = field(default_factory=Path)
    update_rules: dict[str, Any] = field(default_factory=dict)
    rules: dict = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        self.rules = {
            '剩餘天數': 100,
            '已轉換 (%)': 30,
            '轉換價值': [75, 120],
            '轉換溢價率 (%)': 3,
            '發債位階': 70,
            '收盤位階': 65,
            'CB 收盤價': [75, 120]
            }
        allow_rules = set(self.rules.keys())
        update_rules = set(self.update_rules.keys())

        if not update_rules.issubset(allow_rules):
            raise ValueError(f"Invalid rules: {update_rules - allow_rules}")
        else:
            self.rules.update(self.update_rules)







@dataclass
class ProcessorResultDTO(BaseDTO):
    result: Path
    status: bool = field(default=True)


