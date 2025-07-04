import asyncio
from os import getenv
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from app.user import user


async def main():
    load_dotenv()
    bot = Bot(token=getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(user)
    dp.startup.register(on_startup)
    dp.shutdown.register(shutdown)
    await dp.start_polling(bot)



async def on_startup(dispatcher):
    print('Starting bot...')


async def shutdown(dispatcher: Dispatcher):
    print('Shutting down...')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass