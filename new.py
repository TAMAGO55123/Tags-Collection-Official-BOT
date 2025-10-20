import discord
from discord.ext import commands, tasks
import os
from datetime import datetime
import asyncio
from dotenv import load_dotenv
import re
from typing import Union
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="tags_", intents=intents)

TOKEN = os.getenv("b_TOKEN")  # TOKENの取得


async def main(bot:commands.Bot):
    @bot.event
    async def on_ready():
        print(f'{bot.user} としてログインしました^o^')
        try:
            synced = await bot.tree.sync()
            print(f'Synced {len(synced)} commands')
        except Exception as e:
            print(f'Error syncing commands: {e}')
        await send_update_message()
        await bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name=f'Tags Collection Ver2'))

    for cog in os.listdir("cogs2"):
        if cog.endswith(".py"):
            await bot.load_extension(f"cogs2.{cog[:-3]}")

    class SendEmbedModal(discord.ui.Modal):
        def __init__(self, channel:discord.TextChannel, message:str):
            super().__init__(
                title="フォーム",
                timeout=None,
            )

            self.messages = discord.ui.TextInput(
                label="Color Code",
                style=discord.TextStyle.short,
                max_length=6,
                required=False,
            )
            self.add_item(self.messages)

            self.channel = channel
            self.message = message

        async def on_submit(self, interaction:discord.Interaction):
            if self.messages.value:
                a = int(f"0x{self.messages.value}", 16)
            else:
                a = None
            await self.channel.send(embed=discord.Embed(description=self.message, color=a))
            await interaction.response.send_message("sended.",ephemeral=True)

    @bot.tree.context_menu(name="メッセージを再送信")
    async def message_re_send(interaction:discord.Interaction, message:discord.Message):
        if interaction.user.guild_permissions.administrator:
            await message.channel.send(content=message.content, embeds=message.embeds)
            await interaction.response.send_message(content="sended.",ephemeral=True)
        else:
            await interaction.response.send_message(content="このアプリは、管理者のみ実行可能です。", ephemeral=True)

    @bot.tree.context_menu(name="メッセージを埋め込みに変換")
    async def message_send_embed(interaction:discord.Interaction, message:discord.Message):
        if interaction.user.guild_permissions.administrator:
            modal = SendEmbedModal(channel=message.channel, message=message.content)
            await interaction.response.send_modal(modal)
        else:
            await interaction.response.send_message(content="このアプリは、管理者のみ実行可能です。", ephemeral=True)
    
    @bot.tree.context_menu(name="埋め込みをメッセージに変換")
    async def embed_send_message(interaction:discord.Interaction, message:discord.Message):
        if interaction.user.guild_permissions.administrator:
            a = ""
            for i in message.embeds:
                a = a + i.description
            await message.channel.send(content=a)
            await interaction.response.send_message("sended.", ephemeral=True)
        else:
            await interaction.response.send_message(content="このアプリは、管理者のみ実行可能です。", ephemeral=True)

    async def send_update_message():
        update_id = 1408781350819069955
        update = await bot.fetch_channel(update_id)
        embed = discord.Embed(title='BOTが起動しました^o^',description="BOTが起動されました",color=0x0004ff,timestamp=datetime.now())
        await update.send(embed=embed)

    @bot.tree.context_menu(name="手動認証(管理者)")
    async def manual_verify(interaction:discord.Interaction, message:discord.Message):
        if interaction.user.guild_permissions.administrator:
            role = message.guild.get_role(1345231376026304653)
            await message.author.add_roles(role)
            await message.author.send(f"手動にて認証が完了いたしました。\n実行者: {interaction.user.name}")
            await interaction.response.send_message(f"ロール:{role.name} 付与完了。")
            await message.add_reaction("✅")
        else:
            await interaction.response.send_message("このコマンドは管理者のみ実行できます。",ephemeral=True)
    
    @bot.event
    async def on_message(message:discord.Message):
        if type(message.channel) != discord.DMChannel:
            if (message.channel.category.id == 1408781349631950856):
                if (message.author.id == 557628352828014614):
                        if ('Welcome' in message.content):
                            if ('Category: [Tag]' in message.content):
                                a:Union[re.Match,None] = re.search(r'```([\s\S]*?)```', message.embeds[1].description)
                                if a:
                                    b = a.group()[4:-3]
                                    if (b != ''):
                                        await message.channel.send(content=f"これは自動招待確認用メッセージです。\n{b}")
                                        try:
                                            c = await bot.fetch_invite(b)
                                            d = discord.Embed(
                                                title="情報",
                                                description=f"**Name**: `{c.guild.name}`,\n**ID**: `{c.guild.id}`",
                                                colour=discord.Colour.green()
                                            )
                                            await message.channel.send(embed=d)
                                        except (ValueError, discord.NotFound, discord.HTTPException) as e:
                                            await message.channel.send('招待が取得できませんでした。')
        await bot.process_commands(message)
    
    await bot.start(TOKEN)

try:
    discord.utils.setup_logging()
    asyncio.run(main(bot=bot))
except Exception as e:
    print(f'エラーが発生しました: {e}')
