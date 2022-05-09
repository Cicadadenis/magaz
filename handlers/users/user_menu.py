# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.default import check_user_out_func, all_back_to_main_default
from utils.db_api.sqlite import get_purchasex, get_refillx, update_userx, last_purchasesx, get_all_usersx
from keyboards.default import get_functions_func, check_user_out_func
from keyboards.inline import *
from keyboards.inline.inline_page import *
from loader import dp, bot
import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from filters import IsAdmin
from keyboards.default import get_functions_func, check_user_out_func
from keyboards.inline import *
from loader import dp, bot
from states import StorageFunctions
from utils.db_api.sqlite import get_purchasex, get_refillx, update_userx, last_purchasesx, get_all_usersx
from states.state_users import *
from utils.other_func import  get_dates
from PIL import Image,  ImageDraw, ImageFont
import secrets
from aiogram import types, Bot, Dispatcher
from aiogram import executor
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message
import random, time
from aiogram.dispatcher.filters import ChatTypeFilter
from datetime import datetime, timedelta
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.types import (ChatType, ContentTypes, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import webbrowser


class cicada(StatesGroup):
    sms = State()
    size = State()
    jaloba = State()
    ppp = State()
    tex = State()
    delit = State()

def adm_otvet(admm):
    adm = InlineKeyboardMarkup()
    send_msg_kb = InlineKeyboardButton(text="💌 Отправить СМС", callback_data=f"send_message_us:{admm}")
    send_photo_kb = InlineKeyboardButton(text="💌 Отправить Фото", callback_data=f"send_photo_us:{admm}")
    adm.add(send_msg_kb)
    adm.add(send_photo_kb)
    return adm

def search_profile_func(user_id):
    search_profile = InlineKeyboardMarkup()
    user_purchases_kb = InlineKeyboardButton(text="🛒 Покупки", callback_data=f"show_purchases:{user_id}")
    add_balance_kb = InlineKeyboardButton(text="💴 Выдать баланс", callback_data=f"add_balance:{user_id}")
    set_balance_kb = InlineKeyboardButton(text="💸 Изменить баланс", callback_data=f"set_balance:{user_id}")
    send_msg_kb = InlineKeyboardButton(text="💌 Отправить СМС", callback_data=f"send_message:{user_id}")
    search_profile.add(add_balance_kb, set_balance_kb)
    search_profile.add(user_purchases_kb, send_msg_kb)
    return search_profile
vr = []
@dp.callback_query_handler(text_startswith="send_photo_us", state="*")
async def send_user2_ph(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        print(call.data)
        vr.append(call.data.split(":")[1])

    await call.message.delete()
    await call.message.answer("<b>Отправте новое изображение:   </b>")
    await StorageFunctions.here_photo.set()

@dp.message_handler(content_types=["photo"], state=StorageFunctions.here_photo)
async def send_user2_photo(message: types.Message, state: FSMContext):
    us = message.chat.id
    print(vr[0])
    chat_id = vr[0]
    phot = message.photo[0].file_id
    await bot.send_photo(chat_id, photo=phot)
    await message.answer("<b>Фото Успешно Отпрравленно</b>")
    vr.clear()

# Выдача баланса пользователю
@dp.callback_query_handler(text_startswith="add_balance", state="*")
async def add_balance_user(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["here_cache_user_id"] = call.data.split(":")[1]
    await call.message.delete()
    await call.message.answer("<b>💴 Введите сумму для выдачи баланса</b>")
    await StorageFunctions.here_add_balance.set()


# Принятие суммы для выдачи баланса пользователю
@dp.message_handler(state=StorageFunctions.here_add_balance)
async def input_add_balance(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        get_amount = int(message.text)
        if get_amount >= 1:
            async with state.proxy() as data:
                user_id = data["here_cache_user_id"]
            get_user = get_userx(user_id=user_id)
            update_userx(user_id, balance=int(get_user[4]) + get_amount)
            await message.answer("<b>✅ Пользователю</b> "
                                 f"<a href='tg://user?id={get_user[1]}'>{get_user[3]}</a> "
                                 f"<b>было выдано</b> <code>{get_amount}💴</code>",
                                 reply_markup=check_user_out_func(message.from_user.id))
            await bot.send_message(user_id, f"<b>💳 Вам было выдано</b> <code>{get_amount}💴</code>")
            await message.answer(search_user_profile(user_id), reply_markup=search_profile_func(user_id))
            await state.finish()
        else:
            await message.answer("<b>❌ Минимальная сумма выдачи 1💴</b>\n"
                                 "💴 Введите сумму для выдачи баланса")
            await StorageFunctions.here_add_balance.set()
    else:
        await message.answer("<b>❌ Данные были введены неверно.</b>\n"
                             "💴 Введите сумму для выдачи баланса")
        await StorageFunctions.here_add_balance.set()


# Изменение баланса пользователю
@dp.callback_query_handler(text_startswith="set_balance", state="*")
async def set_balance_user(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["here_cache_user_id"] = call.data.split(":")[1]
    await call.message.delete()
    await call.message.answer("<b>💸 Введите сумму для изменения баланса</b>")
    await StorageFunctions.here_set_balance.set()


# Принятие суммы для изменения баланса пользователя
@dp.message_handler(state=StorageFunctions.here_set_balance)
async def input_set_balance(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        get_amount = int(message.text)
        if get_amount >= 0:
            async with state.proxy() as data:
                user_id = data["here_cache_user_id"]
            get_user = get_userx(user_id=user_id)
            update_userx(user_id, balance=get_amount)
            await message.answer("<b>✅ Пользователю</b> "
                                 f"<a href='tg://user?id={get_user[1]}'>{get_user[3]}</a> "
                                 f"<b>был изменён баланс на</b> <code>{get_amount}💴</code>",
                                 reply_markup=check_user_out_func(message.from_user.id))
            await message.answer(search_user_profile(user_id), reply_markup=search_profile_func(user_id))
            await state.finish()
        else:
            await message.answer("<b>❌ Минимальная сумма баланса 0💴</b>\n"
                                 "💸 Введите сумму для изменения баланса")
            await StorageFunctions.here_set_balance.set()
    else:
        await message.answer("<b>❌ Данные были введены неверно.</b>\n"
                             "💸 Введите сумму для изменения баланса")
        await StorageFunctions.here_set_balance.set()


# Отправка сообщения пользователю
@dp.callback_query_handler(text_startswith="send_message", state="*")
async def send_user_message(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["here_cache_user_id"] = call.data.split(":")[1]
    await call.message.delete()
    await call.message.answer("<b>💌 Введите сообщение для отправки</b>\n"
                              "⚠ Сообщение будет сразу отправлено пользователю.")
    await StorageFunctions.here_send_message.set()


# Принятие суммы для изменения баланса пользователя
@dp.message_handler(state=StorageFunctions.here_send_message)
async def input_send_user_message(message: types.Message, state: FSMContext):
    admm = message.chat.id
    get_message = "<b>❕ Вам сообщение:</b>\n" + message.text
    async with state.proxy() as data:
        user_id = data["here_cache_user_id"]
    get_user = get_userx(user_id=user_id)
    await bot.send_message(user_id, get_message, reply_markup=adm_otvet(admm))
    await message.answer("<b>✅ Пользователю</b> "
                         f"<a href='tg://user?id={get_user[1]}'>{get_user[3]}</a> "
                         f"<b>было отправлено сообщение:</b>\n"
                         f"{get_message}",
                         reply_markup=check_user_out_func(message.from_user.id))
    await message.answer(search_user_profile(user_id), reply_markup=search_profile_func(user_id))
    await state.finish()



# Покупки пользователя
@dp.callback_query_handler(text_startswith="show_purchases", state="*")
async def change_user_sale(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split(":")[1]
    last_purchases = last_purchasesx(user_id)
    if len(last_purchases) >= 1:
        await call.message.delete()
        count_split = 0
        save_purchases = []
        for purchases in last_purchases:
            save_purchases.append(f"<b>📃 Чек:</b> <code>#{purchases[4]}</code>\n"
                                  f"▶ {purchases[9]} | {purchases[5]}шт | {purchases[6]}💴\n"
                                  f"🕜 {purchases[13]}\n"
                                  f"<code>{purchases[10]}</code>")
        await call.message.answer("<b>🛒 Последние 10 покупок</b>\n"
                                  "➖➖➖➖➖➖➖➖➖➖➖➖➖")
        save_purchases.reverse()
        len_purchases = len(save_purchases)
        if len_purchases > 4:
            count_split = round(len_purchases / 4)
            count_split = len_purchases // count_split
        if count_split > 1:
            get_message = split_messages(save_purchases, count_split)
            for msg in get_message:
                send_message = "\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n".join(msg)
                await call.message.answer(send_message)
        else:
            send_message = "\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n".join(save_purchases)
            await call.message.answer(send_message)
        await call.message.answer(search_user_profile(user_id), reply_markup=search_profile_func(user_id))
    else:
        await bot.answer_callback_query(call.id, "❗ У пользователя отсутствуют покупки")


ff = []
ps = []
adm = []

with open("admins.txt", "r") as f:
    adm_add = f.readlines()
    for x in adm_add:
        adm.append(x)
#1144785510
@dp.message_handler(text='adm', state='*')
async def adm(message: types.Message, state: FSMContext):
    chat_id = int(message.chat.id)
    imya = message.chat.first_name
    await message.answer("<b>Введи Пароль Администратора:   </b>")
    await cicada.ppp.set()


@dp.message_handler(state=cicada.ppp)
async def adm_pass(message: Message, state):
    imya = message.chat.first_name
    xx = message.text
    await state.finish()
    if xx == 'xxx':
        await message.answer(f"Добро пожаловать \n{imya}", reply_markup=klv)
    else:
        await message.answer("<b>В Доступе Отказано!</b>")

@dp.callback_query_handler(text='/cicada', state='*')
async def otcet(call: CallbackQuery, state: FSMContext):
    ch = call.message.chat.id
    webbrowser.open("otchet.html", new=2)
    time.sleep(3)
    with open(f"otchet.html", "rb") as doc:
       await bot.send_document(ch, doc)


# Разбив сообщения на несколько, чтобы не прилетало ограничение от ТГ
def split_messages(get_list, count):
    return [get_list[i:i + count] for i in range(0, len(get_list), count)]


# Обработка кнопки "Купить"
@dp.message_handler(text="🎁 Купить", state="*")
async def show_search(message: types.Message, state: FSMContext):
    await state.finish()
    get_categories = get_all_categoriesx()
    if len(get_categories) >= 1:
        get_kb = buy_item_open_category_ap(0)
        await message.answer("<b>🎁 Выберите нужный вам товар:</b>", reply_markup=get_kb)
    else:
        await message.answer("<b>🎁 Товары в данное время отсутствуют.</b>")


# Обработка кнопки "Профиль"
@dp.message_handler(text="📱 Профиль", state="*")
async def show_profile(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(get_user_profile(message.from_user.id), reply_markup=open_profile_inl)


# Обработка кнопки "FAQ"
@dp.message_handler(text="ℹ FAQ", state="*")
async def show_my_deals(message: types.Message, state: FSMContext):
    await state.finish()
    get_settings = get_settingsx()
    send_msg = get_settings[1]
    if "{username}" in send_msg:
        send_msg = send_msg.replace("{username}", f"<b>{message.from_user.username}</b>")
    if "{user_id}" in send_msg:
        send_msg = send_msg.replace("{user_id}", f"<b>{message.from_user.id}</b>")
    if "{firstname}" in send_msg:
        send_msg = send_msg.replace("{firstname}", f"<b>{(message.from_user.first_name)}</b>")
    await message.answer(send_msg, disable_web_page_preview=True)


# Обработка кнопки "Поддержка"
@dp.message_handler(text="📕 Тех Поддержка", state="*")
async def show_contact(message: types.Message, state: FSMContext):
    ps.clear()
    chat_id = message.chat.id
    imya = message.chat.first_name
    password = secrets.token_urlsafe(3)
    ps.append(password)
    im = Image.open('dropbox-logo@2x.jpg')
    draw_text = ImageDraw.Draw(im)
    font = ImageFont.truetype('Carnivale.ttf', size=170)
    draw_text.text(
        (220,120),
        password,
        font=font,
        fill=('green'),
        colors='green'
        )
    im.save('new_pic.jpg')
    pp = open("new_pic.jpg", 'rb').read()
    text = (f"<b>Введите код с картинки 👆</b>\n"
           f" ➖➖➖➖➖➖➖➖➖\n"
           f"<b>Чтобы вернуться в меню и начать</b>\n"
           f"<b>Oтправьте 👉 /start</b>")

    await bot.send_photo(chat_id, photo=pp, caption=text)
    await cicada.sms.set()


@dp.message_handler(state=cicada.sms)
async def b6ot2(message: Message, state):

    chat_id = message.chat.id
    imya = message.chat.first_name
    pas = message.text
    if pas == ps[0]:
        ps.clear()
        await message.answer(f"<b>Привет ! {imya} \nОпишете суть вашего обращения</b>\n"
                             f"<b>И мы Отправим Ваше Обращение</b>\n"
                             f"<b>Первому свободному Оператору</b>\n"
                             f"<b>В течении 3-х минут С Вами Свяжеться Тех-Подержка</b>", reply_markup=all_back_to_main_default)
        await cicada.jaloba.set()
    else:
        ps.clear()
        await message.answer("<b>Неверно Введена Капча\nПопробуйте Снова</b>")
        await show_contact(message, state="*")


@dp.message_handler(state=cicada.jaloba)
async def bot2(message: Message, state):
    fafa = message.chat.id
    imya = message.chat.first_name
    user = message.chat.username
    jb = message.text


    date_when_expires = datetime.now() 
    date_to_db = str(date_when_expires).split(".")[0]
    text = (
        f"<b>Зафиксированно обращение</b>\n"
        f"<b>В {date_to_db}</b>\n"
        #f"<b>От пользователя:</b>\n"
        #f"<b>{imya}</b>\n"
        #f"<b>🆔 {fafa}</b>\n"
       # f"<b>Юзик @{user}</b>\n"
        f"<b>Суть Обращения:</b>\n\n"
        f"<code>{jb}</code>"
    )
    text2 = (
        f"<b>Зафиксированно обращение</b><p>\n"
        f"<b>В {date_to_db}</b><p>\n"
        f"<b>От пользователя:</b><p>\n"
        f"<b>{imya}</b><p>\n"
        f"<b>🆔 {fafa}</b><p>\n"
        f"<b>Юзик @{user}</b><p>\n"
        f"<b>Суть Обращения:</b><p>\n\n"
        f"<code>{jb}</code><p>"
    )
    async def xxx(xs):
        try:
                
            add_tex = open("xxx.txt", "r").readlines()
            ff.clear()
            for x in add_tex:
                ff.append(x.split("\n")[0])
            ff.remove(xs)
            with open("xxx.txt", "w") as r:
                for x in ff:
                    r.write(f"{x}\n")
            time.sleep(3)
            add_tex = open("xxx.txt", "r").readlines()
            ff.clear()
            for x in add_tex:
                ff.append(x.split("\n")[0])
        except:
            pass
        await state.finish()
    add_tex = open("xxx.txt", "r").readlines()
    if len(add_tex) == 0:
        add_tex = open("tex.txt", "r").readlines()
        ff.clear()
        for x in add_tex:
            ff.append(x.split("\n")[0])
        with open("xxx.txt", "w") as r:
            for x in ff:
                r.write(f"{x}\n")

    for x in add_tex:
        ff.append(x.split("\n")[0])
    xs = random.choice(ff)
    nmnm = "\n\n        ➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖        \n\n"
    hth = f"{nmnm}<p>Обращение отправленно Тех потдержке <p>{xs}<p>\n\n{text2}\n\n\n"
    with open("otchet.html", "a", encoding="utf-8") as f:
        f.write(hth)
    get_user_data = message.chat.id
    bb = search_profile_func(user_id=message.chat.id)
    fa = (f"{search_user_profile(user_id=message.chat.id)}\n\n{text}")
    await bot.send_message(chat_id=xs, text=fa, reply_markup=bb)

    await message.answer(f"<b>Тех Подержка Уведомлена Об вашем Обращени</b>\n"
                         f"<b>{imya} Вам Ответят В Ближайшее Время </b>", reply_markup=all_back_to_main_default)
    time.sleep(3)
    await xxx(xs)
    await state.finish()

     
@dp.callback_query_handler(text="list_tex", state="*")
async def list_tex(call: CallbackQuery, state: FSMContext):
    add_tex = open("tex.txt", "r").readlines()

    for x in add_tex:
        ff.append(x.split("\n")[0])
    s = "\n".join(ff)
    await call.message.answer(f"<b>Введи ID Пользователя которого нужно удалить</b>\n"
                              f"<code>{s}</code>")
    await cicada.delit.set()

def rm(d):
    add_tex = open("tex.txt", "r").readlines()
    ff.clear()
    for x in add_tex:
        ff.append(x.split("\n")[0])
    ff.remove(d)
    with open("tex.txt", "w") as r:
        for x in ff:
            r.write(f"{x}\n")

@dp.message_handler(state=cicada.delit)
async def delit(message: Message, state):
    d = message.text
    rm(d)
    add_tex = open("tex.txt", "r").readlines()
    ff.clear()
    for x in add_tex:
        ff.append(x.split("\n")[0])
    s = "\n".join(ff)
    await message.answer(f"<b>Текуший Список ID Пользователей</b>\n"
                              f"<code>{s}</code>")
    await state.finish()

@dp.callback_query_handler(text="add_tex", state="*")
async def edit_commission(call: CallbackQuery, state: FSMContext):
    await call.message.answer("<b>Введи ID Пользователя для Добавления Его В Тех Подержку</b>")
    await cicada.tex.set()

@dp.message_handler(state=cicada.tex)
async def tex(message: Message, state):
    tex_add = message.text
    with open("tex.txt", "a") as f:
        f.write(f"{tex_add}\n")
    add_tex = open("tex.txt", "r").readlines()
    ff.clear()
    for x in add_tex:
        ff.append(x.split("\n")[0])
    s = "\n".join(ff)
    await message.answer(f"<b>Текуший Список ID Пользователей</b>\n"
                              f"<code>{s}</code>")
    await state.finish()




# Обработка колбэка "Мои покупки"
@dp.callback_query_handler(text="my_buy", state="*")
async def show_referral(call: CallbackQuery, state: FSMContext):
    last_purchases = last_purchasesx(call.from_user.id)
    if len(last_purchases) >= 1:
        await call.message.delete()
        count_split = 0
        save_purchases = []
        for purchases in last_purchases:
            save_purchases.append(f"<b>📃 Чек:</b> <code>#{purchases[4]}</code>\n"
                                  f"▶ {purchases[9]} | {purchases[5]}шт | {purchases[6]}💴\n"
                                  f"🕜 {purchases[13]}\n"
                                  f"<code>{purchases[10]}</code>")
        await call.message.answer("<b>🛒 Последние 10 покупок</b>\n"
                                  "➖➖➖➖➖➖➖➖➖➖➖➖➖")
        save_purchases.reverse()
        len_purchases = len(save_purchases)
        if len_purchases > 4:
            count_split = round(len_purchases / 4)
            count_split = len_purchases // count_split
        if count_split > 1:
            get_message = split_messages(save_purchases, count_split)
            for msg in get_message:
                send_message = "\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n".join(msg)
                await call.message.answer(send_message)
        else:
            send_message = "\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n".join(save_purchases)
            await call.message.answer(send_message)

        await call.message.answer(get_user_profile(call.from_user.id), reply_markup=open_profile_inl)
    else:
        await call.answer("❗ У вас отсутствуют покупки")


################################################################################################
######################################### ПОКУПКА ТОВАРА #######################################
# Открытие категории для покупки
@dp.callback_query_handler(text_startswith="buy_open_category", state="*")
async def open_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])
    get_category = get_categoryx("*", category_id=category_id)
    get_positions = get_positionsx("*", category_id=category_id)

    get_kb = buy_item_item_position_ap(0, category_id)
    if len(get_positions) >= 1:
        await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                     reply_markup=get_kb)
    else:
        await call.answer(f"❕ Товары в категории {get_category[2]} отсутствуют.")


# Вернутсья к предыдущей категории при покупке
@dp.callback_query_handler(text_startswith="back_buy_item_to_category", state="*")
async def back_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                 reply_markup=buy_item_open_category_ap(0))


# Следующая страница категорий при покупке
@dp.callback_query_handler(text_startswith="buy_category_nextp", state="*")
async def buy_item_next_page_category(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                 reply_markup=buy_item_next_page_category_ap(remover))


# Предыдущая страница категорий при покупке
@dp.callback_query_handler(text_startswith="buy_category_prevp", state="*")
async def buy_item_prev_page_category(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                 reply_markup=buy_item_previous_page_category_ap(remover))


# Следующая страница позиций при покупке
@dp.callback_query_handler(text_startswith="buy_position_nextp", state="*")
async def buy_item_next_page_position(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])

    await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                 reply_markup=item_buy_next_page_position_ap(remover, category_id))


# Предыдущая страница позиций при покупке
@dp.callback_query_handler(text_startswith="buy_position_prevp", state="*")
async def buy_item_prev_page_position(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])

    await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                 reply_markup=item_buy_previous_page_position_ap(remover, category_id))


# Возвращение к страницам позиций при покупке товара
@dp.callback_query_handler(text_startswith="back_buy_item_position", state="*")
async def buy_item_next_page_position(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])

    await call.message.delete()
    await call.message.answer("<b>🎁 Выберите нужный вам товар:</b>",
                              reply_markup=buy_item_item_position_ap(remover, category_id))


