import pytest
import requests_mock

from connector.mirakl_api import MiraklApi


@pytest.fixture
def api_client():
    return MiraklApi(auth_token="test_token", url="http://testurl.com")


def test_accept_orders_success(api_client):
    with requests_mock.Mocker() as m:
        m.get("http://testurl.com/api/orders",
              json={"orders": [{"order_id": "1", "order_lines": [{"order_line_id": "10"}]}]}, status_code=200)
        m.put("http://testurl.com/api/orders/1/accept", status_code=204)
        accepted_orders = api_client.accept_orders("test_state")
        assert "10" in accepted_orders


def test_accept_orders_no_orders(api_client):
    with requests_mock.Mocker() as m:
        m.get("http://testurl.com/api/orders", json={"orders": []}, status_code=200)
        accepted_orders = api_client.accept_orders("test_state")
        assert accepted_orders == []


def test_accept_orders_no_order_lines(api_client):
    with requests_mock.Mocker() as m:
        m.get("http://testurl.com/api/orders", json={"orders": [{"order_id": "1", "order_lines": []}]}, status_code=200)
        with pytest.raises(Exception) as exception_info:
            api_client.accept_orders("test_state")
        assert "no order lines" in str(exception_info.value)


def test_accept_order_line_failure(api_client):
    order_id = "123"
    order_line_id = "456"

    with requests_mock.Mocker() as m:
        m.put(f"http://testurl.com/api/orders/{order_id}/accept", status_code=400)
        with pytest.raises(Exception) as exception_info:
            api_client.accept_order_line(order_id, order_line_id)
        assert "Error while accepting order" in str(exception_info.value)


def test_get_order_by_state_success(api_client):
    with requests_mock.Mocker() as m:
        m.get("http://testurl.com/api/orders", json={"orders": [{"order_id": "1"}]}, status_code=200)
        orders = api_client.get_order_by_state("test_state")
        assert "orders" in orders


def test_get_order_by_state_failure(api_client):
    with requests_mock.Mocker() as m:
        m.get("http://testurl.com/api/orders", status_code=400)
        with pytest.raises(Exception) as exception_info:
            api_client.get_order_by_state("test_state")
        assert "Error while getting orders" in str(exception_info.value)
