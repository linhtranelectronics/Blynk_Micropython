import time
import network
from machine import Pin
import BlynkLib
from time import sleep

from connectWifi import connectTo
connectTo("free", "12345678") #chỗ này điền tên wifi và mật khẩu

#chỗ này điền mã auth lấy từ device info trên trang blynk.io
BLYNK_AUTH = "JVRGgvJuGe4k7jKt7jT2mzfF9aWhHoyk" 
blynk = BlynkLib.Blynk(BLYNK_AUTH)

led = Pin(2, Pin.OUT)
btn = Pin(0, Pin.IN)
@blynk.on("V0") #nhận dữ liệu từ pin V0
def v0_read_handler(value): #read the value
	if int(value[0]) == 1:
		led.value(1) #bật đèn
	else:
		led.value(0) #tắt đèn



while True:
	blynk.run()
	
	if(btn.value() == 0): #kiểm tra trạng thái nút nhấn
		sleep(0.2)
		led.value(not led.value()) #thay đổi trạng thái đèn
		blynk.virtual_write(0, led.value()) #gửi trạng thái lên app
	


