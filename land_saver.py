import os
import subprocess
from modules.lands import Land, CoordinateSystem
from modules import land_dao

LOGS_DIR = "logs"
DATA_FILE = "data.json"

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

current_process = None

def print_current_lands():
    print("현재 땅 데이터:")
    lands = land_dao.load_lands()

    if not lands:
        print("등록된 땅 데이터가 없습니다.")
    else:
        latest_land = lands[-1]
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

        new_land = Land(li, 0)
        lands = land_dao.load_lands()
        lands.append(new_land)
        land_dao.save_lands(lands)
        land_dao.save_log(lands)
        print("저장을 완료했습니다.")
        print_current_lands()

    except ValueError:
        print("유효한 숫자를 입력해주세요.")

def input_servo_angle():
    lands = land_dao.load_lands()

    if not lands:
        print("등록된 땅 데이터가 없습니다.")
        return

    print("현재 땅 데이터:")
    latest_land = lands[-1]
    for vertex in latest_land.coordinates:
        print(f"latitude: {vertex.lat}, longitude: {vertex.lon}")
    print(f"서보모터 각도: {latest_land.servo_motor_angle}")

    try:
        angle = int(input("변경할 서보모터 각도를 입력하세요: "))
        print(f"이전 각도: {latest_land.servo_motor_angle}")
        latest_land.servo_motor_angle = angle
        print(f"변경된 각도: {latest_land.servo_motor_angle}")
        land_dao.save_lands(lands)
        land_dao.save_log(lands)
        print("서보모터 각도를 저장했습니다.")
        print_current_lands()

    except ValueError:
        print("숫자를 입력해주세요.")

def view_current_settings():
    lands = land_dao.load_lands()
    if lands:
        latest_land = lands[-1]
        print(f"서보모터 각도: {latest_land.servo_motor_angle}")
        print("꼭짓점 좌표:")
        for vertex in latest_land.coordinates:
            print(f"latitude: {vertex.lat}, longitude: {vertex.lon}")
    else:
        print("등록된 땅 데이터가 없습니다.")

def start_manual_mode():
    global current_process

    try:
        if current_process and current_process.poll() is None:
            current_process.terminate()
            current_process.wait()
            print("이전 서비스를 종료했습니다.")

        current_process = subprocess.Popen(["python3", "/home/user/dronekit_seed-master/modules/manual_servo_motor_operation.py"])
        print("수동 모드를 백그라운드에서 시작합니다.")

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

def start_auto_mode():
    global current_process

    try:
        if current_process and current_process.poll() is None:
            current_process.terminate()
            current_process.wait()
            print("이전 서비스를 종료했습니다.")

        current_process = subprocess.Popen(["python3", "/home/user/dronekit_seed-master/seed_start.py", "speed_servo"])
        print("자동 모드를 백그라운드에서 시작합니다.")

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

def stop_current_process():
    global current_process, manual_mode_active, auto_mode_active

    if current_process and current_process.poll() is None:
        current_process.terminate()
        current_process.wait()
        print("현재 작업 중인 백그라운드 프로세스를 종료했습니다.")
        manual_mode_active = False
        auto_mode_active = False
    else:
        print("현재 실행 중인 프로세스가 없습니다.")

def main():
    global manual_mode_active, auto_mode_active
    manual_mode_active = False
    auto_mode_active = False

    while True:
        print("\n메뉴를 선택하세요:")
        print("1: 땅 좌표값 입력")
        print("2: 서보모터 각도 입력")
        print("3: 지정된 좌표 및 서보모터 각도 보기")
        print("4: 자동 모드 시작")
        print("5: 수동 모드 시작")
        print("6: 현재 작업 중인 백그라운드 프로세스 종료 및 메뉴 재표시")
        print("7: 종료")

        choice = input("선택: ")

        if choice == '1':
            input_land()
        elif choice == '2':
            input_servo_angle()
        elif choice == '3':
            view_current_settings()
        elif choice == '4':
            if auto_mode_active:
                print("자동 모드가 이미 활성화되어 있습니다.")
            else:
                start_auto_mode()
                auto_mode_active = True
                manual_mode_active = False
        elif choice == '5':
            if manual_mode_active:
                print("수동 모드가 이미 백그라운드에서 실행 중입니다.")
            else:
                start_manual_mode()
                manual_mode_active = True
                auto_mode_active = False
        elif choice == '6':
            stop_current_process()
        elif choice == '7':
            print("프로그램을 종료합니다.")
            stop_current_process()
            break
        else:
            print("잘못된 선택입니다. 다시 선택해주세요.")

if __name__ == "__main__":
    main()
