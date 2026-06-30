print("起動開始")
import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv
import json
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="o!", intents=intents, help_command=None)
tree = bot.tree

class UnmuteView(discord.ui.View):
    def __init__(self, target_member: discord.Member):
        super().__init__(timeout=60) 
        self.target_member = target_member

    @discord.ui.button(label="タイムアウト解除", style=discord.ButtonStyle.green, custom_id="unmute_button")
    async def unmute_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await self.target_member.edit(timed_out_until=None)
            await interaction.response.send_message(f"{self.target_member.mention} のタイムアウトを解除した。")
            
            # ボタンを押した後にボタンを無効化（グレーアウト）する
            button.disabled = True
            await interaction.message.edit(view=self)
            
        except discord.Forbidden:
            await interaction.response.send_message("Botに権限がないから解除できない。")


async def json_edit(kinds, count):
    with open('count.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    data[kinds] += count
    data["all"] += count
    with open('count.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    all_count = data["all"]
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming,
                                                name=f"{all_count}回の「お」(合計値)",
                                                url="https://www.youtube.com/watch?v=uC3wcyVB8yg"
                                                ))

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming,
                                                name="x回の「お」(合計値)",
                                                url="https://www.youtube.com/watch?v=uC3wcyVB8yg"
                                                ))
    await tree.sync()
    print("ログインした")
    print("起動完了した")


@bot.event
async def on_message(message):
    if message.channel.id in (ここにチャンネルIDを入れる):
        if message.author.bot:
            return
        
        message_content = message.content

        if message_content.count("お") > 0:
            count = message_content.count("お")
            await json_edit("お", count)
        if message_content.count("お゙") > 0:
            count = message_content.count("お゙")
            await json_edit("お゙", count)
        if message_content.count("ぉ") > 0:
            count = message_content.count("ぉ")
            await json_edit("ぉ", count)
        if message_content.count("ぉ゙") > 0:
            count = message_content.count("ぉ゙")
            await json_edit("ぉ゙", count)
        if message_content.count("オ") > 0:
            count = message_content.count("オ")
            await json_edit("オ", count)
        if message_content.count("オ゙") > 0:
            count = message_content.count("オ゙")
            await json_edit("オ゙", count)
        if message_content.count("ォ") > 0:
            count = message_content.count("ォ")
            await json_edit("ォ", count)
        if message_content.count("ォ゙") > 0:
            count = message_content.count("ォ゙")
            await json_edit("ォ゙", count)
        if message_content.count("ｵ") > 0:
            count = message_content.count("ｵ")
            await json_edit("ｵ", count)
        if message_content.count("御") > 0:
            count = message_content.count("御")
            await json_edit("御", count)
        if message_content.count("o") > 0:
            count = message_content.count("o")
            await json_edit("o", count)
        if message_content.count("O") > 0:
            count = message_content.count("O")
            await json_edit("O", count)

        if not any(char in message_content for char in ("お","お゙","ぉ","ぉ゙","オ","オ゙","ォ","ォ゙","ｵ","御","o","O")):
            try:
                duration = datetime.timedelta(minutes=1)
                await message.author.timeout(duration, reason="[お]を言わなかった罪")
                    
                view = UnmuteView(target_member=message.author)
                embed = discord.Embed(
                    title=f"{message.author.name} をタイムアウトの刑に処した。",
                    description="「お」の類の文字を含まないメッセージを送信しました。\nよって「[お]を言わなかった罪」として貴様を1分タイムアウトの刑にした。\n下のボタンを押すと解除されます。")
                await message.channel.send(embed=embed,view=view)
            except discord.Forbidden:
                return


@tree.command(name="ping", description="ping計測します")
async def ping(ctx: discord.Interaction):
    text = f'{round(bot.latency*1000)}ms'
    embed = discord.Embed(title='Pong!', description=text)
    await ctx.response.send_message(embed=embed)


@tree.command(name="name", description="お前の名前を おお にします")
async def nameO(interaction: discord.Interaction):
    try:
        user = interaction.user
        await user.edit(nick="おおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおお")
        await interaction.response.send_message(f"お前のニックネームを変更した。")
    except discord.Forbidden:
        await interaction.response.send_message("Botに権限がない。\n権限よこせ。")

@tree.command(name="count", description="「お」の回数を表示します")
async def countO(interaction: discord.Interaction):
    with open('count.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    embed = discord.Embed(title='「お」の発言回数',
                          description=f'''
合計回数・・・{data["all"]}回
「お」・・・ {data["お"]} 回
「お゙」・・・ {data["お゙"]} 回
「ぉ」・・・ {data["ぉ"]} 回
「ぉ゙」・・・ {data["ぉ゙"]} 回
「オ」・・・ {data["オ"]} 回
「オ゙」・・・ {data["オ゙"]} 回
「ォ」・・・ {data["ォ"]} 回
「ォ゙」・・・ {data["ォ゙"]} 回
「ｵ」・・・ {data["ｵ"]} 回
「御」・・・ {data["御"]} 回
「o」・・・ {data["o"]} 回
「O」・・・ {data["O"]} 回
                          '''
                          )
    await interaction.response.send_message(embed=embed)




bot.run(TOKEN)
