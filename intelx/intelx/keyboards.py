from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    keyboard = [
        [InlineKeyboardButton("💎 Generate IntelX Mail", callback_data="generate")],
        [
            InlineKeyboardButton("📬 Inbox", callback_data="inbox"),
            InlineKeyboardButton("🔄 Refresh", callback_data="refresh")
        ],
        [InlineKeyboardButton("🗑 Delete Mail", callback_data="delete")]
    ]
    return InlineKeyboardMarkup(keyboard)
