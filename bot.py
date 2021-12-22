# -*- coding: utf-8 -*-
from jusanmart import Product
import time
from datetime import datetime

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


TOKEN = '######'

bot = Bot(TOKEN)
dp = Dispatcher(bot)


products_in_sell = dict()
saved_prices = dict()


def form(info):
    name = info.name
    shop = info.shop
    price = info.price

    return f'{datetime.now().strftime("%Y-%m-%d %H:%M")} Цена на "{name}" изменен {price} в магазине {shop}'


async def send(key, id):
    print(id + f'  {form(key)}')
    await bot.send_message(id, text=form(key))


@dp.message_handler(commands=['start'])
async def main(message: types.Message):
    await message.reply('Secret Key')


def push_to_scan(products):
    print('started')
    while True:
        global saved_prices
        for key in products:
            for tovar in products[key]:
                zat = Product(tovar)
                if zat.name not in saved_prices:
                    saved_prices[zat.name] = zat.price
                    print(saved_prices)
                else:
                    if saved_prices[zat.name] != zat.price:
                        saved_prices[zat.name] = zat.price
                        send(zat, key)

        time.sleep(300)


@dp.message_handler()
async def check(message: types.Message):
    global products_in_sell
    if message.text.lower() == 'complete':
        await bot.send_message(message.from_user.id, text='Ссылка на товар: ')
    elif 'https://jmart.kz' in message.text:
        key = message.text
        await bot.send_message(message.from_user.id, text='Сохранён!')
        if str(message.from_user.id) in products_in_sell.keys():
            products_in_sell[str(message.from_user.id)].append(message.text)
        else:
            if message.from_user.id not in products_in_sell:
                products_in_sell[str(message.from_user.id)] = []
            else:
                products_in_sell[str(message.from_user.id)].append(message.text)

        await bot.send_message(message.from_user.id, text='Добавить еще? Если все, напишите "complete"')
    elif 'add link' in message.text.lower():
        await bot.send_message(message.from_user.id, text='Вашы товары сохранены. Чтобы добавить еще напишите "add link"')
        push_to_scan(products_in_sell)

if __name__ == '__main__':
    executor.start_polling(dp)

# macbook = Product('1336396')
#
# print(macbook)
