from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.write_log_input import WriteLogInput
from ...models.write_log_response_201 import WriteLogResponse201
from ...models.write_log_response_400 import WriteLogResponse400
from ...types import Response


def _get_kwargs(
    level: str,
    *,
    client: Client,
    json_body: WriteLogInput,
) -> Dict[str, Any]:
    url = "{}/logs/{level}".format(client.base_url, level=level)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[WriteLogResponse201, WriteLogResponse400]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = WriteLogResponse201.from_dict(response.json())

        return response_201
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = WriteLogResponse400.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[WriteLogResponse201, WriteLogResponse400]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    level: str,
    *,
    client: Client,
    json_body: WriteLogInput,
) -> Response[Union[WriteLogResponse201, WriteLogResponse400]]:
    """Write to log.

    Args:
        level (str):
        json_body (WriteLogInput):  Example: {'message': 'Success message', 'context': {'code':
            10}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[WriteLogResponse201, WriteLogResponse400]]
    """

    kwargs = _get_kwargs(
        level=level,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    level: str,
    *,
    client: Client,
    json_body: WriteLogInput,
) -> Optional[Union[WriteLogResponse201, WriteLogResponse400]]:
    """Write to log.

    Args:
        level (str):
        json_body (WriteLogInput):  Example: {'message': 'Success message', 'context': {'code':
            10}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[WriteLogResponse201, WriteLogResponse400]
    """

    return sync_detailed(
        level=level,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    level: str,
    *,
    client: Client,
    json_body: WriteLogInput,
) -> Response[Union[WriteLogResponse201, WriteLogResponse400]]:
    """Write to log.

    Args:
        level (str):
        json_body (WriteLogInput):  Example: {'message': 'Success message', 'context': {'code':
            10}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[WriteLogResponse201, WriteLogResponse400]]
    """

    kwargs = _get_kwargs(
        level=level,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    level: str,
    *,
    client: Client,
    json_body: WriteLogInput,
) -> Optional[Union[WriteLogResponse201, WriteLogResponse400]]:
    """Write to log.

    Args:
        level (str):
        json_body (WriteLogInput):  Example: {'message': 'Success message', 'context': {'code':
            10}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[WriteLogResponse201, WriteLogResponse400]
    """

    return (
        await asyncio_detailed(
            level=level,
            client=client,
            json_body=json_body,
        )
    ).parsed
