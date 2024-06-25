import time
from dronekit import connect
from modules.lands import CoordinateSystem
from modules import land_dao
from modules.servo_motor import ServoMotor

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
        self.current_speed = None  # 초기화: 속도를 저장할 변수
        self.mode = None  # 초기 모드는 None으로 설정

    def __connect_vehicle(self):
        print(f"Connecting to vehicle on: {self.connection_string}")
        vehicle = connect(self.connection_string, wait_ready=True)
        print("드론 연결 완료")
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

                    # 속도 제어 모드에서 추가적인 작업 수행
                    if self.mode == "speed_control":
                        self.__start_speed_servo()

                time.sleep(0.5)  # 0.5초 간격으로 출력

        finally:
            self.vehicle.close()
            print("드론 연결 종료")

    def __find_current_land_index(self):
        global_location = self.__get_global_location()
        drone_coordinate_system = CoordinateSystem(global_location.lat, global_location.lon)
        print(f"드론의 현재 위치: latitude: {drone_coordinate_system.lat}, longitude: {drone_coordinate_system.lon}")

        # 최근 위치 기록 추가
        self.position_history.append(drone_coordinate_system)
        if len(self.position_history) > AVERAGE_POSITION_COUNT:
            self.position_history.pop(0)  # 가장 오래된 위치 제거

        for index, land in enumerate(self.lands):
            if land.contains(drone_coordinate_system):
                return index

        return OUT_OF_LANDS

    def __get_global_location(self):
        global_frame = self.vehicle.location.global_frame
        return global_frame

    def __get_groundspeed(self):
        groundspeed = self.vehicle.groundspeed  # 미터/초로 단위가 설정됩니다.
        return groundspeed

    def print_current_state(self):
        if self.current_land_index == OUT_OF_LANDS:
            print("드론이 지정된 땅 좌표 바깥에 있습니다.")
        else:
            land = self.lands[self.current_land_index]
            print("현재 땅 데이터:")
            for idx, coord in enumerate(land.coordinates):
                print(f"좌표 {idx + 1}: latitude: {coord.lat}, longitude: {coord.lon}")
            print(f"서보모터 각도: {land.servo_motor_angle}")

        # 속도 출력
        current_speed = self.__get_groundspeed()
        formatted_speed = round(current_speed, 2) if current_speed is not None else "N/A"
        print(f"현재 속도: {formatted_speed} m/s")

        print(f"현재 서보모터 각도: {self.servo_motor.current_angle}")

    def set_mode(self, mode):
        self.mode = mode

    def get_mode(self):
        return self.mode

if __name__ == "__main__":
    def sitl_start():
        from modules.drone_sitl import DroneSitl
        drone_sitl = DroneSitl()
        start(drone_sitl.sitl.connection_string())

    def real_start():
        start("/dev/ttyACM0")

    def start(connection_string):
        my_drone = MyDrone(connection_string)
        my_drone.seed_start()

    real_start()
