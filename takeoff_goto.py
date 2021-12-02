from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

drone = connect("127.0.0.1:14550", wait_ready=True)
def takeoff(altitude):
    while drone.is_armable is not True:
        time.sleep(1)
    drone.mode = VehicleMode("GUIDED")

    drone.armed = True

    while drone.armed is not True:
        time.sleep(0.5)
    drone.simple_takeoff(altitude)
    
    while drone.location.global_relative_frame.alt < altitude * 0.99:
        time.sleep(1)

takeoff(30)

location = LocationGlobalRelative(-35.36223671, 149.16509335, 30)
drone.simple_goto(location)
