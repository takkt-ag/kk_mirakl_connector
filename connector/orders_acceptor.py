import os
import sys

from .container_api import ContainerApi, LogLevel, ContainerApiError
from .mirakl_api import MiraklApi

container_api = ContainerApi()

mirakle_api_token: str = os.getenv("MIRAKL_API_TOKEN")
mirakle_api_url: str = os.getenv("MIRAKL_API_URL")
mirakle_order_status = os.getenv("MIRAKL_ORDER_STATUS")

mirakle_api: MiraklApi = MiraklApi(mirakle_api_token, mirakle_api_url)


def accept_mirakl_orders():
    """
    Accept all orders with given state

    Returns:
        None
    Raises:
        ContainerApiError: if status code is not 204
        ContainerApiError: if no order lines
    """
    try:
        result = mirakle_api.accept_orders(order_state_codes=mirakle_order_status)
        print(f"Accepted order lines: {result}")
        container_api.log(LogLevel.SUCCESS, f"Accepted orders: {result}")
    except ContainerApiError as error:
        container_api.log(LogLevel.ERROR, error.message)
        print(error.message, file=sys.stderr)
