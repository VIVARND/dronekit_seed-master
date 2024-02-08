import dronekit_sitl

class DroneSitl:
    def __init__(self):
        self.__sitl = dronekit_sitl.start_default()

    @property
    def sitl(self):
        return self.__sitl
    
    def __del__(self):
        self.sitl.stop()
        print("sitl stop")
    
