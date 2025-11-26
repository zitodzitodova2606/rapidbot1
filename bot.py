# bot.py
# RapidSchool — to'liq, barqaror Telegram bot
# Python 3.10+ va pyTelegramBotAPI kerak

import os
import time
import json
import traceback
from telebot import TeleBot, types

# ============ CONFIG ============
TELEGRAM_TOKEN = "8335173637:AAHTDqKg01vJGlg5kFOTguD5_nCsVSQS0kE"
ADMIN_CHAT_IDS = [5564746814, 5606069749]
CHANNEL_LINK = "https://t.me/+jS-EaqspbHEwYmVi"
ADMIN_USERNAME = "@rapid_school"

# ================= DATA YO‘LLARI =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))      # bot.py joylashgan papka
DATA_DIR = os.path.join(BASE_DIR, "data")                  # data papka
USERS_FILE = os.path.join(DATA_DIR, "users.json")          # foydalanuvchi bazasi
SCREENSHOTS_DIR = os.path.join(DATA_DIR, "screenshots")    # screenshotlar papkasi
WELCOME_PHOTO = os.path.join(BASE_DIR, "welcome.jpg")      # welcome rasm

# Papkalarni tekshirish/yaratish
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=2)

# ================= BOT OBYEKTI =================
bot = TeleBot(TELEGRAM_TOKEN, parse_mode=None)

# ================= HELPERS =================
def safe_load_users():
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return {}
            return data
    except Exception:
        return {}

def safe_save_users(users):
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("users save error:", e)

def ensure_user(chat_id):
    users = safe_load_users()
    sid = str(chat_id)
    if sid not in users:
        users[sid] = {
            "phone": None,
            "pending_screenshot": None,
            "payment_made": False,
            "approved": False,
            "created_at": int(time.time())
        }
        safe_save_users(users)
    return users

def update_user_field(chat_id, key, value):
    users = safe_load_users()
    sid = str(chat_id)
    if sid not in users:
        users[sid] = {}
    users[sid][key] = value
    safe_save_users(users)

def get_user(chat_id):
    users = safe_load_users()
    return users.get(str(chat_id), {})

# ============ LONG TEXTS (AS-IS, NO SHORTENING) ============
WELCOME_CAPTION = (
    "📖 Assalomu alaykum Zamonaviy Rejissura + Open AI online kursiga hush kelibsiz!\n\n"
    "Siz bu kurs orqali 500$+ 1000$ daromadli ishga ega bo'lishingiz va professionallikga qadam qo'yishingiz aniq! "
    "Bu kursni Xoziroq Supper chegirma narxda xarid qiling (24 soat ichida narx o'zgarishi mumkin!)\n\n"
    "Birinci 10 ta foydalanuvchiga Sirli SUPPER imkoniyat beriladi🎁?\n"
    "🏆 Har 3 oyda barcha bot orqali kurs olgan o‘quvchilar orasidan 3 ta g‘olib aniqlanib, ular klip yoki rolik suratga olishlari uchun RAPID_SCHOOL tomonidan BEPUL texnika beriladi! (1 kunga) ⚡️"
)

COURSE_FULL_TEXT = (
    "📖 Online kurs haqida 📖\n\n"
    "💎 Kurs davomiyligi: doimiy yopiq kanalda qolasiz!\n"
    "⭐️ Gold tarif: Rejissura, Operatorlik, Montaj — 24 ta online dars, mentorlarsiz, sertifikatsiz.\n"
    "⭐️ Premium tarif: Zamonaviy Rejissura, Operatorlik, Montaj, Color, Grafika, Musiqa bilan ishlash, Open AI — barcha darsliklar faqat shu tarifda! 34+ ta  darslik va doimiy joylanib boriladigan VEO3, NANOBANANA, KLING AI, RUNWEY, GIMINI, SORA2 AI darslari zamonaviy kasb!\n\n"
    "⏳ Chegirma faqat 24 soat ichida amal qiladi! Asil narxga qaytmasidanoq xozir xarid qiling.\n\n"
    "🎁 Birinchi 10 ta foydalanuvchiga 3 ta BEPUL OFFLINE Rejissura VA OPEN AI Sun'iy Intellekt darsida ishtrok etish imkoni beriladi!\n"
    "🏆 Har 3 oyda barcha bot orqali kurs olgan o‘quvchilar orasidan 3 ta g‘olib aniqlanib, ular klip yoki rolik suratga olishlari uchun BEPUL texnikalar RAPID_SCHOOL tomonidan beriladi!\n"
    "⚡️ Bunday imkoniyatni qo‘ldan boy bermang! Daromadingizni 5x dan 10x gacha oshirish imkoniyati sizni kutmoqda! Bundan tashqari sizni oldinda 1000$ dan 2000$ gacha daromadli ishlar kutadi. Bugungi imkon ertaga bo'lmasligi mumkin.."
)

