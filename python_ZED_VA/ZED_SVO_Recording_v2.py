
#!/usr/bin/env python3
import time
import sys
import pyzed.sl as sl
import numpy as np
import cv2

def main():
    
    if len(sys.argv) != 3:
        print("Please specify collection time (seconds), and path to save files")
        exit()
    max_time = sys.argv[1]
    print(max_time)

    #delay program 60 sec, so that user can get to start location
    print("You have 10 seconds to get to start location before program will begin")
    time.sleep(10)
    print("Initializing camera")

    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.RESOLUTION_HD720
    init.depth_mode = sl.DEPTH_MODE.DEPTH_MODE_NONE

    cam = sl.Camera()
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit(1)

    path_output = sys.argv[2]
    err = cam.enable_recording(path_output, sl.SVO_COMPRESSION_MODE.SVO_COMPRESSION_MODE_AVCHD)
    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit(1)

    runtime = sl.RuntimeParameters()
    print("SVO is Recording")
    #frames_recorded = 0

    #get start time
    start_time = time.time()

    print("Starting to collect data")

    while (time.time() -start_time)<float(max_time):
        if cam.grab(runtime) == sl.ERROR_CODE.SUCCESS :
            # Each new frame is added to the SVO file
            state = cam.record()
            #if state["status"]:
                #frames_recorded += 1
            #print("Frame count: " + str(frames_recorded), end="\r")

    # Stop recording
    cam.disable_recording()
    cam.close()

if __name__ == "__main__":
    main()
