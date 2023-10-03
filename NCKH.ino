// *** A4988 ***
//  MS1   MS2   MS3   Microstep resolution
//  Low   Low   Low       Full step = 1 bước = 1.8'
//  High  Low   Low       1/2 step
//  Low   High  Low       1/4 step
//  High  High  Low       1/8 step
//  High  High  High      1/16 step
//.....................................
//  *** 8825 ***
//  Low   Low   Low       Full step
//  High  Low   Low       Half step
//  Low   High  Low       1/4 step
//  High  High  Low       1/8 step
//  Low   Low   High      1/16 step
//  High  Low   High      1/32 step
//  Low   High  High      1/32 step
//  High  High  High      1/32 step

/*********************************************************************
  This is an example for our Monochrome OLEDs based on SH110X drivers

  This example is for a 128x64 size display using I2C to communicate
  3 pins are required to interface (2 I2C and one reset)

  Adafruit invests time and resources providing this open source code,
  please support Adafruit and open-source hardware by purchasing
  products from Adafruit!

  Written by Limor Fried/Ladyada  for Adafruit Industries.
  BSD license, check license.txt for more information
  All text above, and the splash screen must be included in any redistribution

  i2c SH1106 modified by Rupert Hirst  12/09/21
*********************************************************************/



#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

/* Uncomment the initialize the I2C address , uncomment only one, If you get a totally blank screen try the other*/
#define i2c_Address 0x3c  //initialize with the I2C addr 0x3C Typically eBay OLED's
//#define i2c_Address 0x3d //initialize with the I2C addr 0x3D Typically Adafruit OLED's

#define SCREEN_WIDTH 128  // OLED display width, in pixels
#define SCREEN_HEIGHT 64  // OLED display height, in pixels
#define OLED_RESET -1     //   QT-PY / XIAO
Adafruit_SH1106G display = Adafruit_SH1106G(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);


#define NUMFLAKES 10
#define XPOS 0
#define YPOS 1
#define DELTAY 2


#define LOGO16_GLCD_HEIGHT 16
#define LOGO16_GLCD_WIDTH 16

int tep0 = 12;
int dir0 = 13;
int ena0 = 11;

//
int tep1 = 7;
int dir1 = 8;
int ena1 = 6;
//

int chieuX = 0, chieuY = 1;

int speed = 650;
void setup() {
  Serial.begin(9600);

  delay(250);                        // wait for the OLED to power up
  display.begin(i2c_Address, true);  // Address 0x3C default
  display.clearDisplay();
  // text display tests
  display.setTextSize(1);
  display.setTextColor(SH110X_WHITE);
  display.setCursor(0, 0);
  display.println("Hi let's go");
  display.display();
  delay(2000);
  //Serial.begin(9600);
  pinMode(ena0, OUTPUT);  // Enable pin dùng để khởi động motor
  pinMode(tep0, OUTPUT);  // Step chân xung
  pinMode(dir0, OUTPUT);  // Dir xác định chiều quay

  pinMode(ena1, OUTPUT);  // Enable pin dùng để khởi động motor
  pinMode(tep1, OUTPUT);  // Step chân xung
  pinMode(dir1, OUTPUT);  // Dir xác định chiều quay

  digitalWrite(ena0, 0);  // Set Enable LOW - khởi động motor

  digitalWrite(ena1, 0);  // Set Enable LOW - khởi động motor
}

bool flagSwitchX = false;
bool flagSwitchY = false;
void loop() {
  static int x = 0, y = 0;
  String gocX = "";
  String gocY = "";
  int gocQuayX = 0, gocQuayY = 0;
  if (Serial.available() > 0) {
    gocX = Serial.readStringUntil('\n');
    gocY = Serial.readStringUntil(',');
    String direction = Serial.readStringUntil('.');
    //00,01 phải => x = 0: 10,11 trái => x = 1
    // 01,11 trên => y = 1: 00,10 dưới => y = 0

    // if (direction == "00" || direction == "10" ) {
    //   chieuX = 0;
    //   chieuY = 0;
    //   flagSwitchX = false;
    //   flagSwitchY = false;
    // } else if (direction == "01" || direction == "11") {
    //   chieuX = 1;
    //   chieuY = 1;
    //   flagSwitchX = false;
    //   flagSwitchY = false;
    // }else{ // NULL HOẶC OK ĐỀU DỪNG // nhưng OK ĐỂ BẮN SÚNG CÒN NULL để sleep
    //   flagSwitchX = true;
    //   flagSwitchY = true;
    // }
    // 00,01 phải => x = 0: 10,11 trái => x = 1
    // 00,10 dưới => y = 0: 01,11 trên => y = 1

    if (direction == "00") {
      chieuX = 0;
      chieuY = 0;
      flagSwitchX = false;
      flagSwitchY = false;
    } else if (direction == "01") {
      chieuX = 0;
      chieuY = 1;
      flagSwitchX = false;
      flagSwitchY = false;
    } else if (direction == "10") {
      chieuX = 1;
      chieuY = 0;
      flagSwitchX = false;
      flagSwitchY = false;
    } else if (direction == "11") {
      chieuX = 1;
      chieuY = 1;
      flagSwitchX = false;
      flagSwitchY = false;
    } else if(direction == "OK"){
      flagSwitchX = true;
      flagSwitchY = true;
    }




    if (gocX != "") {  // cập nhật lại góc
      gocQuayX = gocX.toInt();
      //gocQuayY = gocY.toInt();
      x = 0;
      //y = 0;
    }
    if (gocY != "") {  // cập nhật lại góc
      gocQuayY = gocY.toInt();
      //gocQuayY = gocY.toInt();
      y = 0;
      //y = 0;
    }


    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("GOCX:");
    display.setCursor(30, 0);
    display.println(gocX);
    display.setCursor(0, 10);
    display.println("GOCY:");
    display.setCursor(30, 10);
    display.println(gocY);
    display.setCursor(0, 20);
    display.println("DIR:");
    display.setCursor(30, 20);
    display.println(direction);


    display.setCursor(0, 30);
    display.println("FLAG:");
    display.setCursor(30, 30);
    display.println(flagSwitchX);
    display.display();
  }


  //Chân dir dùng để xác định chiều quay (hoặc thay đổi dây của motor)
  //digitalWrite(dir1,chieu); //Chân dir dùng để xác định chiều quay (hoặc thay đổi dây của motor)
  
  if (!flagSwitchX) {
    if (gocQuayX != 0) {
      digitalWrite(dir0, chieuX);
      for (x; x < gocQuayX; x++)  //Quay 1 vòng
      {
        digitalWrite(tep0, HIGH);  // Cạnh lên
        //digitalWrite(tep1,HIGH); // Cạnh lên
        delayMicroseconds(speed);   //Thời gian xuất xung = tốc độ quay
        digitalWrite(tep0, LOW);  // Cạnh xuống
        //digitalWrite(tep1,LOW); // Cạnh xuống
        delayMicroseconds(speed);
      }
    }
  }
  
  if (!flagSwitchY) {
    if (gocQuayY != 0) {
      digitalWrite(dir1, chieuY);
      for (y; y < gocQuayY; y++)  //Quay 1 vòng
      {
        digitalWrite(tep1, HIGH);  // Cạnh lên
        //digitalWrite(tep1,HIGH); // Cạnh lên
        delayMicroseconds(speed);   //Thời gian xuất xung = tốc độ quay
        digitalWrite(tep1, LOW);  // Cạnh xuống
        //digitalWrite(tep1,LOW); // Cạnh xuống
        delayMicroseconds(speed);
      }
    }
  }
}