import sys
sys.path.append("/home/user/.pyenv/versions/3.9.10/lib/python3.9/site-packages")

from dronekit import connect, VehicleMode
from modules.lands import Land, CoordinateSystem
from modules.servo_motor import ServoMotor
from modules import land_dao

NOT_CONATAIN_ANGLE = 0
OUT_OF_LANDS = -1

class MyDrone:

    def __init__(self, connection_string):
        self.lands = land_dao.load_lands()
        self.current_land_index = OUT_OF_LANDS
        self.connection_string = connection_string
        self.servo_motor = ServoMotor()  

    def seed_start(self):
        while True:
            new_current_index = self.__find_current_land_index()

            if new_current_index != self.current_land_index:
                print("구역을 이동했으므로 서보모터 각도를 변경합니다")
                self.current_land_index = new_current_index
                angle = self.lands[new_current_index].sub_motor_angle if new_current_index != OUT_OF_LANDS else 0
                self.servo_motor.change_angle(angle)
    
    def __find_current_land_index(self):
        global_location = self.__get_global_location()
        drone_coordinate_system = CoordinateSystem(global_location.lat, global_location.lon)

        for index, land in enumerate(self.lands):
            if land.contain(drone_coordinate_system):
                return index
    
        return OUT_OF_LANDS    

    def __get_global_location(self):
        # 시뮬레이터의 호스트 및 포트 설정
        sim_host = '127.0.0.1'  # 시뮬레이터 호스트 IP
        sim_port = 5760  # 시뮬레이터 TCP 포트

        # 시뮬레이터에 연결
        print("Connecting to simulator on %s:%s" % (sim_host, sim_port))
        connection_string = f'tcp:{sim_host}:{sim_port}'
        vehicle = connect(connection_string, wait_ready=True)

        # 드론의 위치 정보 가져오기
        global_frame = vehicle.location.global_frame

        # 연결 종료
        vehicle.close()
        print("Location 가져오기 Completed")

        return global_frame

if __name__ == "__main__":
    # 시뮬레이터로부터 드론에 연결하여 시뮬레이션 실행
    my_drone = MyDrone(None)
    my_drone.seed_start()
