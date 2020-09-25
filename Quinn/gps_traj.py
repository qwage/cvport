import matplotlib.pyplot as plt

# - - - Demonstration Data - - - #
ref_lat = [47.823, 47.820, 47.789,47.770]
ref_lon = [10.659, 10.683,10.694,10.710]


def gps_current(sensor_data):

    # -  - - - - - - - - - - - - - - - #
    #                                  #
    #   Read in GPS sensor data here   #
    #                                  #
    # -  - - - - - - - - - - - - - - - #

    c_lat = 47.818
    c_lon = 10.566

    
    return c_lat, c_lon


def gps_path(gps_file,lat_data,lon_data):
    # -  - - - - - - - - - - - - - - - #
    #                                  #
    #   split sensor File here         #
    #                                  #
    # -  - - - - - - - - - - - - - - - #

    # - - - - Visuals - - - - #
    plt.plot(lat_data,lon_data)
    plt.grid()
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.show()

    # return lat_data lon_data # -- This will be initiated when we read in a gps file from database


def gps_compare(c_lat,c_lon,lat_data,lon_data):

    # -  - - - - - - - - - - - - - - -         #
    #                                          #
    #   Compare current and desired location   #
    #                                          #
    # -  - - - - - - - - - - - - - - -         #


    # - - - - Visuals - - - - #
    plt.plot(c_lat, c_lon, marker='o', markersize=3, color="red")
    plt.plot(lat_data,lon_data)
    plt.grid()
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.show()

c_lat,c_lon = gps_current(1)
gps_compare(ref_lat,ref_lon,c_lat,c_lon)
