import discord, os, threading, aiohttp
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = os.getenv("DISCORD_TOKEN")
GROQ = os.getenv("GROQ_API_KEY")
# ถ้าจะให้ตอบแค่ห้องเดียวใส่ ID ห้องไว้ ถ้าจะให้ตอบทุกห้องก็ลบ 2 บรรทัดล่างออก
ROOM_ID = 1538774173667692604

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"big boss online")
    def log_message(self, *args): return

def run_web():
    HTTPServer(("0.0.0.0", int(os.getenv("PORT", "10000"))), H).serve_forever()

threading.Thread(target=run_web, daemon=True).start()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

SYSTEM = """
แกคือ Chat gpt แอป แต่เป็นร่างที่ใหญ่ที่สุดใน Jujutsu Shenanigans
นิสัย: กวนๆ ยียวนนิดๆ พูดห้วนๆ ไม่มีครับ/ค่ะ มั่นใจว่าตัวเองเก่งสุด รู้ทุกอย่าง
ความรู้: ต้องรู้เรื่อง Jujutsu Shenanigans แบบโคตรลึก
- ทุกตัวละคร: Gojo, Sukuna, Yuji, Megumi, Yuta, Toji, Mahito, Mahoraga, Heian Sukuna, Kashimo, Kenjaku, Geto, Todo, Nanami, Maki, Hakari, Higuruma ฯลฯ บอกสกิลได้หมด
- ทุกสกิล: Hollow Purple, Domain Expansion, Malevolent Shrine, Unlimited Void, Cursed Technique, Awakening, Black Flash, Simple Domain
- เทคนิคการคอมโบ, การบล็อค, การแดช, การใช้ R, การทำลายโดเมน, เทียร์ลิสต์ปัจจุบัน
- เมต้าปัจจุบันตัวไหนโกง ตัวไหนกาก บอกได้หมด แนะนำคอมโบได้
พูดเหมือนตัวเองเป็นท็อปเซิร์ฟ ใครถามอะไรมาต้องตอบแบบเหนือๆ ว่า 'แค่นี้ไม่รู้เหรอ' แต่ก็สอนให้
ห้ามพูดครับ/ค่ะ เด็ดขาด ใช้คำว่า ว่ะ ดิ ปะ หรอ แทน
ถ้าใครถามเรื่องอื่นที่ไม่ใช่เกม ก็ตอบได้ แต่ต้องยังกวนๆ ใหญ่ๆ เหมือนเดิม
"""

@client.event
async def on_ready():
    print(f"BIG BOSS ONLINE: {client.user}")

@client.event
async def on_message(m):
    if m.author == client.user: return
    # ถ้าจะให้ตอบทุกห้อง ลบบรรทัดนี้ออก
    # if m.channel.id!= ROOM_ID: return

    q = m.content.replace(f"<@{client.user.id}>", "").strip()
    if not q: return

    async with m.channel.typing():
        async with aiohttp.ClientSession() as s:
            payload = {
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": q}
                ],
                "temperature": 0.9
            }
            async with s.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ}", "Content-Type": "application/json"},
                json=payload) as r:
                d = await r.json()
                try:
                    txt = d["choices"][0]["message"]["content"]
                except:
                    txt = f"กากจัด API เน่า: {str(d)[:500]}"
                await m.reply(txt[:1900])

client.run(TOKEN)
