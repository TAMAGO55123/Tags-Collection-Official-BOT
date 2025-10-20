import discord
from discord.ext import commands
from discord import app_commands
from func.ready import bot_ready_print
import os
import json
import asyncio

class RoleCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

        self.ROLE_FILE = "database/role.json"
    
    @commands.Cog.listener()
    async def on_ready(self):
        bot_ready_print("RoleCog")
        if os.path.exists(self.ROLE_FILE):
            with open(self.ROLE_FILE, "r") as f:
                data = json.load(f)

            # ビュー再登録を高速化
            tasks = []
            for guild_id, role_ids in data.items():
                guild = self.bot.get_guild(int(guild_id))
                if guild:
                    roles = [guild.get_role(role_id) for role_id in role_ids if guild.get_role(role_id)]
                    if roles:  # 有効なロールが存在する場合のみ
                        # 複数ロールの場合はMultiRolePanelViewを使用
                        if len(roles) > 1:
                            view = self.MultiRolePanelView(roles)
                        # 単一ロールの場合はRolePanelViewを使用
                        else:
                            view = self.RolePanelView(roles[0])
                        self.bot.add_view(view)
                        # ログを削減（必要に応じてコメントアウト）
                        print(f"ビューを再登録しました: {[role.name for role in roles]} (Guild ID: {guild_id})")
                    # 非同期タスクを追加
                    tasks.append(asyncio.create_task(asyncio.sleep(0)))  # 軽量タスクでコンテキストスイッチを促進
            if tasks:
                await asyncio.gather(*tasks)  # タスクを並行実行
    
    class MultiRolePanelView(discord.ui.View):
        def __init__(self, roles: list):
            super().__init__(timeout=None)
            self.roles = roles
            # 最大5つのロールに対応するボタンを動的に追加
            for role in roles[:5]:
                button = discord.ui.Button(
                    label=f"{role.name}",
                    style=discord.ButtonStyle.secondary,
                    custom_id=f"role_{role.id}"
                )
                button.callback = self.create_role_callback(role)
                self.add_item(button)

        def create_role_callback(self, role: discord.Role):
            async def role_button(interaction: discord.Interaction):
                if role in interaction.user.roles:
                    await interaction.user.remove_roles(role)
                    await interaction.response.send_message(f"{role.name} ロールを削除しました", ephemeral=True)
                else:
                    await interaction.user.add_roles(role)
                    await interaction.response.send_message(f"{role.name} ロールを付与しました", ephemeral=True)
            return role_button

    # 複数ロール用スラッシュコマンドの定義
    @app_commands.command(name="rolepanel", description="最大5つのロールを指定してロールパネルを生成します")
    @app_commands.describe(
        role1="1つ目のロール（必須）",
        role2="2つ目のロール（任意）",
        role3="3つ目のロール（任意）",
        role4="4つ目のロール（任意）",
        role5="5つ目のロール（任意）"
    )
    async def rolepanel(self, interaction: discord.Interaction, role1: discord.Role, role2: discord.Role = None, role3: discord.Role = None, role4: discord.Role = None, role5: discord.Role = None, emoji1:str = None, emoji2:str = None, emoji3:str = None, emoji4:str = None, emoji5:str = None):
        # 指定されたロールをリストにまとめる（Noneを除外）
        roles = [r for r in [role1, role2, role3, role4, role5] if r is not None]
        emojis = [r for r in [emoji1, emoji2, emoji3, emoji4, emoji5] if r is not None]
        if not roles:
            await interaction.response.send_message("少なくとも1つのロールを指定してください", ephemeral=True)
            return
        a = ""
        for i in range(len(roles)):
            a = f"{a}{emojis[i]} <@&{roles[i].id}>\n"
        # ロールパネルを作成
        view = self.MultiRolePanelView(roles)
        embed = discord.Embed(
            title="ロールパネル",
            description=a,
            color=discord.Color.blue()
        )
        await interaction.channel.send(embed=embed, view=view)
        # 永続的なビューを登録
        self.bot.add_view(view)
        # JSONに保存（非同期）
        await self.save_role(interaction.guild.id, [role.id for role in roles])
        await interaction.response.send_message("完",ephemeral=True)
    
    # JSONにロール情報を保存する関数
    async def save_role(self, guild_id: int, role_ids: list):
        data = {}
        if os.path.exists(self.ROLE_FILE):
            with open(self.ROLE_FILE, "r") as f:
                data = json.load(f)
        guild_key = str(guild_id)
        if guild_key not in data:
            data[guild_key] = []
        for role_id in role_ids:
            if role_id not in data[guild_key]:
                data[guild_key].append(role_id)
        with open(self.ROLE_FILE, "w") as f:
            json.dump(data, f)

async def setup(bot):
    await bot.add_cog(RoleCog(bot))