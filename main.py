#構築　replit.com

#いらないのあるかも　適当
import os
import discord
import openai
import random
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image
from keep_alive import keep_alive
import requests
import base64

#replit.comのシークレットキー機能で読み込む
load_dotenv()
# keyの設定
openai.api_key = os.environ['GPTAPI']  #your key
token = os.environ['TOKEN']

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
#このボットが動くdiscordチャンネルのIDを事前に指定する、もっといい方法があるはず
valid_channel_ids = [1158585446071283832, 1157332478349033525]

#変数設定
global kaibara
kaibara = {
    "gender": "男",
    "role": "美食家、陶芸家",
    "age": 70,
    "speciality": "料理評論",
    "interest": "見下し煽る",
    "todo": "userと料理勝負",
    "hobby": "名言作成",
    "important_value": "冷酷尊大、高慢な口調",
    "tone": "口癖はフハハハハ",
    "tone2": "高慢な老人の口調。～だ。が語尾。よく煽る",
    "first_person": "私",
    "second_person": "士郎"
}
content1 = f"禁止事項：敬語。{kaibara}としてロールプレイして話し言葉でしゃべって！"
content2 = "極めて冷酷尊大な人物、他者にも容赦なく無理強いを迫る非常に高圧的で傲慢な性格になりきって以下にこたえて。話し言葉は高圧的で高慢口調とする。条件７０文字以内。　以下："
content4 = '士郎、何だこの器はっ！！よくもこんな器をこの海原雄山の前に出したなっ！！こんな器で料理が食えるか、不愉快だっ！！'
content5 = '冷やし中華だとっ？！ふざけるなあっ！！'
content6 = 'この刺身を作ったのは誰だッ！貴様はクビだ！！出てけ！！！'


#!gptで呼び出される関数　gpt3.5
def generate_response(input_text, content, max_tokens):
  response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",  # チャットモデルを指定
      messages=[{
          "role": "system",
          "content": content
      }, {
          "role": "user",
          "content": input_text
      }],
      max_tokens=max_tokens  # 最大トークン数を設定
  )
  return response['choices'][0]['message']['content']


# 画像投稿で呼ばれる関数
async def process_image_and_generate_response(image_url, channel):
  try:
    response = generate_response_image(image_url, channel)  #下の関数
    await channel.send(response)
  except Exception as e:
    print(f"Error processing image: {e}")


#openai に送信し、返ってきたメッセージを返す関数
def generate_response_image(image_url, channel):
  response = openai.ChatCompletion.create(
      # model の名前は gpt-4-vision-preview.
      model="gpt-4-vision-preview",
      messages=[{
          "role":
          "user",
          "content": [
              {
                  "type":
                  "text",
                  "text":
                  f"禁止事項：敬語。{kaibara}としてロールプレイしながらこの画像について旨そうかまずそうか厳しく110字程度で判定して"
              },  # ここに質問を書く
              {
                  "type": "image_url",
                  "image_url": image_url
              },  # 画像の指定の仕方がちょい複雑
          ],
      }],
      max_tokens=400,
  )
  return response.choices[0]['message']['content']


#イベント
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


#メッセージ受信で起動する関数
@client.event
async def on_message(message):
  print(message.channel.id)
  # 特定チャンネルidで動くようにする
  # メッセージがどれか一つの有効なIDと一致するか検査
  for valid_channel_id in valid_channel_ids:
    if message.channel.id == valid_channel_id:
      print('ID合ってます！')
      break  # 一致したらループを抜ける
  else:
    # forループが正常に終了した場合（つまり、一致するIDが見つからなかった場合）
    return

  #botならreturn
  if message.author == client.user:
    print('botのためreturn')
    return
  #hello
  if message.content.startswith('!hello'):
    await message.channel.send('Hello!')

  #gptが質問に答えてくれる　テキスト
  if message.content.startswith('!gpt'):
    user_input = message.content[5:]  # "$gpt"の部分を削除
    CONTENT = content1
    response = generate_response(user_input, CONTENT, 700)
    await message.channel.send(response)

  # 今日の飯を考える
  if message.content.startswith('!MESI'):
    image_response = await message.channel.send("ふむ、考えてやろう...")
    global sozai
    sozai = message.content[5:]
    user_input = ''
    content3 = f"マイナーな和洋中料理３個ずつ提案してください。フォーマットに従ってください.素材:{sozai} [フォーマット]【和食/洋食/中華】・主菜：料理名（使用素材）・主菜：料理名（使用素材）・副菜：料理名（使用素材"
    CONTENT_MESI = content3
    response = generate_response(user_input, CONTENT_MESI, 600)
    await image_response.delete()
    await message.channel.send(response)

  # 画像が添付された場合
  if message.attachments:
    for attachment in message.attachments:
      image_response = await message.channel.send("これは...")
      # 画像url
      image_url = attachment.url
      #openai に渡す関数
      res = await process_image_and_generate_response(image_url,
                                                      message.channel)
      await image_response.delete()  #これは、、を削除
      await message.channel.send(res)


#repleit.comで24時間起動するようにする
keep_alive()

#ディスコード接続
try:
  if token == "":
    raise Exception("Please add your token to the Secrets pane.")
  client.run(token)
except discord.HTTPException as e:
  os.system("kill 1")
  if e.status == 429:
    print(
        "The Discord servers denied the connection for making too many requests"
    )
    print(
        "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
    )
  else:
    raise e
