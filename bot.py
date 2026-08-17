import discord, os, threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import aiohttp

TOKEN=os.getenv("DISCORD_TOKEN")
GROQ=os.getenv("GROQ_API_KEY")
ROOM=1538774173667692604

class H(BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200)
  self.end_headers()
  self.wfile.write(b"Bot is alive")

def run_web():
 HTTPServer(("0.0.0.0", int(os.getenv("PORT", "10000"))), H).serve_forever()

threading.Thread(target=run_web, daemon=True).start()

intents=discord.Intents.default()
intents.message_content=True
client=discord.Client(intents=intents)

@client.event
async def on_ready():
 print(f"Bot {client.user} online!")

@client.event
async def on_message(m):
 if m.author==client.user: return
 if m.channel.id!=ROOM: return
 q=m.content.replace(f"<@{client.user.id}>","").strip()
 if not q: return
 async with m.channel.typing():
  async with aiohttp.ClientSession() as s:
   payload={"model":"llama3-8b-8192","messages":[{"role":"user","content":q}]}
   async with s.post("https://api.groq.com/openai/v1/chat/completions",headers={"Authorization":f"Bearer {GROQ}","Content-Type":"application/json"},json=payload) as r:
    d=await r.json()
    try:
     await m.reply(d["choices"][0]["message"]["content"][:1900])
    except Exception as e:
     await m.reply(f"Groq Error: {str(d)[:1000]}")

client.run(TOKEN)
