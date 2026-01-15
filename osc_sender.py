# osc_sender.py
from pythonosc.udp_client import SimpleUDPClient

VSEE_IP = "127.0.0.1"
VSEE_PORT = 39539  # ← VSeeFaceのVMC receiverのポートと同じにする

client = SimpleUDPClient(VSEE_IP, VSEE_PORT)

def send_expression(name: str, value: float):
    # VMC: Blendshape value
    client.send_message("/VMC/Ext/Blend/Val", [name, float(value)])
    # これが無いと反映されない環境があるので「Apply」も投げる
    client.send_message("/VMC/Ext/Blend/Apply", 1)

def clear_all():
    # よく使うプリセットを0に戻す（必要なら増やしてOK）
    for k in ["Neutral", "Joy", "Angry", "Sorrow", "Fun", "Surprise"]:
        client.send_message("/VMC/Ext/Blend/Val", [k, 0.0])
    client.send_message("/VMC/Ext/Blend/Apply", 1)
