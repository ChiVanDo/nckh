import cv2
import numpy as np
import math
import serial
import time

# Mở cổng COM


def redcolor(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower = [0, 100, 100]
    upper = [10, 255, 255]

    lower_red = np.array(lower)  # Giá trị thấp của màu đỏ
    upper_red = np.array(upper)  # Giá trị cao của màu đỏ
    kernel_size = (9, 9)
    blurred_image = cv2.GaussianBlur(hsv_image, kernel_size, 0)

    # Tạo mask dựa trên phạm vi màu đỏ
    mask = cv2.inRange(blurred_image, lower_red, upper_red)

    # Áp dụng mask lên ảnh gốc
    result = cv2.bitwise_and(image, image, mask=mask)
    # cv2.imshow('hh',result)

    # _, thresholded = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY) # chuyen anh sang B
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Find contours
    cv2.drawContours(image, contours, -1, (0, 0, 255), 2)  # ve Contours
    x, y, w, h = 0, 0, 0, 0

    if len(contours) != 0:
        x, y, w, h = cv2.boundingRect(contours[0])
        
      
    goc_quay_Px, goc_quay_Py = 0, 0
    direction = "null"
    if x != 0 and y != 0:
        Px = kcx(x, y, w, h)
        Py = kcy(x, y, w, h)
        if(Py > 15 or Px > 15):
            print("PixelX", Px)
            print("PixelY", Py)
            if x > 320 and y > 240:  # Phải/Dưới
                direction = "00"
            elif x > 320 and y < 240:  # Phải/Trên
                direction = "01"
            elif x < 320 and y > 240:  # Trái/Dưới
                direction = "10"
            elif x < 320 and y < 240:  # Trái/Trên
                direction = "11"
            
            goc_quay_Px = int((Px / 3.2) * 10)
            goc_quay_Py = int((Py / 4.3) * 10)
                
            # if(x > 320 or y > 240):
            #     goc_quay_Px = int((Px / 3.2) * 10)
            #     goc_quay_Py = int((Py / 3.2) * 10)
            # elif x < 320 or y < 240:
            #     goc_quay_Px = int((Px / 3.2) * 10)
            #     goc_quay_Py = int((Py / 3.2) * 10)
        elif Px < 15 and Py < 15:
            direction = "OK"
      
        

    drawKC(image, x, y, w, h)
    
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 255), 2)  # ve hinh chu nhat quanh contours
    
    print(goc_quay_Px,":", goc_quay_Py ,":", direction)
    return str(goc_quay_Px), str(goc_quay_Py), direction


def detecfire(image):
    blur = cv2.GaussianBlur(image, (15, 15), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    cv2.imshow("HSV", hsv)

    lower = [18, 50, 50]
    upper = [35, 255, 255]

    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    mask = cv2.inRange(hsv, lower, upper)

    cv2.imshow("mask", mask)

    img_out = cv2.bitwise_and(image, hsv, mask=mask)

    cv2.imshow("Original Image", image)
    cv2.imshow("FIRE", img_out)

    return img_out
def drawxy(img, x, y, w, h):
    cv2.line(img, (320, 0), (320, 480), (0, 255, 255), 2)  # dọc  y
    cv2.line(img, (0, 240), (640, 240), (0, 255, 255), 2)  # ngang x

    cv2.putText(
        img, "x", (620, 230), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA
    )
    cv2.putText(
        img, "y", (330, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA
    )
def drawKC(img, x, y, w, h):
    cv2.line(img, (320, y + int(h / 2)), (x + int(w / 2), y + int(h / 2)), (0, 255, 0), 2)  # line từ Y ra tâm ngọn lửa
    cv2.line(img, (x + int(w / 2), 240), (x + int(w / 2), y + int(h / 2)), (0, 255, 0), 2)  # line từ X ra tâm ngọn lửa
def distances(x, y, w, h):
    tam_lua = (x + int(w / 2), y + int(h / 2))
    # Tọa độ của điểm 1
    x1, y1 = 0, 240
    # Tọa độ của điểm 2
    x2, y2 = 320, 240  # x2 là tâm màn hình,
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    # In ra khoảng cách
    print(f"kc: {distance}")
    print(tam_lua)
def kcx(x, y, w, h):
    # Tọa độ của điểm 1
    # x1, y1 = 0, 240
    # Tọa độ của điểm 2
    # x2, y2 = 320, 240
    # tọa độ điểm 1
    # x1,y1 = 320, y+int(h/2)
    # tọa độ điểm 2
    # x2,y2 = x+int(w/2), y+int(h/2)
    kc = math.sqrt(
        ((x + int(w / 2) - 320)) ** 2 + ((y + int(h / 2)) - (y + int(h / 2))) ** 2
    )

    return kc
def kcy(x, y, w, h):
    # Tọa độ của điểm 1
    # x1, y1 = 0, 240
    # Tọa độ của điểm 2
    # x2, y2 = 320, 240
    # tọa độ điểm 1
    # tam_lua = (x+int(w/2), y+int(h/2))

    # x1,y1 = x+int(w/2), 240
    # tọa độ điểm 2
    # x2,y2 = x+int(w/2), y+int(h/2)
    # distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    kc = math.sqrt(
        ((x + int(w / 2)) - (x + int(w / 2))) ** 2 + ((y + int(h / 2)) - 240) ** 2
    )

    return kc
def main():
    ser = serial.Serial("COM3", 9600)
    fire_cascade = cv2.CascadeClassifier("nckh/fire_detection.xml")
    cam = cv2.VideoCapture(1)

    x, y, w, h = 0, 0, 0, 0
    flag = False
    last_send_time = time.time()
    while True:
        _, image = cam.read()
        
        #PackageGocPx, PackageGocPy, PackageDirection = redcolor(image)
        current_time = time.time()
        if current_time - last_send_time >= 1.5:  # 0.5 giây = 500ms
            
            PackageGocPx, PackageGocPy, PackageDirection = redcolor(image)
            str = PackageGocPx + "\n" + PackageGocPy + "," + PackageDirection + "."
            
            if(PackageDirection != "null" or PackageDirection != "OK"):
                print("hi")
                ser.write(str.encode())
            
            last_send_time = current_time  
                

        
        
          
    
        
        
        #image = cv2.resize(image_raw, (1024, 765))
        #fire = fire_cascade.detectMultiScale(image, 1.2, 1)
        drawxy(image, x, y, w, h)
        # for x, y, w, h in fire:
        #     cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        #     print("kc x:", kcx(x, y, w, h))
        #     print("kc y:", kcy(x, y, w, h))

        #     if x > 320:
        #         print("Lua ben phải")
        #     elif x < 320:
        #         print("Lua ben trai")
        #     else:
        #         print("O giua")

        # # distances(x,y,w,h)
        # if w != 0:
        #     drawKC(image, x, y, w, h)

        cv2.imshow("fr", image)
        k = cv2.waitKey(1)
        if k % 256 == 27:
            print("Close")
            break

    cam.release()
    cv2.destroyAllWindows()
    # ser.close()


if __name__ == "__main__":
      # Thay 'COMx' bằng tên cổng COM của Arduino
    # Đóng cổng COM
    main()
