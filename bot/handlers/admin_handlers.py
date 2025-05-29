from aiogram import Router, types
from aiogram.filters import Command
from config import ADMIN_IDS
from services import get_all_bookings

router = Router()

@router.message(Command("admin_stats"))
async def cmd_admin_stats(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("У вас нет доступа к этой команде.")
        return

    records = get_all_bookings()
    if not records:
        await message.answer("Нет записей.")
        return

    text = "| Дата | Услуга | Ник | Телефон |\n|---|---|---|---|\n"
    for r in records:
        text += f"| {r['Дата']} | {r['Услуга']} | {r['Ник']} | {r['Телефон']} |\n"
    await message.answer(f"<pre>{text}</pre>", parse_mode="HTML")
