import discord
from discord.ext import commands
from discord import app_commands
from func.ready import bot_ready_print
from func.data import verify_str
import os
import json
import asyncio
import urllib.parse

class VerifyCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

        self.ROLE_FILE = "database/verify.json"
    
    @commands.Cog.listener()
    async def on_ready(self):
        bot_ready_print("VerifyCog")
        if os.path.exists(self.ROLE_FILE):
            with open(self.ROLE_FILE, "r") as f:
                data = json.load(f)

            # ビュー再登録を高速化
            tasks = []
            for guild_id, role_ids in data.items():
                guild = self.bot.get_guild(int(guild_id))
                if guild:
                    for role_id in role_ids:
                        role = guild.get_role(role_id)
                        if role:  # ロールが存在する場合のみ
                            view = self.VerifyWebPanelView(role)
                            for item in view.children:
                                if isinstance(item, discord.ui.Button):
                                    item.custom_id = f"verify_{role.id}"
                            self.bot.add_view(view)
                            # ログを削減（必要に応じてコメントアウト）
                            print(f"ビューを再登録しました: {role.name} (ID: {role_id})")
                        # 非同期タスクを追加
                        tasks.append(asyncio.create_task(asyncio.sleep(0)))  # 軽量タスクでコンテキストスイッチを促進
            if tasks:
                await asyncio.gather(*tasks)  # タスクを並行実行

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.channel.id == 1408781350819069960:
            if message.author.name == "認証Web To ディスコ":
                data = message.content.split(',')
                user = message.guild.get_member(int(data[0]))
                if data[1] == "yes":
                    role = message.guild.get_role(1408781348134719597)
                    await message.add_reaction("<:shori:1411616015338700861>")
                    await message.add_reaction("<:kanryo:1411615975983288380>")
                else:
                    # role = message.guild.get_role(1411134096171733167)
                    role = message.guild.get_role(1408781348134719597)
                    await message.add_reaction("<:nenrei:1411616046632144916>")
                    await message.add_reaction("<:ihan:1411615896916721664>")
                await user.add_roles(role)
                await message.reply(embed=discord.Embed(description=f"name:{user.name}"))
        await self.bot.process_commands(message)
    
    class VerifyWebPanelView(discord.ui.View):
        def __init__(self, role: discord.Role):
            super().__init__(timeout=None)  # タイムアウトを無効化
            self.role = role

        @discord.ui.button(label="認証", style=discord.ButtonStyle.green, custom_id=None)
        async def role_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            avatar_id = interaction.user.display_avatar.url.split('/')[5]
            if interaction.user.avatar:
                defa = False
            else:
                defa = True
            if self.role in interaction.user.roles:
                await interaction.response.send_message("すでに認証済みです。", ephemeral=True)
            else:
                await interaction.response.send_message(embed=discord.Embed(
                    title="Web認証",
                    description=f"以下のリンクから認証してください。\n[Tags Collection Verify Page](https://tags-collection-verify.vercel.app/verify?name={urllib.parse.quote(interaction.user.display_name)}&id={interaction.user.id}&avid={urllib.parse.quote(avatar_id)}&def={defa})"
                ), ephemeral=True)
    
    async def save_role(self, guild_id: int, role_id: int):
        data = {}
        if os.path.exists(self.ROLE_FILE):
            with open(self.ROLE_FILE, "r") as f:
                data = json.load(f)
        guild_key = str(guild_id)
        if guild_key not in data:
            data[guild_key] = []
        if role_id not in data[guild_key]:
            data[guild_key].append(role_id)
        with open(self.ROLE_FILE, "w") as f:
            json.dump(data, f)

    @app_commands.command(name="verify-panel")
    async def verify_panel(self, interaction:discord.Interaction):
        role = interaction.guild.get_role(1408781348134719597)
        view = self.VerifyWebPanelView(role)
        for item in view.children:
            if isinstance(item, discord.ui.Button):
                item.custom_id = f"verify_{role.id}"
        embed = discord.Embed(
            title="認証",
            description=verify_str,
            color=0x00ff00
        )
        await interaction.channel.send(embed=embed, view=view)
        # 永続的なビューを登録
        self.bot.add_view(view)
        # JSONに保存（非同期）
        await self.save_role(interaction.guild.id, role.id)
        await interaction.response.send_message("完",ephemeral=True)

async def setup(bot):
    await bot.add_cog(VerifyCog(bot))