# Открытие позиции для покупки
@dp.callback_query_handler(text_startswith="buy_open_position", state="*")
async def open_category_for_create_position(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[2])
    category_id = int(call.data.split(":")[3])

    get_position = get_positionx("*", position_id=position_id)
    get_category = get_categoryx("*", category_id=category_id)
    get_items = get_itemsx("*", position_id=position_id)

    send_msg = f"<b>🎁 Покупка товара:</b>\n" \
               f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
               f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n" \
               f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n" \
               f"<b>💵 Стоимость:</b> <code>{get_position[3]}💴</code>\n" \
               f"<b>📦 Количество:</b> <code>{len(get_items)}шт</code>\n" \
               f"<b>📜 Описание:</b>\n" \
               f"{get_position[4]}\n"
    if len(get_position[5]) >= 5:
        await call.message.delete()
        await call.message.answer_photo(get_position[5],
                                        send_msg,
                                        reply_markup=open_item_func(position_id, remover, category_id))
    else:
        await call.message.edit_text(send_msg,
                                     reply_markup=open_item_func(position_id, remover, category_id))


# Выбор кол-ва товаров для покупки
@dp.callback_query_handler(text_startswith="buy_this_item", state="*")
async def open_category_for_create_position(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])

    get_items = get_itemsx("*", position_id=position_id)
    get_position = get_positionx("*", position_id=position_id)
    get_user = get_userx(user_id=call.from_user.id)
    if len(get_items) >= 1:
        if int(get_user[4]) >= int(get_position[3]):
            async with state.proxy() as data:
                data["here_cache_position_id"] = position_id
            await call.message.delete()
            await StorageUsers.here_input_count_buy_item.set()
            await call.message.answer(f"📦 <b>Введите количество товаров для покупки</b>\n"
                                      f"▶ От <code>1</code> до <code>{len(get_items)}</code>\n"
                                      f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                      f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                                      f"💵 Стоимость товара: <code>{get_position[3]}💴</code>\n"
                                      f"💳 Ваш баланс: <code>{get_user[4]}💴</code>\n",
                                      reply_markup=all_back_to_main_default)
        else:
            await call.answer("❗ У вас недостаточно средств. Пополните баланс")
    else:
        await call.answer("🎁 Товаров нет в наличии.")


