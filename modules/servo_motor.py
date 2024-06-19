import RPi.GPIO as GPIO

DUTY_CYCLE_BY_ANGLE = {
    0: 3.0, 20: 4.0, 40: 5.0, 60: 6.0, 80: 7.0, 115: 8.0, 140: 9.0
}

class ServoMotor:

    def __init__(self):
        self.servo_pin = 27
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servo_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.servo_pin, 50)
        self.pwm.start(DUTY_CYCLE_BY_ANGLE[0])
        self.current_angle = 0
        self.change_angle(0)  # 초기 각도 설정

    def change_angle(self, angle):
        if angle != self.current_angle:
            if angle not in DUTY_CYCLE_BY_ANGLE:
                raise RuntimeError(f"없는 값을 입력했습니다. number: {angle}")
            print(f"각도를 변경합니다 new: {angle}")
            self.pwm.ChangeDutyCycle(DUTY_CYCLE_BY_ANGLE[angle])
            self.current_angle = angle

    def __del__(self):
        self.pwm.stop()
        GPIO.cleanup()
        print("연결된 pwm이 clean 됩니다")
