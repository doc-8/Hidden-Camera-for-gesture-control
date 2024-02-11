02/10/24

README- Jetson Nano AI Home Station- Hidden Camera for gesture control

1. Project description
2. Hardware used
3. Instructions
4. Special Thanks

1) Project description

In this project the Jetson Nano B01 (A02 would work just the same) was used as a hub to send orders to a raspberry pi pico microcontroller and receive data from an ESP32-S3 Xiao board to allow gesture recognition control of an LED strip. The EPS32S3 board is a very small board that has (among others) both camera and Wifi module. It can easily be hidden in small-or mid-sized objects. In this project the camera was integrated into a christmas ball that had enough space to include a 2000mAh lithium battery. The raspberry pi pico was used to control an LED strip with 300 LEDs. 

Based on this project it's easy to set up a diy home control system with virtually invisible controls.


2) Hardware used

+Jetson Nano B01

AC8265 Wireless NIC Dual Mode Wireless Card for Jetson Nano (or other Wifi option)
JetPack 4.6.0
OpenCV 4.5.3


+XIAO ESP32-S3

Micropython Firmware for the XIAO ESP32S3

Follow the description in the following URL:
https://wiki.seeedstudio.com/XIAO_ESP32S3_Micropython/

Copper Heatsinks for Raspberry Pi 5, Heatsinks CPU Cooler with Thermal Conductive Adhensive Tape for Raspberry Pi 5 
The small square-shaped heatsink was glued to the back of the ESP32-S3 to resolve the problem of exsessive heating of the board during video streaming

3,7V 2000mAh Lithium Batterie 1S 1C LiPo Battery, micro JST 1.25-plug for Arduino Node MCU ESP32 development board 

+Raspberry Pi Pico W


3) Instructions

+ solder a lithium battery to the ESP32-S3 connectors. It's recommended to solder a button or switch in between
+ install mediapipe on the jetoson nano (e.g. from https://github.com/anion0278/mediapipe-jetson)
+ copy the rbp_ files to the raspberry pi pico (e.g. using thonny IDE), rename the rbp_main.py file to just main.py to make the raspberry run it when powered up. make sure the pins in the file match the pins that connet the raspberry pi pico to the LED
+ replace the placeholders for the SSID and Wifi-password in the rbp_secrets.py and rbp_wifi.py files
+ flash the micropython firmware to the ESP32-S3 Xiao (link to instructions in the hardware section)
+ replace the placeholders in the ESP32-S3 main.py. You can look up the network adresses in your rooter or by connecting the devices by USB and running the files in the IDE (the adresses are pasted into the console when the devices connect to the network)
+ copy the esp_ files to the ESP32-S3, rename the esp_main.py to main.py before copying it
+ copy the nano_gesture.py file to the jetson nano and insert the Wifi adress and password that was put into the ESP32-S3 main.py file, also insert the raspberry pi adress

4) The ESP32-S3 Wifi-host code is based on the contributor project by Xiao Ling (link in the hardware section). Thanks for the detailed descriptions and instructions!

