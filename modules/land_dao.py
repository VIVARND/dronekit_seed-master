import json
import os
from datetime import datetime, timedelta
from .lands import Land, CoordinateSystem

DATA_FILE = "data.json"
LOGS1_DIR = "logs1"
LOGS2_DIR = "logs2"
LOG_FILE = "data2.json"  # 기존 로그 파일

# 로그 디렉토리가 없으면 생성
if not os.path.exists(LOGS1_DIR):
    os.makedirs(LOGS1_DIR)

if not os.path.exists(LOGS2_DIR):
    os.makedirs(LOGS2_DIR)

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
    save_log(lands)
    save_speed_log()  # 속도 로그 저장

def save_log(lands):
    log_file = os.path.join(LOGS1_DIR, LOG_FILE)
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "data": [land.to_dict() for land in lands]
    }
    with open(log_file, 'w') as f:
        json.dump(log_entry, f, indent=4)
    clean_old_logs(LOGS1_DIR)

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
    clean_old_logs(LOGS2_DIR)

def get_drone_speed():
    # TODO: 드론의 실제 속도를 가져오는 함수를 작성해야 합니다.
    # 이 함수는 실제 드론의 속도를 반환해야 하며, 여기서는 가상의 예시로 0.0으로 반환합니다.
    return 0.0

def get_drone_location():
    # TODO: 드론의 실제 위치를 가져오는 함수를 작성해야 합니다.
    # 이 함수는 실제 드론의 위치를 반환해야 하며, 여기서는 가상의 예시로 반환합니다.
    return {"latitude": 0.0, "longitude": 0.0}

def clean_old_logs(directory):
    now = datetime.now()
    cutoff = now - timedelta(days=30)  # 30일 후 삭제
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        file_time_str = filename.split('_')[1].split('.')[0] if '_' in filename else None
        try:
            file_time = datetime.strptime(file_time_str, "%Y%m%d_%H%M%S") if file_time_str else None
            if file_time and file_time < cutoff:
                os.remove(filepath)
                print(f"Deleted old log file: {filename}")
        except (ValueError, TypeError):
            # 파일 이름이 예상 형식이 아닌 경우 건너뜁니다.
            continue

# 예제 사용
if __name__ == "__main__":
    # 예제 땅 데이터를 로드하고 저장합니다.
    lands = load_lands()
    save_lands(lands)
