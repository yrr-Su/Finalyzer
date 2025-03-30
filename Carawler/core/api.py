from __future__ import annotations

from typing import TypeVar, Generic, TYPE_CHECKING, Type

from Finalyzer.Carawler.core.base import (
    BaseDTO,
    crawlerInterface,
    processorInterface,
)


ProcessorConfig_T = TypeVar("ProcessorConfig_T", bound="BaseDTO")
CrawlerResult_T = TypeVar("CrawlerResult_T", bound="BaseDTO")


class CrawlerGenerator:

    def __init__(self,
                 crawler: Type[crawlerInterface],
                 processor: Type[processorInterface],
                 process_config_DTO: BaseDTO) -> None:

        self.crawler = crawler()
        self.processor = processor()
        self.process_config_DTO = process_config_DTO

    def generate(self) -> BaseDTO:

        crawled_DTO = self.crawler.get_crawled_data()
        processed_data = self.processor.process(crawled_DTO,
                                                self.process_config_DTO)
        return processed_data



class CrawlerFactory:

    pass

