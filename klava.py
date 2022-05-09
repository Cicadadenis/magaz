from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, inline_keyboard


klv = InlineKeyboardMarkup(row_width=1)
klv.add(
    InlineKeyboardButton('➕ Добавить Теха', callback_data='add_tex'),
    InlineKeyboardButton('➖ Удалить  Теха', callback_data='list_tex'),
    InlineKeyboardButton(' Отчет', callback_data='/cicada')

)