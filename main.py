import discord
from discord.ext import commands
from discord.ext.commands import bot
from dotenv import load_dotenv
import os
from pymongo import MongoClient

coll = MongoClient('mongodb://localhost:27017/').HK_ADVE.ads

load_dotenv('.env')

bot = commands.Bot(command_prefix='.ad ', help_command=None)

am = discord.AllowedMentions.none()



@bot.event
async def on_ready():
    print(f'{bot.user} On Ready.')
    u = await bot.fetch_user(443734180816486441)
    await bot.change_presence(status = discord.Status.online, activity = discord.Game(f"Made By {u}"))

@bot.command(name='create')
async def create_ad(ctx, *, content):
    if os.path.isdir('./Ads/'):
        with open(f'./Ads/{content}.txt', 'a,', encoding='UTF-8') as f:
            f.write(1)
            f.seek(0)
            f.truncate()

    else:
        os.mkdir('./Ads/')
        with open(f'./Ads/{content}.txt', 'a,', encoding='UTF-8') as f:
            f.write(1)
            f.seek(0)
            f.truncate()

    coll.insert_one({"_id": str(content)})
    return await ctx.reply('광고 등록이 완료되었습니다.', allowed_mentions=am)

@bot.command(name='frequency')
async def setfrequency(ctx, *, name):
    if coll.find_one({"_id": str(name)}):
        # least: 최소 노출 빈도, max = 최대 노출 빈도
        await ctx.reply('지금 최소 노출 빈도를 입력하여주세요.', allowed_mentions=am)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        msg = await bot.wait_for('message', check=check)

        least = msg.content

        await ctx.reply('지금 최대 노출 빈도를 입력하여주세요.', allowed_mentions=am)
        msg = await bot.wait_for('message', check=check)
        max = msg.content

        find = {"_id": str(name)}
        setdata = {"$set": {"least": int(least), "max": int(max)}}
        coll.update_one(find, setdata)

        await ctx.reply(f'`{name}` 광고의 최소/최대 빈도 수 설정이 완료되었습니다.', allowed_mentions=am)

    else:
        await ctx.reply(f'`{name}` 이라는 광고를 찾을 수 없습니다.', allowed_mentions=am)


@bot.command(name='time')
async def settime(ctx, *, name):
    if coll.find_one({"_id": str(name)}):

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.reply('지금 노출 수를 입력해주세요.', allowed_mentions=am)
        msg = await bot.wait_for('message', check=check)
        msg = msg.content

        find = {"_id": str(name)}
        setdata = {"$set": {"count": int(msg)}}
        coll.update_one(find, setdata)

        await ctx.reply('노출 수 설정이 완료되었습니다.', allowed_mentions=am)

@bot.command(name='content')
async def setcontent(ctx, *, name):
    if coll.find_one({"_id": str(name)}):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.reply(f'지금 {name} 광고의 내용을 입력해주세요.', allowed_mentions=am)
        msg = await bot.wait_for('message', check=check)
        msg = msg.content

        if os.path.isfile(f'./Ads/{name}.txt'):
            with open(f'./Ads/{name}.txt', 'a', encoding='UTF-8') as f:
                f.write(msg)
        else:
            if os.path.isdir('./Ads/'):
                with open(f'./Ads/{name}.txt', 'a,', encoding='UTF-8') as f:
                    f.write(msg)

            else:
                os.mkdir('./Ads/')
                with open(f'./Ads/{name}.txt', 'a,', encoding='UTF-8') as f:
                    f.write(msg)

        await ctx.reply('완료되었습니다.', allowed_mentions=am)


bot.run(os.getenv("TOKEN"))