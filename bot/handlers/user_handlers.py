import os
from aiogram import Router, types, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards import SERVICES, main_menu, faq_menu_markup, service_pagination_markup
from config import ADMIN_IDS
from services import add_booking

router = Router()


class Booking(StatesGroup):
    waiting_for_phone = State()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    text = """
🎯 Маркетинговые инструменты - для Людей и Бизнеса! 🌟

🎨 Генерация реалистичных говорящих и управляемых вами Аватаров для соцсетей, чат-ботов, презентаций, мастер-классов и обучающих курсов.

🎥 Анимация: презентаций, логотипов компаний и брендов, создание уникальных карточек товаров в 3D, услуг и инструкций.

🌟 Продакшн креативных рекламных роликов, презентаций и личных видео-визиток.
    """
    await message.answer(text=text, reply_markup=main_menu())


@router.message(lambda m: m.text == "🏢 О компании")
async def about_company(message: types.Message):
    text = """
🚀 Добро пожаловать в [Название компании]!

Мы — эксперты в сфере IT, создаем инновационные решения для вашего бизнеса.

🔹 Что мы делаем:
— Разработка веб- и мобильных приложений  
— Облачные технологии и интеграции  
— Кибербезопасность  
— IT-консалтинг и поддержка

🔹 Наши преимущества:
— Более 10 лет опыта  
— Команда профессионалов  
— Решения под ваши задачи

✨ Хотите узнать больше? Перейдите на сайт!
    """
    await message.answer(text, reply_markup=main_menu(show_website=True))


@router.message(lambda m: m.text == "📚 FAQ")
async def faq_menu(message: types.Message):
    await message.answer("Выберите вопрос:", reply_markup=faq_menu_markup())


@router.message(lambda m: m.text and m.text.startswith("Вопрос"))
async def faq_answer(message: types.Message):
    video_map = {
        "Вопрос 1": "videos/video_2025-05-29_14-37-40.mp4",
        "Вопрос 2": "videos/video_2025-05-29_14-37-46.mp4",
    }

    path = video_map.get(message.text)
    if path and os.path.exists(path):
        video_file = FSInputFile(path)
        await message.answer_video(video=video_file, caption=message.text)
    else:
        await message.answer("Видео для этого вопроса пока недоступно.")


@router.message(lambda m: m.text == "🛎️ Услуги")
async def services_list(message: types.Message, state: FSMContext, bot: Bot):
    await state.update_data(idx=0)
    await _send_service(message.chat.id, state, bot)


async def _send_service(chat_id: int, state: FSMContext, bot: Bot):
    data = await state.get_data()
    idx = data.get("idx", 0)
    service = SERVICES[idx]
    markup = service_pagination_markup(idx, len(SERVICES))
    await bot.send_message(chat_id, service, reply_markup=markup)


@router.callback_query(lambda c: c.data in ("prev_service", "next_service", "book_service"))
async def service_navigation(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    idx = data.get("idx", 0)

    if callback.data == "prev_service":
        idx = (idx - 1) % len(SERVICES)
    elif callback.data == "next_service":
        idx = (idx + 1) % len(SERVICES)
    elif callback.data == "book_service":
        await state.set_state(Booking.waiting_for_phone)
        await callback.message.answer("📞Введите номер телефона (11 цифр, начинается с 8):\nПример: 89999999999")
        await callback.answer()
        return

    await state.update_data(idx=idx)
    await callback.message.edit_text(SERVICES[idx], reply_markup=service_pagination_markup(idx, len(SERVICES)))
    await callback.answer()


@router.message(StateFilter(Booking.waiting_for_phone))
async def process_phone(message: types.Message, state: FSMContext, bot: Bot):
    phone = message.text.strip()
    if not (phone.isdigit() and len(phone) == 11 and phone.startswith("8")):
        return await message.answer("Неверный формат. Введите номер телефона из 11 цифр, начинается с 8.")

    data = await state.get_data()
    idx = data.get("idx")
    service = SERVICES[idx]
    username = message.from_user.username or ""
    add_booking(service, username, phone)

    await message.answer("Спасибо! Ваша заявка на услугу принята. Мы свяжемся с вами в ближайшее время.")

    await state.clear()


@router.message(lambda m: m.text == "📞 Связь с нами")
async def contact_us(message: types.Message):
    contact_text = (
        "📞 Телефон: +7 999 999 99 99\n"
        "✉️ Email: info@example.com\n"
        "🌐 Соцсети: https://t.me/yourchannel\n\n"
    )

    if not ADMIN_IDS:
        admins_text = "Связь с менеджерами: нет доступных менеджеров."
    else:
        admins_text = "Связь с менеджерами:\n"
        for admin_id in ADMIN_IDS:
            try:
                chat = await message.bot.get_chat(admin_id)
                if chat.username:
                    admins_text += f"@{chat.username}\n"
                else:
                    admins_text += f"Менеджер {admin_id} (нет username)\n"
            except Exception as e:
                admins_text += f"Менеджер {admin_id} (ошибка: {e})\n"

    await message.answer(contact_text + admins_text)



@router.message(lambda m: m.text == "🔙 Назад")
async def go_back_to_main_menu(message: types.Message):
    await message.answer("Вы вернулись в главное меню:", reply_markup=main_menu())


@router.message(lambda m: m.text == "🌐 Перейти на сайт")
async def open_website(message: types.Message):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Открыть сайт 🌐", url="https://example.com")]
        ]
    )
    await message.answer("Нажмите кнопку ниже, чтобы перейти на наш сайт:", reply_markup=markup)
