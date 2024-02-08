from dronekit import connect, VehicleMode, Vehicle
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
        print(drone_coordinate_system)

        for index, land in enumerate(self.lands):
            if land.contain(drone_coordinate_system):
                return index
    
        return OUT_OF_LANDS    

    def __get_global_location(self):

        # Connect to the Vehicle.
        print("Connecting to vehicle on: %s" % (self.connection_string,))
        vehicle = connect(self.connection_string, wait_ready=False)

        global_frame = vehicle.location.global_frame

        # Close vehicle object before exiting script
        vehicle.close()
        print("location 가져오기 Completed")

        return global_frame
        