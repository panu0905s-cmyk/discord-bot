import discord, aiohttp, os, urllib.parse, asyncio, threading
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = os.getenv("DISCORD_TOKEN")

# หลอก Render ให้เจอพอร์ต (จะได้ใช้ฟรีต่อได้)
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_web():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()

threading.Thread(target=run_web, daemon=True).start()

# บอท Discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def split_text(text, limit=1900):
    return [text[i:i+limit] for i in range(0, len(text), limit)]

@client.event
async def on_ready():
    print(f'✅ {client.user} online')

@client.event
async def on_message(m):
    if m.author == client.user: return
    if m.content.startswith("!ai") or (client.user in m.mentions):
        q = m.content.replace("!ai","").replace(f"<@{client.user.id}>","").strip()
        if not q: q = "สวัสดี"
        # นิสัยกวนๆ
        personality = "คุณคือบอทนิสัยกวนตีน กวนๆ ฮาๆ พูดไทยแสลงเพื่อนสนิท "
        full_q = f"{personality} คำถาม: {q}"
        url = f"https://text.pollinations.ai/{urllib.parse.quote(full_q)}?model=openai"
        async with m.channel.typing():
            try:
                async with aiohttp.ClientSession() as s:
                    async with s.get(url) as r:
                        text = await r.text()
                        for chunk in split_text(text):
                            await m.reply(chunk)
                            await asyncio.sleep(0.5)
            except Exception as e:
                await m.reply(f"เอ๋อ: {e}")

client.run(TOKEN)
