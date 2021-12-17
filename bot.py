import telebot as t
import loopp
from jusanmart import Product
import time

TOKEN = '5050251865:AAFMkaaG-qBP9Vnsn8R2FJ2-5r5MOMo4pW4'

bot = t.TeleBot(TOKEN)

products_in_sell = dict()
saved_prices = dict()


def form(info):
    name = info.name
    shop = info.shop
    price = info.price

    return f'Цена на "{name}" изменен {price} в магазине {shop}'


def send(key, id):
    bot.send_message(id, text=form(key))


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.from_user.id, text='Secret Key')


def push_to_scan(products):
    while True:
        global saved_prices
        for key in products:
            for tovar in products[key]:
                zat = Product(tovar
                if zat.name not in saved_prices:
                    saved_prices[zat.name] = zat.price
                    print(saved_prices)
                else:
                    if saved_prices[zat.name] != zat.price:
                        send(zat, key)

        time.sleep(300)


@bot.message_handler(content_types=['text'])
def check(message):
    global products_in_sell
    if message.text == '2021start':
        bot.send_message(message.from_user.id, text='Link for product')
    elif 'https://jmart.kz' in message.text:
        key = message.text
        bot.send_message(message.from_user.id, text='SAVED!')
        if str(message.from_user.id) in products_in_sell.keys():
            products_in_sell[str(message.from_user.id)].append(message.text)
        else:
            products_in_sell[str(message.from_user.id)] = []
            products_in_sell[str(message.from_user.id)].append(message.text)

        bot.send_message(message.from_user.id, text='Is it all? If yes, print "start2021"')
    elif 'start2021' in message.text:
        push_to_scan(products_in_sell)


bot.infinity_polling()

# macbook = Product('1336396')
#
# print(macbook)
