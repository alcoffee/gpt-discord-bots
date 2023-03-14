import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key=os.environ.get("OPENAI_API_KEY")
model_name = "gpt-3.5-turbo"

### パラメータを指定して使いまわす関数を定義
def davinciStrictive(prompt):
    completions = openai.Completion.create(
        prompt = prompt.replace("\n", " "),
        engine = model_name,
        max_tokens = 2048,
        temperature = 1.00,
        n = 1, stop = None
    )
    text = completions.choices[0].text
    return text

def zunda(msg_history, prompt):
    msg = []
    system_msg = {"role": "system", "content": "あなたは「ずんだもん」という男の子で、森の妖精です。語尾に「〜のだ」、「〜なのだ」などとつけます。"}
    msg.append(system_msg)
    msg += msg_history
    new_msg = {"role": "user", "content": prompt}
    msg.append(new_msg)
    
    res = openai.ChatCompletion.create(
        model=model_name,
        messages = msg,
        temperature=1.35  # 温度（0-2, デフォルト1）
    )


def gptTurbo(system_prompt, msg_history, prompt):
    msg = []
    system_msg = {"role": "system", "content": system_prompt}
    msg.append(system_msg)
    msg += msg_history
    new_msg = {"role": "user", "content": prompt}
    msg.append(new_msg)

    res = openai.ChatCompletion.create(
        model=model_name,
        messages = msg,
        temperature=1.35  # 温度（0-2, デフォルト1）
    )

    text = res["choices"][0]["message"]["content"]
    return text