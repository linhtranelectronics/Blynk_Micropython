import machine
import time
import random
import network
import BlynkLib

# --- CẤU HÌNH THÔNG TIN KẾT NỐI ---
WIFI_SSID = "Linhtran"
WIFI_PASS = "123454321"
BLYNK_AUTH = "e8TjoaAnN_tD3Eu1gP_VsEZhVq_M0eyl"

# --- CẤU HÌNH PHẦN CỨNG ESP32 ---
LED_PIN = 8        # Đèn nối chân số 8
PUMP_PIN = 21      # Bơm nối chân số 21
BUTTON_PIN = 4     # Nút nhấn nối chân số 4

led = machine.Pin(LED_PIN, machine.Pin.OUT)
pump = machine.Pin(PUMP_PIN, machine.Pin.OUT)
button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

# --- BIẾN LƯU TRỰ TRẠNG THÁI ---
led_state = 0
pump_state = 0
last_button_state = 1 
hum_threshold = 0  

# --- KẾT NỐI WIFI ---
print("Dang ket noi Wifi...")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASS)

while not wlan.isconnected():
    time.sleep(0.5)
    print(".", end="")
print("\nWifi da ket noi! IP:", wlan.ifconfig()[0])

# --- KHỞI TẠO BLYNK CHUẨN THƯ VIỆN V1.0.0 ---
# Đặt insecure=True để bỏ qua SSL lỗi context, ép chạy cổng 80
# Trỏ trực tiếp server về cụm Châu Á 'sgp1.blynk.cloud' để thiết bị báo Online ngay lập tức
blynk = BlynkLib.Blynk(BLYNK_AUTH, server='sgp1.blynk.cloud', insecure=True)

# --- XỬ LÝ SỰ KIỆN TỪ BLYNK APP (Theo cấu trúc chuẩn của V1.0.0) ---

# 1. Điều khiển BƠM từ chân ảo V2
@blynk.on('V2')
def write_v2_handler(value):
    global pump_state
    pump_state = int(value[0])
    pump.value(pump_state) 
    print(f"May bom (GPIO 21) duoc dieu khien tu Blynk: {pump_state}")

# 2. Điều khiển ĐÈN từ chân ảo V3
@blynk.on('V3')
def write_v3_handler(value):
    global led_state
    led_state = int(value[0])
    led.value(led_state)   
    print(f"Den (GPIO 8) duoc dieu khien tu Blynk: {led_state}")

# 3. Đọc giá trị CÀI ĐẶT ĐỘ ẨM từ Slider V4
@blynk.on('V4')
def write_v4_handler(value):
    global hum_threshold
    hum_threshold = int(value[0]) 
    print(f"Nguong do am duoc cap nhat tu Slider (V4): {hum_threshold}%")

# 4. Tự động đồng bộ trạng thái khi kết nối thành công tới Blynk Server
@blynk.on('connected')
def connect_handler(*args, **kwargs):
    print("Da ket noi toi Blynk Server! Dang dong bo du lieu ban dau...")
    blynk.sync_virtual(2, 3, 4) # Đồng bộ trạng thái V2, V3, V4 theo hàm chuẩn của thư viện mới

# --- BIẾN PHỤ TRỢ CHO CHU KỲ GỬI DỮ LIỆU ---
last_send_time = 0
send_interval = 5000 

print("He thong bat dau chay...")

# --- VÒNG LẶP CHÍNH ---
while True:
    blynk.run()
    current_time = time.ticks_ms()
    
    # [TÍNH NĂNG 1] Đọc nút nhấn vật lý (Chân số 4) để đảo trạng thái ĐÈN (V3)
    button_state = button.value()
    if button_state != last_button_state:
        time.sleep_ms(50) # Debounce
        if button.value() == button_state: 
            if button_state == 0: # Nút được bấm (kéo xuống GND)
                led_state = 1 - led_state
                led.value(led_state)
                
                # Cập nhật ngược lại giao diện Blynk
                blynk.virtual_write(3, led_state)
                print(f"Nut nhan physical duoc bam. Chuyen trang thai den sang: {led_state}")
            last_button_state = button_state

    # [TÍNH NĂNG 2] Gửi dữ liệu cảm biến ngẫu nhiên theo chu kỳ
    if time.ticks_diff(current_time, last_send_time) > send_interval:
        random_temp = random.randint(20, 45)  
        random_hum = random.randint(40, 95)   
        
        blynk.virtual_write(0, random_temp) # V0: Nhiet do
        blynk.run()
        blynk.virtual_write(1, random_hum)  # V1: Do am
        blynk.run()
        
        print(f"Da cap nhat -> Nhiet do (V0): {random_temp}°C | Do am (V1): {random_hum}%")
        last_send_time = current_time
