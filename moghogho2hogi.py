from dis import disco
import discord, asyncio, random, re, time, os, bs4, urllib, requests, re, pymysql
from discord import message
from discord import channel
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext import tasks
from datetime import datetime

intents = discord.Intents.default()
client = discord.Client(intents=intents)
passwd_token = os.environ['PASSWD_TOKEN']

global tmp_msg
global tmp_index
tmp_msg = []
tmp_index = -1

o_msg_dic = {}
stone_dic = {}

#레이드 dic
global raid_dic
raid_dic = {}

#raid class
class raid:
    def __init__(self, rl, rn, cc):
        self.r_list = rl
        self.r_name = rn
        self.c_count = cc
        self.lv_avg = 0
        
    def set_raid(self, rl, rn ,cc):
        self.r_list = rl
        self.r_name = rn
        self.c_count = cc

    def check_a(self, n):
        tmp_server_msg = '' #메시지
        nickname_ori = n
        nickname = urllib.parse.quote(nickname_ori)
        
        url = f'https://lostark.game.onstove.com/Profile/Character/{nickname}'
        response = requests.get(url)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        #전투정보실 체크
        check = soup.find('div',{'class':'info'})
        if check != None:
            tmp_server_msg = f'로스트아크 전투정보실 점검 중 입니다.'
            return False
        else:
            user_search = soup.body.find('div', {"class":"profile-attention"})
            if user_search != None:
                tmp_server_msg = (f'({nickname_ori})캐릭터 정보가 없습니다. 캐릭터명을 확인해주세요.')
                return False
        return True 

#음식
global food
food = ['치킨','피자','중식','초밥','떡볶이','햄버거','족발보쌈','갈비탕','돈까스','회','찜닭','삼겹살','편의점','컵라면','굶어','국밥','냉면','파스타','마라탕']

#수상한큐브
cube_susang_prob = {
    '레어' : {
        'first' : {
            17544 : ['공격력 : +3%', '마력 : +3%', '크리티컬 확률 : +4%','데미지 : +3%','몬스터 방어율 무시 : +15%'],
            52632 : ['STR : +12','DEX : +12','INT : +12','LUK : +12','공격력 : +12','마력 : +12','STR : +3%','DEX : +3%','INT : +3%','LUK : +3%','올스탯 : +5'],
            105264 : ['최대 HP : +120','최대 MP : +120','공격 시 3% 확률로 32의 HP 회복','공격 시 3% 확률로 32의 MP 회복','공격 시 10% 확률로 6레벨 중독효과 적용','공격 시 5% 확률로 2레벨 기절효과 적용','공격 시 10% 확률로 2레벨 슬로우효과 적용','공격 시 10% 확률로 3레벨 암흑효과 적용','공격 시 5% 확률로 2레벨 빙결효과 적용','격 시 5% 확률로 2레벨 봉인효과 적용']
        },
        'second' : {
            18 : ['공격력 : +3%	','마력 : +3%','크리티컬 확률 : +4%','데미지 : +3%','몬스터 방어율 무시 : +15%'],
            53 : ['STR : +12','DEX : +12','INT : +12','LUK : +12','공격력 : +12','마력 : +12','STR : +3%','DEX : +3%','INT : +3%','LUK : +3%','올스탯 : +5'],
            106 : ['최대 HP : +120','최대 MP : +120','공격 시 3% 확률로 32의 HP 회복','공격 시 3% 확률로 32의 MP 회복','공격 시 10% 확률로 6레벨 중독효과 적용','공격 시 5% 확률로 2레벨 기절효과 적용','공격 시 10% 확률로 2레벨 슬로우효과 적용','공격 시 10% 확률로 3레벨 암흑효과 적용','공격 시 5% 확률로 2레벨 빙결효과 적용','공격 시 5% 확률로 2레벨 봉인효과 적용'],
            62544 : ['공격력 : +6','마력 : +6'],
            187419 : ['STR : +6','DEX : +6','INT : +6','LUK : +6'],
            374732 : ['최대 HP : +60','최대 MP : +60']
        },
        'third' : {
            18 : ['공격력 : +3%	','마력 : +3%','크리티컬 확률 : +4%','데미지 : +3%','몬스터 방어율 무시 : +15%'],
            53 : ['STR : +12','DEX : +12','INT : +12','LUK : +12','공격력 : +12','마력 : +12','STR : +3%','DEX : +3%','INT : +3%','LUK : +3%','올스탯 : +5'],
            106 : ['최대 HP : +120','최대 MP : +120','공격 시 3% 확률로 32의 HP 회복','공격 시 3% 확률로 32의 MP 회복','공격 시 10% 확률로 6레벨 중독효과 적용','공격 시 5% 확률로 2레벨 기절효과 적용','공격 시 10% 확률로 2레벨 슬로우효과 적용','공격 시 10% 확률로 3레벨 암흑효과 적용','공격 시 5% 확률로 2레벨 빙결효과 적용','공격 시 5% 확률로 2레벨 봉인효과 적용'],
            62544 : ['공격력 : +6','마력 : +6'],
            187419 : ['STR : +6','DEX : +6','INT : +6','LUK : +6'],
            374732 : ['최대 HP : +60','최대 MP : +60']
        }
    },
    '에픽' : {
        'first':{
            
        },
        'second':{
    
        },
        'third':{
    
        }
    }
}


#실행 확인
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name="명령어!"))
    stock_loop.start()
    
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

