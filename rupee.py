import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application, 
    CommandHandler, 
    CallbackQueryHandler, 
    ContextTypes, 
    MessageHandler, 
    filters 
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# IMPORTANT: Replace "YOUR_BOT_TOKEN" with your actual Telegram Bot Token
# Note: The provided token is not a real token, please replace it for actual use.
BOT_TOKEN = "8359469817:AAGqO4Fz8mXZYVt-FHqnvfo2QhXK0TvFm2s" 

# --- Interface Content Functions ---
# (get_user_info_text and get_keyboard remain unchanged)

def get_user_info_text(user_id):
    """
    Generates the main text message with user information and pricing details.
    """
    
    user_tg_id = user_id
    balance = '0' # Default Balance 0₹
    
    return (
        "⚠️ **FREE USER ACCOUNT**\n\n"
        "**User Info**\n"
        f"• ID: `{user_tg_id}`\n"  # Monospace code block
        f"• Balance: **₹{balance}**\n"
        "• Plan: **Not Subscribed**\n"
        "• Status: Upgrade for discounts\n\n"
        "🎁 **Benefits**\n"
        "• At this time, no benefits package is available\n\n"
        "💰 **Current Prices**\n"
        # Price values are bolded
        "• Bank: **₹1.60** • Code: **₹2.60**\n"
        "• IFSC: **₹3.00** • State: **₹4.00**\n\n"
        "💎 **Upgrade to Premium for better prices!**"
    )

def get_keyboard():
    """
    Creates the 4x2 grid of buttons (Inline Keyboard).
    """
    keyboard = [
        [
            InlineKeyboardButton("⬇️ 𝗕𝘂𝘆 𝗗𝗮𝘁𝗮", callback_data='buy_data'),
            InlineKeyboardButton("🎩 𝗣𝗿𝗼 𝗠𝗼𝗱𝗲", callback_data='pro_mode')
        ],
        [
            InlineKeyboardButton("💲 𝗥𝗲𝗰𝗵𝗮𝗿𝗴𝗲", callback_data='recharge'),
            InlineKeyboardButton("💎 𝗦𝘂𝗯𝘀𝗰𝗿𝗶𝗯𝗲", callback_data='subscribe')
        ],
        [
            InlineKeyboardButton("🛒 𝗖𝗖 𝗦𝗵𝗼𝗽", callback_data='cc_shop'),
            InlineKeyboardButton("📊 𝗧𝗿𝗮𝗻𝘀𝗮𝗰𝘁𝗶𝗼𝗻 𝗛𝗶𝘀𝘁𝗼𝗿𝘆", callback_data='transaction_history')
        ],
        [
            InlineKeyboardButton("❓ 𝗙𝗔𝗤", callback_data='faq'),
            InlineKeyboardButton("🆘 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 𝗦𝘂𝗽𝗽𝗼𝗿𝘁", callback_data='contact_support')
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

# --- Command Handlers ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command and displays the main user interface."""
    
    context.user_data['awaiting_code'] = False
    
    if update.message:
        message = update.message
    elif update.callback_query and update.callback_query.message:
        message = update.callback_query.message
    else:
        return

    user_id = message.from_user.id
    text = get_user_info_text(user_id)
    reply_markup = get_keyboard()
    
    if update.message:
        await message.reply_text(
            text, 
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    elif update.callback_query:
        await context.bot.send_message(
            chat_id=message.chat_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

# --- Shortened Warning Message ---

WARNING_MESSAGE = (
    "**🚨 Service Suspension Notice**\n\n"
    "We have been mandated to **temporarily halt all data sales** on this bot "
    "due to an ongoing **legal case** filed against our operations.\n\n"
    "We apologize for the inconvenience.\n\n"
    "**For Data Needs & Support:**\n"
    "• **Support:** **@Babakismatwalesupport**\n"
    "• **Channel:** [Babakismatwale Channel](https://t.me/babakismatwalechannel)\n"
    "• **Group:** [Babakismatwale Group](https://t.me/babakismatwalegroup)\n\n"
    "Thank you for your cooperation."
)

# ----------------- HANDLER FOR COMMANDS (/ifsc) -----------------

async def handle_command_warning(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles commands like /ifsc by sending a new legal warning message.
    """
    
    context.user_data['awaiting_code'] = False

    # Sends a NEW MESSAGE with the warning
    await update.message.reply_text(
        WARNING_MESSAGE, 
        parse_mode='Markdown'
    )


# ----------------- HANDLER FOR ALL BUTTON CLICKS -----------------

async def handle_all_clicks_warning(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles all button clicks by sending a small notification (pop-up) and a NEW message.
    """
    query = update.callback_query
    
    # 1. Send the small pop-up notification (The actual 'small' part)
    await query.answer(
        text="⚠️ Service Suspended. Check the new message for details.",
        show_alert=False 
    ) 

    # 2. Send the NEW, full warning message in the chat
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=WARNING_MESSAGE, 
        parse_mode='Markdown',
        disable_web_page_preview=True
    )

    context.user_data['awaiting_code'] = False
    
# --- Conversation Flow Handlers (handle_text_input remains as a safety net) ---

async def handle_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Processes all plain text input. This handler is now mostly a safety net.
    """
    
    if not context.user_data.get('awaiting_code', False):
        return

    user_input = update.message.text.strip()
    context.user_data['awaiting_code'] = False 

    response_text = (
        "❌ **𝐈𝐍𝐕𝐀𝐋𝐈𝐃 𝐎𝐑 𝐔𝐍𝐄𝐗𝐏𝐄𝐂𝐓𝐄𝐃 𝐈𝐍𝐏𝐔𝐓**\n\n"
        "𝐏𝐥𝐞𝐚𝐬𝐞 𝐮𝐬𝐞 𝐭𝐡𝐞 𝐛𝐮𝐭𝐭𝐨𝐧𝐬 𝐛𝐞𝐥𝐨𝐰 𝐨𝐫 𝐬𝐞𝐧𝐝 **/start**."
    )

    await update.message.reply_text(response_text, parse_mode='Markdown')
    
    await start_command(update, context)


def main() -> None:
    """Sets up the application and handlers, then starts the bot."""
    
    application = Application.builder().token(BOT_TOKEN).build()

    # 1. /start command
    application.add_handler(CommandHandler("start", start_command))
    
    # 2. /ifsc command (Sends a new message)
    application.add_handler(CommandHandler("ifsc", handle_command_warning))

    # 3. ALL button clicks (Sends a pop-up and a new message)
    application.add_handler(CallbackQueryHandler(handle_all_clicks_warning))

    # 4. ALL non-command text messages (Safety net)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_input))

    # Run the bot 
    print("Bot is running... Send /start to your bot on Telegram.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
    