import telebot
from telebot import types
import os
from flask import Flask
import threading

# Токен берется из настроек сервера (безопасно)
TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

# --- Мини-сервер для работы 24/7 на Render ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает 24/7!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
# ---------------------------------------------

@bot.message_handler(commands=['start'])
def start(message):
    photo_url = "https://images.unsplash.com/photo-1555066931-4365d14bab8c?q=80&w=1000&auto=format&fit=crop"
    caption_text = (
        "👋 <b>Привет!</b> Это демонстрационный бот <b>BotCraft Studio</b>.\n\n"
        "Я создаю Telegram-ботов на Python для бизнеса. "
        "Этот бот — живой пример моей работы. Понажимай на кнопки ниже, чтобы посмотреть, как всё устроено! 👇"
    )
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_services = types.InlineKeyboardButton("🛠 Услуги и цены", callback_data="services")
    btn_portfolio = types.InlineKeyboardButton("💼 Портфолио", callback_data="portfolio")
    btn_order = types.InlineKeyboardButton("🚀 Заказать бота", callback_data="order")
    btn_faq = types.InlineKeyboardButton("❓ FAQ", callback_data="faq")
    btn_contact = types.InlineKeyboardButton("📞 Контакты", callback_data="contact")
    markup.add(btn_services)
    markup.add(btn_portfolio, btn_order)
    markup.add(btn_faq, btn_contact)
    bot.send_photo(message.chat.id, photo=photo_url, caption=caption_text, reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "services":
        text = (
            "🛠 <b>Что я могу сделать:</b>\n\n"
            "1️⃣ <b>Бот-визитка</b> — меню, цены, контакты. (от 1500 ₽)\n"
            "2️⃣ <b>Бот-магазин</b> — каталог товаров, корзина, оформление заказа. (от 3000 ₽)\n"
            "3️⃣ <b>Бот-автоответчик</b> — отвечает на вопросы клиентов 24/7. (от 1000 ₽)\n\n"
            "ℹ️ <i>Точная стоимость зависит от вашего ТЗ.</i>"
        )
        bot.send_message(call.message.chat.id, text, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    elif call.data == "portfolio":
        text = (
            "💼 <b>Мои работы:</b>\n\n"
            "🔹 <b>Бот для кофейни</b> (демо-версия)\n"
            "🔹 <b>Этот бот-визитка</b> (вы сейчас в нем)\n\n"
            "<i>Хотите такой же для своего бизнеса? Нажмите «Заказать бота»!</i>"
        )
        bot.send_message(call.message.chat.id, text, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    elif call.data == "order":
        text = (
            "🚀 <b>Как заказать бота:</b>\n\n"
            "Напишите мне в личные сообщения: <b>@bot_creator333</b>\n\n"
            "В сообщении укажите:\n"
            "1. Для какой задачи нужен бот.\n"
            "2. Какие функции должны быть.\n"
            "3. Примерные сроки.\n\n"
            "Я отвечу в течение дня и предложу решение!"
        )
        bot.send_message(call.message.chat.id, text, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    elif call.data == "faq":
        text = (
            "❓ <b>Частые вопросы:</b>\n\n"
            "<b>- Сколько времени занимает разработка?</b>\n"
            "От 1 до 3 дней.\n\n"
            "<b>- Бот будет работать 24/7?</b>\n"
            "Да, он работает на сервере без выходных.\n\n"
            "<b>- А если я захочу изменить текст?</b>\n"
            "Я передам вам инструкцию или внесу правки сам."
        )
        bot.send_message(call.message.chat.id, text, parse_mode='HTML')
        bot.answer_callback_query(call.id)
    elif call.data == "contact":
        text = (
            "📞 <b>Связаться со мной:</b>\n\n"
            "Telegram: <b>@bot_creator333</b>\n\n"
            "Пишите, я всегда открыт к диалогу!"
        )
        bot.send_message(call.message.chat.id, text, parse_mode='HTML')
        bot.answer_callback_query(call.id)

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    print("Бот запущен на сервере...")
    bot.infinity_polling()
