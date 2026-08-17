import discord, aiohttp, os, asyncio, threading
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = os.getenv("DISCORD_TOKEN")

# หลอก Render ให้ฟรีได้
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers()
        self.wfile.write(b"Bot is running")
def run_web():
    HTTPServer(("0.0.0.0", int(os.environ.get("PORT", 10000))), Handler).serve_forever()
threading.Thread(target=run_web, daemon=True).start()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ {client.user} online - 402 fixed')

@client.event
async def on_message(m):
    if m.author == client.user: return
    if m.content.startswith("!ai") or (client.user in m.mentions):
        q = m.content.replace("!ai","").replace(f"<@{client.user.id}>","").strip()
        if not q: q = "ทักมา"

        # ใช้ Hack Club ฟรี ไม่ต้องมี Key ไม่ติด 402
        url = "https://ai.hackclub.com/proxy/openai/v1/chat/completions"
        payload = {
            "model": "openai/gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "คุณคือบอทนิสัยกวนตีน ฮาๆ กวนๆ พูดไทยสไตล์เพื่อนสนิท ตอบสั้นๆ แสบๆ"},
                {"role": "user", "content": q}
            ]
        }
        async with m.channel.typing():
            try:
                async with aiohttp.ClientSession() as s:
                    async with s.post(url, json=payload) as r:
                        data = await r.json()
                        text = data['choices'][0]['message']['content']
                        # ตัดข้อความยาว
                        for i in range(0, len(text), 1900):
                            await m.reply(text[i:i+1900])
                            await asyncio.sleep(0.3)
            except Exception as e:
                await m.reply(f"เอ๋อแปป: {e}")

client.run(TOKEN)
