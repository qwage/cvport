"""
Test trajectory planning 

Purdue University, West Lafayette, IN
School of Engineering, Aeronautical and Astronautical Engineering, AAE 497 
Computer Vision
"""

import test_rrt as prg
import os
import matplotlib.pyplot as plt


def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = dir_path + '\\scenarios\\'

    # Create the directory to store the generated images
    if not os.path.exists(file_path):
        try:
            os.mkdir(file_path)
        except OSError:
            print("Creation of the directory %s failed" % file_path)
        else:
            print("Successfully created the directory %s " % file_path)

    for i in range(1, 4):
        prg.main(json_export=True, num=i)

        # Deleting existing image files
        img_file_name = 'Random' + str(i) + '.png'

        # If the directory already existed delete the images that are already in the directory
        if os.path.exists(file_path+img_file_name):
            try:
                os.remove(file_path+img_file_name)
            except OSError as e:
                print("Error: %s : %s" % (file_path+img_file_name, e.strerror))

        # Saving new image files
        plt.savefig(file_path+img_file_name)
        plt.pause(0.05)
        plt.close()

if __name__ == '__main__':
    main()