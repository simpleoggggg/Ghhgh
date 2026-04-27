#Made By @SajagOG | @KindCoders On Telegram. Site Used : Oxaam.com Auto Sign Up & Auto Service Extractor

import requests
import random
import string
import re
import asyncio
import time
import logging
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_user():
    names = ["Rahul", "Priya", "Amit", "Sneha", "Vikram", "Neha"]
    domains = ["gmail.com", "outlook.com", "yahoo.com"]
    name = random.choice(names) + "".join(random.choices(string.ascii_lowercase, k=4))
    email = name.lower() + str(random.randint(100, 999)) + "@" + random.choice(domains)
    phone = "9" + "".join(random.choices(string.digits, k=9))
    password = "Pass@" + "".join(random.choices(string.ascii_letters + string.digits, k=8))
    return {"name": name, "email": email, "phone": phone, "password": password, "country": "India"}

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

def extract_krunshyrole():
    logger.info("=== Oxaam Free Services Credential Extractor (Bot Mode) ===")
    
    session = requests.Session()
    user = generate_user()

    logger.info(f"Creating Oxaam account...")
    logger.info(f"Email    : {user['email']}")
    logger.info(f"Password : {user['password']}\n")


    signup_data = f"name={user['name']}&email={user['email']}&phone={user['phone']}&password={user['password']}&country={user['country']}"
    session.post("https://www.oxaam.com/", 
                 headers={**headers, "Content-Type": "application/x-www-form-urlencoded", "Referer": "https://www.oxaam.com/"}, 
                 data=signup_data, timeout=15)

    login_data = f"email={user['email']}&password={user['password']}"
    session.post("https://www.oxaam.com/login.php", 
                 headers={**headers, "Content-Type": "application/x-www-form-urlencoded", "Referer": "https://www.oxaam.com/"}, 
                 data=login_data, timeout=15)

    logger.info("Fetching free services page...")
    r = session.get("https://www.oxaam.com/freeservice.php", 
                    headers={**headers, "Referer": "https://www.oxaam.com/dashboard.php"}, timeout=15)

    if r.status_code != 200:
        logger.error(f"❌ Failed (Status: {r.status_code})")
        return None, None, None

    html = r.text
    logger.info("✅ Page loaded. Extracting credentials...")

  
    filename = f"oxaam_freeservices_{int(time.time())}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    logger.info(f"✅ Full page saved as '{filename}'")


    js_match = re.search(r'const CREDENTIALS\s*=\s*(\[.*?\]);', html, re.DOTALL | re.IGNORECASE)
    
    if js_match:
        try:
            creds_json = js_match.group(1)
            
            creds_json = re.sub(r'(\w+):', r'"\1":', creds_json)  
            credentials = json.loads(creds_json)
            
            if credentials and isinstance(credentials, list) and len(credentials) > 0:
                pick = random.choice(credentials)  
                email = pick.get("email", "").strip()
                password = pick.get("password", "").strip()
                
                if email and password:
                    logger.info(f"Server - Krunshyrole Premium")
                    logger.info(f"Email - {email}")
                    logger.info(f"Pass  - {password}")
                    logger.info("-" * 45)
                    return "Krunshyrole Premium", email, password
        except Exception as e:
            logger.warning(f"JS parsing failed: {e}")

    fallback = re.findall(
        r'(Krunshyrole[^<]*?Premium).*?Email[^:➜]*[:➜]\s*([\w\.-]+@[\w\.-]+\.\w+).*?Password[^:➜]*[:➜]\s*([^<"\n]+)',
        html, re.DOTALL | re.IGNORECASE
    )

    for block in fallback:
        if len(block) >= 3:
            service = block[0].replace("&nbsp;", " ").strip().title()
            email = block[1].strip()
            password = block[2].strip()
            logger.info(f"Server - {service}")
            logger.info(f"Email - {email}")
            logger.info(f"Pass  - {password}")
            logger.info("-" * 45)
            return service, email, password

    logger.warning("❌ Could not extract Krunshyrole credentials")
    return None, None, None

async def loading_animation(status_msg):
    stages = [
        "Creating fresh Oxaam account...",
        "Logging into Oxaam...",
        "Fetching free services page...",
        "Extracting Krunshyrole Premium credentials..."
    ]
    dots = ["", ".", "..", "..."]
    i = 0
    start_time = time.time()

    while time.time() - start_time < 20:
        stage = stages[i % len(stages)]
        dot = dots[i % len(dots)]
        try:
            await status_msg.edit_text(
                f"🔄 {stage}{dot}\n\n<i>Please wait • Usually takes 8-18 seconds...</i>",
                parse_mode=ParseMode.HTML
            )
        except:
            pass
        await asyncio.sleep(0.7)
        i += 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔥 Gen Crunchyroll", callback_data="gen_krunshy")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 <b>Crunchyroll Farmer Bot</b>\n\n"
        "Click the button to generate fresh <b>Crunchy Premium</b> credentials.\n\n"
        "<i>Shared accounts may expire quickly.</i>",
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "gen_krunshy":
        status_msg = await query.message.reply_text("🚀 Starting generation...", parse_mode=ParseMode.HTML)

        animation_task = asyncio.create_task(loading_animation(status_msg))

        service, email, password = await asyncio.to_thread(extract_krunshyrole)

        animation_task.cancel()
        try:
            await animation_task
        except asyncio.CancelledError:
            pass

        if email and password:
            result_text = (
                f"✅ <b>Crunchyroll Premium Generated!</b>\n\n"
                f"<b>Service :</b> <b> CrunchiefarmV6.6</b>\n"
                f"<b>Email   :</b> <code>{email}</code>\n"
                f"<b>Password:</b> <code>{password}</code>\n\n"
                f"⚠️ <b>Shared account • Can get logged out anytime.</b>"
            )
        else:
            result_text = (
                "❌ <b>Could not extract Krunshyrole credentials this time.</b>\n\n"
                "The site may have updated. Try again in a few minutes.\n"
                "Check the saved HTML file for details."
            )

        await status_msg.edit_text(result_text, parse_mode=ParseMode.HTML)

def main():
    TOKEN = "8613788119:AAGITarKVaBzKxym5hVP3Ylrd8Dk5xb4v0M"

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Crunchyroll Generator Bot is running...")
    print("Terminal shows full logs. HTML files are saved for debugging.\n")
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()