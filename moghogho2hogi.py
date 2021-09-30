import discord, asyncio, random, re, time
from discord import message
from discord import channel
from discord.ext import commands
from discord.ext.commands import Bot
import os

client = discord.Client()

global tmp_msg
global tmp_index
tmp_msg = []
tmp_index = -1

o_msg_dic = {}
stone_dic = {}

#⭕ 변수


#실행 확인
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name="명령어!"))
    
class stone_data:
    def __init__(self):
        self.각인1 = ['◇','◇','◇','◇','◇','◇','◇','◇','◇','◇']
        self.각인2 = ['◇','◇','◇','◇','◇','◇','◇','◇','◇','◇']
        self.감소 = ['◇','◇','◇','◇','◇','◇','◇','◇','◇','◇']
        self.pass_or_fail = ''
        self.pbb_base = 75

    def set_stone_data(self, g1,g2,g3,pof,sm,pb):
        self.각인1 = g1
        self.각인2 = g2
        self.감소 = g3
        self.pass_or_fail = pof
        self.stone_msg = sm
        self.pbb_base = pb

    def set_stone_msg(self, sm):
        self.stone_msg = sm

    def stone_start(self,g):
        if '◇' not in g:
            return
        else:
            pbb_rand = random.randint(1,100)
            if(self.pbb_base > pbb_rand):
                self.pass_or_fail = '🔷'
                found_index = g.index('◇')
                g.remove('◇')
                g.insert(found_index,self.pass_or_fail)
                if self.pbb_base > 25:
                    self.pbb_base -= 10
            elif(self.pbb_base < pbb_rand):
                self.pass_or_fail = '◆'
                found_index = g.index('◇')
                g.remove('◇')
                g.insert(found_index,self.pass_or_fail)
                if self.pbb_base < 75:
                    self.pbb_base += 10


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('토끼'):
        global rabbit_msg
        rabbit_msg = await message.channel.send(f"/)/)\n('   ')/\n(     )")
        await rabbit_msg.add_reaction('👋')
        
    
    if message.content.startswith('졸려'):
        await message.channel.send(f'잘자요')
    if message.content.startswith('잠와'):
        await message.channel.send(f'잘자요')

    if message.content.startswith('$'):
        global o_msg_st
        o_msg_st = message
        print(f"{o_msg_st}")
        await o_msg_st.add_reaction('⭕')


    if message.content.startswith('강화!'):
        global user_item
        global rf_msg
        global rf_msg2
        global user_item_lv
        global rf_pbb
        global rf_user
        global rf_safe

        rf_user = message.author.id
        user_item = message.content[3:]
        rf_pbb = 90
        user_item_lv = 1
        rf_safe = 3

        if(user_item == ''):
            await message.channel.send(f'아이템 이름을 정해주세요. ex) 강화! 어떻게무기가하프')
        else:
            rf_msg = await message.channel.send(f'{user_item}+{user_item_lv}을(를) 강화합니다. 확률 {rf_pbb}%')
            rf_msg2 = await message.channel.send(f'8강 이상에서 👏을 누르시면 명예의템당에 등록됩니다.\n등록시 아이템은 +0이 됩니다.')
            await rf_msg.add_reaction('👍')
            await rf_msg.add_reaction('👏')
        

    #로아 돌깎기---------------
    if message.content.startswith('돌깎자!'):
        global add_user
        add_user = message.author.id

        pbb_base = 75
        pof = ''
        각인1 = ['◇','◇','◇','◇','◇','◇','◇','◇','◇','◇']
        각인2 = ['◇','◇','◇','◇','◇','◇','◇','◇','◇','◇']
        감소 = ['◇','◇','◇','◇','◇','◇','◇','◇','◇','◇']

        msg = await message.channel.send(f"★돌 시뮬★ \n 각인1☝️  : {각인1} \n 각인2✌️ : {각인2} \n 감소 👎  : {감소} \n 확률 : 75%")
        stone_dic[add_user] = stone_data()
        stone_dic[add_user].set_stone_msg(msg)
        await stone_dic[add_user].stone_msg.add_reaction('☝️')
        await stone_dic[add_user].stone_msg.add_reaction('✌️')
        await stone_dic[add_user].stone_msg.add_reaction('👎')

