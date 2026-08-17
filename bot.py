import discord, aiohttp, os, urllib.parse, asyncio, threading
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = os.getenv("DISCORD_TOKEN")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"Bot running")
def run_web(): HTTPServer(("0.0.0.0", int(os.environ.get("PORT", 10000))), Handler).serve_forever()
threading.Thread(target=run_web, daemon=True).start()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready(): print(f'✅ {client.user} online - final fix')

@client.event
async def on_message(m):
    if m.author == client.user: return
    if m.content.startswith("!ai") or (client.user in m.mentions):
        q = m.content.replace("!ai","").replace(f"<@{client.user.id}>","").strip()
        if not q: q = "สวัสดี"
        prompt = f"คุณคือบอทกวนๆ ฮาๆ พูดไทยแสลงเพื่อนสนิท ตอบสั้นๆ: {q}"
        url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}?model=openai&private=true"

        async with m.channel.typing():
            try:
                async with aiohttp.ClientSession() as s:
                    async with s.get(url) as r:
                        text = await r.text()
                        if "402" in text or "PAYMENT" in text or len(text) < 2:
                            raise Exception("Pollinations 402")
                        # ตัดส่ง
                        for i in range(0, len(text), 1900):
                            await m.reply(text[i:i+1900])
                            await asyncio.sleep(0.3)
            except Exception as e:
                # ถ้าพัง ให้ลองอีกตัว
                try:
                    url2 = "https://ai.hackclub.com/proxy/openai/v1/chat/completions"
                    payload = {"model":"openai/gpt-4o-mini","messages":[{"role":"user","content":prompt}]}
                    async with aiohttp.ClientSession() as s2:
                        async with s2.post(url2, json=payload) as r2:
                            data = await r2.json()
                            if 'choices' in data:
                                txt = data['choices'][0]['message']['content']
                                await m.reply(txt[:1900])
                            else:
                                await m.reply(f"ติดบั๊กแปป: {str(data)[:500]}")
                except Exception as e2:
                    await m.reply(f"เอ๋อ: {e} | {e2}")

client.run(TOKEN)
