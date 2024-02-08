
class CoordinateSystem:
    """
    lat 위도
    lon 경도
    """
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
    def __str__(self):
        return "latitude: {}, longitude: {}".format(self.lat, self.lon)

class Land:
    
    LEFT_DOWN = 'left_down'
    LEFT_UP = 'left_up'
    RIGHT_DOWN = 'right_down'
    RIGHT_UP = 'right_up'

    def __init__(self, vertexs, servo_motor_angle):
        """
            직사각형이라고 가정했으며 좌표를 직사각형과 다르게 입력 시 오차가 발생하여 
            예상치 못한 동작이 유발될 수 있음
            추후 땅의 형태는 논의 후 변경할 필요가 있음
        """

        if not isinstance(vertexs, list):
            raise RuntimeError("vertexs 인수의 자료형은 list(CoordinateSystem)이어야 합니다.{}}".format(type(vertexs)))

        if len(vertexs) != 4:
            raise RuntimeError("땅의 꼭짓점들의 개수가 4개가 아닙니다: {}개".format(len(vertexs)))

        # find smallest vertex
        sorted_vertexs_dict = self.__sort_vertexs(vertexs)

        self.left_up = sorted_vertexs_dict[Land.LEFT_UP]
        self.right_up = sorted_vertexs_dict[Land.RIGHT_UP]
        self.left_down = sorted_vertexs_dict[Land.LEFT_DOWN]
        self.right_down = sorted_vertexs_dict[Land.RIGHT_DOWN]
        self.servo_motor_angle = servo_motor_angle 

    def __sort_vertexs(self, vertexs):

        new_vertexs = []

        for vertex in vertexs:
            new_vertexs.append(vertex)

        result = {}
        left_down = self.__find_min_vertex(new_vertexs)
        result[Land.LEFT_DOWN] = left_down
        new_vertexs.remove(left_down)

        right_up = self.__find_max_vertex(new_vertexs)
        result[Land.RIGHT_UP] = right_up
        new_vertexs.remove(right_up)

        if abs(left_down.lat - new_vertexs[0].lat) > abs(left_down.lat - new_vertexs[1].lat):
            result[Land.LEFT_UP] = new_vertexs[0]
            result[Land.RIGHT_DOWN] = new_vertexs[1]
        else:
            result[Land.LEFT_UP] = new_vertexs[1]
            result[Land.RIGHT_DOWN] = new_vertexs[0]

        return result

    def __find_max_vertex(self, vertexs):
        max_sum = vertexs[0].lat + vertexs[0].lon
        max_index = 0

        for index, vertex in enumerate(vertexs):
            if max_sum < vertex.lat + vertex.lon:
                max_sum = vertex.lat + vertex.lon
                max_index = index

        return vertexs[max_index]

    def __find_min_vertex(self, vertexs):
        min_sum = vertexs[0].lat + vertexs[0].lon
        min_index = 0

        for index, vertex in enumerate(vertexs):
            if min_sum > vertex.lat + vertex.lon:
                min_sum = vertex.lat + vertex.lon
                min_index = index
        return vertexs[min_index]
        
    def contain(self, coordinate):  
        """
            직사각형이라고 가정함
        """
        if self.left_up.lat > coordinate.lat or coordinate.lat > self.right_up.lat:
            return False
        
        if self.left_up.lon < coordinate.lon or coordinate.lon < self.left_down.lon:
            return False
        
        return True
    
    def __str__(self):
        return "land: left up - {},\n right up - {},\n left down -  {},\n right down - {},\n servo_motor_angle = {}\n".format(self.left_up, self.right_up, self.left_down, self.right_down, self.servo_motor_angle)
