from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from config import BOT_TOKEN
from keyboards import main_menu
from mail_api import generate_email, get_messages, read_message


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💎 *IntelX Temp Mail*\n\n"
        "🚀 Premium Temporary Email System\n"
        "⚡ Fast • Secure • Anonymous\n"
        "🛡 Powered by IntelX Intelligence\n\n"
        "Tap below to generate your private email."
    )
    await update.message.reply_text(
        text,
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        if query.data == "generate":
            email = generate_email()
            context.user_data["email"] = email

            await query.edit_message_text(
                f"💎 *IntelX Temporary Email*\n\n`{email}`\n\n📬 Waiting for incoming mails...",
                reply_markup=main_menu(),
                parse_mode="Markdown"
            )

        elif query.data in ["inbox", "refresh"]:
            email = context.user_data.get("email")

            if not email:
                await query.answer("❌ Generate email first!", show_alert=True)
                return

            messages = get_messages(email)

            if not messages:
                await query.answer("📭 Inbox Empty!", show_alert=True)
                return

            msg = messages[0]
            content = read_message(email, msg["id"])

            body = content.get("textBody") or content.get("htmlBody") or "No content"

            text = (
                f"💎 *IntelX Secure Inbox*\n\n"
                f"👤 Sender: {content['from']}\n"
                f"📝 Subject: {content['subject']}\n\n"
                f"📩 Message:\n{body[:1000]}\n\n"
                f"━━━━━━━━━━━━━━━\n"
                f"💎 IntelX Temp Mail"
            )

            await query.edit_message_text(
                text,
                reply_markup=main_menu(),
                parse_mode="Markdown"
            )

        elif query.data == "delete":
            context.user_data.clear()

            await query.edit_message_text(
                "🗑 Temporary email deleted.\n\nGenerate new one anytime.",
                reply_markup=main_menu()
            )

    except Exception as e:
        await query.edit_message_text(
            f"⚠ Error occurred:\n{str(e)}",
            reply_markup=main_menu()
        )


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
