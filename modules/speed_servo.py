import sys
from modules.servo_motor import ServoMotor

# ServoMotor 객체 생성
servo_motor = ServoMotor()

def control_servo_with_speed(average_speed):
    try:
        if average_speed >= 0 and average_speed <= 10.00:
            angle = 0  # 0도
        elif average_speed > 10.00 and average_speed <= 20.00:
            angle = 80  # 80도
        elif average_speed > 20.00 and average_speed <= 50.00:
            angle = 140  # 140도
        else:
            angle = None  # 범위 밖이면 서보모터 멈춤
        
        if angle is not None:
            servo_motor.change_angle(angle)
            print(f"속도로 서보모터 제어: 속도 {average_speed} m/s에 따라 각도 {angle}도로 설정됨")
        else:
            print("속도가 범위를 벗어났습니다. 서보모터 멈춤")

    except Exception as e:
        print(f"서보모터 제어 중 오류 발생: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 speed_servo.py <average_speed>")
        sys.exit(1)
    
    average_speed = float(sys.argv[1])
    control_servo_with_speed(average_speed)
