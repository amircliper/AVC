from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import datetime
from persiantools.jdatetime import JalaliDateTime

# توکن ربات خود را اینجا قرار دهید
TOKEN = "6896025574:AAEv0BTAK5tHcxOwdRQwF6q-jHzFV-okdcg"

# فایل‌های ذخیره سازی تاریخ‌ها
file_one = "file_one.txt"
file_two = "file_two.txt"
file_three = "file_three.txt"
file_four = "file_four.txt"
file_five = "file_five.txt"

# تعریف دکمه‌ها
keyboard = [
    [KeyboardButton("💦ثبت زمان💦"), KeyboardButton("❤ثبت زمان❤"), KeyboardButton("😈ثبت زمان😈"),KeyboardButton("🧂ثبت زمان🧂"),KeyboardButton("💜ثبت زمان💜")],
    [KeyboardButton("💦اعلام زمان💦"), KeyboardButton("❤اعلام زمان❤"), KeyboardButton("😈اعلام زمان😈"),KeyboardButton("🧂اعلام زمان🧂"),KeyboardButton("💜ثبت زمان💜")]
]

# ایجاد شیش تا دکمه برای هر کاربر
reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("به ربات زمان‌نگار خوش آمدید!", reply_markup=reply_markup)

def add_time(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    time_now = JalaliDateTime.now().strftime("%Y-%m-%d %H:%M:%S")

    # انتخاب فایل بر اساس شناسه دکمه
    user_file = get_user_file(update.message.text)

    # ثبت زمان در فایل
    with open(user_file, "a") as file:
        file.write(time_now + "\n")

    update.message.reply_text(f"زمان \n{time_now}\n اضافه شد!", reply_markup=reply_markup)

def show_last_time(update: Update, context: CallbackContext) -> None:
    # انتخاب فایل بر اساس شناسه دکمه
    user_file = get_user_file(update.message.text)

    # محاسبه گذشته‌شده از آخرین زمان ثبت شده
    passed_time = calculate_passed_time(user_file)
    if passed_time:
        update.message.reply_text(f"گذشته‌شده از آخرین زمان ثبت شده: \n{passed_time}", reply_markup=reply_markup)
    else:
        update.message.reply_text(f"هیچ زمانی در فایل {user_file} ثبت نشده است!", reply_markup=reply_markup)

def get_user_file(button_text: str) -> str:
    # بر اساس متن دکمه، یکی از سه فایل انتخاب می‌شود
    return {
        '💦ثبت زمان💦': file_one,
        '❤ثبت زمان❤': file_two,
        '😈ثبت زمان😈': file_three,
        '🧂ثبت زمان🧂': file_four,
        '💜ثبت زمان💜': file_five,
        '💦اعلام زمان💦': file_one,
        '❤اعلام زمان❤': file_two,
        '🧂اعلام زمان🧂': file_four,
        '💜ثبت زمان💜': file_five,
    }[button_text]

def calculate_passed_time(file_path: str) -> str:
    try:
        # خواندن آخرین خط از فایل
        with open(file_path, "r") as file:
            lines = file.readlines()
            if lines:
                last_time_str = lines[-1].strip()
                last_time = JalaliDateTime.strptime(last_time_str, "%Y-%m-%d %H:%M:%S")
                now = JalaliDateTime.now()
                delta = now - last_time
                return str(delta)
    except FileNotFoundError:
        pass
    return ""

def main() -> None:
    # تنظیمات ربات
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # اضافه کردن دستورات به ربات
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.regex('💦ثبت زمان💦|❤ثبت زمان❤|😈ثبت زمان😈|🧂ثبت زمان🧂|💜ثبت زمان💜'), add_time))
    dp.add_handler(MessageHandler(Filters.regex('💦اعلام زمان💦|❤اعلام زمان❤|😈اعلام زمان😈|🧂اعلام زمان🧂|💜ثبت زمان💜'), show_last_time))

    # شروع ربات
    updater.start_polling()

    # اجرای ربات تا زمانی
    updater.idle()

if __name__ == '__main__':
    main()
