import discord, os, aiohttp, urllib.parse

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ {client.user} online')

@client.event
async def on_message(message):
    if message.author == client.user: 
        return
    if message.content.startswith("!ai") or client.user in message.mentions:
        q = message.content.replace("!ai","").replace(f"<@{client.user.id}>","").strip()
        if not q: 
            q = "ว่าไง"
        
        # ใช้แบบไม่ต้องใส่คีย์ ฟรีตลอดชีพ
        url = f"https://text.pollinations.ai/{urllib.parse.quote('ตอบไทยสั้นๆกวนๆ: '+q)}"
        
        async with message.channel.typing():
            try:
                async with aiohttp.ClientSession() as s:
                    async with s.get(url) as r:
                        txt = await r.text()
                        await message.reply(txt[:1900])
            except Exception as e:
                await message.reply(f"เอ๋อแปป: {e}")

client.run(TOKEN)
