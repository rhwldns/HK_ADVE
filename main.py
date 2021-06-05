import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import asyncio
from EZPaginator import Paginator
import traceback

coll = MongoClient('mongodb://localhost:27017/').HK_ADVE.ads

load_dotenv('.env')

bot = commands.Bot(command_prefix='.ad ', help_command=None)

am = discord.AllowedMentions.none()


@bot.event
async def on_ready():
    print(f'{bot.user} On Ready.')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(f".ad help"))


def check():
    async def predicate(ctx):
        with open('owners.txt', 'r', encoding='UTF-8') as f:
            line = f.readlines()

        for i in line:
            ii = i.replace('\n', '')
            line.remove(i)
            line.append(ii)

        if str(ctx.author.id) in line:
            return True
        else:
            return False

    return commands.check(predicate)


@bot.event
@check()
async def on_message(msg):
    if msg.author.bot:  # 봇인지 확인
        return

    elif msg.content.startswith('.ad ') or '.ad' in msg.content:  # 커맨드 쓰는지 확인 후 return
        await bot.process_commands(msg)

        return

    else:
        for i in coll.find({}):
            i_channel = i['channel1']
            i_msg_channel_id = msg.channel.id
            i_channel2 = i['channel2']
            if int(i_channel) == int(i_msg_channel_id):
                find = {"_id": str(i['_id'])}
                set_data = {"$inc": {"count_chn1": 1}}
                coll.update_one(find, set_data)

                if int(i['least']) <= int(i['count_chn1']):
                    if int(i['count1']) >= int(i['count']):

                        continue

                    else:
                        with open(f'./Ads/{i["_id"]}.txt', 'r', encoding="UTF-8") as f:
                            ff = f.readlines()

                        asdf = ''
                        for iii in ff:
                            asdf += str(iii)
                        embed = discord.Embed(
                            title=f'{i["_id"]}',
                            description=f'{asdf}',
                            color=0x00FFFF
                        )
                        find = {"_id": str(i['_id'])}
                        set_data = {"$inc": {"count1": 1}}
                        coll.update_one(find, set_data)
                        chn = bot.get_channel(850312230742392852)
                        em = discord.Embed(
                            title='HK AD ㅣ Log',
                            description=f'`{await bot.fetch_channel(int(msg.channel.id))}`채널 - '
                                        f'`{str(i["_id"])}`광고 전송 완료',
                            color=0x00ff00
                        )
                        find = {"_id": str(i['_id'])}
                        set_data = {"$set": {"count_chn1": 0}}
                        coll.update_one(find, set_data)
                        await msg.channel.send(embed=embed)
                        await chn.send(embed=em)

                else:
                    continue

            elif int(i_channel2) == int(i_msg_channel_id):
                find = {"_id": str(i['_id'])}
                set_data = {"$inc": {"count_chn2": 1}}
                coll.update_one(find, set_data)

                if int(i['least']) >= int(i['count_chn2']):
                    if int(i['count1']) >= int(i['count']):
                        continue

                    else:
                        with open(f'./Ads/{i["_id"]}.txt', 'r', encoding="UTF-8") as f:
                            ff = f.readlines()

                        asdf = ''
                        for iii in ff:
                            asdf += str(iii)
                        embed = discord.Embed(
                            title=f'{i["_id"]}',
                            description=f'{asdf}',
                            color=0x00FFFF
                        )
                        find = {"_id": str(i['_id'])}
                        set_data = {"$inc": {"count1": 1}}
                        coll.update_one(find, set_data)
                        chn = bot.get_channel(850312230742392852)
                        em = discord.Embed(
                            title='HK AD ㅣ Log',
                            description=f'`{await bot.fetch_channel(int(msg.channel.id))}`채널 - '
                                        f'`{str(i["_id"])}`광고 전송 완료',
                            color=0x00ff00
                        )
                        find = {"_id": str(i['_id'])}
                        set_data = {"$set": {"count_chn2": 0}}
                        coll.update_one(find, set_data)
                        await msg.channel.send(embed=embed)
                        await chn.send(embed=em)

                else:
                    continue


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

    coll.insert_one(
        {
            "_id": str(content),
            "count1": 0,
            "least": None,
            "max": None,
            "count": 0,
            "channel1": None,
            "channel2": None,
            "count_chn1": 0,
            "count_chn2": 0
        }
    )
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
        def check1(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.reply(f'지금 등록할 채널 **`ID 아이디`**를 입력해주세요.', allowed_mentions=am)
        msg = await bot.wait_for('message', check=check1)
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
                msg = await bot.wait_for('message', check=check1)
                msg = msg.content

                find = {"_id": str(name)}
                setdata = {"$set": {'channel2': int(msg)}}
                coll.update_one(find, setdata)

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
        name='광고를 적용하는 방법',  # 1~6 완료
        value='1) `.ad create name` - name의 광고 생성\n'
              '2) `.ad frequency name 최소값 최대값` - name 광고 빈도 설정\n'
              '3) `.ad time name 노출회수` - name 광고 노출 수 설정\n'
              '4) `.ad content name` - name 광고 내용 설정\n'
              '5) `.ad expose-add name channel(Id)` - name 광고가 노출될 채널을 추가\n'
              '6) `.ad expose-sub name channel(Id)` - name 광고가 노출될 채널을 제거\n',
        inline=False
    )
    embed.add_field(
        name='부차적인 명령어',  # admin add 까지 완료
        value='`.ad list` - 광고 목록 표시\n'
              '`.ad delete name` - name 광고 삭제\n'
              '`.ad detail name` - name 광고 정보 표시\n'
              '`.ad administrator-add @mention` - 해당 사람에게게 광고명령어 사용 권한 추가\n'
              '`.ad administrator-sub @mention` - 해당 사람에게 광고 명령어 사용 권한 제거'
    )

    await ctx.send(embed=embed)


