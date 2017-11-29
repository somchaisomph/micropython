# Repository of my micropython for ESP8266/ESP32

Links:
1. http://docs.micropython.org/en/latest/esp8266/
2. https://github.com/micropython/micropython-esp32
3. https://github.com/micropython/micropython
4. https://github.com/micropython/micropython-lib
5. http://micropython.org/download

<h2>Howto compile  MicroPython Firmware for ESP32</h2>


1. Setting up toolchain 

	- install dependencies :

		sudo apt-get install git wget make libncurses-dev flex bison gperf python python-serial

	-  Download  Xtensa cross-compiler  from http://domoticx.com/sdk-esp32-xtensa-architecture-toolchain/
(alternate : https://github.com/espressif/esp-idf/issues/279)

	-  add Xtensa path to system PATH :  export PATH=$PATH:$HOME/esp/xtensa-esp32-elf/bin

2. Get ESP-IDF
 	 - git clone --recursive https://github.com/espressif/esp-idf.git

	- cd to esp-idf directory then type following command :
		git submodule update --init

3.  download MicroPython for ESP32 from https://github.com/micropython/micropython-esp32
	- cd to eps32 under the micropython-esp32
	
	- create your own file named : "makefile" then add these statements into file :

	ESPIF=/home/somchai/projects/esp32/esp-idf #where esp-idf is
	PORT=/dev/ttyUSB0
	FLASH_MODE=qio
	FLASH_SIZE=4MB
	FLASH_FREQ=40m
	CROSS_COMPILE=xtensa-esp32-elf-

	include Makefile

	- cd to root of repository of MicroPython then do as followings :
		$ git submodule init lib/berkeley-db-1.xx # because Esp32 port has a dependency on it
		$ git submodule update

	- to pre-compile
		$ make -C mpy-cross

	- Then cd to esp32 directory and run :
		$ cd esp32
		$ make

		this produces binary firmware image file in buid subdirectory

	- To erase old firmware use:
		$ make erase
		
	- To flash firmware to ESP32 use :
		$ make deploy 
	
		this uses esptool.py locates in ESP-IDF 
		

<h2>How to upload pre-compiled firmware from micropython </h2>

esptool.py --chip esp32 --port /dev/ttyUSB1 write_flash -z 0x1000 firmware.bin
