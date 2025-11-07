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
BOT_TOKEN = "8359469817:AAF0LSxIRke1b9d8E6DoFw0I5IG5apaldns"

# --- Interface Content Functions ---

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
        "• 20% Bonus on recharge\n\n"
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
    
    # Reset the redeem code state when the main menu is shown
    context.user_data['awaiting_code'] = False
    
    # Determine the message source (from message or callback query)
    if update.message:
        message = update.message
    elif update.callback_query and update.callback_query.message:
        message = update.callback_query.message
    else:
        return

    user_id = message.from_user.id
    
    text = get_user_info_text(user_id)
    reply_markup = get_keyboard()
    
    await message.reply_text(
        text, 
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# --- Conversation Flow Handlers ---

async def initiate_redeem_flow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles any button click OR the /ifsc command, starting the Redeem Code prompt.
    """
    
    # Determine the message source
    if update.callback_query:
        # If it came from a button click, answer the query and edit the message
        query = update.callback_query
        await query.answer() 
        
        # Edit the message to inform the user
        await query.edit_message_text(
            "𝐘𝐨𝐮 𝐢𝐧𝐢𝐭𝐢𝐚𝐭𝐞𝐝 𝐚 𝐬𝐞𝐫𝐯𝐢𝐜𝐞 𝐫𝐞𝐪𝐮𝐢𝐫𝐢𝐧𝐠 𝐚 𝐫𝐞𝐝𝐞𝐞𝐦 𝐜𝐨𝐝𝐞.", 
            parse_mode='Markdown'
        )
        chat_id = query.message.chat_id
    elif update.message:
        # If it came from the /ifsc command
        await update.message.reply_text(
            "𝐘𝐨𝐮 𝐢𝐧𝐢𝐭𝐢𝐚𝐭𝐞𝐝 𝐭𝐡𝐞 **/ifsc** 𝐬𝐞𝐫𝐯𝐢𝐜𝐞 𝐫𝐞𝐪𝐮𝐢𝐫𝐢𝐧𝐠 𝐚 𝐫𝐞𝐝𝐞𝐞𝐦 𝐜𝐨𝐝𝐞.",
            parse_mode='Markdown'
        )
        chat_id = update.message.chat_id
    else:
        return
    
    # 2. Set the state flag in user_data
    context.user_data['awaiting_code'] = True
    
    # 3. Send the prompt for the redeem code (in special Unicode font)
    prompt_text = (
        "🔑 **𝐑𝐄𝐃𝐄𝐄𝐌 𝐂𝐎𝐃𝐄 𝐑𝐄𝐐𝐔𝐈𝐑𝐄𝐃**\n\n"
        "𝐏𝐥𝐞𝐚𝐬𝐞 𝐬𝐞𝐧𝐝 𝐲𝐨𝐮𝐫 𝐫𝐞𝐝𝐞𝐞𝐦 𝐜𝐨𝐝𝐞 𝐧𝐨𝐰.\n\n"
        "𝐈𝐟 𝐲𝐨𝐮 𝐝𝐨𝐧'𝐭 𝐡𝐚𝐯𝐞 𝐚 𝐫𝐞𝐝𝐞𝐞𝐦 𝐜𝐨𝐝𝐞, 𝐲𝐨𝐮 𝐜𝐚𝐧 𝐜𝐨𝐧𝐭𝐚𝐜𝐭 "
        "**@Babakismatwalesupport** 𝐭𝐨 𝐛𝐮𝐲 𝐨𝐧𝐞."
    )
    
    await context.bot.send_message(
        chat_id=chat_id,
        text=prompt_text,
        parse_mode='Markdown'
    )


async def handle_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Processes all plain text input, validates the redeem code, and responds.
    """
    
    # Check if the bot is currently awaiting a redeem code
    if not context.user_data.get('awaiting_code', False):
        return

    user_input = update.message.text.strip()
    
    # Reset the state immediately after receiving the input
    context.user_data['awaiting_code'] = False 

    # --- Redeem Code Logic ---
    # NOTE: Replace this placeholder with your actual validation logic.
    VALID_CODE = "SUCCESSCODE123" 
    
    if user_input.upper() == VALID_CODE:
        response_text = "✅ **𝐂𝐎𝐃𝐄 𝐀𝐂𝐂𝐄𝐏𝐓𝐄𝐃!**\n𝐘𝐨𝐮𝐫 𝐬𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧 𝐡𝐚𝐬 𝐛𝐞𝐞𝐧 𝐬𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐮𝐩𝐝𝐚𝐭𝐞𝐝."
    else:
        # Invalid code response in special English font
        response_text = (
            "❌ **𝐈𝐍𝐕𝐀𝐋𝐈𝐃 𝐑𝐄𝐃𝐄𝐄𝐌 𝐂𝐎𝐃𝐄**\n\n"
            "𝐏𝐥𝐞𝐚𝐬𝐞 𝐜𝐨𝐧𝐭𝐚𝐜𝐭 **@Babakismatwalesupport** 𝐭𝐨 𝐛𝐮𝐲 𝐚 𝐫𝐞𝐝𝐞𝐞𝐦 𝐜𝐨𝐝𝐞."
        )

    await update.message.reply_text(response_text, parse_mode='Markdown')
    
    # Re-display the main menu after the code is handled
    await start_command(update, context)


def main() -> None:
    """Sets up the application and handlers, then starts the bot."""
    
    # Build the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # 1. Handler for the /start command
    application.add_handler(CommandHandler("start", start_command))
    
    # 2. NEW Handler for the /ifsc command (triggers the redeem flow)
    application.add_handler(CommandHandler("ifsc", initiate_redeem_flow))

    # 3. Handler for ALL button clicks (triggers the redeem flow)
    application.add_handler(CallbackQueryHandler(initiate_redeem_flow))

    # 4. Handler for ALL non-command text messages (used to receive the code)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_input))

    # Run the bot 
    print("Bot is running... Send /start to your bot on Telegram.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()



