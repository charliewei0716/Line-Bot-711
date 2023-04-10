from app.domain import store


def test_test():
    store_obj = store.StockItem("test", 123)
    assert store_obj.name == "test"
    assert store_obj.remaining_qty == 123
