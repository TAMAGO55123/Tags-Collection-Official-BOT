import discord
from discord.ext import commands
from discord import app_commands
from func.ready import bot_ready_print
from func.tools import SendModal, admin_per
from func.database import tag

class AdminCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        bot_ready_print("AdminCog")
    
    class admin1(app_commands.Group):
        pass
    
    admin = admin1(name="admin", description="管理者専用コマンド", default_permissions=admin_per)

    @admin.command(name="status",description="ステータスを設定するコマンドです")
    @app_commands.describe(text="ステータスを設定します" ,status="ステータスを設定します",)
    @app_commands.choices(status=[
        app_commands.Choice(name="オンライン / online", value="online"),
        app_commands.Choice(name="オンライン状態を隠す / offline", value="offline"),
        app_commands.Choice(name="離席中 / idle", value="idle"),
        app_commands.Choice(name="取込み中 / dnd", value="dnd"),
    ])
    async def set_status(self, interaction: discord.Interaction, text: str, status: app_commands.Choice[str]):
            # オンライン状態を選択
            if status.value == "online":
                await self.bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name=f"{text}"))
            # オフライン状態を選択
            elif status.value == "offline":
                await self.bot.change_presence(status=discord.Status.invisible, activity=discord.CustomActivity(name=f"{text}"))
            # 離席中状態を選択
            elif status.value == "dnd":
                await self.bot.change_presence(status=discord.Status.dnd, activity=discord.CustomActivity(name=f"{text}"))
            # 取込み中状態を選択
            elif status.value == "idle":
                await self.bot.change_presence(status=discord.Status.idle, activity=discord.CustomActivity(name=f"{text}"))
                
            await interaction.response.send_message(f'ステータスを「{text}」に設定し、状態を「{status.name}」にしました。\n{status.value}', ephemeral=True)
            
    @admin.command(name="send", description="送信")
    async def send(self, interaction:discord.Interaction, channel:discord.TextChannel = None, ifembed:bool = True):
            if channel == None:
                send_channel = interaction.channel
            else:
                send_channel = channel
            modal = SendModal(channel=send_channel,ifembed=ifembed,user=interaction.user)
            await interaction.response.send_modal(modal)

    @admin.command(name="get_thread")
    async def get_tag_count(self, interaction:discord.Interaction):
            tag_db = tag()
            tag_db.cursor.execute('SELECT COUNT(*) FROM tag')
            result = tag_db.cursor.fetchone()
            print(result)

            message1 = f"タグの数: {result[0]}"
            
            voice:discord.VoiceChannel = self.bot.get_channel(1408781348616933484)
            message2 = f"{voice.name}\n↓\nタグの数: {str(result[0])}"
            await voice.edit(name=message1)
            await interaction.response.send_message(content=message2)

async def setup(bot):
    await bot.add_cog(AdminCog(bot))