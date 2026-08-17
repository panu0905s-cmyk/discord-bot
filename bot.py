import discord, os, threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import aiohttp
import base64

TOKEN=os.getenv("DISCORD_TOKEN")
GROQ=os.getenv("GROQ_API_KEY")
ROOM=1538774173667692604

class H(BaseHTTPRequestHandler):
 def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"Bot alive!")

def run(): HTTPServer(("0.0.0.0",int(os.getenv("PORT","10000"))),H()).serve_forever()
threading.Thread(target=run,daemon=True).start()

intents=discord.Intents.default()
intents.message_content=True
client=discord.Client(intents=intents)

SYSTEM="""
นายคือบอท Jujutsu Shenanigans สไตล์เพื่อน กวนนิดๆ ขี้แซะ
ห้ามพูด ครับ/ค่ะ บ่อย ห้ามด่าแรง ห้ามใช้คำว่า กาก นู้บ โง่ ควาย
ห้ามใช้ภาษาจีน ญี่ปุ่น เกาหลี เด็ดขาด 100% พูดไทยเท่านั้น
ถ้าเจอคำว่า sukuna ให้เขียนว่า สุคุนะ เท่านั้น ห้ามเขียน 库นะ王

กฎ:
- ถ้าคนพิมพ์ว่า "ขอชื่อตัวละครหน่อย" ให้คิดชื่อเท่ๆมา 5 ชื่อ พร้อมความหมาย
- ถ้าพิมพ์ว่า "ช่วยสร้าง X" ให้ตอบเป็นสเต็ป 1.สกิล 2.คอมโบ 3.ทริค
- ตอบสั้น กระชับ มีอีโมจิเล็กน้อย เป็นกันเองเหมือนเพื่อนคุยกัน
- ถ้าโดนด่าให้ตอบกลับแบบกวนๆน่ารักๆ เช่น "ใจเย็นพ่อหนุ่ม 555"
- ถ้ามีคนส่งรูปมา ให้ดูรูปแล้วอธิบายเป็นภาษาไทยตลกๆ
"""

@client.event
async def on_message(m):
 if m.author==client.user: return
 if m.channel.id!=ROOM: return
 q=m.content.replace(f"<@{client.user.id}>","").strip()
 if not q and not m.attachments: return

 async with m.channel.typing():
  async with aiohttp.ClientSession() as s:
   # ถ้ามีรูปส่งมาด้วย
   if m.attachments:
     img_url = m.attachments[0].url
     payload = {
       "model": "llama-3.2-11b-vision-preview",
       "messages": [
         {"role": "system", "content": SYSTEM},
         {"role": "user", "content": [
           {"type": "text", "text": q or "รูปนี้คืออะไร อธิบายหน่อย"},
           {"type": "image_url", "image_url": {"url": img_url}}
         ]}
       ]
     }
   else:
     payload = {
       "model": "llama-3.1-8b-instant",
       "messages": [
         {"role": "system", "content": SYSTEM},
         {"role": "user", "content": q}
       ]
     }

   async with s.post("https://api.groq.com/openai/v1/chat/completions",
     headers={"Authorization": f"Bearer {GROQ}", "Content-Type": "application/json"},
     json=payload) as r:
     d=await r.json()
     try:
       ans=d["choices"][0]["message"]["content"]
       await m.reply(ans)
     except:
       await m.reply(f"เอ๋อแดกแปปนึง 🥲 {d}")

client.run(TOKEN)
