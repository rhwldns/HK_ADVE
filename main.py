import discord
from discord.ext import commands
from discord.ext.commands import bot
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import asyncio

coll = MongoClient('mongodb://localhost:27017/').HK_ADVE.ads

load_dotenv('.env')

bot = commands.Bot(command_prefix='.ad ', help_command=None)

am = discord.AllowedMentions.none()


@bot.event
async def on_ready():
    print(f'{bot.user} On Ready.')
    u = await bot.fetch_user(443734180816486441)
    await bot.change_presence(status = discord.Status.online, activity = discord.Game(f"Made By {u}"))


@bot.event
async def on_message(ctx: commands.Context):
    with open(f'Messages/{str(ctx.channel.id)}.txt', 'a', encoding="UTF-8") as f:
        a = f.readline()
        a += 1
        f.seek()
        f.truncate(0)
        f.write(str(a))

    if coll.find_one({"channel1": str(ctx.channel.id)}) or coll.find_one({"channel2": str(ctx.channel.id)}):
        if coll.find_one({"channel1": str(ctx.channel.id)}):
            data = coll.find_one({"channel1": str(ctx.channel.id)})
            if int(data['least']) == int(a):
                with open(f'./Ads/{data["name"]}.txt', 'r+', encoding="UTF-8")as f:
                    des = f.readlines()
                    for i in des:
                        des += i
                embed = discord.Embed(
                    title=data['_id'],
                    description=str(des),
                    color=0x00FFFF
                )
                await ctx.channel.send(embed=embed)
            else:
                pass

        elif coll.find_one({"channel2": str(ctx.channel.id)}):
            data = coll.find_one({"channel1": str(ctx.channel.id)})
            if int(data['least']) == int(a):
                with open(f'./Ads/{data["name"]}.txt', 'r+', encoding="UTF-8")as f:
                    des = f.readlines()
                    for i in des:
                        des += i
                embed = discord.Embed(
                    title=data['_id'],
                    description=str(des),
                    color=0x00FFFF
                )
                await ctx.channel.send(embed=embed)
            else:
                pass


@bot.command(name='create')
async def create_ad(ctx, *, content):
    if os.path.isdir('./Ads/'):
        with open(f'./Ads/{content}.txt', 'a', encoding='UTF-8') as f:
            f.write('1')
            f.seek(0)
            f.truncate()

    else:
        os.mkdir('./Ads/')
        with open(f'./Ads/{content}.txt', 'a,', encoding='UTF-8') as f:
            f.write('1')
            f.seek(0)
            f.truncate()

    coll.insert_one({"_id": str(content), "least": None, "max": None, "count": 0, "channel1": None, "channel2": None})
    return await ctx.reply('광고 등록이 완료되었습니다.', allowed_mentions=am)


@bot.command(name='frequency')
async def set_frequency(ctx, *, name):
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

    else:
        await ctx.reply(f'`{name}` 이라는 광고를 찾을 수 없습니다.', allowed_mentions=am)


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

    else:
        await ctx.reply(f'`{name}` 이라는 광고를 찾을 수 없습니다.', allowed_mentions=am)


@bot.command(name='expose-add')
async def add_expose(ctx, *, name):
    if coll.find_one({"_id": str(name)}):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.reply(f'지금 등록할 채널 **`ID 아이디`**를 입력해주세요.', allowed_mentions=am)
        msg = await bot.wait_for('message', check=check)
        msg = msg.content

        find = {"_id": str(name)}
        setdata = {"$set": {'channel1': int(msg)}}
        coll.update_one(find, setdata)

        a = await ctx.send('만약 채널을 하나 더 추가하고 싶은 경우에는 아래 :white_check_mark: 이모지를 눌러주세요.\n시간 제한 : 10초')
        await a.add_reaction('✅')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '✅'

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=10, check=check)

            if str(reaction.emoji) == '✅':
                await ctx.reply(f'지금 등록할 2번째 채널 **`ID 아이디`**를 입력해주세요.', allowed_mentions=am)
                msg = await bot.wait_for('message', check=check)
                msg = msg.content

                find = {"_id": str(name)}
                setdata = {"$set": {'channel2': int(msg)}}
                coll.update_one(find, setdata)
                await ctx.send('완료되었습니다.')

            else:
                await ctx.send('채널 추가 중단, 첫 번째 채널만 등록했습니다.')
        except asyncio.TimeoutError:
            await ctx.send('시간이 초과되었습니다.')

        await ctx.reply('등록이 완료되었습니다!', allowed_mentions=am)


@bot.command(name='expose-sub')
async def sub_expose(ctx, *, name):
    if coll.find_one({"_id": str(name)}):

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['✅', '⭕']

        await ctx.reply(f'첫 번째 채널을 삭제하시려면 :white_check_mark: 를,'
                        f'\n두 번째 채널을 삭제하시려면 :o: 를 눌러주세요.', allowed_mentions=am)

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=10, check=check)

            if str(reaction.emoji) == '✅':
                find = {"_id": str(name)}
                setdata = {"$set": {'channel1': None}}
                coll.update_one(find, setdata)

                await ctx.send('첫 번째 채널 삭제를 완료했습니다.')
            else:
                find = {"_id": str(name)}
                setdata = {"$set": {'channel2': None}}
                coll.update_one(find, setdata)

                await ctx.send('두 번째 채널 삭제를 완료했습니다.')

        except asyncio.TimeoutError:
            await ctx.send('시간이 초과되었습니다.')


bot.run(os.getenv("TOKEN"))