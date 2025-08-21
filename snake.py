from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random

# -------------------- GLOBAL GAME STATE --------------------
players = []
positions = {}
current_turn = 0
game_started = False
winner_declared = False
MAX_TILE = 100

# Sample snake and ladder positions
snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

# -------------------- COMMAND HANDLERS --------------------

async def startgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global players, positions, current_turn, game_started, winner_declared
    players = []
    positions = {}
    current_turn = 0
    game_started = False
    winner_declared = False
    await update.message.reply_text("🐍🪜 Snake & Ladder ဂိမ်းအသစ် စတင်လိုက်ပါပြီ! /join နဲ့ ဝင်ပါ။")

async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global players, game_started
    user = update.effective_user

    if game_started:
        await update.message.reply_text("ဂိမ်းစပြီးသားဖြစ်ပါတယ်။")
        return

    if user.id not in [p['id'] for p in players]:
        if len(players) < 5:
            players.append({"id": user.id, "name": user.first_name, "spins": 0})
            positions[user.id] = 0
            await update.message.reply_text(f"👤 {user.first_name} ဝင်ပြီးပါပြီ။")
        else:
            await update.message.reply_text("ကစားသူအများဆုံး ၅ ယောက်ထိသာ ဝင်လို့ရပါတယ်။")

    if len(players) >= 2:
        game_started = True
        await update.message.reply_text(f"🎮 ဂိမ်းစမယ်! ပထမဦးဆုံးလှိမ့်မယ့်သူက {players[0]['name']} ပါ။ /spin နဲ့ စလိုက်ပါ။")

async def spin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_turn, players, positions, winner_declared

    if not game_started or winner_declared:
        await update.message.reply_text("ဂိမ်း မစသေးပါ (သို့) ပြီးသွားပါပြီ။")
        return

    user = update.effective_user
    player = players[current_turn]

    if user.id != player['id']:
        await update.message.reply_text("မင်း順番 မဟုတ်သေးပါ။")
        return

    spin_value = random.randint(1, 6)
    player['spins'] += 1
    old_pos = positions[user.id]
    new_pos = old_pos + spin_value

    result_msg = f"🎯 {user.first_name} က spin လှိမ့်လိုက်ပြီ! 👉 {spin_value}\n"

    if new_pos in snakes:
        result_msg += f"😵 မြွေကိုထိမိတယ်! {new_pos} → {snakes[new_pos]}\n"
        new_pos = snakes[new_pos]
    elif new_pos in ladders:
        result_msg += f"🎉 လှေကားတက်တယ်! {new_pos} → {ladders[new_pos]}\n"
        new_pos = ladders[new_pos]

    if new_pos >= MAX_TILE:
        positions[user.id] = MAX_TILE
        winner_declared = True
        result_msg += f"🏁 {user.first_name} ရောက်သွားပြီ! ဂိမ်းအနိုင်ရသူပါ။\n\n📊 Spins Count:\n"
        leaderboard = sorted(players, key=lambda p: p['spins'])
        for idx, p in enumerate(leaderboard, 1):
            result_msg += f"{idx}. {p['name']} – {p['spins']} spins\n"
        await update.message.reply_text(result_msg)
        return

    positions[user.id] = new_pos
    result_msg += f"📍 အခုအနေအထား: {new_pos}"
    await update.message.reply_text(result_msg)

    current_turn = (current_turn + 1) % len(players)
    await update.message.reply_text(f"➡️ နောက်順番: {players[current_turn]['name']} /spin")

def main():
    import os
    TOKEN = os.getenv("8366451382:AAE-0k-uObwUokQ_FXYxnakV38IDKR-rioo")  # Replace with your bot token or use env var

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("startgame", startgame))
    app.add_handler(CommandHandler("join", join))
    app.add_handler(CommandHandler("spin", spin))

    print("Snake & Ladder Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()