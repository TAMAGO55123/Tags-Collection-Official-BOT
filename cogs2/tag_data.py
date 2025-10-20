import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
from func.ready import bot_ready_print
from typing import Literal
from func.database import tag as tag_dbs
from func.data import lang_data

class TagAdminCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

        self.tag_log = 1408781350399508486
        self.tag_nofi = 1409368112993927379
    
    @commands.Cog.listener()
    async def on_ready(self):
        bot_ready_print("TagAdminCog")

    class tag_db1(app_commands.Group):
        pass

    tag_db = tag_db1(name="newtag", description="管理者タグ管理コマンド")
    
    @tag_db.command(name="add", description="追加")
    @app_commands.choices(kind=[
        Choice(name="標準", value="1408781349241749556"),
        Choice(name="参加申請", value="1408781349241749561"),
        Choice(name="危険単語", value="1408781349631950848"),
        Choice(name="危険", value="1408781349631950852")
    ])
    @app_commands.describe(
        name="タグの名前",
        invite_url="サーバーの招待リンク(あればバニティURLとか)",
        kind="タグの種類(選んでね)",
        lang="タグサーバーの主言語(選んでね)"
    )
    async def tag_add(self, interaction: discord.Interaction, name:str, invite_url:str, kind:Choice[str], lang:Literal["JP","EN","CN"]):
        await interaction.response.defer(thinking=True)
        tag = tag_dbs()
        a = tag.get_tag(name=name)
        if(a):
            await interaction.followup.send(
                embed=discord.Embed(
                    title="そのタグはすでに存在します。",
                    description=f"<#{a}>"
                )
            )
        else:
            aa = self.bot.get_guild(1408781348134719588)
            thread:discord.ForumChannel = aa.get_channel(int(kind.value))
            # print(thread)
            print(lang_data[kind.value][lang])
            lang_tag = thread.get_tag(lang_data[kind.value][lang])
            mes = await thread.create_thread(name=name, content=invite_url,applied_tags=[lang_tag])
            tag.create_tag(name=name, invite=invite_url, message_id=mes[0].id)
            await interaction.followup.send(embed=discord.Embed(
                title="タグ作成",
                description=f"name:{name}\ninvite:{invite_url}\n<#{mes[0].id}>",
                color=discord.Colour.default()
            ))
            await (self.bot.get_channel(self.tag_log)).send(
                embed=discord.Embed(
                    title="タグ作成",
                    description=f"名前:{name}\n招待リンク:{invite_url}\nスレッド:<#{mes[0].id}>\n担当者:{interaction.user.mention}",
                    color=discord.Colour.green()
                )
            )
            await (await (self.bot.get_channel(self.tag_nofi)).send(
                embed=discord.Embed(
                    title="タグが追加されました！",
                    description=f"**名前**:{name}\n**スレッド**:<#{mes[1].id}>",
                    color=discord.Colour.green()
                )
            )).publish()
    
    @tag_db.command(name="name", description="名前を変更します。")
    @app_commands.describe(
        old="元の名前",
        new="新しい名前"
    )
    async def tag_name(self, interaction:discord.Interaction, old:str, new:str):
        tag = tag_dbs()
        a = tag.get_tag(name=old)
        if(a):
            tag.update_name(oldname=old, newname=new)
            b = self.bot.get_channel(int(a[1]))
            await b.edit(name=new)
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="タグの名前を変更しました！",
                    description=f"{old} -> {new}\n<#{a[1]}>",
                    colour=discord.Colour.red()
                )
            )
            await (self.bot.get_channel(self.tag_log)).send(
                embed=discord.Embed(
                    title="タグ名前編集",
                    description=f"古い名前:{old}\n新しい:{new}\nスレッド:<#{a}>\n担当者:{interaction.user.mention}",
                    color=discord.Colour.green()
                )
            )
            await (await (self.bot.get_channel(self.tag_nofi)).send(
                embed=discord.Embed(
                    title="タグの名前が変更されました！",
                    description=f"**古い名前**:{old}\n**新しい名前**:{new}\n**スレッド**:<#{a[1].id}>",
                    color=discord.Colour.orange()
                )
            )).publish()
        else:
            await interaction.response.send_message("そのタグは存在しません。", ephemeral=True)
    
    @tag_db.command(name="invite",description="招待変更")
    @app_commands.describe(
        name="タグの名前",
        invite_url="新しいサーバーの招待リンク"
    )
    async def tag_edit(self, interaction:discord.Interaction, name:str, invite_url:str):
        tag = tag_dbs()
        a = tag.get_tag(name=name)
        if(a):
            tag.update_invite(name=name, invite=invite_url)
            tagth = interaction.guild.get_thread(int(a[1]))
            await tagth.starter_message.edit(content=invite_url)
            await interaction.response.send_message(embed=discord.Embed(
                title="招待変更",
                description=f"{name} : {invite_url}\n<#{a[1]}>"
            ))
            await (self.bot.get_channel(1402344952247357590)).send(
                embed=discord.Embed(
                    title="タグ招待編集",
                    description=f"名前:{name}\n招待リンク:{invite_url}\nスレッド:<#{a}>\n担当者:{interaction.user.mention}",
                    color=discord.Colour.green()
                )
            )
        else:
            await interaction.response.send_message("そのタグは存在しません。", ephemeral=True)

    @tag_db.command(name="ticket",description="チケット用")
    @app_commands.choices(kind=[
        Choice(name="標準", value="1408781349241749556"),
        Choice(name="参加申請", value="1408781349241749561"),
        Choice(name="危険単語", value="1408781349631950848"),
        Choice(name="危険", value="1408781349631950852")
    ])
    @app_commands.describe(
        name="タグの名前",
        invite_url="サーバーの招待リンク(あればバニティURLとか)",
        kind="タグの種類(選んでね)",
        lang="タグサーバーの主言語(選んでね)",
        member="チケットを開いた人"
    )
    async def tag_ticket(self, interaction: discord.Interaction, name:str, invite_url:str, kind:Choice[str], lang:Literal["JP","EN","CN"], member:discord.Member):
        await interaction.response.defer(thinking=True, ephemeral=True)
        tag = tag_dbs()
        a = tag.get_tag(name=name)
        if(a):
            await interaction.channel.send(embeds=[
                discord.Embed(
                    title="そのタグはすでに存在するようです。",
                    description=f"<#{a}>",
                    colour=discord.Colour.yellow()
                ),
                discord.Embed(
                        description="確認したら一番上のメッセージからCloseボタンを押してチャンネルを閉じてください。",
                        color=discord.Color.green()
                )
            ],content=member.mention)
        else:
            thread:discord.ForumChannel = interaction.guild.get_channel(int(kind.value))
            #print(thread)
            print(lang_data[kind.value][lang])
            lang_tag = thread.get_tag(lang_data[kind.value][lang])
            mes = await thread.create_thread(name=name, content=invite_url,applied_tags=[lang_tag])
            tag.create_tag(name=name, invite=invite_url, message_id=mes[0].id)
            await interaction.channel.send(
                embeds=[
                    discord.Embed(
                        title="タグを作成しました！",
                        description=f"名前:{name}\n招待リンク:{invite_url}\nスレッド:<#{mes[0].id}>\n担当者:{interaction.user.mention}",
                        color=discord.Colour.green()
                    ),
                    discord.Embed(
                        description="確認したら一番上のメッセージからCloseボタンを押してチャンネルを閉じてください。",
                        color=discord.Color.green()
                    )
                ],
                content=member.mention
            )
            await (self.bot.get_channel(1402344952247357590)).send(
                embed=discord.Embed(
                    title="タグ作成",
                    description=f"名前:{name}\n招待リンク:{invite_url}\nスレッド:<#{mes[0].id}>\n担当者:{interaction.user.mention}",
                    color=discord.Colour.green()
                )
            )
            await (await (self.bot.get_channel(1402345532550156298)).send(
                embed=discord.Embed(
                    title="タグが追加されました！",
                    description=f"**名前**:{name}\n**スレッド**:<#{mes[0].id}>",
                    color=discord.Colour.green()
                )
            )).publish()
        await interaction.followup.send(content="sended.", ephemeral=True)
    
    @tag_db.command(name="delete", description="タグを削除します。")
    @app_commands.describe(
        name="タグの名前"
    )
    async def tag_delete(self, interaction:discord.Interaction, name:str):
        tag = tag_dbs()
        a = tag.get_tag(name=name)
        if(a):
            tag.delete_tag(name=name)
            b = self.bot.get_channel(int(a[1]))
            b_id = b.id
            await b.delete(reason=f"{interaction.user.name}がtag_deleteを実行しました。")
            if b_id != interaction.channel.id:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title="タグを削除しました！",
                        description=f"名前:{name}",
                        colour=discord.Colour.yellow()
                    )
                )
            await (self.bot.get_channel(1402344952247357590)).send(
                embed=discord.Embed(
                    title="タグ削除",
                    description=f"名前:{name}\n招待リンク:{a[0]}\n担当者:{interaction.user.mention}",
                    color=discord.Colour.green()
                )
            )
        else:
            await interaction.response.send_message("そのタグは存在していません。", ephemeral=True)



async def setup(bot):
    await bot.add_cog(TagAdminCog(bot))