import discord
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
# intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!hello'):
        print('Hello!')
        await message.channel.send('Hello!')


load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

client.run(TOKEN)
