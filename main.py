import telebot
import re
from telebot import types
import os
import sys
import django

# Путь к корню проекта в sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'crm_panel'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_system.crm_panel.settings')

# Инициализация Django
django.setup()

# Импорт моделей
from crm_system.leads.models import UserRequest


bot = telebot.TeleBot(os.environ.get("TELEGRAM_TOKEN"))
#YOUR_USER_ID = 1404001228
ADMIN_ID = 1404001228
import os
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

customer_data = {}  # Для хранения данных по каждому пользователю


# Продукты
PRODUCTS = {
    "bungalow": {
        "name": "Бунгало",
        "photo": "images/bungalow.webp",
        "desc_file": "description/bungalow.txt"
    },
    "double_bungalow": {
        "name": "Двойное бунгало",
        "photo": "images/double_bungalow.webp",
        "desc_file": "description/double_bungalow.txt",
    },
    "royal_cabin": {
        "name": "КОРОЛЕВСКАЯ КАЮТА",
        "photo": "images/royal_cabin.jpg",
        "desc_file": "description/royal_cabin.txt"
    },
    "deluxe_cottage": {
        "name": "Коттедж Делюкс",
        "photo": "images/deluxe_cottage.jpg",
        "desc_file": "description/deluxe_cottage.txt"
    },
    "terranova_1": {
        "name": "Terranova – 1 спальня",
        "photo": "images/terranova_1.jpg",
        "desc_file": "description/terranova_1.txt"
    },
    "terranova_2": {
        "name": "Terranova – 2 спальни",
        "photo": "images/terranova_2.jpg",
        "desc_file": "description/terranova_2.txt"
    },
    "terranova_3": {
        "name": "Terranova – 3 спальни",
        "photo": "images/terranova_3.jpg",
        "desc_file": "description/terranova_3.txt"
    },
    "royal_family": {
        "name": "Королевская семья",
        "photo": "images/royal_family.jpg",
        "desc_file": "description/royal_family.txt"
    },
    "santorini": {
        "name": "Санторини",
        "photo": "images/santorini.jpg",
        "desc_file": "description/santorini.txt"
    },
    "murano": {
        "name": "Мурано",
        "photo": "images/murano.jpg",
        "desc_file": "description/murano.txt"
    },
    "modular_system": {
        "name": "МОДУЛЬНАЯ СИСТЕМА",
        "photo": "images/modular_system.jpg",
        "desc_file": "description/modular_system.txt"
    }
}


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Контакты")
    btn2 = types.KeyboardButton("Сайт компании")
    btn3 = types.KeyboardButton("О нас")
    btn4 = types.KeyboardButton("Частые вопросы")
    btn5 = types.KeyboardButton("Другое")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)

    with open('../../PycharmProjects/DiplomBotBuildCompany/.venv/company_intro.txt', 'r', encoding='utf-8') as f:
        company_intro = f.read()
        bot.send_message(chat_id, text=f'Добрый день 😊, {message.from_user.first_name}!', reply_markup=markup)
        bot.send_message(chat_id, text=company_intro)

    show_menu(message)


