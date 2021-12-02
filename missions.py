from dronekit import Command, connect, VehicleMode, LocationGlobalRelative
import time
from pymavlink import mavutil

drone = connect("127.0.0.1:14550", wait_ready=True)

def takeoff(altitude):
    while drone.is_armable is not True:
        time.sleep(1)

    drone.mode = VehicleMode("GUIDED")

    drone.armed = True

    while drone.armed is not True:
        time.sleep(0.5)

    drone.simple_takeoff(altitude)
    
    while drone.location.global_relative_frame.alt < altitude * 0.9:
        time.sleep(1)

def mission_function():
    global command
    command = drone.commands

    command.clear()
    time.sleep(1)

    # TAKEOFF
    command.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0, 10))

    # WAYPOINT
    command.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, -35.36265286, 149.16514170, 20))
    command.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, -35.36318559, 149.16607666, 30))

    # RTL
    command.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH, 0, 0, 0, 0, 0, 0, 0, 0, 0))
    
    command.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH, 0, 0, 0, 0, 0, 0, 0, 0, 0))

    command.upload()

takeoff(10)

mission_function()
command.next = 0
drone.mode = VehicleMode("AUTO")
while True:
    next_waypoint = command.next

    print(f"next command {next_waypoint}")
    time.sleep(1)
    if next_waypoint is 4:
        print("Mission completed.")
        break