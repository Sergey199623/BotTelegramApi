import telebot
from telebot import types
import const
from geopy.distance import vincety

bot = telebot.TeleBot(const.API_TOKEN)

markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_address = types.KeyboardButton('Адреса магазинов', request_location=True) #Кнопка адресов магазинов
btn_payment = types.KeyboardButton('Способы оплаты') #Создание кнопки оплаты
btn_delivery = types.KeyboardButton('Способы доставки')
markup_menu.add(btn_adress, btn_payment, btn_delivery)

markup_inline_payment = types.InlineKeyboardMarkup()
btn_in_cash = types.InlineKeyboardMarkupButton('Наличные', callback_data='cash')
btn_in_card = types.InlineKeyboardMarkupButton('Карта', callback_data='card')
btn_in_invoice = types.InlineKeyboardMarkupButton('Перевод', callback_data='invoice')

markup_inline_payment.add(btn_in_cash, btn_in_card, btn_in_invoice)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Привет, я бот интернет магазина!", reply_markup=markup_menu)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	print(message)
	if message.text == "Способы доставки":
		bot.reply_to(message, "Доставка курьером, самовывоз, почта России", reply_markup=markup_menu)
	elif message.text == "Способы оплаты":
		bot.reply_to(message, "В наших магазинах доступные следующие Способы оплаты", reply_markup=markup_menu)
	else:
		bot.reply_to(message, message.text, reply_markup=markup_menu)


@bot.message_handler(func=lambda message: True, content_types = ['location'])
def magazin_location(message):
	print(message)
	lon = message.location.longitude
	lat = message.location.latitude

	distance = []
	for m in const.MAGAZINS:
		result = vincenty((m['latm'], m['lonm']), (lat, lon)).kilometers
		distance.append(result)
	index = distance.index(min(distance))
	
	bot.send_message(message.chat.id,'Ближайший к Вам магазин')	
	bot.send_venue(message.chat.id, 
		const.MAGAZINS[index]['latm'],
		const.MAGAZINS[index]['lonm'],
		const.MAGAZINS[index]['title'],
		const.MAGAZINS[index]['address'])

@bot.callback_query_handler(func = lambda call: True)	
def callback_back_payment(call):
	print(call)
	if call.data == 'cash':
		bot.send_message(call.message.chat.id, text="""
			Оплата наличными производится в рублях, в кассах магазина
			""", reply_markup=markup_inline_payment)







bot.polling()	