#@tasks.loop(seconds=60)
#async def stock_loop():
#    if datetime.now().hour == 23 and datetime.now().minute == 30:
#        conn_lt_init = pymysql.connect(
#        user = 'jonsu0129',
#        password = passwd_token,
#        host = 'discord-database-kr.cqops5vysvnr.ap-northeast-2.rds.amazonaws.com',
#        db = 'testDB',
#        charset = 'utf8'
#        )
#        cur_lt_init = conn_lt_init.cursor()
#        sql_lt_init = "update userTable set ltcount = 3"
#            
#        cur_lt_init.execute(sql_lt_init)
#        conn_lt_init.commit()
#        conn_lt_init.close()
#        await client.get_channel(792887565589282827).send(f'복권이 3개로 초기화됐습니다.')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('강화명령어!'):
        weapon_help = discord.Embed(title=f"강화명령어!", color=0x62c1cc)
        weapon_help.add_field(name = "※이용방법※", value = f'무기등록 후 알맞은 명령어를 입력하세요', inline = False)
        weapon_help.add_field(name = "🔴무기등록! 무기종류 무기이름", value = f'무기를 등록합니다. 무기종류: 한손검 (추가예정)', inline = False)
        weapon_help.add_field(name = "🟡무기이름변경! 무기이름", value = f'유저의 무기의 이름을 (무기이름)으로 변경합니다.', inline = False)
        weapon_help.add_field(name = "🟢무기정보! 무기이름", value = f'(무기이름)을 가진 무기의 정보를 보여줍니다.', inline = False)
        weapon_help.add_field(name = "🔵무기잠재! 큐브이름", value = f'(큐브이름)으로 무기의 잠재능력 옵션을 재설정합니다. (큐브 종류: 수상한큐브) ※beta', inline = False)
        weapon_help.add_field(name = "🔵무기강화!", value = f'무기를 강화합니다. (확률은 메이플스토리 스타포스 강화 확률과 같습니다.) ※beta', inline = False)
        await message.channel.send(embed=weapon_help)

    if message.content.startswith('무기등록! '):
        await message.channel.send(f'정지된 기능입니다...')
        weapon_type = message.content.split()[1]
        weapon_name = message.content.split()[2]
        
        conn_weapon = pymysql.connect(
            user = 'jonsu0129',
            password = passwd_token,
            host = 'discord-database-kr.cqops5vysvnr.ap-northeast-2.rds.amazonaws.com',
            db = 'testDB',
            charset = 'utf8'
        )

        cur_weapon_exist_samename = conn_weapon.cursor()
        cur_weapon_exist_samename_sql = "select * from testDB.weaponTable where weapon_name = %s"

        cur_weapon_exist_samename.execute(cur_weapon_exist_samename_sql,{weapon_name})
        cur_weapon_exist_samename = cur_weapon_exist_samename.fetchall()
        print(f'{cur_weapon_exist_samename}')
        
        if cur_weapon_exist_samename != ():
            await message.channel.send(f'<@{message.author.id}> 같은 이름의 무기가 존재합니다. ({weapon_name})')
        else:
            cur_weapon_exist = conn_weapon.cursor()
            cur_weapon_exist_sql = "select * from testDB.weaponTable where userId = %s"
            cur_weapon_exist.execute(cur_weapon_exist_sql,message.author.id)
            cur_weapon_exist = cur_weapon_exist.fetchall()
            # print(f'{cur_weapon_exist}')
            if cur_weapon_exist == ():
                if weapon_type == "한손검":
                    cur_weapon = conn_weapon.cursor()
                    cur_weapon.execute(f"insert into weaponTable VALUES('{weapon_name}','{weapon_type}',150,150,0,0,0,0,326,0,30,20,0,'레어',0,0,0,0,{message.author.id})")

                    cur_weapon_sql = "update `testDB`.`userTable` set weapon_name = %s where userId = %s"
                    cur_weapon.execute(cur_weapon_sql, ({weapon_name}, {message.author.id}))
                    conn_weapon.commit()
                    conn_weapon.close()
                    await message.channel.send(f'<@{message.author.id}>님이 {weapon_name}({weapon_type})(을)를 등록하였습니다. (무기정보! 무기이름)')
            else:
                await message.channel.send(f'<@{message.author.id}>님은 이미 무기가 존재합니다! 무기 이름: {cur_weapon_exist[0][0]}')

    if message.content.startswith('무기이름변경! '):
        await message.channel.send(f'정지된 기능입니다...')
        weapon_name_new = message.content.split()[1]
        conn_weapon_change = pymysql.connect(
            user = 'jonsu0129',
            password = passwd_token,
            host = 'discord-database-kr.cqops5vysvnr.ap-northeast-2.rds.amazonaws.com',
            db = 'testDB',
            charset = 'utf8'
        )
        cur_weapon_change_exist_samename = conn_weapon_change.cursor()
        cur_weapon_change_exist_samename_sql = "select * from testDB.weaponTable where weapon_name = %s"

        cur_weapon_change_exist_samename.execute(cur_weapon_change_exist_samename_sql,{weapon_name_new})
        cur_weapon_change_exist_samename = cur_weapon_change_exist_samename.fetchall()

        if cur_weapon_change_exist_samename != ():
            await message.channel.send(f'<@{message.author.id}> 같은 이름의 무기가 존재합니다. ({weapon_name_new})')
        else:
            cur_weapon_change = conn_weapon_change.cursor()
            sql_weapon_change_1 = "update `testDB`.`userTable` set weapon_name = %s where userId = %s"
            sql_weapon_change_2 = "update `testDB`.`weaponTable` set weapon_name = %s where userId = %s"
            cur_weapon_change.execute(sql_weapon_change_1,({weapon_name_new},{message.author.id}))

            cur_weapon_change.execute(sql_weapon_change_2,({weapon_name_new},{message.author.id}))
            await message.channel.send(f'<@{message.author.id}>님이 {weapon_name_new}로 무기 이름을 변경하였습니다.')
            conn_weapon_change.commit()
            conn_weapon_change.close()

    if message.content.startswith('무기정보! '):
        await message.channel.send(f'정지된 기능입니다...')
        info_weapon_name = message.content.split()[1]
        conn_weapon_info = pymysql.connect(
            user = 'jonsu0129',
            password = passwd_token,
            host = 'discord-database-kr.cqops5vysvnr.ap-northeast-2.rds.amazonaws.com',
            db = 'testDB',
            charset = 'utf8'
        )
        cur_weapon_info = conn_weapon_info.cursor()
        sql_weapon_info = 'select * from weaponTable where weapon_name = %s'
        cur_weapon_info.execute(sql_weapon_info, {info_weapon_name})
        cur_weapon_info = cur_weapon_info.fetchall()

        if cur_weapon_info == ():
            await message.channel.send(f'<@{message.author.id}> 무기가 존재하지 않습니다. ({info_weapon_name})')
        else:
            cur_weapon_info_user = conn_weapon_info.cursor()
            sql_weapon_info_user = 'select userName from userTable where weapon_name = %s'
            cur_weapon_info_user.execute(sql_weapon_info_user,{info_weapon_name})
            cur_weapon_info_user = cur_weapon_info_user.fetchall()[0][0]
            weapon_info_list = ["무기 종류", "STR", "DEX", "INT", "LUK","최대 HP", "최대 MP", "공격력", "마력", "보스 몬스터 공격 시 데미지", "몬스터 방어율 무시", "올스탯", "잠재등급", "잠재옵션1","잠재옵션2","잠재옵션3"]
            weapon_info_star = ""
            for i in range(1, cur_weapon_info[0][17]+1):
                weapon_info_star += "★"
                if i%5 == 0:
                    weapon_info_star += "   "
                if i % 15 == 0:
                    weapon_info_star += "\n"
                    for j in range(0,13):
                        weapon_info_star += " "
            for i in range(cur_weapon_info[0][17]+1, 26):
                weapon_info_star += "☆"
                if i%5 == 0:
                    weapon_info_star += "   "
                if i % 15 == 0:
                    weapon_info_star += "\n"
                    for j in range(0,13):
                        weapon_info_star += " "

            weapon_info = discord.Embed(title=f"{weapon_info_star}\n{cur_weapon_info_user}의 {cur_weapon_info[0][0]}", color=0x62c1cc)
            for i in range(0,16):
                if cur_weapon_info[0][i+1] == 0 or cur_weapon_info[0][i+1] == "0":
                    pass
                else:
                    if i == 9 or i == 10 or i == 11:
                        weapon_info.add_field(name = f"{weapon_info_list[i]}", value = f'{cur_weapon_info[0][i+1]}%', inline = True)
                    elif i == 13 or i == 14 or i== 15:
                        weapon_info.add_field(name = f"{weapon_info_list[i]}", value = f'{cur_weapon_info[0][i+1]}', inline = False)
                    else:
                        weapon_info.add_field(name = f"{weapon_info_list[i]}", value = f'{cur_weapon_info[0][i+1]}', inline = True)
            await message.channel.send(embed=weapon_info)
            
    if message.content.startswith('무기잠재! '):
        await message.channel.send(f'정지된 기능입니다...')
        cube = message.content.split()[1]
        if(cube == "수상한큐브"):
            conn_cube_susang = pymysql.connect(
            user = 'jonsu0129',
            password = passwd_token,
            host = 'discord-database-kr.cqops5vysvnr.ap-northeast-2.rds.amazonaws.com',
            db = 'testDB',
            charset = 'utf8'
            )
            cur_cube_susang = conn_cube_susang.cursor()
            sql_cube_susang = "select 잠재등급 from weaponTable where userId = %s"

            cur_cube_susang.execute(sql_cube_susang, {message.author.id})
            cur_cube_susang = cur_cube_susang.fetchall()[0][0]
            if(cur_cube_susang == "유니크" or cur_cube_susang == "레전더리"):
                await message.channel.send(f"<@{message.author.id}> 에픽 등급 이하의 장비에만 사용할 수 있습니다. 현재 등급: {cur_cube_susang}")
            elif(cur_cube_susang == "레어"):
                r1 = random.randint(0, 105265)
                r2 = random.randint(0, 374733)
                r3 = random.randint(0,374733)
                print(f'{r1}, {r2}, {r3}')
                if(r1 <= 17544): r1 = 17544
                elif(r1 <= 52632): r1= 52632
                elif(r1<= 105264): r1 = 105264
                if(r2 <= 18) : r2 =18
                elif(r2 <= 53) : r2 =53
                elif(r2 <= 106) : r2 = 106
                elif(r2 <= 62544) : r2 = 62544
                elif(r2 <= 187419) : r2 = 187419
                elif(r2 <= 374732) : r2 = 374732
                if(r3 <= 18) : r3 =18
                elif(r3 <= 53) : r3 =53
                elif(r3 <= 106) : r3 = 106
                elif(r3 <= 62544) : r3 = 62544
                elif(r3 <= 187419) : r3 = 187419
                elif(r3 <= 374732) : r3 = 374732
                susang_rare_1 = random.choice(cube_susang_prob[f'{cur_cube_susang}']['first'][r1])
                susang_rare_2 = random.choice(cube_susang_prob[f'{cur_cube_susang}']['second'][r2])
                susang_rare_3 = random.choice(cube_susang_prob[f'{cur_cube_susang}']['third'][r3])
                # print(f'{susang_rare_1}, {susang_rare_2}, {susang_rare_3}')
                cur_cube_susang_rare = conn_cube_susang.cursor()
                sql_cube_susang_rare = "update `testDB`.`weaponTable` set 잠재옵션1 = %s, 잠재옵션2 = %s, 잠재옵션3 = %s where userId = %s"

                cur_cube_susang_rare.execute(sql_cube_susang_rare, ({susang_rare_1},{susang_rare_2},{susang_rare_3},{message.author.id}))
                
                await message.channel.send(f'잠재능력 옵션이 변경되었습니다. \n등급: {cur_cube_susang}\n잠재옵션1: {susang_rare_1}\n잠재옵션2: {susang_rare_2}\n잠재옵션3: {susang_rare_3}')

                conn_cube_susang.commit()
                conn_cube_susang.close()
                
        elif(cube == "장인의큐브"):
            pass

    if message.content.startswith('무기강화!'):
        await message.channel.send(f'정지된 기능입니다...')
        # L = 40
        # for i in range(0,25):
        #     S = i
        #     starforce_price = 0
        #     if i <= 2:
        #         starforce_price = 1000 + (pow(L,3) * (S + 1)) / 25
        #     elif i <= 9:
        #         starforce_price = 1000 + (pow(L,3) * (S + 1)) / 25
        #     elif i == 10:
        #         starforce_price = 1000 + (pow(L,3) * pow((S + 1),2.7)) / 400
        #     elif i == 11:
        #         starforce_price = 1000 + (pow(L,3) * pow((S + 1),2.7)) / 400
        #     elif i == 12:
        #         starforce_price = 1000 + (pow(L,3) * pow((S + 1),2.7)) / 400
        #     elif i == 13:
        #         starforce_price = 1000 + (pow(L,3) * pow((S + 1),2.7)) / 400
        #     elif i == 14:
        #         starforce_price = 1000 + (pow(L,3) * pow((S + 1),2.7)) / 400
        #     elif i <= 17:
        #         starforce_price = 1000 + (pow(L,3) * pow((S + 1),2.7)) / 200
        #     elif i <= 19:
        #         starforce_price = 1000 + (pow(L,3) * pow((S + 1),2.7)) / 200
        #     elif i <= 21:
        #         starforce_price = 1000 + (pow(L,3) * pow((S + 1),2.7))/ 200
        #     elif i == 22:
        #         starforce_price = 1000 + (pow(L,3) * pow((S + 1),2.7)) / 200
        #     elif i == 23:
        #         starforce_price = 1000 + (pow(L,3) * pow((S + 1),2.7)) / 200
        #     elif i == 24:
        #         starforce_price = 1000 + (pow(L,3) * pow((S + 1),2.7)) / 200
        #     starforce_price = round(starforce_price)
        #     print(f'{i}: {starforce_price}')
            
        conn_cube_starforce = pymysql.connect(
        user = 'jonsu0129',
        password = passwd_token,
        host = 'discord-database-kr.cqops5vysvnr.ap-northeast-2.rds.amazonaws.com',
        db = 'testDB',
        charset = 'utf8'
        )
        cur_starforce = conn_cube_starforce.cursor()
        sql_starforce = "select 스타포스 from weaponTable where userId = %s"

        cur_starforce.execute(sql_starforce, {message.author.id})
        cur_starforce = cur_starforce.fetchall()[0][0]

        L = 40
        starforce_price = 0
        starforce_prob = 0
        starforce_num = random.randint(1,1001)
        await message.channel.send(f'<@{message.author.id}>')
        if cur_starforce <= 2:
            starforce_price = 1000 + (pow(L,3) * (cur_starforce + 1)) / 25
            starforce_prob = (95 - 5 * cur_starforce) * 10
            if starforce_num <= starforce_prob:
                cur_starforce_wl = conn_cube_starforce.cursor()
                sql_starforce_wl = "UPDATE `testDB`.`weaponTable` SET 스타포스 = %s WHERE userId = %s;"
                cur_starforce_wl.execute(sql_starforce_wl, ({cur_starforce+1},{message.author.id}))
                await message.channel.send(f'스타포스 강화를 성공하셨습니다. {cur_starforce+1}성(+1)')
                conn_cube_starforce.commit()
                conn_cube_starforce.close()
            else:
                await message.channel.send(f'스타포스 강화를 실패하셨습니다. {cur_starforce}성(유지)')

        elif cur_starforce<= 9:
            starforce_price = 1000 + (pow(L,3) * (cur_starforce + 1)) / 25
            starforce_prob = (95 - 5 * cur_starforce) * 10
            if starforce_num <= starforce_prob:
                cur_starforce_wl = conn_cube_starforce.cursor()
                sql_starforce_wl = "UPDATE `testDB`.`weaponTable` SET 스타포스 = %s WHERE userId = %s;"
                cur_starforce_wl.execute(sql_starforce_wl, ({cur_starforce+1},{message.author.id}))
                await message.channel.send(f'스타포스 강화를 성공하셨습니다. {cur_starforce+1}성(+1)')
                conn_cube_starforce.commit()
                conn_cube_starforce.close()
            else:
                await message.channel.send(f'스타포스 강화를 실패하셨습니다. {cur_starforce}성(유지)')

        elif cur_starforce == 10:
            starforce_price = 1000 + (pow(L,3) * pow((cur_starforce + 1),2.7)) / 400
            starforce_prob = (100 - 5 * cur_starforce)*10
            if starforce_num <= starforce_prob:
                cur_starforce_wl = conn_cube_starforce.cursor()
                sql_starforce_wl = "UPDATE `testDB`.`weaponTable` SET 스타포스 = %s WHERE userId = %s;"
                cur_starforce_wl.execute(sql_starforce_wl, ({cur_starforce+1},{message.author.id}))
                await message.channel.send(f'스타포스 강화를 성공하셨습니다. {cur_starforce+1}성(+1)')
                conn_cube_starforce.commit()
                conn_cube_starforce.close()
            else:
                await message.channel.send(f'스타포스 강화를 실패하셨습니다. {cur_starforce}성(유지)')

        elif cur_starforce == 11:
            starforce_price = 1000 + (pow(L,3) * pow((cur_starforce + 1),2.7)) / 400
            starforce_prob = (100 - 5 * cur_starforce)*10
            if starforce_num <= starforce_prob:
                cur_starforce_wl = conn_cube_starforce.cursor()
                sql_starforce_wl = "UPDATE `testDB`.`weaponTable` SET 스타포스 = %s WHERE userId = %s;"
                cur_starforce_wl.execute(sql_starforce_wl, ({cur_starforce+1},{message.author.id}))
                await message.channel.send(f'스타포스 강화를 성공하셨습니다. {cur_starforce+1}성(+1)')
                conn_cube_starforce.commit()
                conn_cube_starforce.close()
            else:
                await message.channel.send(f'스타포스 강화를 실패하셨습니다. {cur_starforce}성(유지)')

        elif cur_starforce == 12:
            starforce_price = 1000 + (pow(L,3) * pow((cur_starforce + 1),2.7)) / 400
            starforce_prob = (100 - 5 * cur_starforce)*10
            if starforce_num <= starforce_prob:
                cur_starforce_wl = conn_cube_starforce.cursor()
                sql_starforce_wl = "UPDATE `testDB`.`weaponTable` SET 스타포스 = %s WHERE userId = %s;"
                cur_starforce_wl.execute(sql_starforce_wl, ({cur_starforce+1},{message.author.id}))
                await message.channel.send(f'스타포스 강화를 성공하셨습니다. {cur_starforce+1}성(+1)')
                conn_cube_starforce.commit()
                conn_cube_starforce.close()
            else:
                await message.channel.send(f'스타포스 강화를 실패하셨습니다. {cur_starforce}성(유지)')

        elif cur_starforce == 13:
            starforce_price = 1000 + (pow(L,3) * pow((cur_starforce + 1),2.7)) / 400
            starforce_prob = (100 - 5 * cur_starforce)*10
            if starforce_num <= starforce_prob:
                cur_starforce_wl = conn_cube_starforce.cursor()
                sql_starforce_wl = "UPDATE `testDB`.`weaponTable` SET 스타포스 = %s WHERE userId = %s;"
                cur_starforce_wl.execute(sql_starforce_wl, ({cur_starforce+1},{message.author.id}))
                await message.channel.send(f'스타포스 강화를 성공하셨습니다. {cur_starforce+1}성(+1)')
                conn_cube_starforce.commit()
                conn_cube_starforce.close()
            else:
                await message.channel.send(f'스타포스 강화를 실패하셨습니다. {cur_starforce}성(유지)')

        elif cur_starforce == 14:
            starforce_price = 1000 + (pow(L,3) * pow((cur_starforce + 1),2.7)) / 400
            starforce_prob = (100 - 5 * cur_starforce)*10
            if starforce_num <= starforce_prob:
                cur_starforce_wl = conn_cube_starforce.cursor()
                sql_starforce_wl = "UPDATE `testDB`.`weaponTable` SET 스타포스 = %s WHERE userId = %s;"
                cur_starforce_wl.execute(sql_starforce_wl, ({cur_starforce+1},{message.author.id}))
                await message.channel.send(f'스타포스 강화를 성공하셨습니다. {cur_starforce+1}성(+1)')
                conn_cube_starforce.commit()
                conn_cube_starforce.close()
            else:
                await message.channel.send(f'스타포스 강화를 실패하셨습니다. {cur_starforce}성(유지)')

        elif cur_starforce <= 17:
            starforce_price = 1000 + (pow(L,3) * pow((cur_starforce + 1),2.7)) / 200
            starforce_prob = 321
            if starforce_num <= starforce_prob:
                cur_starforce_wl = conn_cube_starforce.cursor()
                sql_starforce_wl = "UPDATE `testDB`.`weaponTable` SET 스타포스 = %s WHERE userId = %s;"
                cur_starforce_wl.execute(sql_starforce_wl, ({cur_starforce+1},{message.author.id}))
                await message.channel.send(f'스타포스 강화를 성공하셨습니다. {cur_starforce+1}성(+1)')
                conn_cube_starforce.commit()
                conn_cube_starforce.close()
            else:
                cur_starforce_wl = conn_cube_starforce.cursor()
                sql_starforce_wl = "UPDATE `testDB`.`weaponTable` SET 스타포스 = %s WHERE userId = %s;"
                cur_starforce_wl.execute(sql_starforce_wl, ({cur_starforce-1},{message.author.id}))
                await message.channel.send(f'스타포스 강화를 성공하셨습니다. {cur_starforce-1}성(-1)')
                conn_cube_starforce.commit()
                conn_cube_starforce.close()

        elif cur_starforce <= 19:
            starforce_price = 1000 + (pow(L,3) * pow((cur_starforce + 1),2.7)) / 200
            starforce_prob = 328
            if starforce_num <= starforce_prob:
                cur_starforce_wl = conn_cube_starforce.cursor()
                sql_starforce_wl = "UPDATE `testDB`.`weaponTable` SET 스타포스 = %s WHERE userId = %s;"
                cur_starforce_wl.execute(sql_starforce_wl, ({cur_starforce+1},{message.author.id}))
                await message.channel.send(f'스타포스 강화를 성공하셨습니다. {cur_starforce+1}성(+1)')
                conn_cube_starforce.commit()
                conn_cube_starforce.close()
            else:
                cur_starforce_wl = conn_cube_starforce.cursor()
                sql_starforce_wl = "UPDATE `testDB`.`weaponTable` SET 스타포스 = %s WHERE userId = %s;"
                cur_starforce_wl.execute(sql_starforce_wl, ({cur_starforce-1},{message.author.id}))
                await message.channel.send(f'스타포스 강화를 성공하셨습니다. {cur_starforce-1}성(-1)')
                conn_cube_starforce.commit()
                conn_cube_starforce.close()

        elif cur_starforce <= 21:
            starforce_price = 1000 + (pow(L,3) * pow((cur_starforce + 1),2.7))/ 200
            starforce_prob = 370
            if starforce_num <= starforce_prob:
                cur_starforce_wl = conn_cube_starforce.cursor()
                sql_starforce_wl = "UPDATE `testDB`.`weaponTable` SET 스타포스 = %s WHERE userId = %s;"
                cur_starforce_wl.execute(sql_starforce_wl, ({cur_starforce+1},{message.author.id}))
                await message.channel.send(f'스타포스 강화를 성공하셨습니다. {cur_starforce+1}성(+1)')
                conn_cube_starforce.commit()
                conn_cube_starforce.close()
            else:
                cur_starforce_wl = conn_cube_starforce.cursor()
                sql_starforce_wl = "UPDATE `testDB`.`weaponTable` SET 스타포스 = %s WHERE userId = %s;"
                cur_starforce_wl.execute(sql_starforce_wl, ({cur_starforce-1},{message.author.id}))
                await message.channel.send(f'스타포스 강화를 성공하셨습니다. {cur_starforce-1}성(-1)')
                conn_cube_starforce.commit()
                conn_cube_starforce.close()

        elif cur_starforce == 22:
            starforce_price = 1000 + (pow(L,3) * pow((cur_starforce + 1),2.7)) / 200
            starforce_prob = 224
            if starforce_num <= starforce_prob:
                cur_starforce_wl = conn_cube_starforce.cursor()
                sql_starforce_wl = "UPDATE `testDB`.`weaponTable` SET 스타포스 = %s WHERE userId = %s;"
                cur_starforce_wl.execute(sql_starforce_wl, ({cur_starforce+1},{message.author.id}))
                await message.channel.send(f'스타포스 강화를 성공하셨습니다. {cur_starforce+1}성(+1)')
                conn_cube_starforce.commit()
                conn_cube_starforce.close()
            else:
                cur_starforce_wl = conn_cube_starforce.cursor()
                sql_starforce_wl = "UPDATE `testDB`.`weaponTable` SET 스타포스 = %s WHERE userId = %s;"
                cur_starforce_wl.execute(sql_starforce_wl, ({cur_starforce-1},{message.author.id}))
                await message.channel.send(f'스타포스 강화를 성공하셨습니다. {cur_starforce-1}성(-1)')
                conn_cube_starforce.commit()
                conn_cube_starforce.close()

        elif cur_starforce == 23:
            starforce_price = 1000 + (pow(L,3) * pow((cur_starforce + 1),2.7)) / 200
            starforce_prob = 314
            if starforce_num <= starforce_prob:
                cur_starforce_wl = conn_cube_starforce.cursor()
                sql_starforce_wl = "UPDATE `testDB`.`weaponTable` SET 스타포스 = %s WHERE userId = %s;"
                cur_starforce_wl.execute(sql_starforce_wl, ({cur_starforce+1},{message.author.id}))
                await message.channel.send(f'스타포스 강화를 성공하셨습니다. {cur_starforce+1}성(+1)')
                conn_cube_starforce.commit()
                conn_cube_starforce.close()
            else:
                cur_starforce_wl = conn_cube_starforce.cursor()
                sql_starforce_wl = "UPDATE `testDB`.`weaponTable` SET 스타포스 = %s WHERE userId = %s;"
                cur_starforce_wl.execute(sql_starforce_wl, ({cur_starforce-1},{message.author.id}))
                await message.channel.send(f'스타포스 강화를 성공하셨습니다. {cur_starforce-1}성(-1)')
                conn_cube_starforce.commit()
                conn_cube_starforce.close()

        elif cur_starforce == 24:
            starforce_price = 1000 + (pow(L,3) * pow((cur_starforce + 1),2.7)) / 200
            starforce_prob = 406
            if starforce_num <= starforce_prob:
                cur_starforce_wl = conn_cube_starforce.cursor()
                sql_starforce_wl = "UPDATE `testDB`.`weaponTable` SET 스타포스 = %s WHERE userId = %s;"
                cur_starforce_wl.execute(sql_starforce_wl, ({cur_starforce+1},{message.author.id}))
                await message.channel.send(f'스타포스 강화를 성공하셨습니다. {cur_starforce+1}성(+1)')
                conn_cube_starforce.commit()
                conn_cube_starforce.close()
            else:
                cur_starforce_wl = conn_cube_starforce.cursor()
                sql_starforce_wl = "UPDATE `testDB`.`weaponTable` SET 스타포스 = %s WHERE userId = %s;"
                cur_starforce_wl.execute(sql_starforce_wl, ({cur_starforce-1},{message.author.id}))
                await message.channel.send(f'스타포스 강화를 성공하셨습니다. {cur_starforce-1}성(-1)')
                conn_cube_starforce.commit()
                conn_cube_starforce.close()

        starforce_price = round(starforce_price)

    if message.content.startswith('골라! '):
        sel_list = message.content.split()
        sel_list.remove('골라!')
        sel_one = random.choice(sel_list)
        await message.channel.send(f"2hogi's pick : ★{sel_one}★")

    if message.content.startswith('송금!'):
        await message.channel.send(f'정지된 기능입니다...')
        wire_data = message.content.split()
        wire_sender_id = message.author.id
        wire_rr = wire_data[1][2:][:-1]
        wire_money = int(wire_data[2])
        print(f'{wire_data}, {wire_sender_id}, {wire_rr}')

        conn_wire = pymysql.connect(
            user = 'jonsu0129',
            password = passwd_token,
            host = 'discord-database-kr.cqops5vysvnr.ap-northeast-2.rds.amazonaws.com',
            db = 'testDB',
            charset = 'utf8'
        )

        cur_wire_user_money = conn_wire.cursor()
        sql_wire_user_money = "SELECT * FROM testDB.userTable WHERE userId = %s"

        wire_user_money = cur_wire_user_money.execute(sql_wire_user_money, message.author.id)
        wire_user_money = int(cur_wire_user_money.fetchall()[0][2])


        if(wire_user_money < wire_money):
            await message.channel.send(f"<@{message.author.id}> 보유 골드가 부족합니다. (보유 골드 : {wire_user_money}G, 보낼 골드 : {wire_money}G)")
        else:
            cur_wire_rr_money = conn_wire.cursor()
            sql_wire_rr_money = "SELECT * FROM testDB.userTable WHERE userId = %s"

            wire_rr_money = cur_wire_rr_money.execute(sql_wire_rr_money, wire_rr)
            wire_rr_money =int(cur_wire_rr_money.fetchall()[0][2])

            cur_wire_update_money_1 = conn_wire.cursor()
            sql_wire_update_money_1 = "UPDATE `testDB`.`userTable` SET money = %s WHERE userId = %s;"

            cur_wire_update_moeny_2 = conn_wire.cursor()
            sql_wire_update_money_2 = "UPDATE `testDB`.`userTable` SET money = %s WHERE userId = %s;"


            wire_user_money -= wire_money
            wire_rr_money += wire_money
            
            await message.channel.send(f'<@{message.author.id}>님이 <@{wire_rr}>님에게 {wire_money}G를 송금하였습니다. (보유 골드 : {wire_user_money}G)')

            cur_wire_update_money_1.execute(sql_wire_update_money_1, ({wire_user_money},{message.author.id}))

            cur_wire_update_moeny_2.execute(sql_wire_update_money_2, ({wire_rr_money},{wire_rr}))

            conn_wire.commit()
            conn_wire.close()
    
    if message.content.startswith('복권지급! '):
        await message.channel.send(f'정지된 기능입니다...')
        if message.author.id == 268568994108145674:
            conn_add_lt = pymysql.connect(
            user = 'jonsu0129',
            password = passwd_token,
            host = 'discord-database-kr.cqops5vysvnr.ap-northeast-2.rds.amazonaws.com',
            db = 'testDB',
            charset = 'utf8'
            )
            lt_num = message.content[6:]
            cur_add_lt = conn_add_lt.cursor()
            sql_add_lt = "update userTable set ltcount = ltcount + %s"
            
            cur_add_lt.execute(sql_add_lt, (lt_num))
            conn_add_lt.commit()
            conn_add_lt.close()
            await message.channel.send(f'복권 {lt_num}개가 지급되었습니다.')
        else:
            await message.channel.send(f'<@{message.author.id}>접근 권한이 없습니다!')
        
    if message.content.startswith('복권초기화!'):
        await message.channel.send(f'정지된 기능입니다...')
        if message.author.id == 268568994108145674:
            conn_lt_init = pymysql.connect(
            user = 'jonsu0129',
            password = passwd_token,
            host = 'discord-database-kr.cqops5vysvnr.ap-northeast-2.rds.amazonaws.com',
            db = 'testDB',
            charset = 'utf8'
            )
            cur_lt_init = conn_lt_init.cursor()
            sql_lt_init = "update userTable set ltcount = 3"
            
            cur_lt_init.execute(sql_lt_init)
            conn_lt_init.commit()
            conn_lt_init.close()
            await message.channel.send(f'복권이 3개로 초기화됐습니다.')
        else:
            await message.channel.send(f'<@{message.author.id}>접근 권한이 없습니다!')
    
    if message.content.startswith('주사위!'):
        await message.channel.send(f"<@{message.author.id}> 주사위 : ★ {random.randint(1,100)} ★ (1~100)")
    
    if message.content.startswith('개양파'):
        await message.channel.send(f"빠큐")
    
    if message.content.startswith('명령어!'):
        await message.channel.send(f'🔴DB를 이용한 기능은 정지되었습니다.🔴')
        help = discord.Embed(title=f"명령어!", color=0x62c1cc)
        help.add_field(name = "버스!", value = f'4인 기준 분배금을 알려줍니다.', inline = False)
        help.add_field(name = "검색!", value = f'검색! (닉네임)으로 간단한 정보를 보여줍니다.', inline = False)
        help.add_field(name = "토끼", value = f'귀여운 토끼가 나옵니다.', inline = False)
        help.add_field(name = "졸려", value = f'목혹호 2호기가 반응을 해줍니다.', inline = False)
        help.add_field(name = "잠와", value = f'목혹호 2호기가 반응을 해줍니다.', inline = False)
        help.add_field(name = "뭐먹", value = f'목혹호 2호기가 음식을 추천해줍니다.', inline = False)
        help.add_field(name = "뭐먹리스트", value = f'목혹호 2호기의 음식 추천 리스트를 보여줍니다.', inline = False)
        help.add_field(name = "뭐먹 추가/삭제", value = f'뭐먹리스트의 음식을 추가/삭제 할 수 있습니다. ex) 뭐먹 (음식) 삭제, 뭐먹 (음식) 추가', inline = False)
        help.add_field(name = "가위바위보", value = f'목혹호 2호기와 가위바위보를 할 수 있습니다. ex) 가위바위보 가위', inline = False)
        help.add_field(name = "lotto!", value = f'목혹호 2호기가 로또 번호를 추천해줍니다.', inline = False)
        help.add_field(name = "오늘도", value = f'목혹호 2호기가 반응을 해줍니다.', inline = False)
        help.add_field(name = "행복하세요?", value = f'목혹호 2호기가 반응을 해줍니다.', inline = False)
        help.add_field(name = "야", value = f'목혹호 2호기가 \'야\' 갯수에 따라 반응을 해줍니다.', inline = False)
        help.add_field(name = "ㅋㅋㅋㅋ", value = f'목혹호 2호기가 일정 확률로 반응을 해줍니다.', inline = False)
        help.add_field(name = "돌깎자!", value = f'어빌리티 스톤을 깎을 수 있습니다. (test)', inline = False)
        help.add_field(name = "언퉤", value = f'목혹호 2호기가 퇴근할 시간을 말해줍니다.',inline = False)
        help.add_field(name = "주식!", value = f'현재 주가를 보여줍니다.',inline = False)
        help.add_field(name = "주식구매!", value = f'주식을 구매합니다. ex) 주식구매! 5 개양파코리아',inline = False)
        help.add_field(name = "주식판매!", value = f'주식을 판매합니다. ex) 주식판매! 5 개양파코리아',inline = False)
        help.add_field(name = "송금!", value = f'다른 유저에게 골드를 보낼 수 있습니다. ex) 송금! @유저언급 10000',inline = False)
        await message.channel.send(embed=help)
        
    if message.content.startswith('도박명령어!'):
        gamble_help = discord.Embed(title=f"도박명령어!", color=0x62c1cc)
        gamble_help.add_field(name = "배팅가위바위보", value = f'목혹호와 가위바위보하여 이기면 배팅금만큼 골드를 얻습니다.\nex) 배팅가위바위보 가위 1000', inline = False)
        gamble_help.add_field(name = "복권!", value = f'복권을 긁습니다. 티켓을 하나 소모합니다.', inline = False)
        gamble_help.add_field(name = "룰렛! ", value = f'룰렛을 돌립니다. 룰렛! 뒤에 베팅할 금액을 적습니다. ex)룰렛! 100\n당첨 배율 : 7️⃣7️⃣7️⃣(x5000), 🔴🔴🔴(x777), 🟡🟡🟡(x333), 🟢🟢🟢(x77), 🔵🔵🔵(x33), 🟣🟣🟣(x15), ⚪⚪⚪(x5)\n※룰렛에 각 도형이 나올 확률은 다릅니다.※', inline = False)
        gamble_help.add_field(name = "랭킹!", value = f'골드 랭킹을 확인합니다.', inline = False)
        gamble_help.add_field(name = "내정보!", value = f'정보를 확인합니다.', inline = False)
        gamble_help.add_field(name = "등록!", value = f'계정을 등록하고 10000G를 받습니다.', inline = False)
        gamble_help.add_field(name = "파산!", value = f'파산 신청을 합니다. 보유 골드가 1000G이하일 때 5000G를 받습니다.', inline = False)
        await message.channel.send(embed=gamble_help)
        
    if message.content.startswith('등록!'):
        await message.channel.send(f'정지된 기능입니다...')
        conn = pymysql.connect(
            user = 'jonsu0129',
            password = passwd_token,
            host = 'discord-database-kr.cqops5vysvnr.ap-northeast-2.rds.amazonaws.com',
            db = 'testDB',
            charset = 'utf8'
        )
        cur = conn.cursor()
        cur_check_insert = conn.cursor()

        sql_check = "SELECT EXISTS(SELECT * FROM userTable WHERE userId = %(userId)s)"
        cur_check_insert.execute(sql_check, {"userId": {message.author.id}})
        chch = cur_check_insert.fetchone()[0]
        
        if chch == 1:
            await message.channel.send(f'<@{message.author.id}>이미 존재하는 id입니다.')
        else:
            cur.execute(f"INSERT INTO userTable VALUES('{message.author}','{message.author.id}',10000, NULL, 3, 0, 0, NULL)")
            await message.channel.send(f'<@{message.author.id}>등록되었습니다.(+10000G)')
            conn.commit()
            conn.close()

    if message.content.startswith('데이터삭제!'):
        await message.channel.send(f'정지된 기능입니다...')
        conn_del = pymysql.connect(
            user = 'jonsu0129',
            password = passwd_token,
            host = 'discord-database-kr.cqops5vysvnr.ap-northeast-2.rds.amazonaws.com',
            db = 'testDB',
            charset = 'utf8'
        )
        cur_del = conn_del.cursor()
        cur_check_delete = conn_del.cursor()
        sql = "DELETE FROM userTable WHERE userId = %(userId)s"

        sql_check = "SELECT EXISTS(SELECT * FROM userTable WHERE userId = %(userId)s)"
        cur_check_delete.execute(sql_check, {"userId": {message.author.id}})
        chch = cur_check_delete.fetchone()[0]
        
        if chch == 1:
            cur_del.execute(sql, {"userId" : {message.author.id}})
            conn_del.commit()
            conn_del.close()
            await message.channel.send(f'<@{message.author.id}> 데이터가 삭제되었습니다.')
        else:
            await message.channel.send(f'<@{message.author.id}> 데이터가 존재하지 않습니다.')

    if message.content.startswith('내정보!'):
        await message.channel.send(f'정지된 기능입니다...')
        conn_info = pymysql.connect(
        user = 'jonsu0129',
        password = passwd_token,
        host = 'discord-database-kr.cqops5vysvnr.ap-northeast-2.rds.amazonaws.com',
        db = 'testDB',
        charset = 'utf8'
        )
    
        cur_info = conn_info.cursor()
        lsp_info = "SELECT * FROM testDB.userTable WHERE userId = %(userId)s"
        cur_info.execute(lsp_info, {"userId": {message.author.id}})
        user_info = cur_info.fetchall()
        userName = user_info[0][0]
        userMoney = user_info[0][2]
        user_lt = user_info[0][4]
        user_weapon = user_info[0][7]
        
        gamble_info = discord.Embed(title=f"{userName}", color=0x62c1cc)
        gamble_info.add_field(name = "보유 골드", value = f'{userMoney}G', inline = False)
        gamble_info.add_field(name = "보유 티켓", value = f'{user_lt}개', inline = False)
        gamble_info.add_field(name = "보유 무기", value = f'{user_weapon}', inline = False)
        await message.channel.send(embed=gamble_info)

        conn_info.close()
        
    if message.content.startswith('주식구매! '):
        await message.channel.send(f'정지된 기능입니다...')
        conn_stock_buy = pymysql.connect(
            user = 'jonsu0129',
            password = passwd_token,
            host = 'discord-database-kr.cqops5vysvnr.ap-northeast-2.rds.amazonaws.com',
            db = 'testDB',
            charset = 'utf8'
        )
        msg_split = message.content.split()
        stock_buy_name = msg_split[2]
        stock_buy_num = int(msg_split[1])

        cur_price_stock_buy = conn_stock_buy.cursor()
        sql_price_stock_buy = "SELECT * FROM testDB.discordStock WHERE stockName = %s"

        price_stock_buy = cur_price_stock_buy.execute(sql_price_stock_buy, '(주)' + stock_buy_name)
        price_stock_buy = cur_price_stock_buy.fetchall()[0][1]
        
        cur_user_money = conn_stock_buy.cursor()
        sql_user_money = "SELECT * FROM testDB.userTable WHERE userId = %s"

        user_money_stock_buy = cur_user_money.execute(sql_user_money, message.author.id)
        user_money_stock_buy = cur_user_money.fetchall()[0][2]

        if user_money_stock_buy < price_stock_buy * stock_buy_num:
            await message.channel.send(f'<@{message.author.id}> 보유 골드가 부족합니다. (보유 골드 : {user_money_stock_buy}G) (주식 가격 : {price_stock_buy * stock_buy_num}G)')    
        else:
            user_money_stock_buy -= price_stock_buy * stock_buy_num
            
            cur_user_stock = conn_stock_buy.cursor()
            sql_user_stock = f"SELECT `(주){stock_buy_name}` from testDB.userTable where userId = %s"
            user_stock = cur_user_stock.execute(sql_user_stock, message.author.id)
            user_stock = cur_user_stock.fetchall()[0][0]
            user_stock += stock_buy_num

            cur_stock_buy = conn_stock_buy.cursor()
            sql_stock_buy = f"UPDATE testDB.userTable SET `money` = %s, `(주){stock_buy_name}` = %s WHERE `userId` = %s"
            cur_stock_buy.execute(sql_stock_buy, (user_money_stock_buy, user_stock, message.author.id))
            
            conn_stock_buy.commit()
            conn_stock_buy.close()
            await message.channel.send(f'<@{message.author.id}> (주){stock_buy_name}을(를) {stock_buy_num}주 구매하였습니다. (보유 골드 : {user_money_stock_buy}G)\n(보유 (주){stock_buy_name} : {user_stock}주)')

    if message.content.startswith('주식판매! '):
        await message.channel.send(f'정지된 기능입니다...')
        conn_stock_sell = pymysql.connect(
            user = 'jonsu0129',
            password = passwd_token,
            host = 'discord-database-kr.cqops5vysvnr.ap-northeast-2.rds.amazonaws.com',
            db = 'testDB',
            charset = 'utf8'
        )
        msg_split = message.content.split()
        stock_sell_name = msg_split[2]
        stock_sell_num = int(msg_split[1])

        cur_price_stock_sell = conn_stock_sell.cursor()
        sql_price_stock_sell = "SELECT * FROM testDB.discordStock WHERE stockName = %s"
        price_stock_sell = cur_price_stock_sell.execute(sql_price_stock_sell, '(주)' + stock_sell_name)
        price_stock_sell = cur_price_stock_sell.fetchall()[0][1]

        cur_user_stock = conn_stock_sell.cursor()
        sql_user_stock = f"SELECT `(주){stock_sell_name}` from testDB.userTable where userId = %s"
        user_stock = cur_user_stock.execute(sql_user_stock, message.author.id)
        user_stock = cur_user_stock.fetchall()[0][0]

        if user_stock < stock_sell_num:
            await message.channel.send(f'<@{message.author.id}> 보유 주식이 부족합니다. (보유 (주){stock_sell_name} : {user_stock}주)')    
        else:
            cur_user_money = conn_stock_sell.cursor()
            sql_user_money = "SELECT * FROM testDB.userTable WHERE userId = %s"
            user_money_stock_sell = cur_user_money.execute(sql_user_money, message.author.id)
            user_money_stock_sell = cur_user_money.fetchall()[0][2]
            user_stock -= stock_sell_num

            user_money_stock_sell += price_stock_sell * stock_sell_num

            cur_stock_sell = conn_stock_sell.cursor()
            sql_stock_sell = f"UPDATE testDB.userTable SET `money` = %s, `(주){stock_sell_name}` = %s WHERE `userId` = %s"
            cur_stock_sell.execute(sql_stock_sell, (user_money_stock_sell, user_stock, message.author.id))
            
            conn_stock_sell.commit()
            conn_stock_sell.close()
            await message.channel.send(f'<@{message.author.id}> (주){stock_sell_name}을(를) {stock_sell_num}주 판매하였습니다. (보유 골드 : {user_money_stock_sell}G)\n(보유 (주){stock_sell_name} : {user_stock}주)')
        
    if message.content.startswith('주식!'):
        await message.channel.send(f'정지된 기능입니다...')
        conn_stock = pymysql.connect(
            user = 'jonsu0129',
            password = passwd_token,
            host = 'discord-database-kr.cqops5vysvnr.ap-northeast-2.rds.amazonaws.com',
            db = 'testDB',
            charset = 'utf8'
        )

        cur_stock = conn_stock.cursor()
        sql_stock = "SELECT * FROM testDB.discordStock"

        cur_stock.execute(sql_stock)
        stock_tuple = cur_stock.fetchall()

        stock = discord.Embed(title=f"현재 주가 {time.strftime('%Y.%m.%d - %H:%M:%S')}", color=0x62c1cc)
        stock.add_field(name = "(주)개양파코리아", value = f'{stock_tuple[0][1]}G({round(last_gypkr_rand,2)}%)',inline = False)
        stock.add_field(name = "(주)단밤바이오", value = f'{stock_tuple[1][1]}G({round(last_dbbio_rand,2)}%)',inline = False)
        await message.channel.send(embed=stock)
    
    if message.content.startswith('룰렛! '):
        await message.channel.send(f'정지된 기능입니다...')
        conn_roulette = pymysql.connect(
            user = 'jonsu0129',
            password = passwd_token,
            host = 'discord-database-kr.cqops5vysvnr.ap-northeast-2.rds.amazonaws.com',
            db = 'testDB',
            charset = 'utf8'
        )
        roulette_bet = int(message.content[4:])

        cur_roulette_money = conn_roulette.cursor()
        cur_roulette_win = conn_roulette.cursor()

        sql_money = "SELECT * FROM testDB.userTable WHERE userId = %(userId)s"
        sql_roulette = "UPDATE userTable SET money = %s WHERE userID = %s"

        userMoney_roulette = cur_roulette_money.execute(sql_money, {"userId": {message.author.id}})
        userMoney_roulette = cur_roulette_money.fetchall()[0][2]

        if userMoney_roulette < roulette_bet:
            await message.channel.send(f'<@{message.author.id}>보유 골드가 부족합니다. (보유 골드 : {userMoney_roulette}G)')
        else:

            Roulette_list=['7️⃣','🔴','🔴','🟡','🟡','🟡','🟢','🟢','🟢','🟢','🟢','🔵','🔵','🔵','🔵','🔵','🔵','🔵','🔵','🟣','🟣','🟣','🟣','🟣','🟣','🟣','🟣','🟣','🟣','⚪','⚪','⚪','⚪','⚪','⚪','⚪','⚪','⚪','⚪','⚪','⚪','⚪']
            Roulette_1 = random.choice(Roulette_list)
            Roulette_2 = random.choice(Roulette_list)
            Roulette_3 = random.choice(Roulette_list)

            userMoney_roulette -= roulette_bet
            
            if Roulette_1 == Roulette_2 == Roulette_3 and Roulette_1 == '7️⃣':
                userMoney_roulette += roulette_bet*5000
                await message.channel.send(f'{Roulette_1}{Roulette_2}{Roulette_3}')
                await message.channel.send(f'<@{message.author.id}> 당첨!! 상금 : {roulette_bet}x5000')
            elif Roulette_1 == Roulette_2 == Roulette_3 and Roulette_1 == '🔴':
                userMoney_roulette += roulette_bet*777
                await message.channel.send(f'{Roulette_1}{Roulette_2}{Roulette_3}')
                await message.channel.send(f'<@{message.author.id}> 당첨!! 상금 : {roulette_bet}x777 (보유 골드 : {userMoney_roulette}G)')
            elif Roulette_1 == Roulette_2 == Roulette_3 and Roulette_1 == '🟡':
                userMoney_roulette += roulette_bet*333
                await message.channel.send(f'{Roulette_1}{Roulette_2}{Roulette_3}')
                await message.channel.send(f'<@{message.author.id}> 당첨!! 상금 : {roulette_bet}x333 (보유 골드 : {userMoney_roulette}G)')
            elif Roulette_1 == Roulette_2 == Roulette_3 and Roulette_1 == '🟢':
                userMoney_roulette += roulette_bet*77
                await message.channel.send(f'{Roulette_1}{Roulette_2}{Roulette_3}')
                await message.channel.send(f'<@{message.author.id}> 당첨!! 상금 : {roulette_bet}x77 (보유 골드 : {userMoney_roulette}G)')
            elif Roulette_1 == Roulette_2 == Roulette_3 and Roulette_1 == '🔵':
                userMoney_roulette += roulette_bet*33
                await message.channel.send(f'{Roulette_1}{Roulette_2}{Roulette_3}')
                await message.channel.send(f'<@{message.author.id}> 당첨!! 상금 : {roulette_bet}x33 (보유 골드 : {userMoney_roulette}G)')
            elif Roulette_1 == Roulette_2 == Roulette_3 and Roulette_1 == '🟣':
                userMoney_roulette += roulette_bet*15
                await message.channel.send(f'{Roulette_1}{Roulette_2}{Roulette_3}')
                await message.channel.send(f'<@{message.author.id}> 당첨!! 상금 : {roulette_bet}x15 (보유 골드 : {userMoney_roulette}G)')
            elif Roulette_1 == Roulette_2 == Roulette_3 and Roulette_1 == '⚪':
                userMoney_roulette += roulette_bet*5
                await message.channel.send(f'{Roulette_1}{Roulette_2}{Roulette_3}')
                await message.channel.send(f'<@{message.author.id}> 당첨!! 상금 : {roulette_bet}x5 (보유 골드 : {userMoney_roulette}G)')
            else:
                await message.channel.send(f'{Roulette_1}{Roulette_2}{Roulette_3}')
                await message.channel.send(f'<@{message.author.id}> 꽝! (보유 골드 : {userMoney_roulette}G)')
                
            cur_roulette_win.execute(sql_roulette, (userMoney_roulette, message.author.id))
            conn_roulette.commit()
            conn_roulette.close()
        
    if message.content.startswith('복권!'):
        await message.channel.send(f'정지된 기능입니다...')
        conn_lotto = pymysql.connect(
        user = 'jonsu0129',
        password = passwd_token,
        host = 'discord-database-kr.cqops5vysvnr.ap-northeast-2.rds.amazonaws.com',
        db = 'testDB',
        charset = 'utf8'
        )
        
        cur_lotto_1 = conn_lotto.cursor()
        sql_lotto_1 = "SELECT * FROM testDB.userTable WHERE userId = %(userId)s"
        cur_lotto_1.execute(sql_lotto_1, {"userId": {message.author.id}})
        userMoney_lotto = cur_lotto_1.fetchall()[0][2]
        
        cur_lotto_3= conn_lotto.cursor()
        sql_lotto_3 = "SELECT * FROM testDB.userTable WHERE userId = %(userId)s"
        cur_lotto_3.execute(sql_lotto_3, {"userId": {message.author.id}})
        ticket_lotto = cur_lotto_3.fetchall()[0][4]
        
        if ticket_lotto == 0:
            await message.channel.send(f'<@{message.author.id}>보유 복권 티켓이 부족합니다.')
        else:
            lotto_dice = random.randint(0,100)

            cur_lotto_2 = conn_lotto.cursor()
            sql_lotto_2 = "UPDATE `testDB`.`userTable` SET money = %s, ltcount = %s WHERE userName = %s;"

            print(lotto_dice)
            ticket_lotto -= 1
            if lotto_dice == 100:
                userMoney_lotto += 1000000
                await message.channel.send(f'★★★★★★★★★★★★\n★★★  1등 당첨  ★★★\n★★★★★★★★★★★★')
                await message.channel.send(f'<@{message.author.id}>님이 1등에 당첨되셨습니다. (상금 1000000G) (남은 티켓 {ticket_lotto}개)')
            elif lotto_dice >= 96:
                userMoney_lotto += 247500
                await message.channel.send(f'★★★★★★★★★★\n★★★  2등2  ★★★\n★★★★★★★★★★')
                await message.channel.send(f'<@{message.author.id}>님이 2등에 당첨되셨습니다. (상금 247500G) (남은 티켓 {ticket_lotto}개)')
            elif lotto_dice >= 86:
                userMoney_lotto += 99000
                await message.channel.send(f'★★★★\n★ 3등 ★\n★★★★')
                await message.channel.send(f'<@{message.author.id}>님이 3등에 당첨되셨습니다. (상금 99000G) (남은 티켓 {ticket_lotto}개)')
            elif lotto_dice >= 66:
                userMoney_lotto += 44500
                await message.channel.send(f'★4등★')
                await message.channel.send(f'<@{message.author.id}>님이 4등에 당첨되셨습니다. (상금 44500G) (남은 티켓 {ticket_lotto}개)')
            elif lotto_dice >= 1:
                userMoney_lotto += 1000
                await message.channel.send(f'5등')
                await message.channel.send(f'<@{message.author.id}>님이 5등에 당첨되셨습니다. (상금 1000G) (남은 티켓 {ticket_lotto}개)')
            elif lotto_dice == 0:
                userMoney_lotto += 0
                await message.channel.send(f'꽝꽝꽝꽝꽝\n꽝꽝꽝꽝꽝\n꽝꽝꽝꽝꽝\n꽝꽝꽝꽝꽝\n꽝꽝꽝꽝꽝')
                await message.channel.send(f'<@{message.author.id}>님이 꽝에 당첨되셨습니다. (상금 0G) (남은 티켓 {ticket_lotto}개)')

            cur_lotto_2.execute(sql_lotto_2, ({userMoney_lotto},{ticket_lotto},{message.author}))
            conn_lotto.commit()
            conn_lotto.close()    
        
    if message.content.startswith('배팅가위바위보 '):
        await message.channel.send(f'정지된 기능입니다...')
        lsp_user = ''
        lsp_list=['가위','바위','보']
        lsp_client = random.choice(lsp_list)
        lsp_bat = 0
        
        conn_lsp = pymysql.connect(
            user = 'jonsu0129',
            password = passwd_token,
            host = 'discord-database-kr.cqops5vysvnr.ap-northeast-2.rds.amazonaws.com',
            db = 'testDB',
            charset = 'utf8'
        )
        
        lsp_cur_1 = conn_lsp.cursor()
        lsp_cur_2 = conn_lsp.cursor()
        lsp_sql_1 = "SELECT * FROM testDB.userTable WHERE userId = %(userId)s"
        lsp_sql_2 = "UPDATE userTable SET money = %s WHERE userID = %s"
        
        lsp_cur_1.execute(lsp_sql_1, {"userId": {message.author.id}})
        userMoney = lsp_cur_1.fetchall()[0][2]
        
        if message.content.startswith('배팅가위바위보 가위 '): #12
            lsp = '가위'
            lsp_bat = int(message.content[11:])
            if userMoney < lsp_bat:
                await message.channel.send(f'보유 골드가 부족합니다!(보유 골드 : {userMoney}G)')
            else:
                if lsp_client == '가위':
                    await message.channel.send(f'{lsp_client}! 당신은 비겼습니다.\n<@{message.author.id}>님의 현재 골드 {userMoney}G(+0G)')
                if lsp_client == '바위':
                    userMoney -= lsp_bat
                    lsp_cur_2.execute(lsp_sql_2, (userMoney, message.author.id))
                    await message.channel.send(f'{lsp_client}! 당신은 졌습니다.\n<@{message.author.id}>님의 현재 골드 {userMoney}G(-{lsp_bat}G)')
                if lsp_client == '보':
                    userMoney += lsp_bat
                    await message.channel.send(f'{lsp_client}! 당신은 이겼습니다.\n<@{message.author.id}>님의 현재 골드 {userMoney}G(+{lsp_bat}G)')
                    lsp_cur_2.execute(lsp_sql_2, (userMoney, message.author.id))
        if message.content.startswith('배팅가위바위보 바위 '):
            lsp = '바위'
            lsp_bat = int(message.content[11:])
            if userMoney < lsp_bat:
                await message.channel.send(f'보유 골드가 부족합니다!(보유 골드 : {userMoney}G)')
            else:
                if lsp_client == '가위':
                    userMoney += lsp_bat
                    await message.channel.send(f'{lsp_client}! 당신은 이겼습니다.\n<@{message.author.id}>님의 현재 골드 {userMoney}G(+{lsp_bat}G)')
                    lsp_cur_2.execute(lsp_sql_2, (userMoney, message.author.id))
                if lsp_client == '바위':
                    await message.channel.send(f'{lsp_client}! 당신은 비겼습니다.\n<@{message.author.id}>님의 현재 골드 {userMoney}G(+0G)')
                if lsp_client == '보':
                    userMoney -= lsp_bat
                    await message.channel.send(f'{lsp_client}! 당신은 졌습니다.\n<@{message.author.id}>님의 현재 골드 {userMoney}G(-{lsp_bat}G)')
                    lsp_cur_2.execute(lsp_sql_2, (userMoney, message.author.id))
        if message.content.startswith('배팅가위바위보 보 '):
            lsp = '보'
            lsp_bat = int(message.content[10:])
            if userMoney < lsp_bat:
                await message.channel.send(f'보유 골드가 부족합니다!(보유 골드 : {userMoney}G)')
            else:
                if lsp_client == '가위':
                    userMoney -= lsp_bat
                    await message.channel.send(f'{lsp_client}! 당신은 졌습니다.\n<@{message.author.id}>님의 현재 골드 {userMoney}G(-{lsp_bat}G)')
                    lsp_cur_2.execute(lsp_sql_2, (userMoney, message.author.id))
                if lsp_client == '바위':
                    userMoney += lsp_bat
                    await message.channel.send(f'{lsp_client}! 당신은 이겼습니다.\n<@{message.author.id}>님의 현재 골드 {userMoney}G(+{lsp_bat}G)')
                    lsp_cur_2.execute(lsp_sql_2, (userMoney, message.author.id))
                if lsp_client == '보':
                    await message.channel.send(f'{lsp_client}! 당신은 비겼습니다.\n<@{message.author.id}>님의 현재 골드 {userMoney}G(+0G)')
        conn_lsp.commit()
        conn_lsp.close()
        
    if message.content.startswith('랭킹!'):
        await message.channel.send(f'정지된 기능입니다...')
        conn_rank = pymysql.connect(
            user = 'jonsu0129',
            password = passwd_token,
            host = 'discord-database-kr.cqops5vysvnr.ap-northeast-2.rds.amazonaws.com',
            db = 'testDB',
            charset = 'utf8'
        )
        
        cur_rank_1 = conn_rank.cursor()
        sql_rank_1 = '''UPDATE userTable A, (
                        SELECT  
                            B.userName,
                            B.money,
                            @rownum := @rownum + 1 AS RNUM
                        FROM userTable B, (SELECT @rownum := 0) AS ROWNUM
                        ORDER BY B.money DESC
                        ) C
                        SET 
                            A.ranking = C.RNUM
                        WHERE
                            A.userName = C.userName'''
        cur_rank_1.execute(sql_rank_1)
        
        conn_rank.commit()
        
        cur_rank_2 = conn_rank.cursor()
        lsp_rank_2 = "SELECT userName, money, ranking FROM userTable order by money desc"
        cur_rank_2.execute(lsp_rank_2)
        user_rank = cur_rank_2.fetchall()

        user_rank_list = discord.Embed(title=f"랭킹!(보유골드순)", color=0x62c1cc)
        user_rank_list.add_field(name = "1등", value = f'{user_rank[0][0]}, {user_rank[0][1]}G', inline = False)
        user_rank_list.add_field(name = "2등", value = f'{user_rank[1][0]}, {user_rank[1][1]}G', inline = False)
        user_rank_list.add_field(name = "3등", value = f'{user_rank[2][0]}, {user_rank[2][1]}G', inline = False)
        user_rank_list.add_field(name = "4등", value = f'{user_rank[3][0]}, {user_rank[3][1]}G', inline = False)
        user_rank_list.add_field(name = "5등", value = f'{user_rank[4][0]}, {user_rank[4][1]}G', inline = False)
        await message.channel.send(embed=user_rank_list)
        
        conn_rank.close()
        
    if message.content.startswith('파산!'):
        await message.channel.send(f'정지된 기능입니다...')
        conn_gu = pymysql.connect(
            user = 'jonsu0129',
            password = passwd_token,
            host = 'discord-database-kr.cqops5vysvnr.ap-northeast-2.rds.amazonaws.com',
            db = 'testDB',
            charset = 'utf8'
            )
        cur_gu_1 = conn_gu.cursor()
        sql_gu_1 = "SELECT * FROM testDB.userTable WHERE userId = %(userId)s"
        cur_gu_1.execute(sql_gu_1, {"userId": {message.author.id}})
            
        userMoney_gu = cur_gu_1.fetchall()[0][2]
        if userMoney_gu <= 1000:
            
            cur_gu_2 = conn_gu.cursor()
            sql_gu_2 = "UPDATE `testDB`.`userTable` SET `money` = %(money)s WHERE (`userName` = %(userName)s)"
            userMoney_gu += 5000
            cur_gu_2.execute(sql_gu_2, {'money' : {userMoney_gu},'userName' : {message.author}})
            conn_gu.commit()
            conn_gu.close()
            
            await message.channel.send(f'<@{message.author.id}>님이 파산 신청을 하였습니다. 보유 골드 {userMoney_gu}G(+5000G)')
            
        else:
            await message.channel.send(f'<@{message.author.id}>보유 골드가 1000G 이하일 때 파산 신청을 할 수 있습니다. (보유 골드{userMoney_gu}G)')
        
        
    if message.content.startswith('<@885425395397177345>'):
        if message.author.dm_channel:
            await message.author.dm_channel.send("왜불러")
        elif message.author.dm_channel is None:
            await message.author.create_dm()
            await message.author.dm_channel.send("왜불러")

    if message.content.startswith('언퉤'):
        go_home = ['16시','17시','18시','19시','20시','21시','22시','지금!']
        await message.channel.send(f'<@{message.author.id}>은(는) {random.choice(go_home)} 퉤근')

    if message.content.startswith('버스! '):
        bus_msg = message.content.split()
        
        bus_mc = int(bus_msg[1])
        bus_ds = int(bus_msg[2])
        bus_gm = [0,0,0,0,0,0]
        bus_res = bus_ds - bus_mc
        bus_at = 0
        
        for i in range(len(bus_msg)-3):
            bus_gm[i] = int(bus_msg[3+i])
        
        for j in range(len(bus_msg)-3):
            bus_at += bus_gm[j]
        
        bus_res = (bus_res + bus_at) * 0.95 / 4
        
        embed = discord.Embed(title=f"4인 버스 기준", color=0x62c1cc)
        embed.add_field(name = "미참", value = f'{bus_mc}', inline = True)
        embed.add_field(name = "독식", value = f'{bus_ds}', inline = True)
        embed.add_field(name = "경매", value = f'{bus_at}', inline = True)
        embed.add_field(name = "분배금", value = f'{bus_res}', inline = False)
        embed.add_field(name = "주의", value = f'※미참을 각자 받았을 때 기준※', inline = False)
        await message.channel.send(embed=embed)
  
    if message.content.startswith('사사게! '):
        ssg_msg = ''
        keyword_ori = message.content[5:]
        keyword = urllib.parse.quote(keyword_ori)
        url = f'https://www.inven.co.kr/board/lostark/5355?query=list&p=1&sterm=&name=subjcont&keyword={keyword}'
        response = requests.get(url)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        ssg = soup.body.find('div',{'class':'board-list'}).get_text()
        p_ssg = re.compile(f'.*{keyword_ori}.*')
        real_ssg = p_ssg.findall(ssg)
        real_ssg = ''.join(real_ssg)
        real_ssg = real_ssg.replace('                                                                                             ', '\n')
        real_ssg = real_ssg.replace('                                               ','')
        if real_ssg != '':
            ssg_msg = ssg_msg + real_ssg + '\n'

        if ssg_msg != '':
            await message.channel.send(f'{real_ssg}')
        else:
            await message.channel.send(f'검색결과가 없습니다.')
    
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
    
    if message.content.startswith('토끼'):
        global rabbit_msg
        rabbit_msg = await message.channel.send(f"/)/)\n('   ')/\n(     )")
        await rabbit_msg.add_reaction('👋')
        await rabbit_msg.add_reaction('😆')
        
    if message.content.startswith('졸려'):
        await message.channel.send(f'잘자요')
    if message.content.startswith('잠와'):
        await message.channel.send(f'잘자요')
            
