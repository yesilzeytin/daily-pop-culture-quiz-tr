import os
import json
import google.generativeai as genai
from datetime import datetime, timezone
import random

# --- Initialize Gemini client ---
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# --- Load exclusion list (past_questions.json) ---
exclusions = []
past_file = "past_questions.json"

if os.path.exists(past_file):
    try:
        with open(past_file, "r", encoding="utf-8") as f:
            exclusions = json.load(f)
            if not isinstance(exclusions, list):
                print("⚠️ past_questions.json was invalid, resetting.")
                exclusions = []
    except Exception as e:
        print(f"⚠️ Could not load past_questions.json: {e}")
        exclusions = []
else:
    # Create empty file for first run
    with open(past_file, "w", encoding="utf-8") as f:
        json.dump([], f)

# --- Themes ---
themes = [
    # 🎬 Film & TV
    "Türk dizileri",
    "Netflix Türkiye yapımları",
    "Türk komedi filmleri",
    "Yeşilçam klasikleri",
    "Cem Yılmaz filmleri",
    "Recep İvedik ve popüler Türk komedileri",
    "Global gişe rekortmeni filmler (Marvel, DC, Avatar, vb.)",
    "Oscar ödüllü filmler",
    "Disney animasyonları",
    "Animasyon filmler",
    "Pixar filmleri",
    "Netflix global dizileri (Stranger Things, Squid Game, vb.)",
    "HBO dizileri (Game of Thrones, The Last of Us, vb.)",
    "Anime serileri (Naruto, One Piece, Attack on Titan, vb.)",
    "Kore dizileri (K-drama popüler yapımlar)",
    "Global diziler",

    # 🎵 Müzik
    "Türk pop müziği (Tarkan, Sezen Aksu, Kenan Doğulu, vb.)",
    "Arabesk müzik (Orhan Gencebay, Müslüm Gürses, vb.)",
    "Rap müzik Türkiye (Ceza, Sagopa, Ezhel, vb.)",
    "Rock müzik Türkiye (Duman, maNga, Mor ve Ötesi)",
    "Eurovision’da Türkiye (Sertab Erener, maNga, vb.)",
    "Global pop müzik (Taylor Swift, Billie Eilish, vb.)",
    "K-Pop (BTS, Blackpink, vb.)",
    "Global rap (Drake, Eminem, Kanye West, vb.)",
    "Latin müzik (Shakira, Maluma, Bad Bunny, vb.)",
    "80’ler ve 90’lar Türk müziği",
    "80’ler ve 90’lar global müzik",

    # ⚽ Spor
    "Türk futbolu (Süper Lig, Galatasaray, Fenerbahçe, Beşiktaş, Trabzonspor, vb.)",
    "Türkiye millî futbol takımı",
    "Türk basketbolu (Anadolu Efes, Fenerbahçe Beko, vb.)",
    "NBA basketbolu (Michael Jordan, LeBron James, vb.)",
    "Şampiyonlar Ligi tarihi",
    "Dünya Kupası tarihi",
    "Formula 1 (Schumacher, Hamilton, Verstappen, vb.)",
    "Tenis (Nadal, Federer, Djokovic, Serena Williams, vb.)",
    "Olimpiyat oyunları (Türk sporcular, global başarılar)",
    "Voleybol (Türk Kadın Voleybol Milli Takımı – Filenin Sultanları)",
    "Global spor tarihi",
    "Türk spor tarihi",

    # 🎮 Oyun & Dijital Kültür
    "PC Oyunları",
    "The Witcher (oyun ve dizi)",
    "Nintendo oyunları (Mario, Zelda, Pokémon)",
    "PlayStation efsane oyunları (God of War, Uncharted)",
    "Twitch fenomenleri",
    "YouTube Türkiye (Enes Batur, Orkun Işıtmak, vb.)",
    "Global YouTubers (MrBeast, PewDiePie vb.)",
    "Instagram fenomenleri",

    # 🌍 Genel Popüler Kültür & Ünlüler
    "Türk ünlüleri (oyuncular, şarkıcılar, sosyal medya fenomenleri)",
    "Survivor Türkiye yarışmacıları",
    "MasterChef Türkiye yarışmacıları",
    "Global ünlüler (Hollywood starları, şarkıcılar)",
    "Kraliyet ailesi (Britanya vb.)",
    "Moda ikonları",
    "Met Gala & Oscar kırmızı halısı",
    "Influencer’lar (Türkiye + global)",
    "Nobel edebiyat ödülleri (Orhan Pamuk vb.)",
    "Harry Potter evreni",
    "Yüzüklerin Efendisi evreni",
    "Star Wars evreni",
    "Marvel Sinematik Evreni",
    "DC Comics filmleri",
    "Bilindik Türk tarihi olayları",
    "Bilindik global tarihi olaylar",
    "Birinci Dünya Savaşı",
    "İkinci Dünya Savaşı",
    "Soğuk Savaş",
    "Tarihteki büyük dolandırıcılar",
    "Nobel kazananları",
    "Altın Kelebek ödülleri",
    "Türk magazin tarihi",

    # 📱 Teknoloji & Trendler
    "Tüketici elektroniği",
    "Esports turnuvaları (LoL Worlds, CS:GO Majors)",
    "İnternet tarihi",
    "İnternet mizah tarihi",

    # 🎉 Eğlenceli & Nostalji
    "Cartoon Network çizgi filmleri",
    "Nickelodeon çizgi filmleri",
    "Disney Channel çizgi filmleri",
    "Fox Kids çizgi filmleri",
    "Yumurcak TV çizgi filmleri",
    "Çocukluğumuzun atıştırmalıkları (Cino, Tipitip vb.)",
    "Popüler internet meme kültürü (Türkiye + global)",
    "Caps kültürü Türkiye",
    "Vine ve TikTok fenomenleri",
    "Twitter Türkiye akımları"
]

