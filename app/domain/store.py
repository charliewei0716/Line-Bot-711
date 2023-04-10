from typing import List
from dataclasses import dataclass


class Store:
    def __init__(
        self,
        poi_id: str,
        poi_name: str,
        tel_no: str,
        fax_no: str,
        address: str,
        service: List[str]
    ):
        self._poi_id = poi_id
        self._poi_name = poi_name
        self._tel_no = tel_no
        self._fax_no = fax_no
        self._address = address
        self._service = service

    @property
    def poi_id(self) -> str:
        return self._poi_id

    @property
    def poi_name(self) -> str:
        return self._poi_name

    @property
    def tel_no(self) -> str:
        return self._tel_no

    @property
    def fax_no(self) -> str:
        return self._fax_no

    @property
    def address(self) -> str:
        return self._address

    @property
    def service(self) -> List[str]:
        return self._service


@dataclass
class StockItem:
    name: str
    remaining_qty: int


@dataclass
class CategoryStockItem:
    name: str
    list_item: List[StockItem]
