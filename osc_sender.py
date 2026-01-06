from pythonosc import udp_client
import time

# VNyAN の OSC 設定に合わせる
VNYAN_IP = "127.0.0.1"
VNYAN_PORT = 28569

client = udp_client.SimpleUDPClient(VNYAN_IP, VNYAN_PORT)

print("OSC send test start")

while True:
    # 頭を左右に振るテスト
    client.send_message("/avatar/parameters/HeadYaw", 0.5)
    time.sleep(1)
    client.send_message("/avatar/parameters/HeadYaw", -0.5)
    time.sleep(1)
