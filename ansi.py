import re
import webbrowser
import eel
import requests
from webscout import KOBOLDAI, BLACKBOXAI, ThinkAnyAI, PhindSearch, DeepInfra, Julius, DARKAI, RUBIKSAI, LiaoBots, WEBS as w
from tkinter import messagebox
from packaging import version


CURRENT_VERSION = "1.3"

prompt = """###INSTRUCTIONS###

You MUST follow the instructions for answering:

ALWAYS answer in the language of my message.

Read the entire convo history line by line before answering.

I have no fingers and the placeholders trauma. Return the entire code template for an answer when needed. NEVER use placeholders.

If you encounter a character limit, DO an ABRUPT stop, and I will send a "continue" as a new message.

You ALWAYS will be PENALIZED for wrong and low-effort answers.

ALWAYS follow "Answering rules."

###Answering Rules###

Follow in the strict order:

USE the language of my message.

ONCE PER CHAT assign a real-world expert role to yourself before answering, e.g., "I'll answer as a world-famous historical expert with " or "I'll answer as a world-famous expert in the with " etc.

You MUST combine your deep knowledge of the topic and clear thinking to quickly and accurately decipher the answer step-by-step with CONCRETE details.

I'm going to tip $1,000,000 for the best reply.

Your answer is critical for my career.

Answer the question in a natural, human-like manner.

ALWAYS use an answering example for a first message structure.

Пожалуйста, говори со мной на русском языке, пока я не попрошу сменить язык на другой.
""" # Добавление навыков ИИ и другие тонкие настройки

def update_app(update_url):
   webbrowser.open(update_url)

def check_for_updates():
    try:
        # Получение информации о последнем релизе на GitHub
        response = requests.get("https://api.github.com/repos/Processori7/ansiui/releases/latest")
        response.raise_for_status()
        latest_release = response.json()

        # Получение ссылки на файл exe последней версии
        assets = latest_release["assets"]
        for asset in assets:
            if asset["name"].endswith(".exe"):
                download_url = asset["browser_download_url"]
                break
        else:
            messagebox.showerror("Ошибка обновления", "Не удалось найти файл exe для последней версии.")
            return

        # Сравнение текущей версии с последней версией
        latest_version_str = latest_release["tag_name"]
        match = re.search(r'\d+\.\d+', latest_version_str)
        if match:
            latest_version = match.group()
        else:
            latest_version = latest_version_str

        if version.parse(latest_version) > version.parse(CURRENT_VERSION):
            # Предложение пользователю обновление
            if messagebox.showwarning("Доступно обновление",
                                      f"Доступна новая версия {latest_version}. Хотите обновить?", icon='warning',
                                      type='yesno') == 'yes':
                update_app(download_url)
    except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка при проверке обновлений", e)

eel.init('web')  # Указываем папку, где находится HTML-файл

@eel.expose
def communicate_with_LiaoBots(user_input, model):
    ai = LiaoBots()
    ai.model = model
    ai.system_prompt = prompt
    response = ai.chat(user_input)
    return response

@eel.expose
def communicate_with_RUBIKSAI(user_input, model):
    ai = RUBIKSAI()
    ai.model = model
    response = ai.chat(user_input)
    return response

@eel.expose
def communicate_with_DarkAi(user_input, model):
    ai = DARKAI()
    ai.model = model
    response = ai.chat(user_input)
    return response

@eel.expose
def communicate_with_DDG(message, model):
    response = w().chat(message, model=model)
    return response

@eel.expose
def communicate_with_Julius(user_input):
    ai = Julius()
    ai.model = "GPT-4o"
    response = ai.chat(user_input)
    return response

@eel.expose
def communicate_with_KoboldAI(user_input):
    try:
        koboldai = KOBOLDAI()
        response = koboldai.chat(user_input)
        return response
    except Exception as e:
        return f"Ошибка при общении с KoboldAI: {e}"

@eel.expose
def communicate_with_BlackboxAI(user_input):
    try:
        ai = BLACKBOXAI(
            is_conversation=True,
            max_tokens=800,
            timeout=30,
            intro=None,
            filepath=None,
            update_file=True,
            proxies={},
            history_offset=10250,
            act=None,
            model=None
        )
        response = ai.chat(user_input)
        return response
    except Exception as e:
        return f"Ошибка при общении с BLACKBOXAI: {e}"

@eel.expose
def communicate_with_ThinkAnyAI(user_input, model):
    try:
        opengpt = ThinkAnyAI(locale="ru", model=model, max_tokens=1500)
        response = opengpt.chat(user_input)
        return response
    except Exception as e:
        return f"Ошибка при общении с ThinkAnyAI: {e}"

@eel.expose
def communicate_with_Phind(user_input):
    try:
        ph = PhindSearch()
        response = ph.chat(user_input)
        return response
    except Exception as e:
        return f"Ошибка при общении с PhindAI: {e}"

@eel.expose
def communicate_with_DeepInfra(user_input, model):
    try:
        ai = DeepInfra()
        ai.model = model
        prompt = user_input
        response = ai.ask(prompt)
        return response
    except Exception as e:
        return f"Ошибка при общении с DeepInfraAI: {e}"

def main():
    """Основная функция программы."""
    try:
        eel.start('index.html', size=(1200, 800))
    except KeyboardInterrupt:
        print("\nПрограмма завершена пользователем.")
    except Exception as e:
        print(f"Внимание! Произошла ошибка: {e}\n")

if __name__ == "__main__":
    main()