import requests


class MiraklApi:
    GET_ALL_ORDERS_URL = "/api/orders"
    ACCEPT_ORDER_URL = "/api/orders/{order_id}/accept"

    def __init__(self, auth_token: str, url: str):
        self.auth_token = auth_token
        self.url = url

    def accept_orders(self, order_state_codes: str) -> list:
        """
        Accept all orders with given state

        Args:
            order_state_codes:
        Returns:
            None
        Raises:
            Exception: if status code is not 204
            Exception: if no order lines
        """
        all_orders = self.get_order_by_state(order_state_codes)
        accepted_orders_lines: list = []

        for order in all_orders.get("orders"):
            order_id: str = order.get("order_id")
            order_lines: list = order.get("order_lines")

            if order_lines:
                for order_line in order_lines:
                    order_line_id: str = order_line.get("order_line_id")
                    is_order_accepted: bool = self.accept_order_line(order_id, order_line_id)

                    if is_order_accepted:
                        accepted_orders_lines.append(order_line_id)
                        print(f"Order line {order_line_id} accepted")
            else:
                raise Exception(f"Error while accepting order {order_id}: no order lines")

        return accepted_orders_lines

    def accept_order_line(self, order_id: str, order_line_id: str) -> bool:
        """
        Accept order line
        Args:
            order_id:
            order_line_id:

        Returns:
            True if order line was accepted
        Raises:
            Exception: if status code is not 204
        """
        accept_order_response = requests.put(f"{self.url}{self.ACCEPT_ORDER_URL.format(order_id=order_id)}",
                                             headers={"Authorization": self.auth_token},
                                             json={"order_lines": [{"accepted": True, "id": order_line_id}]})

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
            raise Exception(f"Error while getting orders: {all_orders.text}")

        return all_orders.json()