chosen_themes = random.sample(themes, 5)
print(chosen_themes)

# --- Build prompt ---
prompt = f"""
Generate 5 multiple-choice trivia questions in Turkish about pop culture.
Focus ONLY on these themes today: {', '.join(chosen_themes)}.
- Questions can include Turkish and global pop culture.
- Avoid American-only or similar topics (NFL, MLB, vb.).
- Each question should have exactly 5 answer choices.
- Provide the correct answer clearly marked.
- Make sure questions vary in difficulty but not too hard (easy to slightly hard).
- Correct answer can be any option between the 5 options provided.
- Write all content in Turkish.
- Do NOT repeat or closely paraphrase any of these previous questions:
{json.dumps(exclusions, indent=2)}

Format the output strictly as JSON in this structure:

{{
  "questions": [
    {{
      "question": "Diriliş Ertuğrul dizisinde Ertuğrul Bey’i hangi oyuncu canlandırmıştır?",
      "options": [
        "Engin Altan Düzyatan",
        "Burak Özçivit",
        "Kıvanç Tatlıtuğ",
        "Kenan İmirzalıoğlu",
        "Çağatay Ulusoy"
      ],
      "correct": 0
    }}
  ]
}}
"""

# --- Call Gemini ---
response = genai.GenerativeModel("gemini-3.8-flash").generate_content(prompt)
content = response.text.strip()

# --- Clean Markdown fences if model wrapped in ```json ... ``` ---
if content.startswith("```"):
    first_newline = content.find("\n")
    if first_newline != -1:
        content = content[first_newline:].strip()
    else:
        content = content[3:].strip()
if content.endswith("```"):
    content = content[:-3].strip()

# --- Parse JSON ---
try:
    data = json.loads(content)
except json.JSONDecodeError as e:
    print("\n--- MODEL OUTPUT ---")
    print(content)
    print("--------------------\n")
    raise ValueError(f"Gemini returned invalid JSON. Error: {e}") from e

# --- Save new questions ---
with open("questions.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ Saved new questions.json at", datetime.now(timezone.utc).isoformat())

# --- Update past_questions.json (FIFO, max 50) ---
new_questions = [q["question"] for q in data.get("questions", [])]
exclusions.extend(new_questions)

# Keep only last 50 (drop oldest first)
if len(exclusions) > 50:
    exclusions = exclusions[-50:]

with open(past_file, "w", encoding="utf-8") as f:
    json.dump(exclusions, f, indent=2, ensure_ascii=False)

print(f"📦 past_questions.json updated (total stored: {len(exclusions)})")
