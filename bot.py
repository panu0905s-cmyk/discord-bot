import discord
import aiohttp
import os
from urllib.parse import quote

TOKEN = os.getenv("DISCORD_TOKEN")
PERSONALITY = "แกคือบอท Discord ชื่อ Chat gpt ตอบกวนๆ เป็นกันเอง ภาษาไทย"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ {client.user} ออนไลน์')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("!ai") or client.user in message.mentions:
        txt = message.content.replace("!ai","").replace(f"<@{client.user.id}>","").strip()
        if not txt:
            txt = "ว่าไง"
        prompt = f"{PERSONALITY}\nคนพิมพ์: {txt}\nตอบ:"
        async with message.channel.typing():
            try:
                safe = quote(prompt)
                url = f"https://text.pollinations.ai/{safe}"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as r:
                        t = await r.text()
                await message.reply(t[:1900])
            except Exception as e:
                await message.reply(f"Error: {e}")

client.run(TOKEN)
