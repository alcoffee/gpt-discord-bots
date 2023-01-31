import discord
import os
from dotenv import load_dotenv

import openai
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import datetime

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

load_dotenv()
openai.api_key=os.environ.get("OPENAI_API_KEY")
model_name = "text-davinci-003"

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

# エンジンの定義
engine = sqlalchemy.create_engine('sqlite:///database.db', echo=True)

# sqlalchemyでデータベースのテーブルを扱うための宣言
Base = sqlalchemy.ext.declarative.declarative_base()

# テーブルのフィールドを定義
class Session(Base):
    __tablename__ = 'sessions'
    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    prompt = sqlalchemy.Column(sqlalchemy.String(500))
    completion = sqlalchemy.Column(sqlalchemy.String(500))
    channel_id = sqlalchemy.Column(sqlalchemy.String(100))
    created_at = sqlalchemy.Column(sqlalchemy.DateTime)

# データベースにテーブルを作成
Base.metadata.create_all(engine)

# データベースに接続するためのセッションを準備
SessionDataBase = sqlalchemy.orm.sessionmaker(bind=engine)

class SessionManager:
    def __init__(self):
        self.session = SessionDataBase()

    def add_record(self, prompt, completion, channel_id):
        # レコードを準備し、セッションを通してデータベースに送る
        s = Session(
            prompt=prompt,
            completion=completion,
            channel_id=channel_id,
            created_at=datetime.datetime.now()
        )
        self.session.add(s)
        self.session.commit()

    def get_pair_list(self, channel_id):
        # channel_idを指定して、promptとcompletionを古い順に取得する
        record_list = self.session.query(Session).filter_by(channel_id=channel_id).order_by(Session.created_at.desc()).limit(10).all() 
        # promptとcompletionのペアの配列を取得する
        pair_list = [(record.prompt, record.completion) for record in record_list]
        return pair_list

    def delete_pair_list(self, channel_id):
        # データベースから指定されたchannel_idのレコードを削除する
        record_list = self.session.query(Session).filter_by(channel_id=channel_id).all()
        for record in record_list:
            self.session.delete(record)
        self.session.commit()

    def get_pair_count(self, channel_id):
        # データベースから指定されたchannel_idのレコードの件数を取得する
        count = self.session.query(Session).filter_by(channel_id=channel_id).count()
        return count

sm = SessionManager()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # General以外には全てに常駐
    if message.channel.name != "一般":
        input_prompt = message.content.strip()
        template = ""
        for prompt, completion in sm.get_pair_list(message.channel.id):
            template += "User:"+prompt + "\n"
            template += "Assistant:"+completion + "\n"
        prompt = template + "User: " + input_prompt + "\n" + "Assistant: "
        print(prompt)
        completion = davinciStrictive(prompt)
        sm.add_record(input_prompt, completion, message.channel.id)
        await message.channel.send(completion)

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
client.run(TOKEN)
