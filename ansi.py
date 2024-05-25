import eel
from ai4free import KOBOLDAI, BLACKBOXAI, ThinkAnyAI, PhindSearch, DeepInfra
from freeGPT import Client

eel.init('web')  # Указываем папку, где находится HTML-файл

@eel.expose
def communicate_with_model(message):
    """Взаимодействует с моделью для генерации ответа."""
    try:
        resp = Client.create_completion("gpt3", message)
        return resp
    except Exception as e:
        return f"Ошибка при общении с моделью: {e}"

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
        responce = ai.chat(user_input)
        return responce
    except Exception as e:
        return f"Ошибка при общении с BLACKBOXAI: {e}"

@eel.expose
def communicate_with_ThinkAnyAI(user_input):
    try:
        opengpt = ThinkAnyAI()
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
def communicate_with_DeepInfra(user_input):
    try:
        ai = DeepInfra(
            model="meta-llama/Meta-Llama-3-70B-Instruct",
            is_conversation=True,
            max_tokens=800,
            timeout=30,
            intro=None,
            filepath=None,
            update_file=True,
            proxies={},
            history_offset=10250,
            act=None,
        )
        message = ai.ask(user_input)
        responce = ai.get_message(message)
        return responce
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