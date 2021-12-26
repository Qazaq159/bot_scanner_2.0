# -*- coding: utf-8 -*-
from jusanmart import Product
import time
from datetime import datetime
import pytz
import telebot as tele
from config import TOKEN
from db import DataModel, DB

bot = tele.TeleBot(TOKEN)
ala = pytz.timezone('Asia/Almaty')

products_table = DB('table.db')
products_original = DataModel(products_table.get_connection())
products_original.init_table()

prices = dict()


def form(info):
    name = info.name
    shop = info.shop
    price = info.price

    return f'{datetime.now(ala).strftime("%Y-%m-%d %H:%M")} Цена на "{name}" изменен {price} в магазине {shop}'


def send(key, chat_id):
    print(chat_id + f' {datetime.now(ala).strftime("%Y-%m-%d %H:%M")} ' + f' {form(key)}')
    bot.send_message(chat_id, text=form(key))


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, text='Индивидуальный код:')


def push_to_scan(products_links):
    global prices
    print(products_links)
    while True:
        for link in products_links:
            product = Product(link[1])
            if product.name not in prices:
                prices[product.name] = product.price
            elif product.price != prices[product.name]:
                prices[product.name] = product.price
                send(product, chat_id=link[2])
            # elif product.price == prices[product.name]:
            #     print('Constant price for this item >>!' + product.name + ': ' + product.price)
            time.sleep(7)


@bot.message_handler()
def check(message):
    if message.text.lower() == 'add link':
        bot.send_message(message.chat.id, text='Отправьте ссылку на товар ->')
    elif 'https://jmart.kz' in message.text:
        if message.text.count('jmart.kz') > 1:
            links = str(message.text).split('\n')
            if links.count('') != 0:
                links.remove('')
            for link in links:
                if products_original.check_link(link, message.chat.id) == False:
                    products_original.insert_product(link=str(link), chat_id=message.chat.id)
        else:
            if products_original.check_link(message.text, message.chat.id) == False:
                products_original.insert_product(link=str(message.text), chat_id=message.chat.id)
        bot.send_message(message.chat.id, text='Сохранён, чтобы еще добавить отправьте ссылку ->')
    elif message.text.lower() == 'complete':
        links = products_original.get_data(chat_id=message.chat.id)
        bot.send_message(message.chat.id, text='Все товары сохранены, чтобы еще добавить напишете "add link"')
        push_to_scan(links)
    elif message.text.lower() == '??delete??':
        products_original.delete()
        products_original.init_table()
        bot.send_message(message.chat.id, text='Your data has resetted (X)')


if __name__ == '__main__':
    bot.infinity_polling()

# macbook = Product('1336396')
#
# print(macbook)
