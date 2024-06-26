
import time
from dronekit import connect, VehicleMode, Vehicle
from modules.lands import Land, CoordinateSystem
from modules.servo_motor import ServoMotor
from modules import land_dao

NOT_CONTAIN_ANGLE = 0
OUT_OF_LANDS = -1
LOCATION_UPDATE_INTERVAL = 0.5  # 위치 업데이트 간격 (초)
AVERAGE_POSITION_COUNT = 10     # 평균을 내기 위한 위치 샘플 개수

class MyDrone:

    def __init__(self, connection_string):
        self.lands = land_dao.load_lands()
        self.current_land_index = OUT_OF_LANDS
        self.connection_string = connection_string
        self.servo_motor = ServoMotor()
        self.last_update_time = time.time()
        self.vehicle = self.__connect_vehicle()  # 드론 연결을 초기화 시점에서 수행
        self.position_history = []

    def __connect_vehicle(self):
        print(f"Connecting to vehicle on: {self.connection_string}")
        vehicle = connect(self.connection_string, wait_ready=True)
        print("location 가져오기 Completed")
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

                        if new_current_index == OUT_OF_LANDS:
                            print("드론이 지정된 땅 좌표 바깥에 있습니다. 서보모터 각도를 0도로 설정합니다.")
                            self.servo_motor.change_angle(NOT_CONTAIN_ANGLE)
                        else:
                            print("구역을 이동했으므로 서보모터 각도를 변경합니다")
                            angle = self.lands[new_current_index].servo_motor_angle
                            self.servo_motor.change_angle(angle)

                    self.print_current_state()

                time.sleep(0.5)  # 0.5초 간격으로 출력

        finally:
            self.vehicle.close()
            print("Vehicle 연결이 종료되었습니다.")

    def __find_current_land_index(self):
        global_location = self.__get_global_location()
        drone_coordinate_system = CoordinateSystem(global_location.lat, global_location.lon)
        print(f"드론의 현재 위치: latitude: {drone_coordinate_system.lat}, longitude: {drone_coordinate_system.lon}")

        # 최근 위치 기록 추가
        self.position_history.append(drone_coordinate_system)
        if len(self.position_history) > AVERAGE_POSITION_COUNT:
            self.position_history.pop(0)  # 가장 오래된 위치 제거

        # 평균 위치 계산
        average_lat = sum(coord.lat for coord in self.position_history) / len(self.position_history)
        average_lon = sum(coord.lon for coord in self.position_history) / len(self.position_history)

        print(f"평균 위치: latitude: {average_lat}, longitude: {average_lon}")

        for index, land in enumerate(self.lands):
            if land.contains(drone_coordinate_system):
                return index

        return OUT_OF_LANDS

    def __get_global_location(self):
        global_frame = self.vehicle.location.global_frame
        return global_frame

    def print_current_state(self):
        if self.current_land_index == OUT_OF_LANDS:
            print("드론이 지정된 땅 좌표 바깥에 있습니다.")
        else:
            land = self.lands[self.current_land_index]
            print("현재 땅 데이터:")
            for idx, coord in enumerate(land.coordinates):
                print(f"좌표 {idx + 1}: latitude: {coord.lat}, longitude: {coord.lon}")
            print(f"서보모터 각도: {land.servo_motor_angle}")

        print(f"현재 서보모터 각도: {self.servo_motor.current_angle}")

if __name__ == "__main__":
    def sitl_start():
        drone_sitl = DroneSitl()
        start(drone_sitl.sitl.connection_string())

    def real_start():
        start("/dev/ttyACM0")

    def start(connection_string):
        my_drone = MyDrone(connection_string)
        my_drone.seed_start()

    real_start()