#가위바위보-----------------------------
    if message.content.startswith('가위바위보'):
        lsp_user = ''
        lsp_list=['가위','바위','보']
        lsp_client = random.choice(lsp_list)

        if message.content == '가위바위보 가위':
            lsp = '가위'
            if lsp_client == '가위':
                await message.channel.send(f'{lsp_client}! 당신은 비겼습니다.')
            if lsp_client == '바위':
                await message.channel.send(f'{lsp_client}! 당신은 졌습니다.')
            if lsp_client == '보':
                await message.channel.send(f'{lsp_client}! 당신은 이겼습니다.')
        if message.content == '가위바위보 바위':
            lsp = '바위'
            if lsp_client == '가위':
                await message.channel.send(f'{lsp_client}! 당신은 이겼습니다.')
            if lsp_client == '바위':
                await message.channel.send(f'{lsp_client}! 당신은 비겼습니다.')
            if lsp_client == '보':
                await message.channel.send(f'{lsp_client}! 당신은 졌습니다.')
        if message.content == '가위바위보 보':
            lsp = '보'
            if lsp_client == '가위':
                await message.channel.send(f'{lsp_client}! 당신은 졌습니다.')
            if lsp_client == '바위':
                await message.channel.send(f'{lsp_client}! 당신은 이겼습니다.')
            if lsp_client == '보':
                await message.channel.send(f'{lsp_client}! 당신은 비겼습니다.')

#'뭐먹' 응답
   
    if message.content.startswith('뭐먹'):
        food = ['치킨','피자','중식','초밥','떡볶이','햄버거','족발보쌈','갈비탕','돈까스','회','찜닭','삼겹살','편의점','컵라면','굶어','국밥','냉면','파스타','마라탕','']
        if message.content == '뭐먹리스트':
            await message.channel.send(f'{food}')
        else:
            choice_food = random.choice(food)
            await message.channel.send(f"2hogi's pick : ★{choice_food}★")

#로또 번호 
    if message.content.startswith('/lotto'):
        lotto_num = []
        while len(lotto_num) < 6:
            tmp_num = random.randint(1,45)
            if tmp_num not in lotto_num:
                lotto_num.append(tmp_num)
        lotto_num.sort()
        await message.channel.send(f"2hogi's pick : ★{lotto_num}★")
#'대답' 응답
    if message.content.startswith('대답'):
       await message.channel.send('ㅇㅅㅇ')

    if message.content.startswith('승'):
        if message.author.id == 268573021210542080:
           await message.channel.send(f'<@{message.author.id}>호!')

#'2호기' 응답 
    if message.content.startswith('2호기'):
       await message.channel.send('why?')
#'오늘도' 응답     
    if message.content.startswith('오늘도'):
        await message.channel.send('화이팅!')
#'니얼굴' 응답
    if message.content.startswith('니얼굴'):
         if message.author.id == 279906131017465857:
           await message.channel.send(f'<@{message.author.id}>쭈꾸미')
#'야' 응답
    if message.content.startswith('야'):
        user_msg = list(message.content)
        a = int(user_msg.count('야'))

        if a > 15:
            await message.channel.send(f'<@{message.author.id}>그만해')

        elif message.author.id == 279906131017465857:
            await message.channel.send(f'<@{message.author.id}>'+'뭐'*a)
            
            if message.author.dm_channel:
                await message.author.send(f'뭐'*a)
            elif message.author.dm_channel is None:
                channel = await message.author.create_dm()
                await channel.send('뭐'*a)            

        else:
            await message.channel.send('호'*a)
            
#'ㅋㅋㅋㅋ' 응답
    if message.content.startswith('ㅋㅋㅋㅋ'):
        if message.author.id == 279906131017465857:
            await message.channel.send(f'<@{message.author.id}>쪼개?')
        else:
            await message.channel.send('ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ')
