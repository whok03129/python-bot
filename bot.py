import telebot
from telebot import types

API_TOKEN = '8159245807:AAEhpbjlZIoXDEb5nmKiHOrlijah0bYO2Zg'  # Your bot token
OWNER_ID = 7685837210  # Your Telegram ID

bot = telebot.TeleBot(API_TOKEN)

# Store user input in memory (use DB in production)
user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    order_btn = types.InlineKeyboardButton("🛒 Order Now", callback_data='order_now')
    markup.add(order_btn)
    bot.send_message(message.chat.id, "👋 Welcome to LibertyFetch!\nClick the button below to place an order.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'order_now')
def order_now(call):
    user_data[call.from_user.id] = {}
    bot.send_message(call.message.chat.id, "📛 What's your *Full Name*?", parse_mode="Markdown")
    bot.register_next_step_handler_by_chat_id(call.message.chat.id, process_name)

def process_name(message):
    user_data[message.from_user.id]['name'] = message.text
    bot.send_message(message.chat.id, "📦 Enter *Product Details + Link*:", parse_mode="Markdown")
    bot.register_next_step_handler(message, process_product)

def process_product(message):
    user_data[message.from_user.id]['product'] = message.text
    bot.send_message(message.chat.id, "🏠 Enter your *Full Address*:", parse_mode="Markdown")
    bot.register_next_step_handler(message, process_address)

def process_address(message):
    user_data[message.from_user.id]['address'] = message.text
    bot.send_message(message.chat.id, "📱 Enter your *Email or WhatsApp Number*:", parse_mode="Markdown")
    bot.register_next_step_handler(message, process_contact)

def process_contact(message):
    user_data[message.from_user.id]['contact'] = message.text
    info = user_data[message.from_user.id]
    
    summary = (
        f"🆕 *New Order Received!*\n\n"
        f"👤 Name: {info['name']}\n"
        f"📦 Product: {info['product']}\n"
        f"🏠 Address: {info['address']}\n"
        f"📱 Contact: {info['contact']}"
    )

    bot.send_message(message.chat.id, "✅ Your order has been placed! We'll get in touch soon.", parse_mode="Markdown")
    bot.send_message(OWNER_ID, summary, parse_mode="Markdown")

bot.infinity_polling()