@bot.message_handler(commands=['menu'])
def show_menu(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Наши продукты", callback_data="portfolio"))
    markup.add(types.InlineKeyboardButton("Сайт компании", callback_data="services"))
    markup.add(types.InlineKeyboardButton("Оставить заявку", callback_data="request"))
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_inline(call):
    if call.data == "portfolio":
        markup = types.InlineKeyboardMarkup()
        for key, product in PRODUCTS.items():
            markup.add(types.InlineKeyboardButton(product["name"], callback_data=f"product_{key}"))
        bot.send_message(call.message.chat.id, "Наши продукты:", reply_markup=markup)
        # bot.send_message(call.message.chat.id, "Здесь вы можете ознакомиться с нашими продуктами:")
        # with open('/Users/albina/PycharmProjects/TelegramBot/venv/images/portfolio1.jpg', 'rb') as photo:
        #     bot.send_photo(call.message.chat.id, photo)
        # with open('/Users/albina/PycharmProjects/TelegramBot/venv/images/portfolio2.jpg', 'rb') as photo:
        #     bot.send_photo(call.message.chat.id, photo)

    elif call.data == "services":
        bot.send_message(call.message.chat.id, text="🌐 Более подробно ознакомиться с информацией Вы можете на нашем сайте: https://greenhouseru.ru")

    elif call.data == "request":
        bot.send_message(call.message.chat.id, 'Отлично! Давайте начнем. Введите ваше имя:')
        bot.register_next_step_handler(call.message, get_name)

    # elif call.data == 'users':
    #     if call.from_user.id == YOUR_USER_ID:
    #         users = UserRequest.objects.all()
    #         if users:
    #             info = ""
    #             for user in users:
    #                 info += f"Имя: {user.name}, Фамилия: {user.surname}, Телефон: {user.phone}, Дизайн: {user.designinfo}\n\n"
    #             bot.send_message(call.message.chat.id, info)
    #         else:
    #             bot.send_message(call.message.chat.id, "Заявок пока нет.")
    #     else:
    #         bot.send_message(call.message.chat.id, 'У вас нет прав на просмотр списка заявок.')
    elif call.data.startswith("product_"):
        key = call.data.split("product_")[1]
        product = PRODUCTS.get(key)

        if product:
            # Отправка фото
            try:
                with open(product["photo"], "rb") as photo:
                    bot.send_photo(call.message.chat.id, photo)
            except FileNotFoundError:
                bot.send_message(call.message.chat.id, f"Файл {product['photo']} не найден.")

            # Чтение описания из файла
            try:
                with open(product["desc_file"], "r", encoding="utf-8") as f:
                    description = f.read()
            except FileNotFoundError:
                description = "Описание временно недоступно."

            # Отправка текста
            bot.send_message(
                call.message.chat.id,
                f"<b>{product['name']}</b>\n\n{description}",
                parse_mode="HTML"
            )

            # Кнопки
            back_markup = types.InlineKeyboardMarkup()
            back_markup.add(types.InlineKeyboardButton("Оставить заявку", callback_data="request"))
            back_markup.add(types.InlineKeyboardButton("⬅️ Назад ко всем продуктам", callback_data="portfolio"))
            bot.send_message(call.message.chat.id, "Что вы хотите сделать дальше?", reply_markup=back_markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "Контакты":
        bot.send_message(message.chat.id, text="Номер телефона: +7(900) 257-33-33 \nПочта: greenhouse.mail@yandex.ru")

    elif message.text == "Сайт компании":
        bot.send_message(message.chat.id, text=" 🌐Более подробно ознакомиться с информацией Вы можете  на нашем сайте https://greenhouseru.ru")

    elif message.text == "О нас":
        with open('about_us.txt', 'r', encoding='utf-8') as f:
            company_intro = f.read()
        bot.send_message(message.chat.id, text=company_intro)

    elif message.text == "Частые вопросы":
        with open('questions.txt', 'r', encoding='utf-8') as f:
            questions = f.read()
        bot.send_message(message.chat.id, text=questions)

    elif message.text == "Другое":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(
            types.KeyboardButton("Наши продукты"),
            types.KeyboardButton("Этапы работы"),
            types.KeyboardButton("Оставить заявку"),
            types.KeyboardButton("Вернуться в меню")
        )
        bot.send_message(message.chat.id, text="Выберите действие с клавиатуры:", reply_markup=markup)

    elif message.text == "Наши продукты":
        markup = types.InlineKeyboardMarkup()
        for key, product in PRODUCTS.items():
            markup.add(types.InlineKeyboardButton(product["name"], callback_data=f"product_{key}"))
        bot.send_message(message.chat.id, "Наши продукты:", reply_markup=markup)

    elif message.text == "Этапы работы":
        with open('work_point.txt', 'r', encoding='utf-8') as f:
            price_and_services = f.read()
        bot.send_message(message.chat.id, text=price_and_services)

    elif message.text == "Оставить заявку":
        bot.send_message(message.chat.id, 'Отлично! Давайте начнем. Введите ваше имя:')
        bot.register_next_step_handler(message, get_name)

    # elif message.text == "Посмотреть заявки":
    #     if message.from_user.id == YOUR_USER_ID:
    #         users = UserRequest.objects.all()
    #         if users:
    #             info = ""
    #             for user in users:
    #                 info += f"Имя: {user.name}, Фамилия: {user.surname}, Телефон: {user.phone}, Дизайн: {user.designinfo}\n\n"
    #             bot.send_message(message.chat.id, info)
    #         else:
    #             bot.send_message(message.chat.id, "Заявок пока нет.")
    #     else:
    #         bot.send_message(message.chat.id, 'У вас нет прав на просмотр списка заявок.')

    elif message.text == "Вернуться в меню":
        start(message)

    else:
        bot.send_message(message.chat.id, "Извините, я не понимаю ваш запрос. Пожалуйста, воспользуйтесь клавиатурой.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("product_"))
def handle_product_selection(call):
    product_key = call.data.replace("product_", "")
    product = PRODUCTS.get(product_key)

    if not product:
        bot.send_message(call.message.chat.id, "Продукт не найден.")
        return

    try:
        with open(product["photo"], "rb") as photo:
            bot.send_photo(call.message.chat.id, photo, caption=product["description"])
    except Exception:
        bot.send_message(call.message.chat.id, product["description"] + "\n\n(Изображение временно недоступно)")

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Оставить заявку", callback_data="request"))
    markup.add(types.InlineKeyboardButton("Вернуться назад ко всем продуктам", callback_data="portfolio"))
    bot.send_message(call.message.chat.id, "Что хотите сделать дальше?", reply_markup=markup)

def get_name(message):
    chat_id = message.chat.id
    customer_data[chat_id] = {}
    customer_data[chat_id]['name'] = message.text.strip()
    bot.send_message(chat_id, 'Введите вашу фамилию:')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    chat_id = message.chat.id
    customer_data[chat_id]['surname'] = message.text.strip()
    bot.send_message(chat_id, 'Введите ваш номер телефона:')
    bot.register_next_step_handler(message, get_phone)


def get_phone(message):
    chat_id = message.chat.id
    phone = message.text.strip()

    if not re.match(r'^(\+7|8)\d{10}$', phone):
        bot.send_message(chat_id, 'Неверный формат номера телефона. Введите номер в формате +71234567890 или 81234567890:')
        bot.register_next_step_handler(message, get_phone)
        return

    customer_data[chat_id]['phone'] = phone
    bot.send_message(chat_id, 'Введите вашу почту (например, example@mail.ru):')
    bot.register_next_step_handler(message, get_email)

def get_email(message):
        chat_id = message.chat.id
        email = message.text.strip()

        # Простейшая проверка email
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            bot.send_message(chat_id, 'Пожалуйста, введите корректный email:')
            bot.register_next_step_handler(message, get_email)
            return

        customer_data[chat_id]['email'] = email
        bot.send_message(chat_id, 'Введите услугу, которая вас заинтересовала или вопрос, который Вы бы хотели узнать у нас:')
        bot.register_next_step_handler(message, get_project_info)


def get_project_info(message):
    chat_id = message.chat.id
    orderinfo = message.text.strip()
    data = customer_data.get(chat_id, {})

    UserRequest.objects.create(
        name=data.get('name'),
        surname=data.get('surname'),
        phone=data.get('phone'),
        email=data.get('email'),
        orderinfo=orderinfo
    )

    bot.send_message(chat_id, 'Ваша заявка успешно отправлена, ожидайте обратной связи от менеджера!')
    customer_data.pop(chat_id, None)

    # уведомление менеджеру
    admin_msg = (
        f"🔔 Новая заявка в администрировании!\n"
        f"Имя: {data.get('name')}\n"
        f"Фамилия: {data.get('surname')}\n"
        f"Телефон: {data.get('phone')}\n"
    )
    bot.send_message(ADMIN_ID, admin_msg)

bot.polling(none_stop=True)
