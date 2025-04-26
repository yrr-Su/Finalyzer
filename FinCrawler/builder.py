from __future__ import annotations

from pathlib import Path

from FinCrawler.core.factory import CrawlerFactory
from FinCrawler.core.dto import thefewProcessorConfigDTO



class CrawlerBuilder:

    def __init__(self,
                 rules: dict,
                 output: Path | str) -> None:

        self.rules = rules
        self.output = Path(output)



    def build(self) -> Path:

        generator = CrawlerFactory.create(
            input_config_DTO=thefewProcessorConfigDTO(
                update_rules = self.rules,
                output = self.output
                )
            )
        result_dto = generator.generate()
        print(f"\nProcess result:\n\t{result_dto.result.name}")

        return result_dto.result
