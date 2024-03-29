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
        # SITL(Software in the Loop)을 시작하여 시뮬레이션을 실행합니다.
        # 실제 드론에 연결하려면 connection_string을 설정해야 합니다.
        connection_string = self.connection_string or 'tcp:127.0.0.1:5760'
        print("Connecting to simulator on %s" % connection_string)
        vehicle = connect(connection_string, wait_ready=True)

        while True:
            new_current_index = self.__find_current_land_index(vehicle)

            if new_current_index != self.current_land_index:
                print("구역을 이동했으므로 서보모터 각도를 변경합니다")
                self.current_land_index = new_current_index
                angle = self.lands[new_current_index].sub_motor_angle if new_current_index != OUT_OF_LANDS else 0
                self.servo_motor.change_angle(angle)
    
    def __find_current_land_index(self, vehicle):
        global_location = self.__get_global_location(vehicle)
        drone_coordinate_system = CoordinateSystem(global_location.lat, global_location.lon)

        for index, land in enumerate(self.lands):
            if land.contain(drone_coordinate_system):
                return index
    
        return OUT_OF_LANDS    

    def __get_global_location(self, vehicle):
        # 드론의 위치 정보 가져오기
        global_frame = vehicle.location.global_frame
        print("Location 가져오기 Completed")
        return global_frame

if __name__ == "__main__":
    # 시뮬레이터로부터 드론에 연결하여 시뮬레이션 실행
    my_drone = MyDrone(None)  # 여기서는 시뮬레이션을 실행할 것이므로 connection_string을 None으로 설정합니다.
    my_drone.seed_start()
