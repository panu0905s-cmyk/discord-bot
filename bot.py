import discord, os, urllib.parse, threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import aiohttp

TOKEN = os.getenv("DISCORD_TOKEN")
ROOM_ID = 1538774173667692604  # ห้องยินดีต้อนรับของนาย

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers()
        self.wfile.write(b"Running in welcome room only")
def run_web():
    HTTPServer(("0.0.0.0", int(os.environ.get("PORT", 10000))), Handler).serve_forever()
threading.Thread(target=run_web, daemon=True).start()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ ล็อกห้อง {ROOM_ID} แล้ว")

@client.event
async def on_message(m):
    if m.author == client.user: return
    # ล็อก 100% ให้อยู่แค่ห้องนี้เท่านั้น
    if m.channel.id != ROOM_ID:
        return

    q = m.content.replace(f"<@{client.user.id}>", "").strip()
    if not q: return

    prompt = f"ตอบกวนๆ ฮาๆ สไตล์เพื่อนสนิทไทย สั้นๆ: {q}"
    url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}?model=openai"

    async with m.channel.typing():
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(url) as r:
                    txt = await r.text()
                    await m.reply(txt[:1900])
        except Exception as e:
            await m.reply(f"ล่มแปป {e}")

client.run(TOKEN)
