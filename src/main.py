import discord, logging
from dotenv import load_dotenv
import os, sys

# 別ファイルを取り込む
import open_ai
import sql_interface

# ログの設定
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('test.log'),
    ])

# インテンツ？
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

load_dotenv()

# sqlの管理
sm = sql_interface.SessionManager()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # General以外には全てに常駐
    if message.channel.name != "一般":
        input_prompt = message.content.strip()
        msg_history = []
        logging.info(input_prompt)
        for prompt, completion in sm.get_pair_list(message.channel.id):
            msg_history.append({"role":"user", "content": prompt})
            msg_history.append({"role":"assistant", "content": completion})
        completion = open_ai.zunda(msg_history, input_prompt)
        logging.info(completion)
        sm.add_record(input_prompt, completion, message.channel.id)
        await message.channel.send(completion)

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
client.run(TOKEN)