#명령어 리스트 출력
    if message.content.startswith('명령어!'):
       await message.channel.send('명령어 list : 돌깎자!, 뭐먹, 대답, 2호기, 오늘도, 니얼굴, 야, ㅋㅋㅋㅋ, 가위바위보 ?, 강화!')



#로아 돌깎기---------------
@client.event
async def on_reaction_add(reaction, user):
    if user.bot == 1:
        global rf_pbb
        global user_item_lv
        global user_item
        user_item_lv = 1
        rf_pbb = 90
        return None
    if str(reaction.emoji) == "👍":
        if rf_user == user.id:
            pbb_rnd = random.randint(1, 100)
            if pbb_rnd < rf_pbb:
                user_item_lv+=1
                if(rf_pbb >10):
                    rf_pbb-=10
                elif(rf_pbb > 1):
                    rf_pbb-=1
                else:
                    pass
                await rf_msg2.edit(content=f'강화를 성공하였습니다! {user_item}+{user_item_lv-1} -> {user_item}+{user_item_lv}')
            elif pbb_rnd >= rf_pbb:
                if(pbb_rnd % 2 == 1 and user_item_lv < 10):
                    await rf_msg2.edit(content=f'강화를 실패하였습니다! 강화 단계는 유지됩니다! {user_item}+{user_item_lv} -> {user_item}+{user_item_lv}')
                else:
                    if(user_item_lv < 6):
                        tmp_lv = user_item_lv
                        user_item_lv-=1
                        rf_pbb +=10
                        await rf_msg2.edit(content=f'강화를 실패하였습니다! {user_item}+{tmp_lv} -> {user_item}+{user_item_lv}')
                    else:
                        tmp_lv = user_item_lv
                        user_item_lv = 0
                        rf_pbb = 100
                        await rf_msg2.edit(content=f'강화를 실패하였습니다! {user_item}+{tmp_lv} -> {user_item}+{user_item_lv}')
            else:
                print('error 강화 error 강화 error 강화')
            await rf_msg.edit(content=f'{user_item}+{user_item_lv}을(를) 강화합니다. 확률 : {rf_pbb}%')

    if str(reaction.emoji) == "👏":
        if rf_user == user.id:
            if user_item_lv > 7:
                await client.get_channel(890645163993624607).send(f'<@{rf_user}>님이 ★{user_item}+{user_item_lv}★을(를) 달성하였습니다!')
                tmp_lv = user_item_lv
                user_item_lv = 0
                rf_pbb = 100
                await rf_msg2.edit(content=f'★명예의템당에 {user_item}+{tmp_lv}(이)가 등록되었습니다.★\n{user_item}+{tmp_lv} -> {user_item}+{user_item_lv}')
            else:
                await rf_msg2.edit(content=f'+8 이상일때 눌러주세요. 현재 +{user_item_lv} 확률 : {rf_pbb}%')
                await client.get_channel(792887565589282827).send(f'<@{rf_user}>(이)가 말안듣고 8강 아래(+{user_item_lv} 따리)에서 👏을 눌렀어오')


        

