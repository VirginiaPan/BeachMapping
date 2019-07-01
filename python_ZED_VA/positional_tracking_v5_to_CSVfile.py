
import pyzed.sl as sl
import shutil 

def main():
    # Create a Camera object
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.RESOLUTION_HD720  # Use HD720 video mode (default fps: 60)
    # Use a right-handed Y-up coordinate system
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.COORDINATE_SYSTEM_RIGHT_HANDED_Y_UP
    init_params.coordinate_units = sl.UNIT.UNIT_METER  # Set units in meters

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        exit(1)

    # Enable positional tracking with default parameters
    py_transform = sl.Transform()  # First create a Transform object for TrackingParameters object
    tracking_parameters = sl.TrackingParameters(init_pos=py_transform)
    err = zed.enable_tracking(tracking_parameters)
    if err != sl.ERROR_CODE.SUCCESS:
        exit(1)

    # Track the camera position until Keyboard Interupt (ctrl-C)
    #i = 0
    zed_pose = sl.Pose()
    zed_imu = sl.IMUData()
    runtime_parameters = sl.RuntimeParameters()

    #added! 
    path = '/media/nvidia/SD1/translation.csv'
    position_file = open(path,'w')
    
    while True:
        try: 
                if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
		    # Get the pose of the left eye of the camera with reference to the world frame
                    zed.get_position(zed_pose, sl.REFERENCE_FRAME.REFERENCE_FRAME_WORLD)
                    zed.get_imu_data(zed_imu, sl.TIME_REFERENCE.TIME_REFERENCE_IMAGE)

		    # Display the translation and timestamp
                    py_translation = sl.Translation()
                    tx = round(zed_pose.get_translation(py_translation).get()[0], 3)
                    ty = round(zed_pose.get_translation(py_translation).get()[1], 3)
                    tz = round(zed_pose.get_translation(py_translation).get()[2], 3)
                    #position_file.write("Translation: Tx: {0}, Ty: {1}, Tz {2}, Timestamp: {3}\n".format(tx, ty, tz, zed_pose.timestamp))
                    position_file.write("{0},{1},{2},{3}\n".format(tx, ty, tz, zed_pose.timestamp))

		    # Display the orientation quaternion
                    #py_orientation = sl.Orientation()
                    #ox = round(zed_pose.get_orientation(py_orientation).get()[0], 3)
                    #oy = round(zed_pose.get_orientation(py_orientation).get()[1], 3)
                    #oz = round(zed_pose.get_orientation(py_orientation).get()[2], 3)
                    #ow = round(zed_pose.get_orientation(py_orientation).get()[3], 3)
                    #position_file.write("Orientation: Ox: {0}, Oy: {1}, Oz {2}, Ow: {3}\n".format(ox, oy, oz, ow))

                    # Display the Rotation Matrix
                    #py_rotationMatrix = zed_pose.get_rotation_matrix()
                    #position_file.write("Got Rotation Matrix, but did not print\n")

		    # Display the Rotation Vector
                    #py_rotationVector = zed_pose.get_rotation_vector()
                    #rx = round(py_rotationVector[0], 3)
                    #ry = round(py_rotationVector[1], 3)
                    #rz = round(py_rotationVector[2], 3)
                    #position_file.write("Rotation Vector: Rx: {0}, Ry: {1}, Rz {2}, Timestamp: {3}\n".format(rx, ry, rz, zed_pose.timestamp))

		    # Display the Euler Angles
                    #py_eulerAngles = zed_pose.get_euler_angles()
                    #ex = round(py_eulerAngles[0], 3)
                    #ey = round(py_eulerAngles[1], 3)
                    #ez = round(py_eulerAngles[2], 3)
                    #position_file.write("EulerAngles: EAx: {0}, EAy: {1}, EAz {2}, Timestamp: {3}\n".format(ex, ey, ez, zed_pose.timestamp))



        except KeyboardInterrupt:
		
		# Close the camera
                zed.close()

    		# Close file
                position_file.close()
                save_position(path)
                print('All Done\n')
                raise
            #i = i + 1

def save_position(og_file):
    while True:
        res = input("Do you want to save the position tracking? [y/n]: ")
        if res == "y":
            params = sl.ERROR_CODE.ERROR_CODE_FAILURE
            while params != sl.ERROR_CODE.SUCCESS:
                filepath = input("Enter filepath name : ")
                #params = filter_params.save(filepath)
                shutil.copy(og_file,filepath)
                print("copying position tracking")
                if params:
                    break
                else:
                    print("Help : you must enter the filepath + filename without extension.")
            break
        elif res == "n":
            print("Mesh filter parameters will not be saved.")
            break
        else:
            print("Error, please enter [y/n].")

if __name__ == "__main__":
    main()
