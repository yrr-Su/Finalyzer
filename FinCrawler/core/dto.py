

from __future__ import annotations

from typing import Any
from dataclasses import dataclass, field
from pathlib import Path

from datetime import datetime

@dataclass
class BaseDTO:
    pass


def _parse_suffix(ori_rules: dict, update_rules: dict) -> str:
    suffix_name = {
        '剩餘天數': '剩',
        '已轉換 (%)': '已轉',
        '轉換價值': '轉',
        '轉換溢價率 (%)': '溢',
        '發債位階': '發',
        '收盤位階': '收',
        'CB 收盤價': 'CB'
    }

    suffix = [datetime.now().strftime('%Y%m%d')]

    for _key in list(update_rules.keys()):
        _value = update_rules[_key]
        _suffix_key = suffix_name[_key]

        if isinstance(_value, list):
            suffix.append(
                f"{_suffix_key}({_value[0]}-{_value[1]})"
                )
        else:
            suffix.append(f"{_suffix_key}({_value})")

    return '_'.join(suffix)







@dataclass
class CarawlerResultDTO(BaseDTO):
    result: dict[str, str]
    status: bool = field(default=True)

@dataclass
class ProcessorConfigDTO(BaseDTO):
    rules: dict[str, Any] = field(default_factory=dict)
    output: Path = field(default_factory=Path)
    output_file: str = field(init=False)

@dataclass
class thefewProcessorConfigDTO(ProcessorConfigDTO):
    output: Path = field(default_factory=Path)
    output_file: str = field(init=False)
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
        allow_keys = set(self.rules.keys())
        update_keys = set(self.update_rules.keys())

        if not update_keys.issubset(allow_keys):
            raise ValueError(f"Invalid rules: {update_keys - allow_keys}")
        else:
            self.rules.update(self.update_rules)

        suffix_str = _parse_suffix(self.rules,
                                   self.update_rules)

        self.output_file = f"選擇權_{suffix_str}.xlsx"






@dataclass
class ProcessorResultDTO(BaseDTO):
    result: Path
    status: bool = field(default=True)


