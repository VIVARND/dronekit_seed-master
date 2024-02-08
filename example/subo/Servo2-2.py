### 【 라즈이노 IoT 】
### (실습 2-2) 서보모터 각도 조절해 보기2 (0도, 45도, 90도, 135도 , 180도,...역순으로 조절하기)
### 학습 자료 제공 페이지 : Rasino.tistory.com/341
# 서보는 PWM을 20ms(50hz) 주기로 동작시키고 펄스 폭(duty)만 조절해 위치(각도)를 조절함.
# 여기서 duty는 1주기 동안 High를 유지하는 기간이며, 
# 20ms 주기에 100% 면 20ms가 되는 것이고 10% 면 2ms 5% 면 1ms가 됨.
# 펄스 폭은 1ms 일때 0도 2ms 일때 180도, 중간값 1.5ms 일때 90도로 이동함.
# 단, 저렴한 서보는 3%~12%(0도~180도)의 동작 특성을 가짐.
# 만약 모터가 떨린다면, 이 범위를 벗어났기 때문이며, 0도에서 떨린다면
# 3%값에서 조금 올려주고, 180도에서 떨린다면 12%에서 값을 조금 내려주면 됨.
import RPi.GPIO as GPIO
import time
servo_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # 50Hz (서보모터 PWM 동작을 위한 주파수)
pwm.start(3.0) #서보의 0도 위치(0.6ms)이동:값 3.0은 pwm주기인 20ms의 3%를 의미하므로,0.6ms됨.
timeA = 0.6

for cnt in range(0, 3) :       # 0부터 3미만까지(3번) for문의 내용을 반복
    pwm.ChangeDutyCycle(3.0)   # 서보모터를 0도로 회전(이동)
    time.sleep(timeA)            # 서보 모터가 이동할 시간을 줌
    pwm.ChangeDutyCycle(5.5)  # 서보 모터를 45도로 회전(이동)
    time.sleep(timeA)            # 서보 모터가 이동할 시간을 줌
    pwm.ChangeDutyCycle(7.5)  # 서보 모터를 90도로 회전(이동)
    time.sleep(timeA)            # 서보 모터가 이동할 시간을 줌
    pwm.ChangeDutyCycle(9.5)  # 서보 모터를 135도로 회전(이동)
    time.sleep(timeA)            # 서보 모터가 이동할 시간을 줌    
    pwm.ChangeDutyCycle(12.5)  # 서보 모터를 180도로 회전(이동)
    time.sleep(timeA)            # 서보 모터가 이동할 시간을 줌
    pwm.ChangeDutyCycle(9.5)  # 서보 모터를 135도로 회전(이동)
    time.sleep(timeA)            # 서보 모터가 이동할 시간을 줌    
    pwm.ChangeDutyCycle(7.5)  # 서보 모터를 90도로 회전(이동)
    time.sleep(timeA)            # 서보 모터가 이동할 시간을 줌
    pwm.ChangeDutyCycle(5.5)  # 서보 모터를 45도로 회전(이동)
    time.sleep(timeA)            # 서보 모터가 이동할 시간을 줌
    pwm.ChangeDutyCycle(3.0)   # 서보모터를 0도로 회전(이동)
    time.sleep(timeA)            # 서보 모터가 이동할 시간을 줌

pwm.ChangeDutyCycle(0.0)
pwm.stop()
GPIO.cleanup()
