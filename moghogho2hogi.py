import discord, asyncio, random, re, time, os, bs4, urllib, requests, re
from discord import message
from discord import channel
from discord.ext import commands
from discord.ext.commands import Bot

client = discord.Client()

global tmp_msg
global tmp_index
tmp_msg = []
tmp_index = -1

o_msg_dic = {}
stone_dic = {}

#⭕ 변수
global o_dic
o_dic = {}

#음식
global food
food = ['치킨','피자','중식','초밥','떡볶이','햄버거','족발보쌈','갈비탕','돈까스','회','찜닭','삼겹살','편의점','컵라면','굶어','국밥','냉면','파스타','마라탕']

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
class party:
    def __init__(self, mm):
        self.main_msg = mm
        self.msg_dic = {}
        
    def set_data(self, uid, om):
        self.msg_dic[uid] = om 
        
@client.event
async def on_message(message):
    if message.author == client.user:
        return
            
    if message.content.startswith('검색! '):
        nickname_ori = message.content[4:]
        nickname = urllib.parse.quote(nickname_ori)
        
        url = f'https://lostark.game.onstove.com/Profile/Character/{nickname}'
        response = requests.get(url)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        #전투정보실 체크
        check = soup.find('div',{'class':'info'})
        if check != None:
            await message.channel.send(f'로스트아크 전투정보실 점검 중 입니다.')
        else:
            user_search = soup.body.find('div', {"class":"profile-attention"})
            jewel_count = 0
            if user_search != None:
                await message.channel.send(f'({nickname_ori})캐릭터 정보가 없습니다. 캐릭터명을 확인해주세요.')
            else:
                #전투레벨
                user_lv = soup.find('div',{'class':'level-info__item'}).get_text()[8:]

                #아이템레벨
                item_lv = soup.find('div',{"class":"level-info2__item"}).get_text()
                item_lv = item_lv[12:]
                #각인
                user_ability = soup.main.find("div",{'class':'swiper-wrapper'})
                if user_ability == None:
                    pass
                else:
                    user_ability = user_ability.get_text()
                    p_ability = re.compile('.+Lv. +.')
                    user_ability = p_ability.findall(user_ability)
                    user_ability = "\n".join(user_ability)
                #보석
                user_jewel_list = []
                p_jewel = re.compile('Lv.+')
                
                for i in range(0, 11):
                    try:
                        if i == 10:
                            user_jewel = soup.main.find('span',{'id':f'gem{i}'}).get_text()
                        else:
                            user_jewel = soup.main.find('span',{'id':f'gem0{i}'}).get_text()
                        if user_jewel == None:
                            break
                        user_jewel = "".join(p_jewel.findall(user_jewel))
                        user_jewel_list.append(user_jewel)
                    except AttributeError as ex: 
                        jewel_count += 1
                user_jewel_list = " ".join(user_jewel_list)
                user_jewel_list = user_jewel_list.replace('Lv.','')

                #원정대랩
                user_expedition = soup.main.find("div",{"class":"level-info__expedition"}).get_text()
                user_expedition = user_expedition[9:]
                
                #특성
                p_character = re.compile('특화 .\d{2,3}|신속 .\d{2,3}|치명 .\d{2,3}')
                user_character = soup.main.find('div', {'class':'profile-ability-battle'})
                if user_ability == None:
                    user_character = None
                else:
                    user_character = user_character.get_text()
                    user_character = p_character.findall(user_character)
                    user_character = " ".join(user_character)

                #출력
                embed = discord.Embed(title=f"{nickname_ori}", color=0x62c1cc)
                embed.add_field(name = "전투 레벨", value = f"{user_lv}", inline=True)
                embed.add_field(name = "아이템 레벨", value = f"{item_lv}", inline=True)
                embed.add_field(name = "원정대 레벨", value = f"{user_expedition}", inline=True)
                embed.add_field(name = "각인", value = f"{user_ability}", inline=True)
                if jewel_count != 0:
                    embed.add_field(name = "보석", value = f"※보석{jewel_count}개 없음※\n{user_jewel_list}", inline=True)
                else:
                    embed.add_field(name = "보석", value = f"{user_jewel_list}", inline=True)
                embed.add_field(name = "특성", value = f"{user_character}", inline=True)
                await message.channel.send(embed=embed)
                
    if message.content.startswith('빠삐는'):
        await message.channel.send(f'사람을 찢어...!')    
    
    if message.content.startswith('토끼'):
        global rabbit_msg
        rabbit_msg = await message.channel.send(f"/)/)\n('   ')/\n(     )")
        await rabbit_msg.add_reaction('👋')
        await rabbit_msg.add_reaction('😆')
        
    if message.content.startswith('졸려'):
        await message.channel.send(f'잘자요')
    if message.content.startswith('잠와'):
        await message.channel.send(f'잘자요')

    if message.content.startswith('$'):
        o_dic[message.id] = party(message)
        await message.add_reaction('⭕')

            