@bot.command(name='list')
async def ad_list(ctx):
    embeds = []
    file_list = os.listdir('./Ads/')
    file_list = [file for file in file_list if file.endswith(".txt")]
    l = ''
    for i in file_list:
        with open(f'./Ads/{i}', 'r', encoding='UTF-8') as f:
            lines = f.readlines()

        for ii in lines:
            l += ii

        ad_data = coll.find_one({"_id": str(i.replace(".txt", ""))})

        ad_least = ad_data['least']
        ad_max = ad_data['max']
        ad_count = ad_data['count']
        embed = discord.Embed(
            title=f'{i.replace(".txt", "")}',
            description=f'{l}\n\n최소 노출 수 : {ad_least}\n최대 노출 수 : {ad_max}\n현재 노출 횟수 : {ad_count}',
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


@bot.command(name='detail')
async def ad_detail(ctx, name: str):
    if coll.find_one({"_id": name}):
        ad_data = coll.find_one({"_id": name})
        least = ad_data['least']
        max = ad_data['max']
        channel1 = ad_data['channel1']
        channel2 = ad_data['channel2']
        embed = discord.Embed(
            title=f'{name} 광고 정보',
            description=f'광고 이름 : {name}\n최소 노출 수 : {least}, 최대 노출 수 : {max}\n\n'
                        f'등록된 채널 1 : <#{channel1}>\n등록된 채널 2 : {channel2}',
            color=0x00FFFF
        )
        await ctx.send(embed=embed)


@bot.command(name='administrator-add')
async def add_administrator(ctx, user: discord.Member):
    with open('owners.txt', 'a', encoding='UTF-8') as f:
        f.write(str(user.id) + '\n')
    await ctx.send(f'`{await bot.fetch_user(int(user.id))}`님에게 광고 명령어 사용 권한을 추가했습니다.')


@bot.command(name='administrator-sub')
async def add_administrator(ctx, user: discord.Member):
    with open("owners.txt", "r") as f:
        lines = f.readlines()

    with open("owners.txt", "w") as f:
        for line in lines:
            if line.strip("\n") != str(user.id):
                f.write(line)
    await ctx.send(f'`{await bot.fetch_user(int(user.id))}`님에게 광고 명령어 사용 권한을 제거했습니다.')


@bot.event
async def on_command_error(ctx, error):
    embed = discord.Embed(
        title=':warning: 에러',
        description=''.join(traceback.format_exception(type(error.__cause__), error.__cause__, error.__cause__.__traceback__ )),
        color=0xff0000
    )
    await ctx.send(embed=embed)
    chn = await bot.get_channel(850312230742392852)
    await chn.send('<@443734180816486441>')
    await chn.send(embed=embed)

bot.run(os.getenv("TOKEN"))
