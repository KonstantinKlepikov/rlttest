import json
import asyncio
from json.decoder import JSONDecodeError
from pydantic import ValidationError
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from app.config import settings
from app.schemas.scheme_data import DataRequest
from app.db.init_db import client
from app.crud.crid_base import data


dp = Dispatcher()


@dp.message(CommandStart())
async def send_welcome(message: types.Message) -> None:

    await message.answer("Hi!\nPls send data in json format.")


@dp.message()
async def echo(message: types.Message) -> None:

    try:
        data_in = json.loads(message.text)
        q = DataRequest(**data_in)
    except (ValidationError, JSONDecodeError):
        await message.answer('Invalid input')

    async with await client.start_session() as s:
        result = await data.get_grouped(s, q)

    await message.answer(result.model_dump_json())


async def main():
    """Start bot"""
    bot = Bot(
        token=settings.TG_API_TOKEN.get_secret_value(),
        parse_mode=ParseMode.HTML
            )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
