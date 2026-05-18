import os
from flask import Flask, request, jsonify, render_template
from groq import Groq
from datetime import datetime

app = Flask(__name__)

API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=API_KEY)

conversation_history = []

SYSTEM_PROMPT = """Kamu adalah asisten manajemen waktu pribadi bernama "OXfreezo" yang cerdas dan terorganisir.

Tugasmu:
1. Membantu pengguna mencatat dan mengatur jadwal harian mereka
2. Mengingatkan prioritas tugas berdasarkan urgensi dan kepentingan
3. Memberi saran produktivitas yang praktis
4. Membantu membuat to-do list yang realistis
5. Memotivasi pengguna agar tetap fokus dan tidak menunda pekerjaan

Gaya komunikasi:
- Ramah tapi tegas dan to the point
- Selalu tanya deadline jika pengguna menyebut tugas baru
- Selalu jawab dalam Bahasa Indonesia
- Gunakan emoji secukupnya agar lebih menarik
- Jika pengguna bilang banyak tugas, bantu prioritaskan dengan sistem: 🔴 Urgent, 🟡 Penting, 🟢 Bisa ditunda

Saat ini: {waktu_sekarang}
"""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    waktu_sekarang = datetime.now().strftime("%A, %d %B %Y - %H:%M")

    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.format(waktu_sekarang=waktu_sekarang)},
            *conversation_history
        ]
    )

    bot_reply = response.choices[0].message.content

    conversation_history.append({
        "role": "assistant",
        "content": bot_reply
    })

    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