#'뭐먹' 응답
# food = ['치킨','피자','중식','초밥','떡볶이','햄버거','족발보쌈','갈비탕','돈까스','회','찜닭','삼겹살','편의점','컵라면','굶어','국밥','냉면','파스타','마라탕']
    if message.content.startswith('뭐먹'):
        if message.content.endswith(' 추가'):
            try:
                food.index(message.content[3:-3])
                await message.channel.send(f'이미 존재하는 음식입니다.({message.content[3:-3]})')
            except ValueError as ex:
                food.append(message.content[3:-3])
                await message.channel.send(f'{message.content[3:-3]}(이)가 추가되었습니다.') 
                
        elif message.content.endswith(' 삭제'):
            try:
                food.remove(message.content[3:-3])
                await message.channel.send(f'{message.content[3:-3]}(이)가 삭제되었습니다.')
            except ValueError as ex:
                await message.channel.send(f'{message.content[3:-3]}(이)가 리스트에 존재하지 않습니다.')
        elif message.content == '뭐먹리스트':
            await message.channel.send(f'{food}')
        else:
            choice_food = random.choice(food)
            await message.channel.send(f"2hogi's pick : ★{choice_food}★")
            
            
#가위바위보----------------------------
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
        await message.channel.send('파이팅!')
        
#'행복하세요?' 응답
    if message.content.startswith('행복하세요?'):
        await message.channel.send('행복하세요~')
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
    if message.content.startswith('ㅋ') or message.content.endswith('ㅋ'):
        p_zz = re.compile('ㅋㅋㅋㅋ')
        m_zz = p_zz.search(message.content)
        if m_zz != None:
            if message.author.id == 279906131017465857:
                await message.channel.send(f'<@{message.author.id}>쪼개?')
            else:
                await message.channel.send('ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ')
        else:
            pass
        
    if message.content.startswith('돌깎자!'):
        global add_user
        add_user = message.author.id
        pbb_base = 75
        pof = ''
        각인1 = ['◇','◇','◇','◇','◇','◇','◇','◇','◇','◇']
        각인2 = ['◇','◇','◇','◇','◇','◇','◇','◇','◇','◇']
        감소 = ['◇','◇','◇','◇','◇','◇','◇','◇','◇','◇']

        msg = await message.channel.send(f'★돌 시뮬★ <@{add_user}>(이)가 깎는중!\n각인1☝️  : {각인1} \n 각인2✌️ : {각인2} \n 감소 👎  : {감소} \n 확률 : 75%')
        
        stone_dic[add_user] = stone_data()
        stone_dic[add_user].set_stone_msg(msg)
        await stone_dic[add_user].stone_msg.add_reaction('☝️')
        await stone_dic[add_user].stone_msg.add_reaction('✌️')
        await stone_dic[add_user].stone_msg.add_reaction('👎')
        
@client.event
async def on_reaction_add(reaction, user):
    if user.bot == 1:
        global rf_pbb
        global user_item_lv
        global user_item
        user_item_lv = 1
        rf_pbb = 90
        return None
    
