from modules.drone_sitl import DroneSitl
from modules.my_drone import MyDrone

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
