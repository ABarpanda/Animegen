import asyncio
import aiohttp
from typing import Dict, Any

async def send_request(session: aiohttp.ClientSession, url: str, data: Dict[str, Any]) -> None:
    async with session.post(url, json=data) as response:
        print(f"Sent request to {url}")

async def periodic_requests(url: str, data: Dict[str, Any], interval: int, count: int) -> None:
    async with aiohttp.ClientSession() as session:
        for _ in range(count):
            asyncio.create_task(send_request(session, url, data))
            await asyncio.sleep(interval)  # Wait before sending the next request

url = "https://api.example.com/endpoint"
data = {"key": "value"}
interval = 5  # Seconds between requests
count = 10  # Number of requests

asyncio.run(periodic_requests(url, data, interval, count))
