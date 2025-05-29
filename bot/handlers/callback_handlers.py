from aiogram import Bot, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from config import ADMIN_IDS
from keyboards import SERVICES
from handlers.user_handlers import Booking, _send_service

router = Router()

"""
Обработчик callback_query для кнопок ВПЕРЕД и НАЗАД
"""
@router.callback_query(lambda c: c.data in ['next', 'prev'])
async def services_cb(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    idx = data.get('idx', 0)
    if callback.data == 'next':
        idx = (idx + 1) % len(SERVICES)
    elif callback.data == 'prev':
        idx = (idx - 1) % len(SERVICES)

    await state.update_data(idx=idx)
    await callback.message.delete()
    await _send_service(callback.message.chat.id, state)
    await callback.answer()


@router.callback_query(lambda c: c.data == 'book')
async def book_cb(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(Booking.waiting_for_phone)
    text="""
    📞Введите номер телефона (11 цифр, начинается с 8):
    Пример: 89999999999
    """
    
    await callback.message.answer(text=text)
    await callback.answer()


@router.callback_query(lambda c: c.data == "contact_admin")
async def handle_contact_admin(callback: CallbackQuery, bot: Bot):
    user = callback.from_user
    username = f"@{user.username}" if user.username else "(без username)"

    await bot.send_message(
        ADMIN_IDS,
        f"🔔 Пользователь хочет связаться с вами:\n\n"
        f"👤 Имя: {user.full_name}\n"
        f"🆔 ID: {user.id}\n"
        f"📎 Username: {username}"
    )

    await callback.message.answer("✅ Спасибо! Администратор свяжется с вами в ближайшее время.")
    await callback.answer()