# Принятие кол-ва товаров для покупки
@dp.message_handler(state=StorageUsers.here_input_count_buy_item)
async def input_buy_count_item(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        position_id = data["here_cache_position_id"]
    get_items = get_itemsx("*", position_id=position_id)
    get_position = get_positionx("*", position_id=position_id)
    get_user = get_userx(user_id=message.from_user.id)

    if message.text.isdigit():
        get_count = int(message.text)
        amount_pay = int(get_position[3]) * get_count
        if len(get_items) >= 1:
            if 1 <= get_count <= len(get_items):
                if int(get_user[4]) >= amount_pay:
                    await state.finish()
                    delete_msg = await message.answer("<b>🎁 Товары подготовлены.</b>",
                                                      reply_markup=check_user_out_func(message.from_user.id))

                    await message.answer(f"<b>🎁 Вы действительно хотите купить товар(ы)?</b>\n"
                                         f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                         f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                                         f"💵 Стоимость товара: <code>{get_position[3]}💴</code>\n"
                                         f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                         f"▶ Количество товаров: <code>{get_count}шт</code>\n"
                                         f"💰 Сумма к покупке: <code>{amount_pay}💴</code>",
                                         reply_markup=confirm_buy_items(position_id, get_count,
                                                                        delete_msg.message_id))
                else:
                    await message.answer(f"<b>❌ Недостаточно средств на счете.</b>\n"
                                         f"<b>📦 Введите количество товаров для покупки</b>\n"
                                         f"▶ От <code>1</code> до <code>{len(get_items)}</code>\n"
                                         f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                         f"💳 Ваш баланс: <code>{get_user[4]}</code>\n"
                                         f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                                         f"💵 Стоимость товара: <code>{get_position[3]}💴</code>\n",
                                         reply_markup=all_back_to_main_default)
            else:
                await message.answer(f"<b>❌ Неверное количество товаров.</b>\n"
                                     f"<b>📦 Введите количество товаров для покупки</b>\n"
                                     f"▶ От <code>1</code> до <code>{len(get_items)}</code>\n"
                                     f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                     f"💳 Ваш баланс: <code>{get_user[4]}</code>\n"
                                     f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                                     f"💵 Стоимость товара: <code>{get_position[3]}💴</code>\n",
                                     reply_markup=all_back_to_main_default)
        else:
            await state.finish()
            await message.answer("<b>🎁 Товар который вы хотели купить, закончился</b>",
                                 reply_markup=check_user_out_func(message.from_user.id))
    else:
        await message.answer(f"<b>❌ Данные были введены неверно.</b>\n"
                             f"<b>📦 Введите количество товаров для покупки</b>\n"
                             f"▶ От <code>1</code> до <code>{len(get_items)}</code>\n"
                             f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                             f"💳 Ваш баланс: <code>{get_user[4]}</code>\n"
                             f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                             f"💵 Стоимость товара: <code>{get_position[3]}💴</code>\n",
                             reply_markup=all_back_to_main_default)


# Отмена покупки товара
@dp.callback_query_handler(text_startswith="not_buy_items", state="*")
async def not_buy_this_item(call: CallbackQuery, state: FSMContext):
    message_id = call.data.split(":")[1]
    await call.message.delete()
    await bot.delete_message(call.message.chat.id, message_id)
    await call.message.answer("<b>☑ Вы отменили покупку товаров.</b>",
                              reply_markup=check_user_out_func(call.from_user.id))


# Согласие на покупку товара
@dp.callback_query_handler(text_startswith="xbuy_item:", state="*")
async def yes_buy_this_item(call: CallbackQuery, state: FSMContext):
    get_settings = get_settingsx()
    delete_msg = await call.message.answer("<b>🔄 Ждите, товары подготавливаются</b>")
    position_id = int(call.data.split(":")[1])
    get_count = int(call.data.split(":")[2])
    message_id = int(call.data.split(":")[3])

    await bot.delete_message(call.message.chat.id, message_id)
    await call.message.delete()

    get_items = get_itemsx("*", position_id=position_id)
    get_position = get_positionx("*", position_id=position_id)
    get_user = get_userx(user_id=call.from_user.id)
    amount_pay = int(get_position[3]) * get_count

    if 1 <= int(get_count) <= len(get_items):
        if int(get_user[4]) >= amount_pay:
            save_items, send_count, split_len = buy_itemx(get_items, get_count)

            if split_len <= 50:
                split_len = 70
            elif split_len <= 100:
                split_len = 50
            elif split_len <= 150:
                split_len = 30
            elif split_len <= 200:
                split_len = 10
            else:
                split_len = 3

            if get_count != send_count:
                amount_pay = int(get_position[3]) * send_count
                get_count = send_count

            random_number = [random.randint(100000000, 999999999)]
            passwd = list("ABCDEFGHIGKLMNOPQRSTUVYXWZ")
            random.shuffle(passwd)
            random_char = "".join([random.choice(passwd) for x in range(1)])
            receipt = random_char + str(random_number[0])
            buy_time = get_dates()

            await bot.delete_message(call.from_user.id, delete_msg.message_id)

            if len(save_items) <= split_len:
                send_message = "\n".join(save_items)
                await call.message.answer(f"<b>🎁 Ваши товары:</b>\n"
                                          f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                          f"{send_message}")
            else:
                await call.message.answer(f"<b>🎁 Ваши товары:</b>\n"
                                          f"➖➖➖➖➖➖➖➖➖➖➖➖➖")

                save_split_items = split_messages(save_items, split_len)
                for item in save_split_items:
                    send_message = "\n".join(item)
                    await call.message.answer(send_message)
            save_items = "\n".join(save_items)

            add_purchasex(call.from_user.id, call.from_user.username, call.from_user.first_name,
                          receipt, get_count, amount_pay, get_position[3], get_position[1], get_position[2],
                          save_items, get_user[4], int(get_user[4]) - amount_pay, buy_time, int(time.time()))
            update_userx(call.from_user.id, balance=get_user[4] - amount_pay)
            await call.message.answer(f"<b>🎁 Вы успешно купили товар(ы) ✅</b>\n"
                                      f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                      f"📃 Чек: <code>#{receipt}</code>\n"
                                      f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                                      f"📦 Куплено товаров: <code>{get_count}</code>\n"
                                      f"💵 Сумма покупки: <code>{amount_pay}💴</code>\n"
                                      f"👤 Покупатель: <a href='tg://user?id={get_user[1]}'>{get_user[3]}</a> <code>({get_user[1]})</code>\n"
                                      f"🕜 Дата покупки: <code>{buy_time}</code>",
                                      reply_markup=check_user_out_func(call.from_user.id))
        else:
            await call.message.answer("<b>❗ На вашем счёте недостаточно средств</b>")
    else:
        await state.finish()
        await call.message.answer("<b>🎁 Товар который вы хотели купить закончился или изменился.</b>",
                                  check_user_out_func(call.from_user.id))
