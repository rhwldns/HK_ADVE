import discord
from discord.ext import commands
from discord.ext.commands import bot
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import asyncio
from EZPaginator import Paginator

coll = MongoClient('mongodb://localhost:27017/').HK_ADVE.ads

load_dotenv('.env')

bot = commands.Bot(command_prefix='.ad ', help_command=None)

am = discord.AllowedMentions.none()


@bot.event
async def on_ready():
    print(f'{bot.user} On Ready.')
    u = await bot.fetch_user(443734180816486441)
    while True:
        await asyncio.sleep(7)
        await bot.change_presence(status = discord.Status.online, activity = discord.Game(f"Made By {u}"))
        await asyncio.sleep(7)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(f".ad help"))


def check():
    async def predicate(ctx):
        with open('owners.txt', 'r', encoding='UTF-8') as f:
            line = f.readlines()

        if str(ctx.author.id) in line:
            return True
        else:
            return False
    return commands.check(predicate)


@bot.event
@check()
async def on_message(msg):
    if msg.content.startswith('.ad'):
        await bot.process_commands(msg)
        pass
    elif msg.author.bot:
        pass

    else:
        if os.path.isfile(f'./Messages/{str(msg.channel.id)}.txt'):
            pass
        else:
            open(f'./Messages/{str(msg.channel.id)}.txt', 'a').close()

        with open(f'./Messages/{str(msg.channel.id)}.txt', 'a', encoding="UTF-8") as f:
            a = f.readline()
            a += 1
            f.truncate(0)
            f.write(str(a))

        if coll.find_one({"channel1": str(msg.channel.id)}) or coll.find_one({"channel2": str(msg.channel.id)}):
            if coll.find_one({"channel1": str(msg.channel.id)}):
                data = coll.find_one({"channel1": str(msg.channel.id)})
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
                    await msg.channel.send(embed=embed)
                else:
                    pass

            elif coll.find_one({"channel2": str(msg.channel.id)}):
                data = coll.find_one({"channel1": str(msg.channel.id)})
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
                    await msg.channel.send(embed=embed)
                else:
                    pass


@bot.command(name='create')
@check()
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
@check()
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
@check()
async def set_time(ctx, *, name):
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
@check()
async def set_content(ctx, *, name):
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
@check()
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
@check()
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


@bot.command(name='help')
@check()
async def help_commands(ctx):

    embed = discord.Embed(
        title='HKAD 봇 도움말',
        description='',
        color=0x00FFFF
    )
    embed.add_field(
        name='광고를 적용하는 방법',
        value='1) `.ad create name` - name의 광고 생성\n'
              '2) `.ad frequency name 최소값 최대값` - name 광고 빈도 설정\n'
              '3) `.ad time name 노출회수` - name 광고 노출 수 설정\n'
              '4) `.ad content name` - name 광고 내용 설정\n'
              '5) `.ad expose-add name channel(Id)` - name 광고가 노출될 채널을 추가\n'
              '6) `.ad expose-sub name channel(Id)` - name 광고가 노출될 채널을 제거\n',
        inline=False
    )
    embed.add_field(
        name='부차적인 명령어',
        value='`.ad list` - 광고 목록 표시\n'
              '`.ad delete name` - name 광고 삭제\n'
              '`.ad detail name` - name 광고 정보 표시\n'
              '`.ad expose-list name` - name 광고가 노출되는 채널 목록 표시\n'
              '`.ad administrator-add @mention` - 해당 사람에게게 광고명령어 사용 권한 추가\n'
              '`.ad administrator-sub @mention` - 해당 사람에게 광고 명령어 사용 권한 제거'
    )


@bot.command(name='list')
async def ad_list(ctx):
    embeds = []
    file_list = os.listdir('./Ads/')
    file_list = [file for file in file_list if file.endswith(".txt")]

    for i in file_list:
        ii = i.replace('.txt', '')
        file_list.remove(i)
        file_list.append(ii)

    for i in file_list:
        with open(f'./Ads/{i}.txt', 'r', encoding='UTF-8') as f:
            lines = f.readlines()

        l = ''

        for i in lines:
            l += i
        embed = discord.Embed(
            title=f'{i}',
            description=f'{l}',
            color=0x00FFFF
        )

        embeds.append(embed)
    msg = await ctx.send(embed=embeds[0])
    await Paginator(
        bot=bot, message=msg, embeds=embeds, only=ctx.author
    ).start()


@bot.command(name='delete')
async def delete_ad(ctx, name: str):
    if coll.find_one({"_id": name}):
        coll.delete_one({"_id": name})
        await ctx.send(f'`{name}` 광고를 삭제했습니다.')
    else:
        await ctx.send('광고를 찾을 수 없습니다.')


bot.run(os.getenv("TOKEN"))