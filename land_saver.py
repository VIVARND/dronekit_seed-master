import os
import subprocess
from modules.lands import Land, CoordinateSystem
from modules import land_dao

LOGS_DIR = "logs"
DATA_FILE = "data.json"

# 로그 디렉토리가 없으면 생성
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

def print_current_lands():
    print("현재 땅 데이터:")
    lands = land_dao.load_lands()

    if not lands:
        print("등록된 땅 데이터가 없습니다.")
    else:
        latest_land = lands[-1]  # 최신 땅 데이터 가져오기
        print(f"서보모터 각도: {latest_land.servo_motor_angle}")
        print("꼭짓점 좌표:")
        for vertex in latest_land.coordinates:
            print(f"latitude: {vertex.lat}, longitude: {vertex.lon}")

def input_land():
    print("땅의 꼭짓점 4개(lat, lon)를 입력해주세요, 직사각형을 기반으로 합니다.")
    print("입력 예시: 12.3, 12.3")

    try:
        li = []

        lat, lon = map(float, input("꼭짓점 1 입력: ").split(","))
        li.append(CoordinateSystem(lat, lon))

        lat, lon = map(float, input("꼭짓점 2 입력: ").split(","))
        li.append(CoordinateSystem(lat, lon))

        lat, lon = map(float, input("꼭짓점 3 입력: ").split(","))
        li.append(CoordinateSystem(lat, lon))

        lat, lon = map(float, input("꼭짓점 4 입력: ").split(","))
        li.append(CoordinateSystem(lat, lon))

        new_land = Land(li, 0)  # 서보모터 각도는 초기값으로 설정
        lands = land_dao.load_lands()
        lands.append(new_land)
        land_dao.save_lands(lands)
        land_dao.save_log(lands)  # 로그 저장 추가
        print("저장을 완료했습니다.")
        print_current_lands()  # 최신 데이터 출력 추가

    except ValueError:
        print("유효한 숫자를 입력해주세요.")

def input_servo_angle():
    lands = land_dao.load_lands()

    if not lands:
        print("등록된 땅 데이터가 없습니다.")
        return

    print("현재 땅 데이터:")
    latest_land = lands[-1]  # 최신 땅 데이터 가져오기
    for vertex in latest_land.coordinates:
        print(f"latitude: {vertex.lat}, longitude: {vertex.lon}")
    print(f"서보모터 각도: {latest_land.servo_motor_angle}")

    try:
        angle = int(input("변경할 서보모터 각도를 입력하세요: "))
        latest_land.servo_motor_angle = angle
        land_dao.save_lands(lands)
        land_dao.save_log(lands)  # 로그 저장 추가
        print("서보모터 각도를 저장했습니다.")
        print_current_lands()  # 최신 데이터 출력 추가

    except ValueError:
        print("숫자를 입력해주세요.")

def start_manual_mode():
    try:
        subprocess.run(["python3", "/home/user/dronekit_seed-master/modules/manual_servo_motor_operation.py"])
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

def start_speed_servo_mode(menu_name):
    try:
        subprocess.run(["python3", "/home/user/dronekit_seed-master/seed_start.py", menu_name])
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

def main():
    # 상태 플래그 초기화
    manual_mode_active = False
    speed_servo_mode_active = False

    while True:
        print("\n메뉴를 선택하세요:")
        print("1: 땅 좌표값 입력")
        print("2: 서보모터 각도 입력")
        print("3: 드론 비행 속도연동 서보모터비레 제어")
        print("4: 수동 모드")
        print("5: 종료")

        choice = input("선택: ")

        if choice == '1':
            input_land()
        elif choice == '2':
            if speed_servo_mode_active:
                print("속도 서보모터 제어 모드가 활성화되어 있습니다. 종료 후 다시 시도해주세요.")
            else:
                input_servo_angle()
        elif choice == '3':
            if manual_mode_active:
                print("수동 모드가 활성화되어 있습니다. 종료 후 다시 시도해주세요.")
            else:
                print("속도로 서보모터 제어 모드입니다.")
                speed_servo_mode_active = True
                start_speed_servo_mode("speed_servo")
                speed_servo_mode_active = False  # 실행 후 비활성화
        elif choice == '4':
            if speed_servo_mode_active:
                print("속도 서보모터 제어 모드가 활성화되어 있습니다. 종료 후 다시 시도해주세요.")
            else:
                print("수동 모드를 시작합니다.")
                manual_mode_active = True
                start_manual_mode()
                manual_mode_active = False  # 실행 후 비활성화
        elif choice == '5':
            print("종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 다시 선택해주세요.")

if __name__ == "__main__":
    main()
