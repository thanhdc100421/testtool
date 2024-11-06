import uiautomator2 as u2
import time
d = u2.connect('emulator-5606') # alias for u2.connect_usb('123456f')
d.app_start("org.telegram.messenger.wec")
d.xpath("//*[@content-desc='New Message']").click(timeout=5)
# Select the object with text 'Clock' and its className is 'android.widget.TextView'
d(text='Not now').click(timeout=1)
d.xpath("//*[@content-desc='Create New Contact']")\
.click()
time.sleep(1)
# get the children or grandchildren
d(className= "android.widget.EditText" , index = 0).set_text("34534543")
d(className= "android.widget.EditText" , index = 4).set_text("34534543")
time.sleep(0.5)
d(text="Create Contact").click()
print(d.info)
