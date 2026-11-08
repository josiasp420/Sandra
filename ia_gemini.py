from google import genai
import dotenv
import os

dotenv.load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
FILE = "chat.txt"

# 🔥 carregar histórico com segurança
def load_history():
    if not os.path.exists(FILE):
        return []
    history = []
    with open(FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue
            role, text = line.split(":", 1)
            role = role.strip()
            text = text.strip()
            # 🔒 garantir roles válidas
            if role not in ["user", "model"]:
                continue
            history.append({
                "role": role,
                "parts": [{"text": text}]
            })
    return history


def save_message(role, text):
    with open(FILE, "a", encoding="utf-8") as f:
        f.write(f"{role}: {text}\n")


def chat(prompt):
    global history
    # user
    cc=10
    while (cc):
        try:
            response = client.models.generate_content(
                model="models/gemini-3.1-flash-lite",
                contents=history
            )
            print("foi")
            break
        except Exception as e:
            print("Fail ,try again",cc)
            cc -= 1
            if (cc == 0):
                print("Falhou infelizmente")
                return (None)


    history.append({
        "role": "user",
        "parts": [{"text": prompt}]
    })
    
    answer = response.text
    # model
    history.append({
        "role": "model",
        "parts": [{"text": answer}]
    })
    save_message("user", prompt)
    save_message("model", answer)
    return answer


history = load_history()
for tdi in history:
    print(tdi,'\n\n\n\n')
#for td in range(0,2):
#     msg = input("Você: ")
#     print("IA:", chat(msg))


