import discord
from discord.ext import commands
from discord import app_commands
from func.ready import bot_ready_print
from func.database import tag as tag_db

class TagCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        bot_ready_print("TagCog")

    class tag1(app_commands.Group):
        pass

    tag = tag1(name="tag", description="タグコマンド")
    
    @tag.command(name="search_tag", description="タグを検索します。")
    @app_commands.describe(name="タグの名前")
    async def search_tag(self, interaction:discord.Interaction, name:str):
        tags = tag_db()
        thread = tags.get_tag(name)
        
        if(thread is None):
            await interaction.response.send_message(embed=discord.Embed(
                title="検索",
                description="タグが見つかりませんでした。\nリンクを持っていたら、<#1408781349631950857>からタグの追加申請をしてみよう！",
                color=0xd450b7
            ))
        else:
            tagth = interaction.guild.get_thread(int(thread[1]))
            oya = tagth.parent.name
            tag = tagth

            if oya == "危険タグ":
                role = interaction.guild.get_role(1390436439140995212)
                if role in interaction.user.roles:
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title="検索",
                            description=f"タグ: {tag.name}\nここからスレッドに飛ぶことができます-> <#{tag.id}>\n分類: {oya}\n**このタグは危険タグに分類されています。**",
                            color=0x0bd708,
                        ),
                        ephemeral=True
                    )
                else:
                    await interaction.response.send_message(
                        "このタグは危険タグに指定されています。\n <#1408781348994551904> からロールを付与してください。",
                        ephemeral=True
                    )
            else:
                await interaction.response.send_message(embed=discord.Embed(
                    title="検索",
                    description=f"タグ: {tag.name}\nここからスレッドに飛ぶことができます-> <#{tag.id}>\n分類: {oya}",
                    color=0x0bd708
                ))
    
    

async def setup(bot):
    await bot.add_cog(TagCog(bot))