PAY_TEXT = (
    "💳 To‘lov qilish:\n\n"
    "Gold tarif narxi: 1,099,000 emas Chegirmada 599,999 so‘m\n"
    "Premium tarif narxi: 2,999,000 emas Supper Chegirmada 749,999 so‘m\n"
    "To‘lov uchun: 9860 1266 3231 1679\n\n"
    "To‘lov qilgandan so‘ng, iltimos, screenshotni botga yuboring. Siz avtomatik kanalga qo'shilasiz."
)

RAUF_TEXT = (
    "1️⃣ 2025-yildan boshlab Open AI rasmiy hamkori sifatida ish yuritib kelmoqdalar\n"
    "2️⃣ Shu yilning o'zida Prezident farmoni bilan SHUXRAT medali sohibi bo'ldilar\n"
    "3️⃣ Ummon-Eslab qol, Tolo, Jaxongir Otajonov- Qaddi baland, Ozodbek Nazarbekov - Uyg'on o'glim va shu kabi katta kliplarda ishlaganlar\n"
    "4️⃣ SABER, ANTI DRON, MEGAPLANET, UEFA kabi katta loyihalar bilan hamkorlik qillib kelmoqdalar va 300+ klip va roliklar muallifi hisoblanadilar.\n"
    "5️⃣ Qur'on oyatlarini SORA2 AI  orqali tayyorlab O'zbekistonni dunyoga tanitib kelmoqdalar, Dubeidagi 1mln $lik tanlovda tashkilotchilar taklifi bilan ishtrok etmoqdalar.\n"
  "5️⃣.1️⃣ Bugungi kunda offline rejimda 50 dan ortiq online rejimda 200 dan ortiq shogirtlar yetishtirib chiqardilar va ularning xozirgi kundagi o'rtacha oylik daromadi 500$+ 1000$+\n"
    "6️⃣ Bugungi kunda oyiga 20,000$+ daromad ko‘radilar\n"
    "Zamonaviy rejissura va Open AI online kursi sizni amaliyotga yo‘naltiradi va daromadingizni 10x gacha oshirishga yordam beradi\n"
    "Oyiga 1,000$ dan 2,000$ gacha sof daromadli ishlarda ishlash imkonini beradi."
   "6️⃣.1️⃣ Ustozning maqsadlari o'zlari bilgan bilim va ilmlarini boshqalarga ulashish orqali ko'plab yoshlarni ish bilan ta'minlash qancha ko'p odamga bizni kurs foyda keltirsa biz bundan shuncha ko'p xursad bo'lamiz! Bilimingizni qo'rqmasdan sarmoya kiriting va o'zingiz orzu qilgandanda kattaroq muvofaqqiyatlarga erishing, Rapid_school professionallikga biz bilan qadam tashlang.\n"

)

FAQ_EMPTY = "❓ Hozircha savollar ko'p emas."

CONTACT_TEXT = "📞 Telefon: +998 99 395 55 33\n📧 Telegram: https://t.me/rapidschool"
ADDRESS_TEXT = (
    "📍 Toshkent shahri, Drujba Narodov, Furqat ko‘chasi 15/1-uy\n"
    "🔗 Xaritada ko‘rish: https://yandex.uz/navi/?whatshere%5Bzoom%5D=20&whatshere%5Bpoint%5D=69.243997,41.308532"
)

CERT_TEXT = "Sertifikat olish uchun admin bilan bog'laning: https://t.me/rapidschool"

# ============ HANDLERS ============

# Start — so'rov: telefon raqamni yuborish + welcome photo if exists
@bot.message_handler(commands=["start"])
def start_handler(m):
    try:
        ensure_user(m.chat.id)
        # prepare keyboard (one-time contact request)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn_contact = types.KeyboardButton("📱 Telefon raqamni yuborish", request_contact=True)
        markup.add(btn_contact)

        # If welcome photo is present, send photo + caption (long welcome)
        if os.path.exists(WELCOME_PHOTO):
            try:
                with open(WELCOME_PHOTO, "rb") as ph:
                    bot.send_photo(m.chat.id, ph, caption=WELCOME_CAPTION, reply_markup=markup)
            except Exception as e:
                # fallback to text if photo fails
                bot.send_message(m.chat.id, WELCOME_CAPTION, reply_markup=markup)
        else:
            bot.send_message(m.chat.id, WELCOME_CAPTION, reply_markup=markup)
    except Exception:
        traceback.print_exc()

# Contact handler — when user shares phone
@bot.message_handler(content_types=["contact"])
def contact_handler(m):
    try:
        if not m.contact or not m.contact.phone_number:
            bot.send_message(m.chat.id, "Iltimos, telefon raqamni kontakt tugmasi orqali yuboring.")
            return
        ensure_user(m.chat.id)
        update_user_field(m.chat.id, "phone", m.contact.phone_number)

        # Inform user + send full course info + menu
        bot.send_message(m.chat.id, "✅ Telefon raqam qabul qilindi! Endi kurs tafsilotlari va menyu quyida:")
        bot.send_message(m.chat.id, COURSE_FULL_TEXT)

        # menu with emojis and FAQ
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("📖 Online kurs haqida 📖", "💳 To‘lov qilish")
        markup.row("📞 Aloqa", "📍 Manzil")
        markup.row("👤 Rauf Nabiev haqida", "🎓 Sertifikat olish")
        markup.row("❓ Eng ko'p beriladigan savollar (FAQ)")

        bot.send_message(m.chat.id, "Quyidagi menyudan tanlang:", reply_markup=markup)
    except Exception:
        traceback.print_exc()

