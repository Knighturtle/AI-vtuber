from osc_sender import send_expression, clear_all
import time

clear_all()
time.sleep(0.5)

print("Joy ON")
send_expression("Joy", 1.0)
time.sleep(2)

print("Joy OFF")
send_expression("Joy", 0.0)
time.sleep(1)

print("done")
input("enter")
