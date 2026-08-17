import discord, os, threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import aiohttp
TOKEN=os.getenv("DISCORD_TOKEN")
GROQ=os.getenv("GROQ_API_KEY")
ROOM=1538774173667692604
class H(BaseHTTPRequestHandler):
 def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"ok")
def run(): HTTPServer(("0.0.0.0",int(os.getenv("PORT",10000))),H).serve_forever()
threading.Thread(target=run,daemon=True).start()
intents=discord.Intents.default()
intents.message_content=True
client=discord.Client(intents=intents)
@client.event
async def on_message(m):
 if m.author==client.user: return
 if m.channel.id!=ROOM: return
 q=m.content.replace(f"<@{client.user.id}>","").strip()
 if not q: return
 async with m.channel.typing():
  try:
   async with aiohttp.ClientSession() as s:
    async with s.post("https://api.groq.com/openai/v1/chat/completions",json={"model":"llama-3.3-70b-versatile","messages":[{"role":"user","content":f"ตอบกวนๆฮาๆสั้นๆแบบเพื่อนสนิทไทย: {q}"}]},headers={"Authorization":f"Bearer {GROQ}"}) as r:
     d=await r.json()
     await m.reply(d['choices'][0]['message']['content'][:1900])
  except Exception as e:
   await m.reply(f"เอ๋อ {e}")
client.run(TOKEN)
