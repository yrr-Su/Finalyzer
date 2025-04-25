

import requests
import pickle
from typing import Any

import bs4

from config.setting import CONFIG
from FinCrawler.core.base import CrawlerInterface
from FinCrawler.core.dto import CarawlerResultDTO


class thefewCrawler(CrawlerInterface):

    def __init__(self) -> None:
        super().__init__()

        self.session = requests.Session()

    @property
    def _crawl_name(self) -> str:
        return 'thefew'

    @property
    def _crawl_url(self) -> str:
        return 'https://thefew.tw/cb'

    def _from_trdata2dict(self, _trData: Any) -> dict:
        _dict = dict()
        for _tr in _trData.find_all('tr'):
            _dt_list = list(_tr.stripped_strings)

            _dict[_dt_list[0]] = _dt_list[1]

        return _dict

    def _crawl(self) -> bs4.BeautifulSoup:
        cookies = pickle.load(
            open(CONFIG.PATH_RESOURCE / 'thefew_cookie.pkl', "rb"))

        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])

        response = self.session.get(self._crawl_url)

        return bs4.BeautifulSoup(response.text, 'html.parser')



    def _parse(self, crawl_raw_data: bs4.BeautifulSoup) -> CarawlerResultDTO:

        tbodyMain_attrs = {
            'data-controller': 'table cb-chart',
            'data-action': 'mouseenter->table#highlight mouseleave->table#unhighlight'
            }

        trId_attrs = {
            'class': "cursor-pointer",
            'data-target': "table.highlight"
            }

        trData_attrs = {
            'data-target': "table.expandable"
            }

        main_body = crawl_raw_data.body
        if main_body is not None:
            main_tbody = main_body.find_all('tbody', attrs=tbodyMain_attrs) # type: ignore

        data = dict()
        for _tbody in main_tbody:

            if _tbody is not None:
                _data = dict()

                trId = _tbody.find('tr', attrs=trId_attrs) # type: ignore
                trData = _tbody.find('tr', attrs=trData_attrs) # type: ignore

                # id
                dt_trId = list(trId.find(attrs={'class': 'w-11/12'}).stripped_strings) # type: ignore
                _data['名稱'] = dt_trId[1]

                # data
                dt_trData1, dt_trData2 = trData.find_all('tbody') # type: ignore

                _data.update(self._from_trdata2dict(dt_trData1))
                _data.update(self._from_trdata2dict(dt_trData2))

                # output the data
                data[dt_trId[0]] = _data

        self.session.close()
        return CarawlerResultDTO(result=data)
