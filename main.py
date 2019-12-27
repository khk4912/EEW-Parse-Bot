from selenium import webdriver
import time
import os
from multiprocessing import Process, Value, Array, Queue, freeze_support
import discord
import asyncio


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('lang=ko_KR')
def eqcheck(q):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("mysecret")
    driver.implicitly_wait(6)
    page = driver.find_element_by_id("iframe")

    driver.switch_to_frame(page)
    print("## EEW started")
    while True:
        menu = driver.find_element_by_css_selector("#phase")
        class_name = menu.get_attribute("class")        # print(class_name)
        if class_name == "phase_wrap noticeP2":
            while True:
                class_name = menu.get_attribute("class")
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
                # os.system("cls")
                q.put([2, origin, gyumo, jindo, myjindo, what, tme, evtime])
                print("Put..")
                print("\n\n")
                print("###### 지진조기경보 발령!")
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
                        txt = """
### 상세 지진정보 분석 완료됨.
{} {}
최대진도 {} ({})
                            """.format(content[2], content[1], content[3], content[4])
                        await self.channel.send(txt)
                        break

                    txt = """
    ### 지진조기경보 발령!

    {}
    발생지 : {}
    예상규모 : {}M
    예상최대진도 : {}
    서울시 동작구 예상진도 : {}
    {} : {}

                    """.format(content[7], content[1], content[2], content[3], content[4], content[5], content[6])
                    await self.send_discord(txt)
                    content = q.get()
    async def send_discord(self, message):
        await self.msg.edit(content=message)
    
    
    async def on_ready(self):
        self.msgid = 
        self.channelid = 
        self.channel = client.get_channel(self.channelid)
        self.msg = await client.channel.fetch_message(self.msgid)

        print("## Discord logged in.")

    async def on_message(self, message):
        if message.content == "!":
            await message.channel.send("wow")

if __name__ == '__main__':
    freeze_support()
    procs = []
    global q
    q = Queue()
    proc = Process(target=eqcheck, args=(q,))
    procs.append(proc)
    proc.start()
    client = KMA()
    client.run("mysecret")