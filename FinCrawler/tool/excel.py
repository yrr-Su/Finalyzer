from __future__ import annotations

import re





class ExcelTool:

    @staticmethod
    def is_chinese(text: str) -> bool:
        return bool(re.search(r'[\u4e00-\u9fff]', text))

    @staticmethod
    def is_numeric(text: str) -> bool:
        return text.replace('.', '', 1).isdigit()

    @staticmethod
    def calculate_column_width(text: str) -> float:

        if ExcelTool.is_numeric(text):
            return len(text) * 1.5
        elif all(ord(c) < 128 for c in text):
            return len(text) * 1.2
        elif ExcelTool.is_chinese(text):
            return len(text) * 3
        else:
            return len(text) * 1.9
