import asyncio
import random
from highrise import BaseBot, Position
from flask import Flask
from threading import Thread

# --- إعداد السيرفر لبقاء البوت حياً على Render ---
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Online!", 200
def run_flask(): app.run(host='0.0.0.0', port=10000)

class MyBot(BaseBot):
    def __init__(self):
        super().__init__()
        # ⚠️ ضع اسم المستخدم الخاص بك هنا لكي تعمل أوامر المشرفين
        self.admins = ["ضع_اسمك_هنا"] 
        self.dancing_users = set()

    async def on_start(self, session_metadata):
        print("✅ تم اتصال البوت بنجاح!")

    async def on_chat(self, user, message):
        try:
            msg = message.strip().lower()
            username = user.username.lower()

            # 1. حركة الكف (للجميع) - اكتب: كف @اسم_الشخص
            if msg.startswith("كف"):
                target = msg.replace("كف", "").strip().replace("@", "")
                room_users = await self.highrise.get_room_users()
                for u, pos in room_users.users:
                    if u.username.lower() == target:
                        await self.highrise.walk_to(Position(pos.x + 0.5, pos.y, pos.z))
                        await asyncio.sleep(1.5)
                        await self.highrise.send_emote("emote-slap", u.id)
                        await self.highrise.chat(f"كف سريع لعيون {user.username}! 😂")
                        break

            # 2. رقص مطول (رقصني / قفل)
            elif "رقصني" in msg:
                self.dancing_users.add(user.id)
                await self.highrise.chat("الرقص المستمر بدأ! اكتب 'قفل' للتوقف.")
                while user.id in self.dancing_users:
                    emotes = ["dance-sexy", "emote-dancing", "dance-pinguin", "dance-russian"]
                    await self.highrise.send_emote(random.choice(emotes), user.id)
                    await asyncio.sleep(8)

            elif "قفل" in msg:
                if user.id in self.dancing_users:
                    self.dancing_users.remove(user.id)
                    await self.highrise.chat("تم إيقاف الرقص.")

            # 3. الرقص بالأرقام (اكتب أي رقم من 1 لـ 100)
            elif msg.isdigit():
                await self.highrise.send_emote(f"emote-{msg}", user.id)

            # 4. أوامر المشرفين (جيب الشخص)
            if username in self.admins:
                if msg.startswith("!جيب"):
                    target = msg.replace("!جيب", "").strip().replace("@", "")
                    room_users = await self.highrise.get_room_users()
                    for u, _ in room_users.users:
                        if u.username.lower() == target:
                            await self.highrise.teleport(u.id, Position(10, 0, 10))
                            await self.highrise.chat(f"تم جلب {u.username} بنجاح 🫡")

        except Exception as e: print(f"Error: {e}")

async def main():
    # تم وضع التوكن والأيدي الخاص بك هنا بدقة
    token = "68bbfb4539e2f67536929eef11c76e1576a3de793dde8d1c7ca5565a99dbb8bf"
    room_id = "69fedff4317dc9f358938d91"
    
    Thread(target=run_flask).start()
    while True:
        try:
            bot = MyBot()
            await bot.run(token, room_id)
        except Exception as e:
            print(f"حدث خطأ في الاتصال: {e}")
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
