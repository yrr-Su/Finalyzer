from __future__ import annotations

import abc
import dataclasses
from typing import Any, TypeVar, Generic

__all__ = [
    "crawlerInterface",
    "processorInterface",
    "BaseDTO",
]


@dataclasses.dataclass
class BaseDTO:
    pass

_CrawledRawT = TypeVar("_CrawledRawT", bound="BaseDTO")
_ResultT = TypeVar("_ResultT", bound="BaseDTO")
_ProcessConfigT = TypeVar("_ProcessConfigT", bound="BaseDTO")


class crawlerInterface(abc.ABC, Generic[_CrawledRawT]):

    @abc.abstractmethod
    def _parse(self, crawl_raw_data: Any) -> _CrawledRawT:
        pass

    @abc.abstractmethod
    def _crawl(self) -> Any:
        pass

    def get_crawled_data(self) -> _CrawledRawT:
        crawl_raw_data = self._crawl()
        return self._parse(crawl_raw_data)



class processorInterface(abc.ABC, Generic[_ProcessConfigT, _ResultT]):

    @abc.abstractmethod
    def process(self,
                crawler_DTO: BaseDTO,
                process_config_DTO: _ProcessConfigT) -> _ResultT:
        pass

