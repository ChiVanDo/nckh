import serial
import time
ser = serial.Serial('COM3', 9600)

def main():
    # 00 Phải/Trên
    # 01 Phải/Dưới
    
    # 10 Trái/Trên
    # 11 Trái/Dưới
    goc = 0
    while True:
        pt,pd,tt,td = '00','01','10','11'
        goc = goc + 1
        
        gocPackage = str(goc) +'\n'
        directionPackage = pt +'.'
        
        
        ser.write(gocPackage.encode()) 
        time.sleep(0.05)
        ser.write(directionPackage.encode()) 
      
        print('STR Sent:' + gocPackage)


if __name__ == "__main__":
    main()