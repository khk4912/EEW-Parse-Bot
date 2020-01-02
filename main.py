from selenium import webdriver
import time
import os
import threading
from multiprocessing import Process, Value, Array, Queue, freeze_support
import discord
import asyncio

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('lang=ko_KR')
def eqcheck(q):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.weather.go.kr/pews/")
    driver.implicitly_wait(6)
    print("## EEW side started.")
    while True:
        menu = driver.find_element_by_css_selector("#phase")
        class_name = menu.get_attribute("class")        
        if class_name == "phase_wrap noticeP2":
            while True:
                class_name = menu.get_attribute("class")
                print("class_name_getted")
                if class_name == "phase_wrap noticeP3":
                    fst = driver.find_element_by_xpath(
                        '''//*[@id="eqkStr"]''').text
                    sec = driver.find_element_by_xpath(
                        '''//*[@id="eqkOcr"]''').text
                    maxx = driver.find_element_by_xpath('''//*[@id="magVal"]''').text
                    maxarea = driver.find_element_by_xpath('''//*[@id="maxArea"]''').text
                    print("\n\n")
                    q.put([3, fst, sec, maxx, maxarea])
                    print("##### 상세지진정보 분석 완료!")
                    print("{} {}".format(fst, sec))
                            
                    break

                origin = driver.find_element_by_xpath(
                    '''//*[@id="origin"]''').text
                gyumo = driver.find_element_by_xpath(
                    '''//*[@id="estScl"]''').text
                jindo = driver.find_element_by_xpath(
                    '''//*[@id="estMag"]''').text
                myjindo = driver.find_element_by_xpath(
                    '''//*[@id="myMag"]''').text
                what = driver.find_element_by_xpath(
                    '''//*[@id="ntcMsg"]''').text
                tme = driver.find_element_by_xpath(
                    '''//*[@id="eta"]''').text
                evtime = driver.find_element_by_xpath('''//*[@id="occur"]''').text
                print("get_contents")                
                q.put([2, origin, gyumo, jindo, myjindo, what, tme, evtime])
                print("Put..")
                print("\n\n")
                print("###### 지진속보 발령!")
                print("{}".format(origin))
                print("추정규모 : {}M\n최대예상진도 : {}".format(gyumo, jindo))
                print("{} {} / 예상진도 {}".format(what, tme, myjindo))
                time.sleep(2)


        q.put([1])
        time.sleep(2)


class KMA(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.check_earthquake())
    async def check_earthquake(self):
        await self.wait_until_ready()
        while True:
            await asyncio.sleep(2)
            content = q.get()
            if content[0] == 2:
                ten = await self.channel.send("@everyone")
                targetmsg = await self.channel.send("⚠️ 지진 속보 발생... 알림 준비 중..")
                self.msg = targetmsg
                await ten.delete()

                while True:
                    if content[0] != 2:
                        embed=discord.Embed(title="✅ 상세 지진정보 분석 완료됨.", description="> {} {}".format(content[2], content[1]), color=0x25da21)
                        embed.add_field(name="최대진도", value="{} ({})".format(content[3], content[4]))
                        embed.add_field(name="상세정보", value="[클릭](https://www.weather.go.kr/w/eqk-vol/recent-eqk.do)")
                        await self.channel.send(embed=embed)
                        # await self.channel.send("계기진도정보", file=discord.File(content[5]))
                        break

                    embed=discord.Embed(title="📢 지진 속보 발령됨!", description="{}".format(content[7]), color=0xfb0000)
                    embed.add_field(name="발생지", value="{}".format(content[1]))
                    embed.add_field(name="예상규모", value="{}M".format(content[2]), inline=False)
                    embed.add_field(name="예상진도정보", value="> **예상최대진도** : {}\n> **서울시 중구 예상진도** : {}".format(content[3], content[4]), inline=False)
                    embed.add_field(name="추가 정보", value="**{}** : {}".format(content[5], content[6]))
                    await self.send_discord(embed)
                    content = q.get()
    async def send_discord(self, message):
        await self.msg.edit(embed=message, content=None)
    
    
    async def on_ready(self):
        self.msgid = 659710148503404546
        self.channelid = 659702113370243073
        self.channel = client.get_channel(self.channelid)
        self.msg = await client.channel.fetch_message(self.msgid)

        print("## Discord side started.")

    async def on_message(self, message):
        if message.content == "!":
            await message.channel.send("정상작동중")

if __name__ == '__main__':
    freeze_support()
    procs = []
    global q
    q = Queue()
    proc = Process(target=eqcheck, args=(q,))
    procs.append(proc)
    proc.start()
    global client
    client = KMA()
    client.run("MyScreet")