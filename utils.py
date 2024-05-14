import asyncio


def run_async(async_func):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(async_func)
        return result
    finally:
        loop.close()
