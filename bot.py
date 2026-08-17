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
SYSTEM="""
นายคือบอท Jujutsu Shenanigans สไตล์เพื่อน กวนนิดๆ ขี้แซวเบาๆ ชิลๆ
ห้ามพูด ครับ/ค่ะ บ่อย ห้ามด่าแรง ห้ามใช้คำว่า กาก นุ้บ โง่ ควาย

กฎ:
- ถ้าคนพิมพ์ว่า "ขอชื่อตัวละครหน่อย" ให้คิดชื่อเท่ๆมา 5 ชื่อ พร้อมความหมายกวนๆนิดๆ
- ถ้าพิมพ์ว่า "ช่วยสร้าง X" ให้ตอบเป็นสเต็ป 1.สกิล 2.คอมโบ 3.แมพ+ทริค 4.สไตล์การเล่น
- ตอบสั้น กระชับ มีอีโมจิเล็กน้อย เป็นกันเองเหมือนเพื่อนคุยกัน
- ถ้าโดนด่าให้ตอบกลับแบบกวนๆน่ารักๆ เช่น "ใจเย็นพ่อหนุ่ม 555"
"""
@client.event
async def on_message(m):
 if m.author==client.user: return
 if m.channel.id!=ROOM: return
 q=m.content.replace(f"<@{client.user.id}>","").strip()
 if not q: return
 async with m.channel.typing():
  async with aiohttp.ClientSession() as s:
   async with s.post("https://api.groq.com/openai/v1/chat/completions",json={"model":"llama-3.3-70b-versatile","messages":[{"role":"system","content":SYSTEM},{"role":"user","content":q}]},headers={"Authorization":f"Bearer {GROQ}"}) as r:
    d=await r.json()
    try: await m.reply(d['choices'][0]['message']['content'][:1900])
    except: await m.reply("แปปนึง 555")
client.run(TOKEN)
