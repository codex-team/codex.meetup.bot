import asyncio

from src.services.servers_controller import servers_controller

loop = asyncio.get_event_loop()

gather = asyncio.gather(servers_controller.create_server(123123123, f'server{i}') for i in range(5))

loop.run_until_complete(gather)