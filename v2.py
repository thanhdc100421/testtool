import threading,subprocess
from datetime import datetime
from  xml.dom.minidom import parse
import time
import uiautomator2 as u2
class Auto:
    def __init__(self,handle):
        self.handle = handle
    def screen_capture(self):
        #os.system(f'adb -s {self.handle} exec-out screencap -p > {name}.png')
        pipe = subprocess.Popen(f'adb -s {self.handle} exec-out screencap -p',
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, shell=True)
        #image_bytes = pipe.stdout.read().replace(b'\r\n', b'\n')
        image_bytes = pipe.stdout.read()
        image = cv2.imdecode(np.fromstring(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        return image
    def changeProxy(self, ip):
        """
        Input Proxy Http IP:PORT
        Thêm Proxy Http IP:PORT
        """
        subprocess.call(f'adb -s {self.handle} shell settings put global http_proxy {ip}', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def remProxy(self):
        """
        Input Proxy Http IP:PORT
        Thêm Proxy Http IP:PORT
        """
        subprocess.call(f'adb -s {self.handle} shell settings put global http_proxy :0', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def click(self,x,y):
        subprocess.call(f'adb -s {self.handle} shell input tap {x} {y}', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    def swipe(self, x1, y1, x2, y2):
        subprocess.call(f"adb -s {self.handle} shell input touchscreen swipe {x1} {y1} {x2} {y2} 1000", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    def Back(self):
        subprocess.call(f"adb -s {self.handle} shell input keyevent 4", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    def DeleteCache(self, package):
        subprocess.check_output(f"adb -s {self.handle} shell pm clear {package}", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    def off(self, package):
        subprocess.call(f"adb -s {self.handle} shell am force-stop {package}", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    def InpuText(self, text=None, VN=None):
        if text == None:
            text =  str(base64.b64encode(VN.encode('utf-8')))[1:]
            subprocess.call(f"adb -s {self.handle} shell ime set com.android.adbkeyboard/.AdbIME", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            subprocess.call(f"adb -s {self.handle} shell am broadcast -a ADB_INPUT_B64 --es msg {text}", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            return
        subprocess.call(f"adb -s {self.handle} shell input text '{text}'", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    def find(self,img='',threshold=0.99):
        img = cv2.imread(img) #sys.path[0]+"/"+img)
        img2 = self.screen_capture()    
        result = cv2.matchTemplate(img,img2,cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        retVal = list(zip(*loc[::-1]))
        #image = cv2.rectangle(img2, retVal[0],(retVal[0][0]+img.shape[0],retVal[0][1]+img.shape[1]), (0,250,0), 2)
        #cv2.imshow("test",image)
        #cv2.waitKey(0)
        #cv2.destroyWindow("test")
        return retVal
    def tapimg(self,img='',tap='',threshold=0.99):
        img = cv2.imread(img) #sys.path[0]+"/"+img)
        tap = cv2.imread(tap)
        img2 = self.screen_capture()    
        result = cv2.matchTemplate(img,img2,cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        retVal = list(zip(*loc[::-1]))
        result2 = cv2.matchTemplate(img,tap,cv2.TM_CCOEFF_NORMED)
        loc2 = np.where(result2 >= threshold)
        retVal2 = list(zip(*loc2[::-1]))
        if retVal > [(0, 0)]:
            self.click(retVal2[0][0],retVal2[0][1])
        else:
            return 0
    def slideCaptcha(self,x,y):
        # adb.excuteAdb(sr, "adb shell screencap -p /sdcard/cap.png")
        # adb.excuteAdb(sr, f"adb pull /sdcard/cap.png {sr}/captcha.png")
        captcha = bypass_slide(self.handle)
        self.swipe(round(x), round(y), int(x)+int(captcha), round(y))
        return True
    def showDevice(self, width: int, height: int, x:int , y: int, title: str):
        """Hiển thị điện thoại của bạn lên màn hình máy tính"""
        subprocess.Popen(f'scrcpy -s {self.handle} --window-title "{title}" --window-x {x} --window-y {y} --window-width {width} --window-height {height}', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    def DumpXML(self):
        name = self.handle
        if ":" in self.handle:
            name = name.replace(":", "").replace(".", "")
        #print(name)
        os.system(f"adb -s {self.handle} shell uiautomator dump && adb -s {self.handle} pull /sdcard/window_dump.xml {name}.xml")
        return name
    def GetXml(self):
        self.DumpXML()
        with parse(self.handle.replace(":", "").replace(".", "")+".xml") as file:
            node = file.getElementsByTagName("node")
            for element in node:
                text = element.getAttribute("text")
                classname = element.getAttribute("class")
                contentdesc = element.getAttribute("content-desc")
                print(classname, text, contentdesc)

    def TapXml(self, text=None, classname=None, content=None, taps=1, typesearch="text&class"):
        self.DumpXML()
        devices = self.handle
        with parse(devices.replace(":", "").replace(".", "")+".xml") as file:
            node = file.getElementsByTagName("node")
            for element in node:
                name = element.getAttribute("text")
                classnames = element.getAttribute("class")
                contentdesc = element.getAttribute("content-desc")
                x, y = element.getAttribute("bounds").split("][")[0].replace("[", "").split(",")
                if name == text and classnames == classname and typesearch == "text&class" or typesearch == "text&class":
                    print("x:"+x, "y:"+y, "Text:"+name)
                    for tap in range(taps):
                        self.click(x, y)
                elif contentdesc == content and classnames == classname and typesearch == "content&class" or typesearch == "class&content":
                    print("x:"+x, "y:"+y, "Text:"+name)
                    for tap in range(taps):
                        self.Click(x, y)
                elif name == text and contentdesc == content and typesearch == "content&text" or typesearch == "text&content":
                    print("x:"+x, "y:"+y, "Text:"+name)
                    for tap in range(taps):
                        self.Click(x, y)
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
soLD = ["1",'2','3','4']

class starts(threading.Thread):
    def __init__(self, device,stt,so_luong):
        super().__init__()
        self.device = device
        self.stt = stt
        self.so_luong = so_luong
    def run(self):
        device = self.device
        stt = self.stt
        so_luong = self.so_luong
        f =open('filedata.txt','a')
        # self.data_max = data_max

        def step1(device):
            d2 = Auto(device)
            d = u2.connect(device)
            d.xpath("//*[@content-desc='Create New Contact']")\
            .click(timeout=5)
            print(" \033[1;31m |\033[1;37m[",self.device,"]\033[1;31m Click Add")
            d(className= "android.widget.EditText" , index = 0).set_text(sdt[stt])
            d(className= "android.widget.EditText" , index = 4).set_text(sdt[stt])
            d(text="Create Contact").click()
            time.sleep(1)
            if  d(text="Cancel"):
                d(text="Cancel").click()
                time.sleep(0.5)
                d2.Back()
            else:
                f.writelines([sdt[stt]])
                f.close()
           
           
            d2.Back()
           
            
            
                       
                       
            # print(device,so_luong)
            # for k in range(stt,4,thread_count):
                 
            #         print(device,"-",k)
            #     #     time.sleep(1)
            #     #     print(f"\033[1;31m "":",sdt[k],"")
                
           

        step1(device)
        
    
                
        # print(device)
        # for i in range(phonenumber):
        # for j in range(m,len(sdt),thread_count):
        #     phone = sdt[j].strip()
        #     time.sleep(0.2)
        # print(f"{device}: {phonenum} ")
        # def batdau(device):
            
        #     d = u2.connect(device)
        #     d.xpath("//*[@content-desc='Create New Contact']")\
        #     .click()
        #     d(className= "android.widget.EditText" , index = 0).set_text(data_max)
        #     d(className= "android.widget.EditText" , index = 4).set_text(data_max)
        #     time.sleep(0.5)
        #     d(text="Create Contact").click()
        #     print(" \033[1;31m |\033[1;37m[",self.nameLD,"]\033[1;31m Add Contact | Time:", time.ctime(time.time()))
        #     d.press("back")
        #     time.sleep(1)
        #     d.press("back")
        # batdau(device)


def main(m):
      
        device = GetDevices()[m]
       
        n = 0
        
       
        for i in range(m,len(sdt),thread_count):
            n+=1
            run = starts(device,i,n)
            run.run()
        
            
for m in range(thread_count):    
    threading.Thread(target=main, args=(m,)).start()
