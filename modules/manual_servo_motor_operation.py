import lgpio
import time

# 사용할 GPIO 핀 번호를 설정.
RC_PIN = 17  # RC 수신기의 신호 핀 번호
SERVO_PIN = 27  # 서보 모터의 신호 핀 번호

# GPIO 핸들 생성 및 핀 설정
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_input(h, RC_PIN)  # RC_PIN을 입력 모드로 설정.

# 서보 모터를 제어하는 클래스를 정의.
class ServoControl:
    def __init__(self, h, pin):
        self.h = h
        self.pin = pin
        lgpio.gpio_claim_output(self.h, self.pin)  # GPIO 핀을 출력 모드로 설정.
        self.servo_pwm = lgpio.tx_pwm(self.h, self.pin, 50, 0)  # PWM 객체를 생성. 주파수는 50Hz, 초기 듀티 사이클은 0으로 설정.

    def set_duty_cycle(self, duty_cycle):
        lgpio.tx_pwm(self.h, self.pin, 50, duty_cycle)  # 듀티 사이클을 설정.
        time.sleep(0.2)  # 안정화를 위해 잠시 대기.

    def set_angle(self, angle):
        # 주어진 각도를 듀티 사이클로 변환.
        duty_cycle = (angle / 180.0) * 10 + 2.5  # 2% 대신 2.5% 사용
        self.set_duty_cycle(duty_cycle)

# ServoControl 클래스의 인스턴스를 생성합니다.
servo_manual = ServoControl(h, SERVO_PIN)

# 평균값을 사용하여 PWM 신호를 읽는 함수
def read_pwm_average(samples=10, interval=0.0001):
    pwm_values = []
    for _ in range(samples):
        pulse_start = time.time()
        pulse_end = pulse_start  # 초기화

        while lgpio.gpio_read(h, RC_PIN) == 0:
            pulse_start = time.time()
        
        while lgpio.gpio_read(h, RC_PIN) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start  # 펄스 지속 시간을 계산합니다.
        pwm_value = round(pulse_duration * 1000000)  # PWM 값으로 변환합니다.
        pwm_values.append(pwm_value)
        
        time.sleep(interval)  # 샘플 간의 시간 간격

    # 평균 PWM 값을 계산합니다.
    average_pwm = sum(pwm_values) / len(pwm_values)
    return average_pwm

try:
    while True:
        # 여러 샘플을 사용하여 평균 PWM 값 읽기
        average_pwm = read_pwm_average(samples=10, interval=0.0001)
        
        # 평균 PWM 값 출력
        print(f"현재 PWM 값: {int(average_pwm)}")
        
        # PWM 값에 따라 서보 모터 각도 설정
        if 850 <= average_pwm <= 1150:
            angle = 0  # 0도
        elif 1400 <= average_pwm <= 1600:
            angle = 50  # 80도
        elif 1800 <= average_pwm <= 2100:
            angle = 110  # 140도
        else:
            angle = None  # 그 외의 경우에는 None (서보 모터 멈춤)
        
        if angle is not None:
            servo_manual.set_angle(angle)  # 서보 모터의 각도를 설정합니다.

        # 설정된 각도 출력
        if angle is not None:
            print(f"현재 각도: {angle} 도")
        else:
            print("서보 모터 멈춤")

        time.sleep(0.5)  # 주기적으로 갱신합니다.

except KeyboardInterrupt:
    lgpio.gpiochip_close(h)  # GPIO 핸들을 정리합니다.
    print("\n프로그램을 종료합니다.")
