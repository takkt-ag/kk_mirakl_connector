import requests
from typing import Optional


class MiraklApi:
    GET_ALL_ORDERS_URL = "/api/orders"
    ACCEPT_ORDER_URL = "/api/orders/{order_id}/accept"

    def __init__(self, auth_token: str, url: str):
        self.auth_token = auth_token
        self.url = url

    def accept_orders(self, order_state_codes: str) -> Optional[list]:
        """
        Accept all orders with given state

        Args:
            order_state_codes:
        Returns:
            list: all order lines that were accepted
            None: if no order lines
        Raises:
            Exception: if status code is not 204
            Exception: if no order lines
        """
        all_orders = self.get_order_by_state(order_state_codes)
        orders_lines_to_accept: list = []

        for order in all_orders.get("orders"):
            order_id: str = order.get("order_id")
            order_lines: list = order.get("order_lines")

            if order_lines:
                for order_line in order_lines:
                    order_line_id: str = order_line.get("order_line_id")
                    orders_lines_to_accept.append(order_line_id)
            else:
                raise Exception(f"Error while accepting order {order_id}: no order lines")

        if orders_lines_to_accept:
            is_order_accepted: bool = self.accept_order_lines(order_id, orders_lines_to_accept)

            if is_order_accepted:
                print(f"Accepted order lines: {orders_lines_to_accept}")
                return orders_lines_to_accept

    def accept_order_lines(self, order_id: str, order_line_ids: list) -> bool:
        """
        Accept order line
        Args:
            order_id:
            order_line_ids:

        Returns:
            True if order line was accepted
        Raises:
            Exception: if status code is not 204
        """
        lines_to_accept: list = [{"accepted": True, "id": order_line_id} for order_line_id in order_line_ids]
        json_to_accept: dict = {"order_lines": lines_to_accept}
        accept_order_response = requests.put(f"{self.url}{self.ACCEPT_ORDER_URL.format(order_id=order_id)}",
                                             headers={"Authorization": self.auth_token},
                                             json=json_to_accept)

        if accept_order_response.status_code != 204:
            raise Exception(f"Error while accepting order {order_id}: {accept_order_response.text}")

        return True

    def get_order_by_state(self, order_state_codes) -> dict:
        """
        Get all orders with given state

        Args:
            order_state_codes:

        Returns:
            dict: all orders with given state
        Raises:
            Exception: if status code is not 200
        """
        all_orders = requests.get(f"{self.url}{self.GET_ALL_ORDERS_URL}",
                                  headers={"Authorization": self.auth_token},
                                  params={"order_state_codes": order_state_codes})

        if all_orders.status_code != 200:
            raise Exception(f"Error while getting orders")

        return all_orders.json()
