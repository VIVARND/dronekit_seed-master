import os
import subprocess
import signal  # 시그널 모듈 추가
from modules.lands import Land, CoordinateSystem
from modules import land_dao

LOGS_DIR = "logs"
DATA_FILE = "data.json"

# 로그 디렉토리가 없으면 생성
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# 현재 실행 중인 서브프로세스를 저장할 변수
current_process = None

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
        print(f"이전 각도: {latest_land.servo_motor_angle}")  # 각도 변경 전 출력
        latest_land.servo_motor_angle = angle
        print(f"변경된 각도: {latest_land.servo_motor_angle}")  # 각도 변경 후 출력
        land_dao.save_lands(lands)
        land_dao.save_log(lands)  # 로그 저장 추가
        print("서보모터 각도를 저장했습니다.")
        print_current_lands()  # 최신 데이터 출력 추가

    except ValueError:
        print("숫자를 입력해주세요.")

def start_manual_mode():
    global current_process  # 전역 변수로 current_process 사용

    try:
        if current_process and current_process.poll() is None:
            current_process.terminate()  # 현재 실행 중인 서비스 종료
            current_process.wait()  # 종료될 때까지 대기
            print("이전 서비스를 종료했습니다.")

        current_process = subprocess.Popen(["python3", "/home/user/dronekit_seed-master/modules/manual_servo_motor_operation.py"])
        print("수동 모드를 백그라운드에서 시작합니다.")

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

def start_auto_mode():
    global current_process  # 전역 변수로 current_process 사용

    try:
        if current_process and current_process.poll() is None:
            current_process.terminate()  # 현재 실행 중인 서비스 종료
            current_process.wait()  # 종료될 때까지 대기
            print("이전 서비스를 종료했습니다.")

        current_process = subprocess.Popen(["python3", "/home/user/dronekit_seed-master/seed_start.py", "speed_servo"])
        print("자동 모드를 백그라운드에서 시작합니다.")

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

def main():
    # 상태 플래그 초기화
    manual_mode_active = False
    auto_mode_active = False  # 자동 모드 상태 플래그 추가

    while True:
        print("\n메뉴를 선택하세요:")
        print("1: 땅 좌표값 입력")
        print("2: 서보모터 각도 입력")
        print("3: 자동 모드 시작")  # 메뉴 수정
        print("4: 수동 모드 시작")  # 메뉴 수정
        print("5: 현재 작업 중인 백그라운드 프로세스 종료 및 메뉴 재표시")
        print("6: 종료")

        choice = input("선택: ")

        if choice == '1':
            input_land()
        elif choice == '2':
            input_servo_angle()
        elif choice == '3':
            if auto_mode_active:
                print("자동 모드가 이미 활성화되어 있습니다.")
            else:
                print("자동 모드를 백그라운드에서 시작합니다.")
                auto_mode_active = True
                start_auto_mode()  # 자동 모드 백그라운드 실행
                manual_mode_active = False  # 수동 모드 비활성화
        elif choice == '4':
            if manual_mode_active:
                print("수동 모드가 이미 백그라운드에서 실행 중입니다.")
            else:
                print("수동 모드를 백그라운드에서 시작합니다.")
                manual_mode_active = True
                start_manual_mode()  # 수동 모드 백그라운드 실행
                auto_mode_active = False  # 자동 모드 비활성화
        elif choice == '5':
            if current_process and current_process.poll() is None:
                current_process.terminate()  # 현재 실행 중인 백그라운드 프로세스 종료
                current_process.wait()  # 종료될 때까지 대기
            print("\n메뉴를 다시 표시합니다.")
        elif choice == '6':
            print("프로그램을 종료합니다.")
            if current_process and current_process.poll() is None:
                current_process.terminate()  # 현재 실행 중인 백그라운드 프로세스 종료
                current_process.wait()  # 종료될 때까지 대기
            break
        else:
            print("잘못된 선택입니다. 다시 선택해주세요.")

if __name__ == "__main__":
    main()
