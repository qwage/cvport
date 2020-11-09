import cv2
import matplotlib.pyplot as plt


# -- Convert Image to Binary -- #
def imgBinary(threshold_val,file_path, wait_key):

    img_grey = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

    img_binary = cv2.threshold(img_grey, threshold_val, 255, cv2.THRESH_BINARY)[1]
    img_RGBcolor = cv2.cvtColor(img_binary,cv2.COLOR_BGR2RGB)

    img_binary_resize = cv2.resize(img_binary, (1920, 1080))

    cv2.imshow("Binary",img_binary_resize)

    height, width = img_binary.shape
    cv2.imwrite("Binary.jpg",img_binary)
    cv2.waitKey(wait_key)
    cv2.destroyAllWindows()

    return height, width, img_binary, img_RGBcolor

def GPS_rect(GPS_cord_input_lat,GPS_cord_input_long,img_binary, height, width):
    # Note that .053 ft is .6 inches and the practical limit for commercial GPS is 7 decimals wich is about 11 mm or .4 inches
    inInFt = 12
    seventh_decml_accuracy = .4 # .4 inch = .0000001 for lat and long

    width_mes = 106 # Width of the drawing in feet
    pxl_scale = width_mes / width # feet per pixle for this drawing
    GPS_scale = (pxl_scale*inInFt) / .4 # 7th decimal addition for the scaled image
    pxl_per_1dcml = 1/(inInFt/.4) * 1/pxl_scale

    topLeftLat = 40.426964
    topLeftLong = -86.913722

    bottomRightLat = topLeftLat + (width*GPS_scale)
    bottomRightLong = topLeftLong + (height*GPS_scale)

    if GPS_cord_input_lat < topLeftLat or GPS_cord_input_long < bottomRightLong or GPS_cord_input_lat > bottomRightLat or GPS_cord_input_long > topLeftLong:
        print('GPS out of range of given image')
        flag = 0
    else:
        flag = 1 

    gps_x = int(abs(topLeftLat - GPS_cord_input_lat) * 1000000 * pxl_per_1dcml)
    gps_y = int(abs(topLeftLong - GPS_cord_input_long) * 1000000 * pxl_per_1dcml)

    print(gps_x)

    img = cv2.cvtColor(img_binary,cv2.COLOR_BGR2RGB)

    # ''' uncomment when not demonstrating

    plt.imshow(img)
    plt.plot(gps_x,gps_y,'ro',markersize=5)
    plt.plot([0,width,width,0,0],[0,0,height,height,0])
    plt.show()
    # ''' uncomment when not demonstrating

    return flag, gps_x, gps_y

def pxl_put_begin(img_RGBcolor, pos_pxlX, pos_pxlY,wait_key):

    img_RGBcolor[pos_pxlY:(pos_pxlY+5),pos_pxlX:(pos_pxlX+5)] = [0,0,255]

    img_RGBcolor_resize = cv2.resize(img_RGBcolor, (1920, 1080))
    
    # -- Uncomment when not demonstrating 
    '''
    cv2.imwrite("Analyze.jpg",img_RGBcolor_resize)
    '''

    # -- Comment out when not demonstrating
    cv2.imshow("Position Marked Image", img_RGBcolor_resize)
    cv2.waitKey(wait_key)
    cv2.destroyAllWindows()

    return img_RGBcolor

def pxl_put_end(anlz,endX,endY,wait_key):
    anlz[endY:(endY+5),endX:(endX+5)] = [0,0,255]

    anlz_resize = cv2.resize(anlz, (1920, 1080))

    cv2.imshow("End and Begining Defined",anlz_resize)
    cv2.waitKey(wait_key)
    cv2.destroyAllWindows()

    cv2.imwrite("Sample.jpg",anlz_resize)

    return anlz

def RRT():
    pass



if __name__ == "__main__":

    # -- Globals -- #
    im_path = 'Airport Floor Plan.jpg'
    threshold_val = 128
    wait_key = 0 # Q is waitkey
    GPS_cord_input_lat = 40.42770
    GPS_cord_input_long = -86.912000
    endX = 800
    

    # -- Function Calls -- #
    height, width, img_binary, img_RGBcolor = imgBinary(threshold_val,im_path,wait_key)
    flag, pos_pxlX, pos_pxlY = GPS_rect(GPS_cord_input_lat,GPS_cord_input_long,img_binary, height, width)
    anlz = pxl_put_begin(img_RGBcolor, pos_pxlX, pos_pxlY, wait_key)
    pxl_put_end(anlz,endX,pos_pxlY,wait_key)