#'뭐먹' 응답
    if message.content.startswith('뭐먹'):
        await message.channel.send(f'정지된 기능입니다...')
        conn_mm = pymysql.connect(
        user = 'jonsu0129',
        password = passwd_token,
        host = 'discord-database-kr.cqops5vysvnr.ap-northeast-2.rds.amazonaws.com',
        db = 'testDB',
        charset = 'utf8'
        )
        
        cur_mm = conn_mm.cursor()
        lsp_mm = "SELECT mm_list FROM mmTable"
        
        cur_mm_add = conn_mm.cursor()
        lsp_mm_add = f"INSERT INTO `testDB`.`mmTable` (`mm_list`) VALUES ('{message.content[3:-3]}')"
        
        cur_mm_del = conn_mm.cursor()
        lsp_mm_del = f"DELETE FROM mmTable WHERE mm_list = %(mm_list)s"
        
        cur_mm.execute(lsp_mm)
        mm_list = cur_mm.fetchall()
        mm = ""
        for i in mm_list:
            if mm == "":
                mm += i[0]
            else:
                mm += ', ' + i[0]
                
        mm_li = mm.split(', ')
        if message.content.endswith(' 추가'):
            try:
                mm_li.index(message.content[3:-3])
                await message.channel.send(f'이미 존재하는 음식입니다.({message.content[3:-3]})')
            except ValueError as ex:
                cur_mm_add.execute(lsp_mm_add)
                await message.channel.send(f'{message.content[3:-3]}(이)가 추가되었습니다.')
                
        elif message.content.endswith(' 삭제'):
            try:
                mm_li.index(message.content[3:-3])
                cur_mm_del.execute(lsp_mm_del, {"mm_list": {message.content[3:-3]}})
                await message.channel.send(f'{message.content[3:-3]}(이)가 삭제되었습니다.')
            except ValueError as ex:
                await message.channel.send(f'{message.content[3:-3]}(이)가 리스트에 존재하지 않습니다.')
        elif message.content == '뭐먹리스트':
            await message.channel.send(f'{mm}')
        else:
            choice_food = random.choice(mm_li)
            await message.channel.send(f"2hogi's pick : ★{choice_food}★")
            
        conn_mm.commit()
        conn_mm.close() 
            
            
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
    if message.content.startswith('lotto!'):
        lotto_num = []
        while len(lotto_num) < 6:
            tmp_num = random.randint(1,45)
            if tmp_num not in lotto_num:
                lotto_num.append(tmp_num)
        lotto_num.sort()
        await message.channel.send(f"2hogi's pick : ★{lotto_num}★")
