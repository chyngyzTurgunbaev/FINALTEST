from aiogram import Router, types

echo_router = Router()


@echo_router.message()
async def echo_message(message: types.Message):
    # Разбиваем сообщение на слова
    words = message.text.split()
    # Переворачиваем порядок слов
    reversed_words = ' '.join(words[::-1])
    # Отправляем сообщение обратно пользователю
    await message.reply(reversed_words)
