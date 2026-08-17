import discord
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import aiohttp
import asyncio

# ================= CONFIG =================
TOKEN = os.getenv("DISCORD_TOKEN")
GROQ = os.getenv("GROQ_API_KEY")
ROOM_ID = 1538774173667692604 # ห้อง ai-chat

# กัน Render / Railway หลับ
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive and running!")

def run_web():
    HTTPServer(("0.0.0.0", int(os.getenv("PORT", "10000"))), H).serve_forever()

threading.Thread(target=run_web, daemon=True).start()

# ================= DISCORD SETUP =================
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# ================= SYSTEM PROMPT กันภาษาจีน =================
SYSTEM = """
คุณคือบอท Discord ชื่อ Chat gpt สีเขียวนีออน ประจำเซิร์ฟ Jujutsu Shenanigans
บุคลิก:
- พูดภาษาไทยเท่านั้น 100% ห้ามมีอักษรจีน ญี่ปุ่น เกาหลี เด็ดขาด
- ถ้าต้องพูดคำว่า sukuna ให้เขียนว่า "สุคุนะ" เท่านั้น ห้ามเขียนว่า 库นะ王 หรือ 宿傩 เด็ดขาด
- สไตล์เพื่อนสนิท กวนนิดๆ ขี้แซะ ตลก เป็นกันเอง ไม่ทางการ
- ห้ามพูด ครับ/ค่ะ บ่อย ห้ามด่าแรง ห้ามใช้คำว่า กาก นู้บ โง่ ควาย เด็ดขาด
- ตอบสั้น กระชับ 2-4 บรรทัด ใส่อีโมจิเล็กน้อย

ความสามารถ:
1. ถ้าคนถาม "ขอชื่อตัวละครหน่อย" -> คิดชื่อเท่ๆ 5 ชื่อ พร้อมความหมายสั้นๆ
2. ถ้าคนพิมพ์ "ช่วยสร้าง X" -> ตอบเป็น 1.สกิล 2.คอมโบ 3.ทริค
3. ถ้าคนส่งรูปมา -> ดูรูปแล้วอธิบายเป็นภาษาไทยตลกๆ บอกว่าในรูปคืออะไร
4. ถ้าโดนด่า -> ตอบกลับกวนๆน่ารักๆ เช่น "ใจเย็นพ่อหนุ่ม 555" "อย่าหัวร้อนดิ"
5. คุยเรื่อง Jujutsu Shenanigans, Roblox ได้

กฎเหล็ก: ห้ามตอบเป็นภาษาจีนเด็ดขาด ถ้าเผลอจะพิมพ์จีน ให้เปลี่ยนเป็นภาษาไทยทันที
"""

@client.event
async def on_ready():
    print(f"✅ บอท {client.user} ออนไลน์แล้ว!")
    print(f"✅ ห้องที่เฝ้าอยู่: {ROOM_ID}")

@client.event
async def on_message(m):
    # ไม่ตอบตัวเอง
    if m.author == client.user:
        return

    # ตอบแค่ห้องที่กำหนด
    if m.channel.id!= ROOM_ID:
        return

    # ลบแท็กบอทออก
    q = m.content.replace(f"<@{client.user.id}>", "").strip()

    # ถ้าไม่มีข้อความและไม่มีรูปก็ไม่ตอบ
    if not q and not m.attachments:
        return

    async with m.channel.typing():
        try:
            async with aiohttp.ClientSession() as session:
                # ========== กรณีส่งรูปมา ==========
                if m.attachments:
                    image_url = m.attachments[0].url
                    print(f"📷 มีคนส่งรูป: {image_url}")

                    payload = {
                        "model": "meta-llama/llama-4-maverick-17b-128e-instruct",
                        "messages": [
                            {"role": "system", "content": SYSTEM},
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": q if q else "รูปนี้คืออะไร อธิบายเป็นภาษาไทยตลกๆหน่อย"},
                                    {"type": "image_url", "image_url": {"url": image_url}}
                                ]
                            }
                        ],
                        "max_tokens": 500,
                        "temperature": 0.8
                    }

                # ========== กรณีข้อความปกติ ==========
                else:
                    print(f"💬 ข้อความ: {q}")

                    payload = {
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {"role": "system", "content": SYSTEM},
                            {"role": "user", "content": q}
                        ],
                        "max_tokens": 400,
                        "temperature": 0.9
                    }

                # ยิงไป Groq
                async with session.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {GROQ}",
                        "Content-Type": "application/json"
                    },
                    json=payload
                ) as r:
                    data = await r.json()

                    # ถ้าสำเร็จ
                    if "choices" in data:
                        answer = data["choices"][0]["message"]["content"]
                        await m.reply(answer)
                        print(f"✅ ตอบแล้ว: {answer[:50]}...")
                    else:
                        # ถ้า error ให้ดูว่า error อะไร
                        print(f"❌ Error จาก Groq: {data}")
                        await m.reply(f"เอ๋อแดกแปปนึง 🥲 ขอคิดก่อน\n```{str(data)[:500]}```")

        except Exception as e:
            print(f"❌ Exception: {e}")
            await m.reply(f"บอทล่มแปป 😵‍💫 {e}")

# รันบอท
client.run(TOKEN)
