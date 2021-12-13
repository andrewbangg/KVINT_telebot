import asyncio
from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor
#@Telepizzabot - адрес бота
# constant
BOT_TOKKEN = '5071184143:AAFM8S1OJhyWBthNwrFHzGaIXnkKDTSJtYg'
chat_id = 479798219  # впишите свой id

# shagi
from aiogram.dispatcher.filters.state import StatesGroup, State


class Shop(StatesGroup):
    step_1 = State()
    step_2 = State()
    step_3 = State()


loop = asyncio.new_event_loop()
bot = Bot(BOT_TOKKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, loop=loop, storage=storage)


async def shutdown(dp):
    await storage.close()
    await bot.close()


async def send_hello(dp):
    await bot.send_message(chat_id=chat_id,
                           text='Привет, я чат-бот для заказы пиццы^_^. Нажми на "/start" и закажем пиццу')


from aiogram.dispatcher import FSMContext


@dp.message_handler(Command('start'), state=None)
async def shop(message: Message):
    await message.answer('Какую вы хотите пиццу? Большую или маленькую?')

    await Shop.step_1.set()


@dp.message_handler(state=Shop.step_1)
async def size_pizza(message: Message, state: FSMContext):
    item = message.text
    await state.update_data(
        {
            'item': item
        }
    )
    if item.lower() == 'большую':
        size = item
    elif item.lower() == 'маленькую':
        size = item
    else:
        return await message.answer(
            'Вы ввели неккоректный размер. Прошу написать какую вы хотите пиццу: Большую или маленькую?')

    await message.answer('Как вы будете платить? Наличкой или Безналичкой?')
    await Shop.next()


@dp.message_handler(state=Shop.step_2)
async def oplata(message: Message, state: FSMContext):
    item_2 = message.text
    await state.update_data(
        {
            'item_2': item_2
        }
    )
    if item_2.lower() == 'наличкой':
        opl = item_2
    elif item_2.lower() == 'безналичкой':
        opl = item_2
    else:
        return await message.answer('Вы ввели неккоректный способ оплаты. Прошу написать: Наличкой или безналичкой')

    data = await state.get_data()
    item = data.get('item')

    await message.answer(f'Вы хотите {item} пиццу оплата - {opl}?')
    await Shop.next()


@dp.message_handler(state=Shop.step_3)
async def vibor(message: Message, state: FSMContext):
    item_3 = message.text
    await state.update_data(
        {
            'item_3': item_3
        }
    )
    if item_3.lower() == 'да':
        otv = item_3
    elif item_3.lower() == 'нет':
        otv = item_3
        await state.finish()
        return await message.answer('Нажми "/start" и мы наченм заново')

    else:
        return await message.answer('Прошу написать ДА или НЕТ')

    data = await state.get_data()
    item_3 = data.get('item')

    await message.answer(f'Спасибо за заказ')

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=send_hello, on_shutdown=shutdown)
