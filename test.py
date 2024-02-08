from modules.lands import Land, CoordinateSystem
def lands_sort_test():

    lu = CoordinateSystem(0, 2)
    ru = CoordinateSystem(0, 0)
    ld = CoordinateSystem(2, 2)
    rd = CoordinateSystem(2, 0)
    land = Land([lu, ru, ld, rd], 45)

    assert land.left_down.lat == 0 and land.left_down.lon == 0
    assert land.left_up.lat == 2 and land.left_up.lon == 0
    assert land.right_up.lat == 2 and land.right_up.lon == 2
    assert land.right_down.lat == 0 and land.right_down.lon == 2

lands_sort_test()

