import discord
from discord.ext import commands
from discord import app_commands
from func.ready import bot_ready_print

class TempCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        bot_ready_print("TempCog")
    
    @app_commands.command(name="rule", description="ルールを表示します")
    async def rule(self, interaction:discord.Interaction):
        rule_str = """\
# ルール
## 1.禁止行為
- メッセージ、レイド、スパムなど
- 招待リンクの貼り付け
- 勧誘、引き抜き行為
## 2.処罰内容
> 1回目　30m TO
> 2回目　1h TO
> 3回目　2h TO
> 4回目　1d TO
> 5回目　7d TO
> 6回目　7d BAN
> 7回目　無期限 BAN
## 3.サーバータグ申請について
<#1408781349631950857> にて、該当するボタンからチケットを作成してください。
ただし以下の行為は忠告するかチケットを閉じる場合があります。
> タグサーバーではないサーバーを貼る
> タグ名を貼る
> タグを申請して抜ける(通知できません)
"""
        
        if interaction.channel.id == 1408781348616933486:
            await interaction.channel.send(embed=discord.Embed(description=rule_str, color=0xffffff))
            await interaction.response.send_message("完",ephemeral=True)
        else:
            await interaction.response.send_message(embed=discord.Embed(description=rule_str,color=0xffffff), ephemeral=True)
    
    @app_commands.command(name="what_tag")
    async def what_tag(self, interaction:discord.Interaction):
        tag_str = ["""\
# サーバータグってなに？
公式からのブログによると...
- サーバーメンバーがDiscord全体でそのサーバーを表現できる
- アイコンと4文字から成り立つもの
とありますが、基本的に好きな文字、デザインのタグをつけている方々が多いような気がします。
""",
"""\
## サーバータグの導入方法
1.ユーザー設定を開く
2.プロフィール設定を開く
3.下の方にあるサーバータグのメニューを開く
4.タグを選ぶ
5.保存する
"""]    
        a = discord.Embed(description=tag_str[0],color=0xffffff)
        b = discord.Embed(description=tag_str[1],color=0xffffff)
        await interaction.channel.send(embeds=[a,b])
        await interaction.response.send_message("完了", ephemeral=True)
        

async def setup(bot):
    await bot.add_cog(TempCog(bot))