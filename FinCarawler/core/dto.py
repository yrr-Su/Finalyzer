

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
    rules = {
            '剩餘天數': 100,
            '已轉換 (%)': 30,
            '轉換價值': [75, 120],
            '轉換溢價率 (%)': 3,
            '發債位階': 70,
            '收盤位階': 65,
            'CB 收盤價': [75, 120]
            }

    def __post_init__(self, update_rules: dict={}) -> None:
        self.rules.update(update_rules)







@dataclass
class ProcessorResultDTO(BaseDTO):
    result: Path
    status: bool = field(default=True)


