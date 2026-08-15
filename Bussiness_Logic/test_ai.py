import asyncio
from services.ai_client import get_ai_prediction

async def main():
    result = await get_ai_prediction(b"test")
    print(result)

asyncio.run(main())
