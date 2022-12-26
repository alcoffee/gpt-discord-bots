import discord
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
print(str(TOKEN))
client.run(TOKEN)
