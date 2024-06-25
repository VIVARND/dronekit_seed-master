# lands.py

class CoordinateSystem:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    @classmethod
    def from_dict(cls, data):
        return cls(data['lat'], data['lon'])

    def __str__(self):
        return f"latitude: {self.lat}, longitude: {self.lon}"

class Land:
    def __init__(self, coordinates, servo_motor_angle):
        self.coordinates = coordinates
        self.servo_motor_angle = servo_motor_angle

    def to_dict(self):
        coordinates_dict = [{"lat": coord.lat, "lon": coord.lon} for coord in self.coordinates]
        return {
            "coordinates": coordinates_dict,
            "servo_motor_angle": self.servo_motor_angle
        }

    @classmethod
    def from_dict(cls, data):
        try:
            coordinates = [CoordinateSystem.from_dict(coord) for coord in data.get('coordinates', [])]
            servo_motor_angle = data.get('servo_motor_angle', 0)
            return cls(coordinates, servo_motor_angle)
        except Exception as e:
            print(f"Error parsing data: {e}")
            return None

    def __str__(self):
        coord_strings = "\n".join([str(coord) for coord in self.coordinates])
        return f"현재 땅 데이터:\n{coord_strings}\nservo_motor_angle: {self.servo_motor_angle}"

    def contains(self, point):
        if not self.coordinates:
            return False

        lats = [coord.lat for coord in self.coordinates]
        lons = [coord.lon for coord in self.coordinates]
        min_lat, max_lat = min(lats), max(lats)
        min_lon, max_lon = min(lons), max(lons)
        return min_lat <= point.lat <= max_lat and min_lon <= point.lon <= max_lon
