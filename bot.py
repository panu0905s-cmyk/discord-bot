import discord, aiohttp, os, urllib.parse, asyncio

TOKEN = os.getenv("DISCORD_TOKEN")
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
    if m.author == client.user:
        return
    if m.content.startswith("!ai") or (client.user in m.mentions):
        q = m.content.replace("!ai","").replace(f"<@{client.user.id}>","").strip()
        if not q:
            q = "สวัสดี"
        # ใช้แบบไม่ต้องใส่ API Key จะได้ไม่ติด 402
        url = f"https://text.pollinations.ai/{urllib.parse.quote(q)}?model=openai&private=true"
        async with m.channel.typing():
            try:
                async with aiohttp.ClientSession() as s:
                    async with s.get(url) as r:
                        text = await r.text()
                        if "402" in text or "error" in text.lower() and len(text) < 500:
                            await m.reply("Pollinations หมดโควต้าแปป ลองใหม่นะ")
                            return
                        for chunk in split_text(text):
                            await m.reply(chunk)
                            await asyncio.sleep(0.5)
            except Exception as e:
                await m.reply(f"เอ๋อ: {e}")

client.run(TOKEN)