# Menu handler
@bot.message_handler(func=lambda m: isinstance(m.text, str) and m.text.strip() in [
    "📖 Online kurs haqida 📖",
    "💳 To‘lov qilish",
    "📞 Aloqa",
    "📍 Manzil",
    "👤 Rauf Nabiev haqida",
    "🎓 Sertifikat olish",
    "❓ Eng ko'p beriladigan savollar (FAQ)"
])
def menu_handler(m):
    try:
        text = m.text.strip()
        if text == "📖 Online kurs haqida 📖":
            bot.send_message(m.chat.id, COURSE_FULL_TEXT)
        elif text == "💳 To‘lov qilish":
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("💳 To‘lov qilganman — screenshot yuboraman", callback_data="paid_send"))
            markup.add(types.InlineKeyboardButton("❌ Bekor qilish", callback_data="paid_cancel"))
            bot.send_message(m.chat.id, PAY_TEXT, reply_markup=markup)
        elif text == "📞 Aloqa":
            bot.send_message(m.chat.id, CONTACT_TEXT)
        elif text == "📍 Manzil":
            bot.send_message(m.chat.id, ADDRESS_TEXT)
        elif text == "👤 Rauf Nabiev haqida":
            bot.send_message(m.chat.id, RAUF_TEXT)
        elif text == "🎓 Sertifikat olish":
            bot.send_message(m.chat.id, CERT_TEXT)
        elif text == "❓ Eng ko'p beriladigan savollar (FAQ)":
            bot.send_message(m.chat.id, FAQ_EMPTY)
    except Exception:
        traceback.print_exc()

# Callback handler for inline buttons
@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("paid_"))
def callback_paid(c):
    try:
        if c.data == "paid_send":
            bot.send_message(c.message.chat.id, "Iltimos, to‘lov qilganingizni ko‘rsatgan screenshotni rasm sifatida yuboring.")
        else:
            bot.send_message(c.message.chat.id, "To‘lov jarayoni bekor qilindi.")
    except Exception:
        traceback.print_exc()

# Photo handler — save screenshot, notify admins, send channel link to user
@bot.message_handler(content_types=["photo"])
def photo_handler(m):
    try:
        ensure_user(m.chat.id)
        users = safe_load_users()
        sid = str(m.chat.id)
        file_info = bot.get_file(m.photo[-1].file_id)
        downloaded = bot.download_file(file_info.file_path)
        filename = f"{sid}_{int(time.time())}.jpg"
        filepath = os.path.join(SCREENSHOTS_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(downloaded)

        # update user record
        update_user_field(m.chat.id, "pending_screenshot", filepath)
        update_user_field(m.chat.id, "payment_made", True)
        update_user_field(m.chat.id, "approved", True)

        # Notify admins with photo + caption (admins must be real user IDs)
        caption = (
            f"🔔 Yangi to‘lov skrinshoti\nFoydalanuvchi: {m.from_user.first_name} (id: {sid})\n"
            f"Tel: {get_user(m.chat.id).get('phone')}\n\n"
            "Eslatma: admin tasdiqlashi shart emas — avtomatik tizim."
        )
        for admin_id in ADMIN_CHAT_IDS:
            try:
                with open(filepath, "rb") as ph:
                    bot.send_photo(admin_id, ph, caption=caption)
            except Exception:
                # if send to admin failed, print error
                print(f"Failed to send screenshot to admin {admin_id}")

        # Send channel/invite link to user (we cannot auto-invite to private link; give the link)
        bot.send_message(m.chat.id, f"🎉 Skrinshot qabul qilindi. Siz avtomatik kanalga qo‘shildingiz (yoki qo‘shilish uchun ssilka):\n{CHANNEL_LINK}")
    except Exception:
        traceback.print_exc()

# Fallback handler to ignore unexpected texts
@bot.message_handler(func=lambda m: True, content_types=["text", "sticker", "video", "document", "audio"])
def fallback_handler(m):
    # If user hasn't shared phone yet, remind them
    user = get_user(m.chat.id)
    if not user.get("phone"):
        try:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn_contact = types.KeyboardButton("📱 Telefon raqamni yuborish", request_contact=True)
            markup.add(btn_contact)
            bot.send_message(m.chat.id, "Iltimos, telefon raqamni yuboring (kontakt tugmasi orqali).", reply_markup=markup)
        except Exception:
            pass
    else:
        # ignore or guide user to menu
        try:
            bot.send_message(m.chat.id, "Kerakli bo‘limni menyudan tanlang. /start bilan qayta boshlash mumkin.")
        except Exception:
            pass

# ============ RUN POLLING WITH RESTART LOOP ============
if __name__ == "__main__":
    print("Bot ishga tushdi... Polling boshlanmoqda.")
    # Keep bot running even if an exception occurs in polling
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print("Polling error:", e)
            traceback.print_exc()
            time.sleep(5)  # wait and restart