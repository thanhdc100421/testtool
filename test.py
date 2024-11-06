import threading,subprocess
from datetime import datetime
from  xml.dom.minidom import parse
import time
import uiautomator2 as u2
def GetDevices():
        devices = subprocess.check_output("adb devices")
        p = str(devices).replace("b'List of devices attached","").replace('\\r\\n',"").replace(" ","").replace("'","").replace('b*daemonnotrunning.startingitnowonport5037**daemonstartedsuccessfully*Listofdevicesattached',"")
        if int(len(p)) > 0:
            listDevices = p.split("\\tdevice")
            listDevices.pop()
            return listDevices
        else:
            return 
GetDevices()
thread_count = len(GetDevices())
sdt = open("data.txt").readlines()

class starts(threading.Thread):
    def __init__(self, device):
        super().__init__()
        self.device = device
       
       
    def run(self,data_max):
        device = self.device
        # self.data_max = data_max
        
       
        # print(device)
        # for i in range(phonenumber):
        # for j in range(m,len(sdt),thread_count):
        #     phone = sdt[j].strip()
        #     time.sleep(0.2)
        # print(f"{device}: {phonenum} ")
        def step1(device):
            
            d = u2.connect(device)
            d.xpath("//*[@content-desc='Create New Contact']")\
            .click(timeout=5)
            print(" \033[1;31m |\033[1;37m[",self.device,"]\033[1;31m Click Add")
            d(className= "android.widget.EditText" , index = 0).set_text(data_max)
            d(className= "android.widget.EditText" , index = 4).set_text(data_max)
            time.sleep(0.5)
            d(text="Create Contact").click()
            print(" \033[1;31m |\033[1;37m[",self.device,"]\033[1;31m ADD Contact =====>>>>  ""\033[1;32m"  ,data_max," \033[1;31m | Time:", time.ctime(time.time()))
            d.press("back")
            time.sleep(1)
            d.press("back")
        step1(device)

        

def main(m):
        device = GetDevices()[m]
        n = 0
        
        run = starts(device)
        d = u2.connect(device)
        d.app_start("org.telegram.messenger.wec")
        print(" \033[1;31m |\033[1;37m[",device,"]\033[1;31m Open Telegram 1")
        d.xpath("//*[@content-desc='New Message']").click(timeout=20)
        d(text='Not now').click(timeout=1)
        for x in range(m,len(sdt),thread_count):
            n+=1
            phone = sdt[x].strip()
            time.sleep(0.5)
            run.run(phone)
            if n == 4:break

for m in range(thread_count):
    threading.Thread(target=main, args=(m,)).start()