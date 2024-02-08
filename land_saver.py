from modules import land_dao
from modules.lands import CoordinateSystem, Land 




def input_land():
    
    print("기존 데이터를 불러옵니다..")
    lands = land_dao.load_lands()

    print("현재 땅 데이터:")
    for land in lands:
        print(land)

    print("땅의 꼭짓점 4개(lat, lon)를 입력해주십시오, 직사각형을 기반으로 합니다\n")
    print("자동으로 정렬되므로 아무 순서로 꼭짓점을 입력해주십시오")
    print("입력 예시: 112.3, 241.44 ")
    
    li = []
    
    lat,lon = map(float, input("꼭짓점 1 입력:").split(","))
    li.append(CoordinateSystem(lat, lon))

    lat,lon = map(float, input("꼭짓점 2 입력:").split(","))
    li.append(CoordinateSystem(lat, lon))

    lat,lon = map(float, input("꼭짓점 3 입력:").split(","))
    li.append(CoordinateSystem(lat, lon))

    lat,lon = map(float, input("꼭짓점 4 입력:").split(","))
    li.append(CoordinateSystem(lat, lon))

    angle = int(input("각도를 입력해주세요 정수형입니다: "))
    new_land = Land(li, angle)

    print(new_land)

    answer = input("위 정보가 맞습니까? (y/n): ")

    if answer == 'y' or answer == 'Y':
        lands.append(new_land)
        land_dao.save_lands(lands)
        print("저장을 완료했습니다.")
    else: 
        print("저장되지 않았습니다.")

input_land()
    