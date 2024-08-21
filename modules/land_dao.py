import json
import os
from datetime import datetime, timedelta
from .lands import Land, CoordinateSystem

DATA_FILE = "data.json"
LOGS_DIR = "logs"
LOGS1_DIR = "logs1"
LOGS2_DIR = "logs2"
LOG_FILE = "data2.json"  # `logs` 디렉토리 내 최신 데이터 로그 파일

# 로그 디렉토리가 없으면 생성
for directory in [LOGS_DIR, LOGS1_DIR, LOGS2_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_lands():
    try:
        with open(DATA_FILE, 'r') as f:
            lands_dict = json.load(f)
            lands = [Land.from_dict(land) for land in lands_dict]
            return [land for land in lands if land is not None]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Error parsing data:", DATA_FILE)
        return []

def save_lands(lands):
    lands_dicts = [land.to_dict() for land in lands]
    with open(DATA_FILE, 'w') as f:
        json.dump(lands_dicts, f, indent=4)
    save_latest_log(lands)  # 최신 데이터 로그 저장
    save_speed_log()  # 속도 로그 저장

def save_latest_log(lands):
    log_file = os.path.join(LOGS_DIR, LOG_FILE)
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "data": [land.to_dict() for land in lands]
    }
    with open(log_file, 'w') as f:
        json.dump(log_entry, f, indent=4)
    clean_old_logs(LOGS1_DIR)  # `logs1` 디렉토리 내 오래된 로그 파일 삭제

def save_land_log(lands):
    log_file = os.path.join(LOGS1_DIR, LOG_FILE)
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "data": [land.to_dict() for land in lands]
    }
    with open(log_file, 'w') as f:
        json.dump(log_entry, f, indent=4)

def save_speed_log():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    speed_log_file = os.path.join(LOGS2_DIR, f"speed_{timestamp}.json")

    speed_log_entry = {
        "timestamp": datetime.now().isoformat(),
        "location": get_drone_location(),  # 드론의 위치를 로그에 추가
        "speed": get_drone_speed(),
    }

    with open(speed_log_file, 'w') as f:
        json.dump(speed_log_entry, f, indent=4)
    clean_old_logs(LOGS2_DIR)  # `logs2` 디렉토리 내 오래된 로그 파일 삭제

def clean_old_logs(directory):
    now = datetime.now()
    cutoff = now - timedelta(days=30)  # 30일 후 삭제
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        try:
            file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            if file_time < cutoff:
                os.remove(filepath)
                print(f"Deleted old log file: {filename}")
        except (ValueError, TypeError):
            continue

def get_drone_speed():
    # TODO: 드론의 실제 속도를 가져오는 함수를 작성해야 합니다.
    return 0.0

def get_drone_location():
    # TODO: 드론의 실제 위치를 가져오는 함수를 작성해야 합니다.
    return {"latitude": 0.0, "longitude": 0.0}

# 서보모터와 좌표 자동 업데이트 예제
def update_servo_motor_and_log():
    lands = load_lands()

    if not lands:
        print("등록된 땅 데이터가 없습니다.")
        return

    # 최신 땅 데이터 가져오기
    latest_land = lands[-1]
    angle = latest_land.servo_motor_angle
    coordinates = latest_land.coordinates

    # 서보모터를 최신 각도로 업데이트
    print(f"서보모터 각도를 {angle}도로 설정합니다.")
    # 실제 서보모터 업데이트 함수 호출 예시
    # servo_motor.change_angle(angle)

    # 최신 좌표 출력
    print("최신 좌표:")
    for idx, coord in enumerate(coordinates):
        print(f"좌표 {idx + 1}: latitude: {coord.lat}, longitude: {coord.lon}")

    # 최신 데이터 로그 기록
    save_lands(lands)  # 최신 데이터 저장
    save_land_log(lands)  # 최신 데이터 `logs1`에 기록
    print("최신 데이터가 로그에 기록되었습니다.")

if __name__ == "__main__":
    # 서보모터와 좌표를 업데이트하고 로그를 기록합니다.
    update_servo_motor_and_log()