#돌깎기 -----------------------------
    if str(reaction.emoji) == "☝️" or str(reaction.emoji) == "✌️" or str(reaction.emoji) == "👎":
        if str(reaction.emoji) == "☝️":
            stone_dic[user.id].stone_start(stone_dic[user.id].각인1)
        if str(reaction.emoji) == "✌️":
            stone_dic[user.id].stone_start(stone_dic[user.id].각인2)
        if str(reaction.emoji) == "👎":
            stone_dic[user.id].stone_start(stone_dic[user.id].감소)
           
        if len(stone_dic[user.id].각인1) + len(stone_dic[user.id].각인2) + len(stone_dic[user.id].감소) == 30:
            await stone_dic[user.id].stone_msg.edit(content=f"★돌 시뮬★ \n 각인1☝️  : {stone_dic[user.id].각인1} \n 각인2✌️ : {stone_dic[user.id].각인2} \n 감소 👎  : {stone_dic[user.id].감소} \n 확률 : {stone_dic[user.id].pbb_base}%")
        if (len(stone_dic[user.id].각인1) + len(stone_dic[user.id].각인2) + len(stone_dic[user.id].감소)) == 30 and '◇' not in stone_dic[user.id].각인1 and '◇' not in stone_dic[user.id].각인2 and '◇' not in stone_dic[user.id].감소:
            await stone_dic[user.id].stone_msg.edit(content=f"★돌 시뮬★ \n 각인1☝️  : {stone_dic[user.id].각인1} \n 각인2✌️ : {stone_dic[user.id].각인2} \n 감소 👎  : {stone_dic[user.id].감소} \n 확률 : {stone_dic[user.id].pbb_base}% \n {stone_dic[user.id].각인1.count('🔷')} {stone_dic[user.id].각인2.count('🔷')} {stone_dic[user.id].감소.count('🔷')} 돌입니다.")
            if stone_dic[user.id].각인1.count('🔷') + stone_dic[user.id].각인2.count('🔷') > 13:
                if stone_dic[user.id].각인1.count('🔷') == 8 and stone_dic[user.id].각인2.count('🔷') == 6:
                    pass
                elif stone_dic[user.id].각인1.count('🔷') == 6 and stone_dic[user.id].각인2.count('🔷') == 8:
                    pass
                else:
                    await client.get_channel(890618012883906590).send(f'<@{add_user}>님이 {stone_dic[user.id].각인1.count("🔷")} {stone_dic[user.id].각인2.count("🔷")} {stone_dic[user.id].감소.count("🔷")} 돌을 깎았습니다!')
                    stone_dic[user.id] = ''


#사용자 이모지 자동 제거
global o_msg

@client.event
async def on_raw_reaction_add(payload):
    channel = await client.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if str(payload.emoji) == '☝️' and payload.user_id != client.user.id and payload.user_id != 885419823499214859:
        await message.remove_reaction('☝️', payload.member)
    if str(payload.emoji) == '✌️' and payload.user_id != client.user.id and payload.user_id != 885419823499214859:
        await message.remove_reaction('✌️', payload.member)
    if str(payload.emoji) == '👎' and payload.user_id != client.user.id and payload.user_id != 885419823499214859:
        await message.remove_reaction('👎', payload.member)
    if str(payload.emoji) == '👍' and payload.user_id != client.user.id and payload.user_id != 885419823499214859:
        await message.remove_reaction('👍', payload.member)
    if str(payload.emoji) == '👏' and payload.user_id != client.user.id and payload.user_id != 885419823499214859:
        await message.remove_reaction('👏', payload.member)
    if str(payload.emoji) == '⭕' and payload.user_id != client.user.id and payload.user_id != 885419823499214859:
        o_msg = await client.get_channel(892220976228618270).send(f'<@{payload.user_id}> 참가! ({o_msg_st.content[1:]})')
        o_msg_dic[payload.user_id] = o_msg
    if str(payload.emoji) == '👋' and payload.user_id != client.user.id and payload.user_id != 885419823499214859:
        for i in range(1,3):
            await rabbit_msg.edit(content=f" /)/)\n('   ')ㅡ\n(     )")
            time.sleep(0.3)
            await rabbit_msg.edit(content=f" /)/)\n('   ')\\\n(     )")
            time.sleep(0.3)
            await rabbit_msg.edit(content=f" /)/)\n('   ')\n(     )")
            time.sleep(0.3)
            await rabbit_msg.edit(content=f" /)/)\n('   ')/\n(     )")
        await message.remove_reaction('👋', payload.member)

@client.event
async def on_raw_reaction_remove(payload): 
    try:
        if str(payload.emoji) == '⭕' and payload.user_id != client.user.id:
            await o_msg_dic[payload.user_id].delete()
    except KeyError as e:
            print(f'{e} : 에러에러에러')

access_token = os.environ['BOT_TOKEN']
client.run(access_token)
