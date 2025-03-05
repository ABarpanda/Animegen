import asyncio
import aiohttp

async def send_request(session, url, data):
   """
    Sends an asynchronous POST request to the given URL with JSON data.

    Args:
        session (aiohttp.ClientSession): The active HTTP session.
        url (str): The endpoint to send the request to.
        data (dict): The payload to include in the request.

    Returns:
        int: The HTTP status code of the response.
    """
    async with session.post(url, json=data) as response:
        print(f"Sent request to {url}, status: {response.status}")

async def periodic_requests(url, data, interval, count):
    """
    Sends multiple POST requests at fixed time intervals.

    Args:
        url (str): The endpoint to send requests to.
        data (dict): The payload to include in each request.
        interval (int): The time (in seconds) to wait between requests.
        count (int): The total number of requests to send.

    Returns:
        None
    """
    async with aiohttp.ClientSession() as session:
        for _ in range(count):
            asyncio.create_task(send_request(session, url, data))  # Asynchronous request
            await asyncio.sleep(interval)  # Wait before sending the next request

# Configuration
url = "https://api.example.com/endpoint"
data = {"key": "value"}
interval = 5  # Time in seconds between each request
count = 10  # Number of requests to send

asyncio.run(periodic_requests(url, data, interval, count))