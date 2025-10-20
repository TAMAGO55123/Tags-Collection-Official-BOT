from func.data import BOT_ADMIN
import discord

# 管理者チェックの関数
def is_bot_admin(user_id:int) -> bool:
    return user_id in BOT_ADMIN

def color_code(code:str) -> int:
    if "#" in code:
        a = code.replace("#", "")
    else:
        a = code

    return int(f"0x{a}", 16)

class SendModal(discord.ui.Modal):
    def __init__(self, channel:discord.TextChannel, ifembed:bool,user:discord.Member):
        super().__init__(
            title="フォーム",
            timeout=None,
        )

        self.messages = discord.ui.TextInput(
            label="メッセージ",
            style=discord.TextStyle.paragraph,
            required=True,
        )
        self.add_item(self.messages)

        self.channel = channel
        self.ifembed = ifembed
        self.user = user

    async def on_submit(self, interaction:discord.Interaction):
        if self.ifembed:
            a = await self.channel.send(embed=discord.Embed(description=self.messages))
        else:
            a = await self.channel.send(content=self.messages)
        await interaction.response.send_message("sended.",ephemeral=True)

admin_per = discord.Permissions()
admin_per.administrator=True