#'오늘도' 응답     
    if message.content.startswith('오늘도'):
        if random.randint(0,99) == 77:
            await message.channel.send('★★★★★\n★파이팅★\n★★★★★')
        else:
            await message.channel.send('파이팅!')
        
#'행복하세요?' 응답
    if message.content.startswith('행복하세요?'):
        await message.channel.send('행복하세요~')
#'야' 응답
    if message.content.startswith('야'):
        user_msg = list(message.content)
        a = int(user_msg.count('야'))

        if a > 15:
            await message.channel.send(f'<@{message.author.id}>그만해')        

        else:
            await message.channel.send('호'*a)
            
#'ㅋㅋㅋㅋ' 응답
    if message.content.startswith('ㅋ') or message.content.endswith('ㅋ'):
        p_zz = re.compile('ㅋㅋㅋㅋ')
        m_zz = p_zz.search(message.content)
        if m_zz != None and random.randint(0,9) == 1:
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
        elif str(reaction.emoji) == "✌️":
            stone_dic[user.id].stone_start(stone_dic[user.id].각인2)
        elif str(reaction.emoji) == "👎":
            stone_dic[user.id].stone_start(stone_dic[user.id].감소)
           
        if len(stone_dic[user.id].각인1) + len(stone_dic[user.id].각인2) + len(stone_dic[user.id].감소) == 30:
            await stone_dic[user.id].stone_msg.edit(content=f"★돌 시뮬★ <@{add_user}>(이)가 깎는중!\n 각인1☝️  : {stone_dic[user.id].각인1} \n 각인2✌️ : {stone_dic[user.id].각인2} \n 감소 👎  : {stone_dic[user.id].감소} \n 확률 : {stone_dic[user.id].pbb_base}%")
        if (len(stone_dic[user.id].각인1) + len(stone_dic[user.id].각인2) + len(stone_dic[user.id].감소)) == 30 and '◇' not in stone_dic[user.id].각인1 and '◇' not in stone_dic[user.id].각인2 and '◇' not in stone_dic[user.id].감소:
            await stone_dic[user.id].stone_msg.edit(content=f"★돌 시뮬★ <@{add_user}>(이)가 깎음!\n 각인1☝️  : {stone_dic[user.id].각인1} \n 각인2✌️ : {stone_dic[user.id].각인2} \n 감소 👎  : {stone_dic[user.id].감소} \n 확률 : {stone_dic[user.id].pbb_base}% \n {stone_dic[user.id].각인1.count('🔷')} {stone_dic[user.id].각인2.count('🔷')} {stone_dic[user.id].감소.count('🔷')} 돌입니다.\n3초 후 돌깍자log 채널로 메시지를 옮깁니다.")
            if stone_dic[user.id].각인1.count('🔷') + stone_dic[user.id].각인2.count('🔷') > 13:
                if stone_dic[user.id].각인1.count('🔷') == 8 and stone_dic[user.id].각인2.count('🔷') == 6:
                    pass
                elif stone_dic[user.id].각인1.count('🔷') == 6 and stone_dic[user.id].각인2.count('🔷') == 8:
                    pass
                else:
                    await client.get_channel(890618012883906590).send(f'<@{user.id}>님이 {stone_dic[user.id].각인1.count("🔷")} {stone_dic[user.id].각인2.count("🔷")} {stone_dic[user.id].감소.count("🔷")} 돌을 깎았습니다!')
                    stone_dic[user.id] = ''
            tmp_st = stone_dic[user.id]
            time.sleep(3)
            await stone_dic[user.id].stone_msg.delete()
            await client.get_channel(903196295869636658).send(f"★돌 시뮬★ <@{add_user}>(이)가 깎음!\n 각인1☝️  : {tmp_st.각인1} \n 각인2✌️ : {tmp_st.각인2} \n 감소 👎  : {tmp_st.감소} \n 확률 : {tmp_st.pbb_base}% \n {tmp_st.각인1.count('🔷')} {tmp_st.각인2.count('🔷')} {tmp_st.감소.count('🔷')} 돌입니다.")
        
        
@client.event
async def on_raw_reaction_add(payload): #이모지 추가할때 액션
    channel = await client.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if channel.id == 891883835548119041:
        if str(payload.emoji) == '☝️' and payload.user_id != client.user.id and payload.user_id != 885419823499214859:
            await message.remove_reaction('☝️', payload.member)
        if str(payload.emoji) == '✌️' and payload.user_id != client.user.id and payload.user_id != 885419823499214859:
            await message.remove_reaction('✌️', payload.member)
        if str(payload.emoji) == '👎' and payload.user_id != client.user.id and payload.user_id != 885419823499214859:
            await message.remove_reaction('👎', payload.member)
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
async def on_raw_reaction_remove(payload):  #이모지 지울때 액션
    pass

access_token = os.environ['BOT_TOKEN']
client.run(access_token)
