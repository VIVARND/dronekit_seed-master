import json
import os
import time
from dronekit import connect, VehicleMode
from modules.lands import Land, CoordinateSystem
from modules.servo_motor import ServoMotor
from modules import land_dao

NOT_CONTAIN_ANGLE = 0
LOCATION_UPDATE_INTERVAL = 0.5  # 위치 업데이트 간격 (초)
AVERAGE_POSITION_COUNT = 10     # 평균을 내기 위한 위치 샘플 개수

class MyDrone:
    def __init__(self, connection_string):
        self.lands = land_dao.load_lands()
        self.current_land_index = -1
        self.connection_string = connection_string
        self.servo_motor = ServoMotor()
        self.last_update_time = time.time()
        self.vehicle = self.__connect_vehicle()
        self.position_history = []

    def __connect_vehicle(self):
        print(f"Connecting to vehicle on: {self.connection_string}")
        vehicle = connect(self.connection_string, wait_ready=True)
        print("Vehicle connected")
        return vehicle

    def seed_start(self):
        try:
            while True:
                current_time = time.time()
                if current_time - self.last_update_time >= LOCATION_UPDATE_INTERVAL:
                    self.last_update_time = current_time
                    new_current_index = self.__find_current_land_index()

                    if new_current_index != self.current_land_index:
                        self.current_land_index = new_current_index

                        if new_current_index == -1:
                            print("드론이 지정된 땅 좌표 바깥에 있습니다.")
                            self.__set_servo_motor_angle(NOT_CONTAIN_ANGLE)
                        else:
                            print("드론이 지정된 구역에 들어왔습니다.")
                            latest_data = self.__load_latest_data()
                            if latest_data and self.current_land_index < len(latest_data['data']):
                                angle = latest_data['data'][self.current_land_index]['servo_motor_angle']
                                self.__set_servo_motor_angle(angle)

                    self.print_current_state()

                time.sleep(LOCATION_UPDATE_INTERVAL)

        finally:
            self.vehicle.close()
            print("Vehicle connection closed.")

    def __find_current_land_index(self):
        global_location = self.__get_global_location()
        drone_coordinate_system = CoordinateSystem(global_location.lat, global_location.lon)
        print(f"드론의 현재 위치: latitude: {drone_coordinate_system.lat}, longitude: {drone_coordinate_system.lon}")

        self.position_history.append(drone_coordinate_system)
        if len(self.position_history) > AVERAGE_POSITION_COUNT:
            self.position_history.pop(0)

        average_lat = sum(coord.lat for coord in self.position_history) / len(self.position_history)
        average_lon = sum(coord.lon for coord in self.position_history) / len(self.position_history)

        print(f"평균 위치: latitude: {average_lat}, longitude: {average_lon}")

        for index, land in enumerate(self.lands):
            if land.contains(drone_coordinate_system):
                return index

        return -1

    def __get_global_location(self):
        return self.vehicle.location.global_frame

    def __load_latest_data(self):
        log_file_path = os.path.join('logs', 'data.json')
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as f:
                return json.load(f)
        return None

    def __set_servo_motor_angle(self, angle):
        if 0 <= angle <= 140:
            print(f"서보모터 각도 변경: {angle}도")
            self.servo_motor.change_angle(angle)
        else:
            print(f"잘못된 서보모터 각도: {angle}. 기본 0도로 설정합니다.")
            self.servo_motor.change_angle(NOT_CONTAIN_ANGLE)

    def print_current_state(self):
        if self.current_land_index == -1:
            print("드론이 지정된 땅 좌표 바깥에 있습니다.")
        else:
            land = self.lands[self.current_land_index]
            print("현재 땅 데이터:")
            for idx, coord in enumerate(land.coordinates):
                print(f"좌표 {idx + 1}: latitude: {coord.lat}, longitude: {coord.lon}")
            print(f"서보모터 각도: {land.servo_motor_angle}")

        print(f"현재 서보모터 각도: {self.servo_motor.current_angle}")

if __name__ == "__main__":
    def real_start():
        start("/dev/ttyACM0")

    def start(connection_string):
        my_drone = MyDrone(connection_string)
        my_drone.seed_start()

    real_start()
