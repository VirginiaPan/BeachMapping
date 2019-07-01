"""
    Mesh sample shows mesh information after filtering and applying texture on frames. The mesh and its filter
    parameters can be saved.
"""
import sys
import pyzed.sl as sl
import shutil

def main():

    if not sys.argv or len(sys.argv) != 2:
        print("Only the path of the output SVO file should be passed as argument.")
        exit(1)

    cam = sl.Camera()
    init = sl.InitParameters()
    
    init.camera_resolution = sl.RESOLUTION.RESOLUTION_HD720  # Use HD720 video mode (default
    init.coordinate_system = sl.COORDINATE_SYSTEM.COORDINATE_SYSTEM_RIGHT_HANDED_Y_UP  # Use a right-handed Y-up coordinate system
    init.coordinate_units = sl.UNIT.UNIT_METER  # Set units in meters
    
    # new for SVO
    init.depth_mode = sl.DEPTH_MODE.DEPTH_MODE_NONE
    ##
    
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()

    runtime = sl.RuntimeParameters()
    spatial = sl.SpatialMappingParameters()
    transform = sl.Transform()
    tracking = sl.TrackingParameters(transform)

    cam.enable_tracking(tracking)
    cam.enable_spatial_mapping(spatial)

    
    #from  Positional Tracking: 
    # Track the camera position until Keyboard Interupt (ctrl-C)
    zed_pose = sl.Pose()
    zed_imu = sl.IMUData()
    runtime_parameters = sl.RuntimeParameters()

    path = '/media/nvidia/SD1/translation.csv'
    position_file = open(path,'w')
    #END from positional tracking

    pymesh = sl.Mesh()
    print("Processing...")


    #new for SVO
    path_output = sys.argv[1]
    err = cam.enable_recording(path_output, sl.SVO_COMPRESSION_MODE.SVO_COMPRESSION_MODE_AVCHD)
    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit(1)
    print("SVO is Recording, use Ctrl-C to stop.")
    frames_recorded = 0
    ##
   
    while True:
        try: 
            cam.grab(runtime)

            # new for SVO
            state = cam.record()
            if state["status"]:
                frames_recorded += 1
            print("Frame count: " + str(frames_recorded), end="\r")
            ##

            cam.request_mesh_async()
            # Get the pose of the left eye of the camera with reference to the world frame
            cam.get_position(zed_pose, sl.REFERENCE_FRAME.REFERENCE_FRAME_WORLD)
            cam.get_imu_data(zed_imu, sl.TIME_REFERENCE.TIME_REFERENCE_IMAGE)

            # Display the translation and timestamp
            py_translation = sl.Translation()
            tx = round(zed_pose.get_translation(py_translation).get()[0], 3)
            ty = round(zed_pose.get_translation(py_translation).get()[1], 3)
            tz = round(zed_pose.get_translation(py_translation).get()[2], 3)
            position_file.write("{0},{1},{2},{3}\n".format(tx, ty, tz, zed_pose.timestamp))

        except KeyboardInterrupt:
            cam.extract_whole_mesh(pymesh)
            cam.disable_tracking()
            cam.disable_spatial_mapping()
            # new for .svo
            cam.disable_recording()
            ##
            filter_params = sl.MeshFilterParameters()
            filter_params.set(sl.MESH_FILTER.MESH_FILTER_HIGH)
            print("Filtering params : {0}.".format(pymesh.filter(filter_params)))

            apply_texture = pymesh.apply_texture(sl.MESH_TEXTURE_FORMAT.MESH_TEXTURE_RGBA)
            print("Applying texture : {0}.".format(apply_texture))
            print_mesh_information(pymesh, apply_texture)

            save_filter(filter_params)
            save_mesh(pymesh)
            cam.close()
            position_file.close()
            save_position(path)
            print("\nFINISH")
            raise

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

def print_mesh_information(pymesh, apply_texture):
    while True:
        res = input("Do you want to display mesh information? [y/n]: ")
        if res == "y":
            if apply_texture:
                print("Vertices : \n{0} \n".format(pymesh.vertices))
                print("Uv : \n{0} \n".format(pymesh.uv))
                print("Normals : \n{0} \n".format(pymesh.normals))
                print("Triangles : \n{0} \n".format(pymesh.triangles))
                break
            else:
                print("Cannot display information of the sl.")
                break
        if res == "n":
            print("Mesh information will not be displayed.")
            break
        else:
            print("Error, please enter [y/n].")


def save_filter(filter_params):
    while True:
        res = input("Do you want to save the mesh filter parameters? [y/n]: ")
        if res == "y":
            params = sl.ERROR_CODE.ERROR_CODE_FAILURE
            while params != sl.ERROR_CODE.SUCCESS:
                filepath = input("Enter filepath name : ")
                params = filter_params.save(filepath)
                print("Saving mesh filter parameters: {0}".format(repr(params)))
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


def save_mesh(pymesh):
    while True:
        res = input("Do you want to save the mesh? [y/n]: ")
        if res == "y":
            msh = sl.ERROR_CODE.ERROR_CODE_FAILURE
            while msh != sl.ERROR_CODE.SUCCESS:
                filepath = input("Enter filepath name: ")
                msh = pymesh.save(filepath)
                print("Saving mesh: {0}".format(repr(msh)))
                if msh:
                    break
                else:
                    print("Help : you must enter the filepath + filename without extension.")
            break
        elif res == "n":
            print("Mesh will not be saved.")
            break
        else:
            print("Error, please enter [y/n].")

if __name__ == "__main__":
    main()
