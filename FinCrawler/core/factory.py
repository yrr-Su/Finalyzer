from __future__ import annotations

from typing import TypeVar, Generic, TYPE_CHECKING, Type

from FinCrawler.core.base import (
    CrawlerInterface,
    ProcessorInterface,
)
from FinCrawler.core.dto import (
    ProcessorConfigDTO,
    ProcessorResultDTO
)
from FinCrawler.core.crawler.thefew import thefewCrawler
from FinCrawler.core.processor.thefew import thefewProcessor


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

    @classmethod
    def create(cls,
               input_config_DTO: ProcessorConfigDTO,
               crawler_name: str='thefew',
               ) -> CrawlerGenerator:

        generator = CrawlerGenerator(crawler=thefewCrawler,
                                     processor=thefewProcessor,
                                     process_config_DTO=input_config_DTO
                                     )

        return generator