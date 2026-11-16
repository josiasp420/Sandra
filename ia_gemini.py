from google import genai
import dotenv
import os

dotenv.load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

class chatIa:
    def __init__(self,id:int):
        self.id = id
        self.FILE = f"chats/chat_{self.id}.txt"
        self.LIST_PROMPTS:list[(str,str)] = []
        self.history = self.load_history()

    # 🔥 carregar histórico com segurança
    def load_history(self):
        if not os.path.exists(self.FILE):
            return []
        history = []
        with open(self.FILE, "r", encoding="utf-8") as f:
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
        with open(self.FILE, "r", encoding="utf-8") as f:
            data = f.read()
            for td in data.split("__enum_prompt"):
                td = td.strip()
                if not td:
                    continue
                if (td[:5] == "user:"):
                    self.LIST_PROMPTS.append(("user",td))
                elif (td[:6] == "model:"):
                    self.LIST_PROMPTS.append(("model",td))
        return history


    def save_message(self, role, text):
        with open(self.FILE, "a", encoding="utf-8") as f:
            f.write(f"{role}: {text}\n")
            f.write("__enum_prompt\n")


    def chat(self, prompt):
        cc=10
        self.history.append({
        "role": "user",
        "parts": [{"text": prompt}]
        })

        while (cc):
            try:
                response = client.models.generate_content(
                    model="models/gemini-3.1-flash-lite",
                    contents=self.history
                )
                print("foi")
                break
            except Exception as e:
                print("Fail ,try again",cc)
                cc -= 1
                if (cc == 0):
                    print("Falhou infelizmente")
                    return (None)
                    self.history.pop(-1)


        answer = response.text
        self.history.append({
            "role": "model",
            "parts": [{"text": answer}]
        })
        self.save_message("user", prompt)
        self.save_message("model", answer)
        return answer

    def getListPrompts(self):
        return self.LIST_PROMPTS
