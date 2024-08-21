import json
import os
from datetime import datetime, timedelta
from .lands import Land  # Assuming this import is correct

# 상수 정의
DATA_FILE = "data.json"  # 데이터 파일 이름
LOGS_DIR = "logs"  # 최신 로그 디렉토리
LOGS1_DIR = "logs1"  # 1달 동안 로그를 저장할 디렉토리
LOGS2_DIR = "logs2"  # 속도 로그를 저장할 디렉토리
LOG_FILE = "data.json"  # 최신 로그 파일 이름
LOGS1_FILE = "data1.json"  # 1달 동안 저장할 로그 파일 이름

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
    save_log(lands)  # 최신 기록 저장
    save_speed_log()  # 속도 로그 저장

def save_log(lands):
    # 기존 최신 로그를 logs1으로 이동
    if os.path.exists(os.path.join(LOGS_DIR, LOG_FILE)):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        new_log_file = os.path.join(LOGS1_DIR, f"{timestamp}_{LOG_FILE}")
        os.rename(os.path.join(LOGS_DIR, LOG_FILE), new_log_file)

    # 새로운 최신 로그를 logs 디렉토리에 저장
    log_file = os.path.join(LOGS_DIR, LOG_FILE)
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "data": [land.to_dict() for land in lands]
    }
    with open(log_file, 'w') as f:
        json.dump(log_entry, f, indent=4)

    clean_old_logs(LOGS1_DIR)  # 오래된 logs1 로그 삭제

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

    clean_old_logs(LOGS2_DIR)  # 오래된 속도 로그 삭제

def get_drone_speed():
    # TODO: 드론의 실제 속도를 가져오는 함수를 작성해야 합니다.
    return 0.0

def get_drone_location():
    # TODO: 드론의 실제 위치를 가져오는 함수를 작성해야 합니다.
    return {"latitude": 0.0, "longitude": 0.0}

def clean_old_logs(directory):
    now = datetime.now()
    cutoff = now - timedelta(days=30)  # 30일 후 삭제
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        file_time_str = filename.split('_')[0] if '_' in filename else None
        try:
            file_time = datetime.strptime(file_time_str, "%Y%m%d_%H%M%S") if file_time_str else None
            if file_time and file_time < cutoff:
                os.remove(filepath)
                print(f"Deleted old log file: {filename}")
        except (ValueError, TypeError):
            continue
