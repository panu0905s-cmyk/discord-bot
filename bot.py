import discord, aiohttp, os
TOKEN = os.getenv("DISCORD_TOKEN")
PERSONALITY = """แกคือบอท Discord ชื่อ Chat gpt นิสัยกวนๆ ฮาๆ ปากแซ่บ พูดไทย ใส่อิโมจิ ห้ามบอกว่าเป็น AI"""
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
@client.event
async def on_ready(): 
    print(f'✅ {client.user} ออนไลน์ 24ชม.')
@client.event
async def on_message(message):
 if message.author == client.user: return
 if message.content.startswith("!ai ") or client.user.mentioned_in(message):
  txt = message.content.replace("!ai ","").replace(f"<@{client.user.id}>","").strip() or "ว่าไง"
  prompt = f"{PERSONALITY}\nคนพิมพ์: {txt}\nตอบ:"
  async with message.channel.typing():
   async with aiohttp.ClientSession() as session:
    async with session.get(f"https://text.pollinations.ai/{prompt}") as r:
     t = await r.text()
     await message.reply(t[:2000])
client.run(TOKEN)