#돌깎기 -----------------------------
    if str(reaction.emoji) == "☝️" or str(reaction.emoji) == "✌️" or str(reaction.emoji) == "👎":
        if str(reaction.emoji) == "☝️":
            stone_dic[user.id].stone_start(stone_dic[user.id].각인1)
        if str(reaction.emoji) == "✌️":
            stone_dic[user.id].stone_start(stone_dic[user.id].각인2)
        if str(reaction.emoji) == "👎":
            stone_dic[user.id].stone_start(stone_dic[user.id].감소)
           
        if len(stone_dic[user.id].각인1) + len(stone_dic[user.id].각인2) + len(stone_dic[user.id].감소) == 30:
            await stone_dic[user.id].stone_msg.edit(content=f"★돌 시뮬★ <@{add_user}>(이)가 깎는중!\n 각인1☝️  : {stone_dic[user.id].각인1} \n 각인2✌️ : {stone_dic[user.id].각인2} \n 감소 👎  : {stone_dic[user.id].감소} \n 확률 : {stone_dic[user.id].pbb_base}%")
        if (len(stone_dic[user.id].각인1) + len(stone_dic[user.id].각인2) + len(stone_dic[user.id].감소)) == 30 and '◇' not in stone_dic[user.id].각인1 and '◇' not in stone_dic[user.id].각인2 and '◇' not in stone_dic[user.id].감소:
            await stone_dic[user.id].stone_msg.edit(content=f"★돌 시뮬★ <@{add_user}>(이)가 깎음!\n 각인1☝️  : {stone_dic[user.id].각인1} \n 각인2✌️ : {stone_dic[user.id].각인2} \n 감소 👎  : {stone_dic[user.id].감소} \n 확률 : {stone_dic[user.id].pbb_base}% \n {stone_dic[user.id].각인1.count('🔷')} {stone_dic[user.id].각인2.count('🔷')} {stone_dic[user.id].감소.count('🔷')} 돌입니다.")
            if stone_dic[user.id].각인1.count('🔷') + stone_dic[user.id].각인2.count('🔷') > 13:
                if stone_dic[user.id].각인1.count('🔷') == 8 and stone_dic[user.id].각인2.count('🔷') == 6:
                    pass
                elif stone_dic[user.id].각인1.count('🔷') == 6 and stone_dic[user.id].각인2.count('🔷') == 8:
                    pass
                else:
                    await client.get_channel(890618012883906590).send(f'<@{user.id}>님이 {stone_dic[user.id].각인1.count("🔷")} {stone_dic[user.id].각인2.count("🔷")} {stone_dic[user.id].감소.count("🔷")} 돌을 깎았습니다!')
                    stone_dic[user.id] = ''
        
#사용자 이모지 자동 제거
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
        o_msg = await client.get_channel(892220976228618270).send(f'<@{payload.user_id}> 참가! ({o_dic[payload.message_id].main_msg.content[1:]})')
        o_dic[payload.message_id].set_data(payload.user_id, o_msg)
    if str(payload.emoji) == '👋' and payload.user_id != client.user.id and payload.user_id != 885419823499214859:
        for i in range(1,3):
            time.sleep(0.3)
            await rabbit_msg.edit(content=f" /)/)\n('   ')ㅡ\n(     )")
            time.sleep(0.3)
            await rabbit_msg.edit(content=f" /)/)\n('   ')\\\n(     )")
            time.sleep(0.3)
            await rabbit_msg.edit(content=f" /)/)\n('   ')ㅡ\n(     )")
            time.sleep(0.3)
            await rabbit_msg.edit(content=f" /)/)\n('   ')/\n(     )")
        await message.remove_reaction('👋', payload.member)
    if str(payload.emoji) == '😆' and payload.user_id != client.user.id and payload.user_id != 885419823499214859:
        await rabbit_msg.edit(content=f" /)/)\n(> <)/\n(     )")
        time.sleep(2)
        await rabbit_msg.edit(content=f"/)/)\n('   ')/\n(     )")
        await message.remove_reaction('😆', payload.member)
        
@client.event
async def on_raw_reaction_remove(payload): 
    try:
        if str(payload.emoji) == '⭕' and payload.user_id != client.user.id:
            await o_dic[payload.message_id].msg_dic[payload.user_id].delete()
    except KeyError as e:
            pass 
        
access_token = os.environ['BOT_TOKEN']
client.run(access_token)
