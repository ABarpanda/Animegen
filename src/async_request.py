import asyncio
import aiohttp
from typing import Dict, Any

async def send_request(session: aiohttp.ClientSession, url: str, data: Dict[str, Any]) -> None:
    """
    Sends an asynchronous POST request to the specified URL with the given data.

    Args:
        session (aiohttp.ClientSession): The aiohttp session to use for the request.
        url (str): The URL to send the request to.
        data (Dict[str, Any]): The JSON data to include in the request body.
    """
    async with session.post(url, json=data) as response:
        print(f"Sent request to {url}")

async def periodic_requests(url: str, data: Dict[str, Any], interval: int, count: int) -> None:
    """
    Sends periodic asynchronous requests to a specified URL.

    Args:
        url (str): The URL to send requests to.
        data (Dict[str, Any]): The data to send with each request.
        interval (int): The time interval (in seconds) between requests.
        count (int): The total number of requests to send.
    """
    async with aiohttp.ClientSession() as session:
        for _ in range(count):
            # Schedule the request to be sent immediately (fire and forget)
            asyncio.create_task(send_request(session, url, data))
            # Pause execution for the specified interval without blocking the event loop
            await asyncio.sleep(interval)

url = "https://api.example.com/endpoint"
data = {"key": "value"}
interval = 5
count = 10

asyncio.run(periodic_requests(url, data, interval, count))