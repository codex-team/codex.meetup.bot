import asyncio

from src.services.servers_controller import servers_controller


async def main():
    tasks = map(lambda i: asyncio.create_task(servers_controller.create_server(123123123, f'server{i}')), range(30))
    await asyncio.wait(tasks)


asyncio.run(main())
