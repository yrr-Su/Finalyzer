from __future__ import annotations

from typing import TypeVar, Generic, TYPE_CHECKING, Type

from FinCarawler.core.base import (
    CrawlerInterface,
    ProcessorInterface,
)
from FinCarawler.core.dto import (
    ProcessorConfigDTO,
    ProcessorResultDTO
)


class CrawlerGenerator:

    def __init__(self,
                 crawler: Type[CrawlerInterface],
                 processor: Type[ProcessorInterface],
                 process_config_DTO: ProcessorConfigDTO) -> None:

        self.crawler = crawler()
        self.processor = processor()
        self.process_config_DTO = process_config_DTO

    def generate(self) -> ProcessorResultDTO:

        crawled_DTO = self.crawler.get_crawled_data()
        processed_data = self.processor.process(crawled_DTO,
                                                self.process_config_DTO)
        return processed_data



class CrawlerFactory:

    pass

