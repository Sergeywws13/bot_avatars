from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

SERVICES = ["🛠️ Услуга 1", "🧰 Услуга 2", "🧪 Услуга 3"]
FAQ_QUESTIONS = ["Вопрос 1", "Вопрос 2"]


def main_menu(show_website: bool = False) -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="🏢 О компании"), KeyboardButton(text="🛎️ Услуги")],
        [KeyboardButton(text="📚 FAQ"), KeyboardButton(text="📞 Связь с нами")]
    ]

    if show_website:
        buttons.append([KeyboardButton(text="🌐 Перейти на сайт")])

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def service_pagination_markup(current_idx: int, total: int):
    buttons = []

    if total > 1:
        buttons.append([
            InlineKeyboardButton(text="⬅️ Назад", callback_data="prev_service"),
            InlineKeyboardButton(text="Вперёд ➡️", callback_data="next_service")
        ])

    buttons.append([
        InlineKeyboardButton(text="📝 Записаться", callback_data="book_service")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

def faq_menu_markup() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=q)] for q in FAQ_QUESTIONS] + [[KeyboardButton(text="🔙 Назад")]],
        resize_keyboard=True
    )

def contact_inline() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✉️ Написать админу", callback_data="contact_admin")]
        ]
    )

