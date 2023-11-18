gptが書いたよ。手抜きすまん


# Discord GPT Bot

このプロジェクトは、Discord上で動作するGPT-3.5モデル,4を利用したチャットボットです。ユーザーが指定したテキストや画像に対して、GPT-3.5が応答します。

## 準備

1. **Replitアカウントの作成**: [Replit](https://replit.com/)にアカウントを作成してください。

2. **Discordボットのトークン取得**:
   - Discord Developer Portalから新しいボットを作成し、トークンを取得してください。
   - [Discord Developer Portal](https://discord.com/developers/applications)

3. **OpenAI APIキーの取得**:
   - [OpenAI](https://beta.openai.com/signup/)でアカウントを作成し、GPT-3.5のAPIキーを取得してください。

4. **環境変数の設定**:
   - Replitの左側のメニューから「Secrets」を選択し、`GPTAPI`と`TOKEN`という名前でOpenAI APIキーとDiscordボットのトークンを設定してください。





コマンド
!hello: ボットが「Hello!」と返すコマンド。
!gpt [質問]: GPT-3.5が指定された質問に対して回答します。
!MESI [素材]: GPT-3.5が指定された素材を元に和洋中料理を提案します。
!gpt [質問] :質問に答えてくれる
そのまま画像投稿


注意事項
一部のコマンドは特定のDiscordチャンネルでのみ実行可能です。有効なチャンネルIDはvalid_channel_ids変数で指定されています。
ボットがDiscordに接続できない場合は、トークンやAPIキーが正しく設定されているか確認してください。
楽しいチャットと美味しい料理をお楽しみください！