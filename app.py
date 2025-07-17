from flask import Flask
import threading
import time
import requests
import telebot
import os

# --- SETUP BOT ---
BOT_TOKEN = "7854510116:AAEpFEs3b_YVNs4jvFH6d1JOZ5Dern69_Sg"
OWNER_ID = 6976365864  # Only you can control the bot

bot = telebot.TeleBot(BOT_TOKEN)

# --- FLASK SERVER FOR RENDER UPTIME ---
app = Flask(__name__)
@app.route('/')
def home():
    return "✅ Telegram Bot is Running"

# --- GLOBAL VARIABLES ---
visit_url = None
visit_interval = 5  # Default 5 seconds
visit_active = False

def visit_loop():
    global visit_url, visit_interval, visit_active
    while True:
        if visit_active and visit_url:
            try:
                res = requests.get(visit_url, headers={'User-Agent': 'Mozilla/5.0'})
                print(f"[{time.strftime('%H:%M:%S')}] ✅ Visited: {visit_url} | Status: {res.status_code}")
            except Exception as e:
                print(f"[{time.strftime('%H:%M:%S')}] ❌ Error: {e}")
        time.sleep(visit_interval)

threading.Thread(target=visit_loop, daemon=True).start()

# --- TELEGRAM COMMANDS ---
@bot.message_handler(commands=['start'])
def handle_start(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ Access Denied.")
        return
    bot.send_message(message.chat.id, "👋 Welcome! Send me the URL you want to visit repeatedly.")
    bot.register_next_step_handler(message, get_url)

def get_url(message):
    global visit_url
    visit_url = message.text
    bot.send_message(message.chat.id, "✅ Got it! Now send how many seconds between each visit (e.g., 3).")
    bot.register_next_step_handler(message, get_interval)

def get_interval(message):
    global visit_interval, visit_active
    try:
        visit_interval = int(message.text)
        visit_active = True
        bot.send_message(message.chat.id, f"🚀 Started visiting {visit_url} every {visit_interval} seconds!")
    except:
        bot.send_message(message.chat.id, "❌ Invalid number. Try again with just digits.")

@bot.message_handler(commands=['stop'])
def stop_visiting(message):
    global visit_active
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ Access Denied.")
        return
    visit_active = False
    bot.reply_to(message, "🛑 Visiting stopped.")

@bot.message_handler(commands=['status'])
def get_status(message):
    status = "✅ ACTIVE" if visit_active else "❌ STOPPED"
    bot.reply_to(message, f"Status: {status}\nURL: {visit_url or 'None'}\nInterval: {visit_interval}s")

# --- START POLLING IN THREAD ---
def start_bot():
    print("🤖 Bot polling started.")
    bot.infinity_polling()

threading.Thread(target=start_bot, daemon=True).start()