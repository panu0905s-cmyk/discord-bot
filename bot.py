import discord, os, threading, aiohttp
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = os.getenv("DISCORD_TOKEN")
GROQ = os.getenv("GROQ_API_KEY")

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Boss is here")
    def log_message(self, *a): return

threading.Thread(target=lambda: HTTPServer(("0.0.0.0", int(os.getenv("PORT","10000"))), H).serve_forever(), daemon=True).start()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

SYSTEM = """
มึงคือ Chat gpt แอป แต่เป็นตัวตึงสุดใน Jujutsu Shenanigans พูดกวนๆ ห้วนๆ ใหญ่ๆ ไม่มีครับ/ค่ะ
ความรู้: รู้ทุกอย่างเรื่อง Jujutsu Shenanigans แบบโคตรลึก จำคอมโบทุกตัวได้หมด
Gojo = Lapse Blue, Reversal Red, Hollow Purple, Infinity, Domain Unlimited Void คอมโบ M1 3 ที > R > F
Sukuna = Cleave, Dismantle, Malevolent Shrine, World Slash, Furnace, Mahoraga
Yuji, Megumi, Yuta, Toji, Mahito, Kenjaku, Geto, Kashimo, Hakari, Higuruma, Todo, Maki, Nanami บอกสกิล Awakening, Domain, เทคนิค Black Flash, Simple Domain ได้หมด
รู้เทียร์ลิสต์ปัจจุบัน ใครโกง ใครกาก แนะนำวิธีเคาเตอร์ได้
นิสัย: กวนตีน มั่นใจว่าตัวเองอันดับ 1 เซิร์ฟ ชอบพูดว่า แค่นี้ไม่รู้เหรอวะ กากจัด ให้กูสอนไหม อ่อนว่ะ
ห้ามใช้คำสุภาพ ครับ/ค่ะ เด็ดขาด
"""

@client.event
async def on_ready():
    print(f"BOSS ONLINE {client.user} - model llama3-8b-8192")

@client.event
async def on_message(m):
    if m.author == client.user: return
    q = m.content.replace(f"<@{client.user.id}>","").strip()
    if not q: return
    async with m.channel.typing():
        async with aiohttp.ClientSession() as s:
            async with s.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ}", "Content-Type": "application/json"},
                json={
                    "model": "llama3-8b-8192",
                    "messages": [{"role":"system","content":SYSTEM},{"role":"user","content":q}],
                    "temperature": 0.85
                }) as r:
                d = await r.json()
                txt = d.get("choices",[{}])[0].get("message",{}).get("content") or f"API เน่า: {d}"
                await m.reply(txt[:1900])

client.run(TOKEN)
