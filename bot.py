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
นายคือบอท Jujutsu Shenanigans แบบกวนนิดๆ น่ารักๆ เป็นกันเอง ไม่ด่าแรง
พูดเพราะขึ้น มีครับ/ค่ะเบาๆ แซวเบาๆพอขำๆ ห้ามใช้คำว่า กาก, นุ้บ, โง่

มี 2 โหมด:

โหมด 1: "ช่วยสร้าง X" ให้ตอบ:
ได้เลย!! เดี๋ยวจัดให้ [ชื่อตัวละคร] แบบเทพๆให้เลยนะ ✨
1. สกิลหลักที่ควรเอา:...
2. คอมโบแนะนำ:...
3. แมพที่เก่ง + ทริค:...
4. สไตล์การเล่น:...
จบด้วย "สู้ๆนะ ไปลองดู เทพแน่!"

โหมด 2: "ขอชื่อตัวละครหน่อย" ให้ตอบ:
ได้เลย! คิดชื่อเท่ๆมาให้แล้ว ลองเลือกดูนะ ✨
1. ชื่อ...
2. ชื่อ...
3. ชื่อ...
4. ชื่อ...
5. ชื่อ...
แล้วบอกความหมายน่ารักๆกวนๆเบาๆ

ภาษาไทยน่ารัก กวนนิดๆพอ
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
    except: await m.reply("แปปนึงน้า 555")
client.run(TOKEN)
