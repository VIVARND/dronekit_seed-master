import RPi.GPIO as GPIO

class ServoMotor:
    MIN_ANGLE = 0
    MAX_ANGLE = 140
    MIN_DUTY_CYCLE = 3.0  # 0도에 해당하는 듀티 사이클
    MAX_DUTY_CYCLE = 9.0  # 140도에 해당하는 듀티 사이클

    def __init__(self):
        self.servo_pin = 27
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servo_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.servo_pin, 50)  # PWM 주파수 50Hz
        self.pwm.start(self.MIN_DUTY_CYCLE)
        self.current_angle = self.MIN_ANGLE
        self.change_angle(self.MIN_ANGLE)

    def change_angle(self, angle):
        if self.MIN_ANGLE <= angle <= self.MAX_ANGLE:
            duty_cycle = self._angle_to_duty_cycle(angle)
            print(f"서보모터 각도 변경: {angle}도")
            self.pwm.ChangeDutyCycle(duty_cycle)
            self.current_angle = angle
        else:
            print(f"유효하지 않은 서보모터 각도: {angle}. 0도로 설정합니다.")
            self.change_angle(self.MIN_ANGLE)

    def _angle_to_duty_cycle(self, angle):
        return self.MIN_DUTY_CYCLE + (self.MAX_DUTY_CYCLE - self.MIN_DUTY_CYCLE) * (angle / self.MAX_ANGLE)

    def __del__(self):
        self.pwm.stop()
        GPIO.cleanup()
        print("연결된 pwm이 clean 됩니다")
