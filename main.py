import asyncio
from aiogram import Bot
import logging
from aiogram.filters import Command
from config import bot, dp, db
from aiogram import Router, F, types
from handlers.survey import survey_router
from handlers.echo import echo_router
start_router = Router()


async def on_startup(bot: Bot):
    await db.create_tables()


@start_router.message(Command('start'))
async def start(message: types.Message):
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[

            [
                types.InlineKeyboardButton(text="Оставить Отзыв", callback_data="feedback")
            ]
        ]

    )
    await message.answer("Hello", reply_markup=kb)


async def main():
    dp.include_router(start_router)
    dp.include_router(survey_router)
    dp.include_router(echo_router)
    dp.startup.register(on_startup)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())