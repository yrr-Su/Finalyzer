from __future__ import annotations

import abc
from typing import Any

from FinCrawler.core.dto import (
    CarawlerResultDTO,
    ProcessorConfigDTO,
    ProcessorResultDTO
)

__all__ = [
    "CrawlerInterface",
    "ProcessorInterface",
]



class CrawlerInterface(abc.ABC):

    @property
    @abc.abstractmethod
    def _crawl_name(self) -> str: ...

    @property
    @abc.abstractmethod
    def _crawl_url(self) -> str: ...

    @abc.abstractmethod
    def _parse(self, crawl_raw_data: Any) -> CarawlerResultDTO:
        pass

    @abc.abstractmethod
    def _crawl(self) -> Any:
        pass

    def get_crawled_data(self) -> CarawlerResultDTO:
        crawl_raw_data = self._crawl()
        return self._parse(crawl_raw_data)



class ProcessorInterface(abc.ABC):
    name = None

    @abc.abstractmethod
    def process(self,
                crawler_DTO: CarawlerResultDTO,
                process_config_DTO: ProcessorConfigDTO
                ) -> ProcessorResultDTO:
        pass

