
from time import sleep
from SX127x.LoRa import *
from SX127x.board_config import BOARD
from RPLCD.i2c import CharLCD
import datetime
import time
import serial
import re
import requests
##########################################################
import bme280
import smbus2 
##########################################################
import RPi.GPIO as GPIO
BUTTON_PIN = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=4, dotsize=10)
lcd.clear()
lcd.write_string('  Hello  World')
##########################################################
import BlynkLib
from BlynkTimer import BlynkTimer

BLYNK_AUTH_TOKEN = 'qTdhnZiZxMPcWAkudaX7VnJzEYCJcyrn'


# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

timer = BlynkTimer()
##############################
#port = 1
#address = 0x76 # Adafruit BME280 address. Other BME280s may be different
#bus = smbus2.SMBus(port)
#bme280.load_calibration_params(bus,address)
##############################
# Led control through V0 virtual pin
##########################################################

def button_released_callback(channel):
	lora.countLcd = lora.countLcd+1
	print("on peleased count ======= "+str(lora.countLcd))
	#lora.setCountLcd(lora.countLcd)
	lora.countSleep = 0
	if lora.countLcd >= 5:
		lora.countLcd = 1
	if lora.countLcd == 1:
		lcd.clear()
		lcd.write_string('  >>> HOME <<<')
	elif lora.countLcd == 2:
		if lora.checkstatusNode1 == 1:
			lcd.clear()
			lcd.write_string('>>> Node1 ON <<<')
			lcd.cursor_pos =(1,0)
			lcd.write_string('Water Level:{}'.format(str(lora.waterLevelNode1)))
			lcd.cursor_pos =(2,0)
			lcd.write_string('T:{}'.format(str(lora.tempNode1))+ '  H:{}'.format(str(lora.humNode1)))
			lcd.cursor_pos =(3,0)
			lcd.write_string(' ---------------')
		else:
			lcd.clear()
			lcd.write_string('>>>Node1 OFF<<<')
			lcd.cursor_pos =(1,0)
			lcd.write_string('Water Level:{}'.format(str(lora.waterLevelNode1)))
			lcd.cursor_pos =(2,0)
			lcd.write_string('T:{}'.format(str(lora.tempNode1))+ '  H:{}'.format(str(lora.humNode1)))
			lcd.cursor_pos =(3,0)
			lcd.write_string(' ---------------')
	elif lora.countLcd == 3:
		if lora.checkstatusNode2 == 1:
			lcd.clear()
			lcd.write_string('>>> Node2 ON <<<')
			lcd.cursor_pos =(1,0)
			lcd.write_string('Water Level:{}'.format(str(lora.waterLevelNode2)))
			lcd.cursor_pos =(2,0)
			lcd.write_string('T:{}'.format(str(lora.tempNode2))+ '  H:{}'.format(str(lora.humNode2)))
			lcd.cursor_pos =(3,0)
			lcd.write_string(' ---------------')
		else:
			lcd.clear()
			lcd.write_string('>>>Node2 OFF<<<')
			lcd.cursor_pos =(1,0)
			lcd.write_string('Water Level:{}'.format(str(lora.waterLevelNode2)))
			lcd.cursor_pos =(2,0)
			lcd.write_string('T:{}'.format(str(lora.tempNode2))+ '  H:{}'.format(str(lora.humNode2)))
			lcd.cursor_pos =(3,0)
			lcd.write_string(' ---------------')
	elif lora.countLcd == 4:
		if lora.checkstatusNode3 == 1:
			lcd.clear()
			lcd.write_string('>>>Node3 ON<<<')
			if lora.pumpModeNode3 == 1:
				if lora.pumpStateNode3 == 1:
					lcd.cursor_pos =(1,0)
					lcd.write_string('M:Auto  P:ON')
				else:
					lcd.cursor_pos =(1,0)
					lcd.write_string('M:Auto  P:OFF')
			else:
				if lora.pumpStateNode3 == 1:
					lcd.cursor_pos =(1,0)
					lcd.write_string('M:Manual  P: ON')
				else:
					lcd.cursor_pos =(1,0)
					lcd.write_string('M:Manual  P: OFF')
			lcd.cursor_pos =(2,0)
			lcd.write_string('T:{}'.format(str(lora.tempNode3))+ '  H:{}'.format(str(lora.humNode3)))
			lcd.cursor_pos =(3,0)
			lcd.write_string(' ---------------')
		else:
			lcd.clear()
			lcd.write_string('>>>Node3 OFF<<<')
			if lora.pumpModeNode3 == 1:
				if lora.pumpStateNode3 == 1:
					lcd.cursor_pos =(1,0)
					lcd.write_string('M:Auto  P:ON')
				else:
					lcd.cursor_pos =(1,0)
					lcd.write_string('M:Auto  P:OFF')
			else:
				if lora.pumpStateNode3 == 1:
					lcd.cursor_pos =(1,0)
					lcd.write_string('M:Manual  P: ON')
				else:
					lcd.cursor_pos =(1,0)
					lcd.write_string('M:Manual  P: OFF')
			lcd.cursor_pos =(2,0)
			lcd.write_string('T:{}'.format(str(lora.tempNode3))+ '  H:{}'.format(str(lora.humNode3)))
			lcd.cursor_pos =(3,0)
			lcd.write_string(' ---------------')
GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING,callback=button_released_callback,bouncetime=500)
###################################################### Blynk Node1 ##############################################################

@blynk.on("V6")
def blynk_handle_vpins(value):
    blynkModeNode1 = int(value[0])
    print("----------------------------------UPDATE--------------------------------------")
    print("blynkModeNode1 ",blynkModeNode1)
    lora.setBlynkModeNode1(blynkModeNode1)
@blynk.on("V7")
def blynk_handle_vpins(value):
    blynkTimeNormalNode1 = float(value[0])
    print("----------------------------------UPDATE--------------------------------------")
    print("blynkTimeNormalNode1 ",blynkTimeNormalNode1)
    lora.setBlynkTimeNormalNode1(blynkTimeNormalNode1)
@blynk.on("V8")
def blynk_handle_vpins(value):
    blynkTimeDebugNode1 = float(value[0])
    print("----------------------------------UPDATE--------------------------------------")
    print("blynkTimeDebugNode1 ",blynkTimeDebugNode1)
    lora.setBlynkTimeDebugNode1(blynkTimeDebugNode1)

###################################################### Blynk Node2 ##############################################################
@blynk.on("V16")
def blynk_handle_vpins(value):
    blynkModeNode2 = int(value[0])
    print("----------------------------------UPDATE--------------------------------------")
    print("blynkModeNode2 ",blynkModeNode2)
    lora.setBlynkModeNode2(blynkModeNode2)
@blynk.on("V17")
def blynk_handle_vpins(value):
    blynkTimeNormalNode2 = float(value[0])
    print("----------------------------------UPDATE--------------------------------------")
    print("blynkTimeNormalNode2 ",blynkTimeNormalNode2)
    lora.setBlynkTimeNormalNode2(blynkTimeNormalNode2)
@blynk.on("V18")
def blynk_handle_vpins(value):
    blynkTimeDebugNode2 = float(value[0])
    print("----------------------------------UPDATE--------------------------------------")
    print("blynkTimeDebugNode2 ",blynkTimeDebugNode2)
    lora.setBlynkTimeDebugNode2(blynkTimeDebugNode2)

###################################################### Blynk Node3 ##############################################################
@blynk.on("V23")
def blynk_handle_vpins(value):
    blynkPumpModeNode3 = int(value[0])
    print("----------------------------------UPDATE--------------------------------------")
    print("blynkPumpModeNode3 ",blynkPumpModeNode3)
    lora.setblynkPumpModeNode3(blynkPumpModeNode3)
@blynk.on("V24")
def blynk_handle_vpins(value):
    blynkModeNode3 = float(value[0])
    print("----------------------------------UPDATE--------------------------------------")
    print("blynkModeNode3 ",blynkModeNode3)
    lora.setBlynkModeNode3(blynkModeNode3)
@blynk.on("V25")
def blynk_handle_vpins(value):
    blynkPumpStateNode3 = float(value[0])
    print("----------------------------------UPDATE--------------------------------------")
    print("blynkPumpStateNode3 ",blynkPumpStateNode3)
    lora.setBlynkPumpStateNode3(blynkPumpStateNode3)
@blynk.on("V28")
def blynk_handle_vpins(value):
    blynkTimeNormalNode3 = float(value[0])
    print("----------------------------------UPDATE--------------------------------------")
    print("blynkTimeNormalNode3 ",blynkTimeNormalNode3)
    lora.setBlynkTimeNormalNode3(blynkTimeNormalNode3)
@blynk.on("V29")
def blynk_handle_vpins(value):
    blynkTimeDebugNode3 = float(value[0])
    print("----------------------------------UPDATE--------------------------------------")
    print("blynkTimeDebugNode3 ",blynkTimeDebugNode3)
    lora.setBlynkTimeDebugNode3(blynkTimeDebugNode3)
    
####################################################### Blynk Gateway ################################################################
@blynk.on("V38")
def blynk_handle_vpins(value):
    blynkWaterLevelStart = float(value[0])
    print("----------------------------------UPDATE--------------------------------------")
    print("blynkWaterLevelStart ",blynkWaterLevelStart)
    lora.setBlynkWaterLevelStart(blynkWaterLevelStart)
@blynk.on("V39")
def blynk_handle_vpins(value):
    blynkWaterLevelStop = float(value[0])
    print("----------------------------------UPDATE--------------------------------------")
    print("blynkWaterLevelStop ",blynkWaterLevelStop)
    lora.setBlynkWaterLevelStop(blynkWaterLevelStop)
@blynk.on("V40")
def blynk_handle_vpins(value):
    blynkUsageStateN1 = int(value[0])
    print("----------------------------------UPDATE--------------------------------------")
    print("blynkUsageStateN1 ",blynkUsageStateN1)
    lora.setBlynkUsageStateN1(blynkUsageStateN1)
@blynk.on("V41")
def blynk_handle_vpins(value):
    blynkUsageStateN2 = int(value[0])
    print("----------------------------------UPDATE--------------------------------------")
    print("blynkUsageStateN2 ",blynkUsageStateN2)
    lora.setBlynkUsageStateN2(blynkUsageStateN2)
@blynk.on("V42")
def blynk_handle_vpins(value):
    blynkUsageStateN3 = int(value[0])
    print("----------------------------------UPDATE--------------------------------------")
    print("blynkUsageStateN3 ",blynkUsageStateN3)
    lora.setBlynkUsageStateN3(blynkUsageStateN3)
@blynk.on("V43")
def blynk_handle_vpins(value):
    lora.usageNotify = int(value[0])
    print("----------------------------------UPDATE--------------------------------------")
    print("usageNotify ",lora.usageNotify)
@blynk.on("V44")
def blynk_handle_vpins(value):
    lora.tokenLine = str(value[0])
    print("----------------------------------UPDATE--------------------------------------")
    print("tokenLine ",lora.tokenLine)
# Led control through V0 virtual pin
#function to sync the data from virtual pins
#@blynk.on("connected")
#def blynk_connected():
#    print("Raspberry Pi Connected to New Blynk")
##########################################################
#def myData(self):
	#bme280_data = bme280.sample(bus,address)
	#temp = bme280_data.temperature
	
#	print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
#	print(self.localAddress_Gateway)
#timer.set_interval(10,myData)
BOARD.setup()  
 
class LoRaGateway(LoRa):
	def __init__(self, verbose=False):
		super(LoRaGateway, self).__init__(verbose)
		self.set_mode(MODE.SLEEP)
		self.set_dio_mapping([0] * 6)
		self.localAddress_Gateway = hex(0xbb)
		self.received_data = 0
		self.localAddress_rx = 0
		self.destination_rx = 0
		self.data_length_rx = 0
		self.stateRx = False
		self.checkDataNode = 0
		self.confirmReceive = False
		self.previousMillisNode1 = int(round(time.time() * 1000))  # ใช้ time.time() เพื่อดึงเวลาปัจจุบัน (ในวินาที) และคูณด้วย 1000 เพื่อแปลงเป็นมิลลิวินาที
		self.previousMillisNode2 = int(round(time.time() * 1000))  # ใช้ time.time() เพื่อดึงเวลาปัจจุบัน (ในวินาที) และคูณด้วย 1000 เพื่อแปลงเป็นมิลลิวินาที
		self.previousMillisNode3 = int(round(time.time() * 1000))  # ใช้ time.time() เพื่อดึงเวลาปัจจุบัน (ในวินาที) และคูณด้วย 1000 เพื่อแปลงเป็นมิลลิวินาที
		self.previousMillisLcd = int(round(time.time() * 1000))  # ใช้ time.time() เพื่อดึงเวลาปัจจุบัน (ในวินาที) และคูณด้วย 1000 เพื่อแปลงเป็นมิลลิวินาที
		self.countLcd = 1
		self.countSleep= 0
		self.flag = 0
		#//////////////////////Node 1/////////////////////////
		self.destination_Node1 = hex(0xa1)
		self.confirmNode1 = "Pass"
		self.waterLevelNode1 = 0
		self.tempNode1 = 0    
		self.humNode1 = 0
		self.battNode1 = 0
		self.stateNode1 = 0
		self.modeNode1 = 0    # 0 = DebugMode , 1 = NormalMode
		self.TimeNormalNode1 = 2
		self.TimeDebugNode1 = 1
		
		self.checkstatusNode1 = 0
		self.blynkModeNode1 = 0
		self.blynkTimeNormalNode1 = 0
		self.blynkTimeDebugNode1 = 0
		
		#//////////////////////Node 2/////////////////////////
		self.destination_Node2 = hex(0xb1)
		self.confirmNode2 = "Pass"
		self.waterLevelNode2 = 0
		self.tempNode2 = 0
		self.humNode2 = 0
		self.battNode2 = 0
		self.stateNode2 = 0
		self.modeNode2 = 0    # 0 = DebugMode , 1 = NormalMode
		self.TimeNormalNode2 = 2
		self.TimeDebugNode2 = 1
		
		self.checkstatusNode2 = 0
		self.blynkModeNode2 = 0
		self.blynkTimeNormalNode2 = 0
		self.blynkTimeDebugNode2 = 0
		
		#//////////////////////Node 3/////////////////////////
		self.destination_Node3 = hex(0xc1)
		self.confirmNode3 = "Pass"
		self.tempNode3 = 0
		self.humNode3 = 0
		self.pumpModeNode3 = 0	   # 0 = Manual    , 1 = Auto
		self.modeNode3 = 0         # 0 = DebugMode , 1 = NormalMode
		self.pumpStateNode3 = 0    # 0 = OFF       , 1 = ON
		self.pumpStatusNode3 = 0   
		self.statusNode3 = 0
		self.TimeNormalNode3 = 2
		self.TimeDebugNode3 = 1
		self.checkstatusNode3 = 0
		self.waterLevelStart = 0
		self.waterLevelStop = 0
		
		self.blynkPumpModeNode3 = 0
		self.blynkModeNode3 = 0
		self.blynkPumpStateNode3 = 0
		self.blynkTimeNormalNode3 = 0
		self.blynkTimeDebugNode3 = 0
		
		#////////////////////////Gateway/////////////////////////////
		self.blynkWaterLevelStart = 0
		self.blynkWaterLevelStop = 0
		self.blynkUsageStateN1 = 0
		self.blynkUsageStateN2 = 0
		self.blynkUsageStateN3 = 0
		self.averageWaterLevel  = 0
		self.usageNotify = 0
		self.tokenLine = ""
	#//////////////////////// value blynk Node 1///////////////////////////
	def setBlynkModeNode1(self, value):
		self.blynkModeNode1 = value
		print("blynk blynkModeNode1 pass", self.blynkModeNode1)
		
	def setBlynkTimeNormalNode1(self, value):
		self.blynkTimeNormalNode1 = value 
		print("blynk blynkTimeNormalNode1 pass", self.blynkTimeNormalNode1)
		
	def setBlynkTimeDebugNode1(self, value):
		self.blynkTimeDebugNode1 = value
		print("blynk blynkTimeDebugNode1 pass", self.blynkTimeDebugNode1)
	#////////////////////////value blynk Node 2///////////////////////////	
	def setBlynkModeNode2(self, value):
		self.blynkModeNode2 = value
		print("blynk blynkModeNode2 pass", self.blynkModeNode2)
		
	def setBlynkTimeNormalNode2(self, value):
		self.blynkTimeNormalNode2 = value
		print("blynk NblynkTimeNormalNode2", self.blynkTimeNormalNode2)
		
	def setBlynkTimeDebugNode2(self, value):
		self.blynkTimeDebugNode2 = value
		print("blynk blynkTimeDebugNode2 pass", self.blynkTimeDebugNode2)
	
	#////////////////////////value blynk Node 3///////////////////////////			
	def setblynkPumpModeNode3(self, value):
		self.blynkPumpModeNode3 = value
		print("blynk blynkPumpModeNode3 pass", self.blynkPumpModeNode3)
		
	def setBlynkModeNode3(self, value):
		self.blynkModeNode3 = value
		print("blynk blynkModeNode3 pass", self.blynkModeNode3)
		
	def setBlynkPumpStateNode3 (self, value):
		self.blynkPumpStateNode3 = value
		print("blynk blynkPumpStateNode3 pass", self.blynkPumpStateNode3)
		
	def setBlynkTimeNormalNode3(self, value):
		self.blynkTimeNormalNode3 = value
		print("blynk blynkTimeNormalNode3 pass", self.blynkTimeNormalNode3)
		
	def setBlynkTimeDebugNode3(self, value):
		self.blynkTimeDebugNode3 = value
		print("blynk blynkTimeDebugNode3 pass", self.blynkTimeDebugNode3)

	def setBlynkWaterLevelStart(self, value):
		self.blynkWaterLevelStart = value
		print("blynk blynkWaterLevelStart pass", self.blynkWaterLevelStart)
		
	def setBlynkWaterLevelStop(self, value):
		self.blynkWaterLevelStop = value
		print("blynk blynkWaterLevelStop pass", self.blynkWaterLevelStop)
	#////////////////////////////Gateway//////////////////////////////////
	def setBlynkUsageStateN1(self, value):
		self.blynkUsageStateN1 = value
		print("blynk blynkUsageStateN1 pass", self.blynkUsageStateN1)
	def setBlynkUsageStateN2(self, value):
		self.blynkUsageStateN2 = value
		print("blynk blynkUsageStateN2 pass", self.blynkUsageStateN2)
	def setBlynkUsageStateN3(self, value):
		self.blynkUsageStateN3 = value
		print("blynk blynkUsageStateN3 pass", self.blynkUsageStateN3)
	#////////////////////////////////////////////////////////////////////
	def setCountLcd(self, value):
		self.countLcd = value
		print("countLcd ==========", self.countLcd)
	def on_rx_done(self):
		#print("\nRxDone")
		self.clear_irq_flags(RxDone=1)
		payload = self.read_payload(nocheck=True)
		print("Received:", payload)
		if payload is not None and len(payload) >= 3 and len(payload) <=50:  # ตรวจสอบว่า payload มีข้อมูลและมีอย่างน้อย 3 องค์ประกอบ
			#self.received_data = bytes(payload).decode("utf-8", 'ignore')
			self.localAddress_rx = payload[0]
			self.destination_rx = payload[1]
			self.data_length_rx = payload[2]
			payload_without_first_three = payload[3:]
			# แปลงเป็นสตริง
			self.received_data  = ''.join([chr(num) for num in payload_without_first_three])
			if re.search(r'[A-Za-z,.[\]]',self.received_data):
				print("trueeeee")
				print("Received (as string)  :", self.received_data)
				blynk.sync_virtual(6,7,8,16,17,18,23,24,25,28,29,38,39,40,41,42,43,44)
				sleep(1)
				self.stateRx = True
				#blynk.sync_virtual(23,24,25,28,29,38,39)
			else:
				print("falseeee")
				
	def checkDataAndUpdate(self):
		if hex(self.localAddress_rx) == self.localAddress_Gateway and hex(self.destination_rx) == self.destination_Node1:
			current_time = datetime.datetime.now()
			print("***********************************************************")
			print("**************************Node 1***************************")
			print("*** destination  :" ,hex(self.destination_rx))
			print("*** localAddress :" ,hex(self.localAddress_rx))
			print("*** data         :" ,self.received_data)
			print("***********************************************************")
			print("***********************************************************")
			try:
				data_list = self.received_data.split(',')
				rxWaterLevelNode1 = float(data_list[0])
				rxTempNode1 = float(data_list[1])
				rxHumNode1 = float(data_list[2])
				rxBattNode1 = float(data_list[3])
				rxStateNode1 = int(data_list[4])
				rxModeNode1 = int(data_list[5])
				rxTimeNormalNode1 = float(data_list[6])
				rxTimeDebugNode1 = float(data_list[7])
				self.confirmReceive = True
			except:
				self.confirmReceive = False
			print(">>>>>>>>>>>>>>>>>>>>>ON<<<<<<<<<<<<<<<<<<<<<<<< ")
			print("blynkModeNode1 "+ str(self.blynkModeNode1))
			print("blynkTimeNormalNode1 "+str(self.blynkTimeNormalNode1))
			print("blynkTimeDebugNode1 "+str(self.blynkTimeDebugNode1))
			#	print("ssss")
			if self.confirmReceive == True:
				if rxModeNode1 == self.modeNode1 and rxTimeNormalNode1 == self.TimeNormalNode1 and rxTimeDebugNode1 == self.TimeDebugNode1:
					if self.blynkModeNode1 == self.modeNode1 and self.blynkTimeNormalNode1 == self.TimeNormalNode1 and self.blynkTimeDebugNode1 == self.TimeDebugNode1:
						print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Case 1 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
						self.waterLevelNode1 = rxWaterLevelNode1
						self.tempNode1 = rxTempNode1
						self.humNode1 = rxHumNode1
						self.battNode1 = rxBattNode1
						self.stateNode1 = rxStateNode1
						self.modeNode1 = rxModeNode1
						self.TimeNormalNode1 = rxTimeNormalNode1
						self.TimeDebugNode1 = rxTimeDebugNode1 
						print("send to blynk"+str(self.waterLevelNode1)+","+str(self.tempNode1)+","+str(self.humNode1)+","+str(self.battNode1)+","+str(self.stateNode1)+","+str(self.modeNode1)+","+str(self.TimeNormalNode1)+","+str(self.TimeDebugNode1))
						
						blynk.virtual_write(1,self.waterLevelNode1 )
						blynk.virtual_write(2,self.tempNode1 )
						blynk.virtual_write(3,self.humNode1 )
						blynk.virtual_write(4,self.battNode1 )
						blynk.virtual_write(5,self.stateNode1 )
						blynk.virtual_write(6,self.modeNode1 )
						blynk.virtual_write(7,self.TimeNormalNode1 )
						blynk.virtual_write(8,self.TimeDebugNode1 )
						stateBlynkRx = False
					else:
						print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Case 2 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
						self.waterLevelNode1 = rxWaterLevelNode1
						self.tempNode1 = rxTempNode1
						self.humNode1 = rxHumNode1
						self.battNode1 = rxBattNode1
						self.stateNode1 = rxStateNode1
						self.modeNode1 = self.blynkModeNode1
						self.TimeNormalNode1 = self.blynkTimeNormalNode1
						self.TimeDebugNode1 = self.blynkTimeDebugNode1 
						print("send to blynk"+str(self.waterLevelNode1)+","+str(self.tempNode1)+","+str(self.humNode1)+","+str(self.battNode1)+","+str(self.stateNode1)+","+str(self.modeNode1)+","+str(self.TimeNormalNode1)+","+str(self.TimeDebugNode1))
						
						blynk.virtual_write(1,self.waterLevelNode1 )
						blynk.virtual_write(2,self.tempNode1 )
						blynk.virtual_write(3,self.humNode1 )
						blynk.virtual_write(4,self.battNode1 )
						blynk.virtual_write(5,self.stateNode1 )
						blynk.virtual_write(6,self.modeNode1 )
						blynk.virtual_write(7,self.TimeNormalNode1 )
						blynk.virtual_write(8,self.TimeDebugNode1 )
						stateBlynkRx = False
				else:
					if self.blynkModeNode1 == self.modeNode1 and self.blynkTimeNormalNode1 == self.TimeNormalNode1 and self.blynkTimeDebugNode1 == self.TimeDebugNode1:
						print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Case 3 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
						self.waterLevelNode1 = rxWaterLevelNode1
						self.tempNode1 = rxTempNode1
						self.humNode1 = rxHumNode1
						self.battNode1 = rxBattNode1
						self.stateNode1 = rxStateNode1
						self.modeNode1 = rxModeNode1
						self.TimeNormalNode1 = rxTimeNormalNode1
						self.TimeDebugNode1 = rxTimeDebugNode1 
						print("send to blynk"+str(self.waterLevelNode1)+","+str(self.tempNode1)+","+str(self.humNode1)+","+str(self.battNode1)+","+str(self.stateNode1)+","+str(self.modeNode1)+","+str(self.TimeNormalNode1)+","+str(self.TimeDebugNode1))
						
						blynk.virtual_write(1,self.waterLevelNode1 )
						blynk.virtual_write(2,self.tempNode1 )
						blynk.virtual_write(3,self.humNode1 )
						blynk.virtual_write(4,self.battNode1 )
						blynk.virtual_write(5,self.stateNode1 )
						blynk.virtual_write(6,self.modeNode1 )
						blynk.virtual_write(7,self.TimeNormalNode1 )
						blynk.virtual_write(8,self.TimeDebugNode1 )
						stateBlynkRx = False
					else:
						print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Case 4 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
						self.waterLevelNode1 = rxWaterLevelNode1
						self.tempNode1 = rxTempNode1
						self.humNode1 = rxHumNode1
						self.battNode1 = rxBattNode1
						self.stateNode1 = rxStateNode1
						self.modeNode1 = rxModeNode1
						self.TimeNormalNode1 = rxTimeNormalNode1
						self.TimeDebugNode1 = rxTimeDebugNode1
						print("send to blynk"+str(self.waterLevelNode1)+","+str(self.tempNode1)+","+str(self.humNode1)+","+str(self.battNode1)+","+str(self.stateNode1)+","+str(self.modeNode1)+","+str(self.TimeNormalNode1)+","+str(self.TimeDebugNode1))
						
						blynk.virtual_write(1,self.waterLevelNode1 )
						blynk.virtual_write(2,self.tempNode1 )
						blynk.virtual_write(3,self.humNode1 )
						blynk.virtual_write(4,self.battNode1 )
						blynk.virtual_write(5,self.stateNode1 )
						blynk.virtual_write(6,self.modeNode1 )
						blynk.virtual_write(7,self.TimeNormalNode1 )
						blynk.virtual_write(8,self.TimeDebugNode1 )
						stateBlynkRx = False
			else:
				print("ConfirmReceive Error")
			current_data = "Time"+str(current_time)+" Data "+self.received_data 
			#print(current_data)
			#with open("logfile.txt", "a") as log_file:
			#	log_file.write(current_data + "\n")
			sleep(0.1)
			self.checkDataNode = 1
		elif hex(self.localAddress_rx) == self.localAddress_Gateway and hex(self.destination_rx) == self.destination_Node2:
			current_time = datetime.datetime.now()
			print("***********************************************************")
			print("**************************Node 2***************************")
			print("*** destination  :" ,hex(self.destination_rx))
			print("*** localAddress :" ,hex(self.localAddress_rx))
			print("*** data         :" ,self.received_data)
			print("***********************************************************")
			print("***********************************************************")
			try:
				data_list = self.received_data.split(',')
				rxWaterLevelNode2 = float(data_list[0])
				rxTempNode2 = float(data_list[1])
				rxHumNode2 = float(data_list[2])
				rxBattNode2 = float(data_list[3])
				rxStateNode2 = int(data_list[4])
				rxModeNode2 = int(data_list[5])
				rxTimeNormalNode2 = float(data_list[6])
				rxTimeDebugNode2 = float(data_list[7])
				self.confirmReceive = True
			except:
				self.confirmReceive = False
			print(">>>>>>>>>>>>>>>>>>>>>ON<<<<<<<<<<<<<<<<<<<<<<<< ")
			print("blynkModeNode2 "+ str(self.blynkModeNode2))
			print("blynkTimeNormalNode2 "+str(self.blynkTimeNormalNode2))
			print("blynkTimeDebugNode2 "+str(self.blynkTimeDebugNode2))
			#	print("ssss")
			if self.confirmReceive == True:
				if rxModeNode2 == self.modeNode2 and rxTimeNormalNode2 == self.TimeNormalNode2 and rxTimeDebugNode2 == self.TimeDebugNode2:
					if self.blynkModeNode2 == self.modeNode2 and self.blynkTimeNormalNode2 == self.TimeNormalNode2 and self.blynkTimeDebugNode2 == self.TimeDebugNode2:
						print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Case 1 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
						self.waterLevelNode2 = rxWaterLevelNode2
						self.tempNode2 = rxTempNode2
						self.humNode2 = rxHumNode2
						self.battNode2 = rxBattNode2
						self.stateNode2 = rxStateNode2
						self.modeNode2 = rxModeNode2
						self.TimeNormalNode2 = rxTimeNormalNode2
						self.TimeDebugNode2 = rxTimeDebugNode2 
						print("send to blynk"+str(self.waterLevelNode2)+","+str(self.tempNode2)+","+str(self.humNode2)+","+str(self.battNode2)+","+str(self.stateNode2)+","+str(self.modeNode2)+","+str(self.TimeNormalNode2)+","+str(self.TimeDebugNode2))
						
						blynk.virtual_write(11,self.waterLevelNode2)
						blynk.virtual_write(12,self.tempNode2)
						blynk.virtual_write(13,self.humNode2)
						blynk.virtual_write(14,self.battNode2)
						blynk.virtual_write(15,self.stateNode2)
						blynk.virtual_write(16,self.modeNode2)
						blynk.virtual_write(17,self.TimeNormalNode2)
						blynk.virtual_write(18,self.TimeDebugNode2)
						stateBlynkRx = False
					else:
						print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Case 2 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
						self.waterLevelNode2 = rxWaterLevelNode2
						self.tempNode2 = rxTempNode2
						self.humNode2 = rxHumNode2
						self.battNode2 = rxBattNode2
						self.stateNode2 = rxStateNode2
						self.modeNode2 = self.blynkModeNode2
						self.TimeNormalNode2 = self.blynkTimeNormalNode2
						self.TimeDebugNode2 = self.blynkTimeDebugNode2 
						print("send to blynk"+str(self.waterLevelNode2)+","+str(self.tempNode2)+","+str(self.humNode2)+","+str(self.battNode2)+","+str(self.stateNode2)+","+str(self.modeNode2)+","+str(self.TimeNormalNode2)+","+str(self.TimeDebugNode2))
						
						blynk.virtual_write(11,self.waterLevelNode2)
						blynk.virtual_write(12,self.tempNode2)
						blynk.virtual_write(13,self.humNode2)
						blynk.virtual_write(14,self.battNode2)
						blynk.virtual_write(15,self.stateNode2)
						blynk.virtual_write(16,self.modeNode2)
						blynk.virtual_write(17,self.TimeNormalNode2)
						blynk.virtual_write(18,self.TimeDebugNode2)
						stateBlynkRx = False
				else:
					if self.blynkModeNode2 == self.modeNode2 and self.blynkTimeNormalNode2 == self.TimeNormalNode2 and self.blynkTimeDebugNode2 == self.TimeDebugNode2:
						print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Case 3 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
						self.waterLevelNode2 = rxWaterLevelNode2
						self.tempNode2 = rxTempNode2
						self.humNode2 = rxHumNode2
						self.battNode2 = rxBattNode2
						self.stateNode2 = rxStateNode2
						self.modeNode2 = rxModeNode2
						self.TimeNormalNode2 = rxTimeNormalNode2
						self.TimeDebugNode2 = rxTimeDebugNode2 
						print("send to blynk"+str(self.waterLevelNode2)+","+str(self.tempNode2)+","+str(self.humNode2)+","+str(self.battNode2)+","+str(self.stateNode2)+","+str(self.modeNode2)+","+str(self.TimeNormalNode2)+","+str(self.TimeDebugNode2))
						
						blynk.virtual_write(11,self.waterLevelNode2)
						blynk.virtual_write(12,self.tempNode2)
						blynk.virtual_write(13,self.humNode2)
						blynk.virtual_write(14,self.battNode2)
						blynk.virtual_write(15,self.stateNode2)
						blynk.virtual_write(16,self.modeNode2)
						blynk.virtual_write(17,self.TimeNormalNode2)
						blynk.virtual_write(18,self.TimeDebugNode2)
						stateBlynkRx = False
					else:
						print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Case 4 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
						self.waterLevelNode2 = rxWaterLevelNode2
						self.tempNode2 = rxTempNode2
						self.humNode2 = rxHumNode2
						self.battNode2 = rxBattNode2
						self.stateNode2 = rxStateNode2
						self.modeNode2 = rxModeNode2
						self.TimeNormalNode2 = rxTimeNormalNode2
						self.TimeDebugNode2 = rxTimeDebugNode2
						print("send to blynk"+str(self.waterLevelNode2)+","+str(self.tempNode2)+","+str(self.humNode2)+","+str(self.battNode2)+","+str(self.stateNode2)+","+str(self.modeNode2)+","+str(self.TimeNormalNode2)+","+str(self.TimeDebugNode2))
						
						blynk.virtual_write(11,self.waterLevelNode2)
						blynk.virtual_write(12,self.tempNode2)
						blynk.virtual_write(13,self.humNode2)
						blynk.virtual_write(14,self.battNode2)
						blynk.virtual_write(15,self.stateNode2)
						blynk.virtual_write(16,self.modeNode2)
						blynk.virtual_write(17,self.TimeNormalNode2)
						blynk.virtual_write(18,self.TimeDebugNode2)
						stateBlynkRx = False
			else:
				print("ConfirmReceive Error")
			current_data = "Time"+str(current_time)+" Data "+self.received_data 
			#print(current_data)
			#with open("logfile.txt", "a") as log_file:
			#	log_file.write(current_data + "\n")
			sleep(0.1)
			self.checkDataNode = 2
		elif hex(self.localAddress_rx) == self.localAddress_Gateway and hex(self.destination_rx) == self.destination_Node3:
			print("***********************************************************")
			print("**************************Node 3***************************")
			print("*** destination  :" ,hex(self.destination_rx))
			print("*** localAddress :" ,hex(self.localAddress_rx))
			print("*** data         :" ,self.received_data)
			print("***********************************************************")
			print("***********************************************************")
			data_list = self.received_data.split(',')
			try:
				rxTempNode3 = float(data_list[0])
				rxHumNode3= float(data_list[1])
				rxPumpModeNode3 = int(data_list[2])
				rxModeNode3 = int(data_list[3])
				rxPumpStateNode3 = int(data_list[4])
				rxPumpStatusNode3 = int(data_list[5])
				rxStatusNode3 = int(data_list[6])
				rxTimeNormalNode3 = float(data_list[7])
				rxTimeDebugNode3= float(data_list[8])
				self.confirmReceive = True
			except:
				self.confirmReceive = False
			print(">>>>>>>>>>>>>>>>>>>>>ON<<<<<<<<<<<<<<<<<<<<<<<< ")
			print("blynkModeNode2 "+ str(self.blynkModeNode2))
			print("blynkTimeNormalNode2 "+str(self.blynkTimeNormalNode2))
			print("blynkTimeDebugNode2 "+str(self.blynkTimeDebugNode2))
			if self.confirmReceive == True:
				#pumpModeNode3...modeNode3....pumpStateNode3..pumpStatusNode3......TimeNormalNode3....TimeDebugNode3.....statusNode3
				if rxPumpModeNode3 == self.pumpModeNode3 and rxModeNode3 == self.modeNode3 and rxPumpStateNode3 == self.pumpStateNode3 and rxTimeNormalNode3 == self.TimeNormalNode3 and rxTimeDebugNode3 == self.TimeDebugNode3:
					if self.blynkPumpModeNode3 == self.pumpModeNode3 and self.blynkModeNode3 == self.modeNode3 and self.blynkPumpStateNode3 == self.pumpStateNode3 and self.blynkTimeNormalNode3 == self.TimeNormalNode3 and self.blynkTimeDebugNode3 == self.TimeDebugNode3:
						print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Case 1 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
						self.tempNode3 = rxTempNode3
						self.humNode3 = rxHumNode3
						self.pumpModeNode3 = rxPumpModeNode3	   
						self.modeNode3 = rxModeNode3         
						self.pumpStateNode3 = rxPumpStateNode3    
						self.pumpStatusNode3 = rxPumpStatusNode3   
						self.statusNode3 = rxStatusNode3
						self.TimeNormalNode3 = rxTimeNormalNode3
						self.TimeDebugNode3 = rxTimeDebugNode3
						print("send to blynk"+str(self.tempNode3)+","+str(self.humNode3)+","+str(self.pumpModeNode3)+","+str(self.modeNode3)+","+str(self.pumpStateNode3)+","+str(self.pumpStatusNode3)+","+str(self.statusNode3)+","+str(self.TimeNormalNode3)+","+str(self.TimeDebugNode3))
					
						blynk.virtual_write(21,self.tempNode3)
						blynk.virtual_write(22,self.humNode3)
						blynk.virtual_write(23,self.pumpModeNode3)
						blynk.virtual_write(24,self.modeNode3)
						blynk.virtual_write(25,self.pumpStateNode3)
						blynk.virtual_write(26,self.pumpStatusNode3)
						blynk.virtual_write(27,self.statusNode3)
						blynk.virtual_write(28,self.TimeNormalNode3)
						blynk.virtual_write(29,self.TimeDebugNode3) 
						stateBlynkRx = False
					else:
						print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Case 2 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
						self.tempNode3 = rxTempNode3
						self.humNode3 = rxHumNode3
						self.pumpModeNode3 = self.blynkPumpModeNode3	   
						self.modeNode3 = self.blynkModeNode3         
						self.pumpStateNode3 = self.blynkPumpStateNode3    
						self.pumpStatusNode3 = rxPumpStatusNode3  
						self.statusNode3 = rxStatusNode3
						self.TimeNormalNode3 = self.blynkTimeNormalNode3
						self.TimeDebugNode3 = self.blynkTimeDebugNode3
						print("send to blynk"+str(self.tempNode3)+","+str(self.humNode3)+","+str(self.pumpModeNode3)+","+str(self.modeNode3)+","+str(self.pumpStateNode3)+","+str(self.pumpStatusNode3)+","+str(self.statusNode3)+","+str(self.TimeNormalNode3)+","+str(self.TimeDebugNode3))
					
						blynk.virtual_write(21,self.tempNode3)
						blynk.virtual_write(22,self.humNode3)
						blynk.virtual_write(23,self.pumpModeNode3)
						blynk.virtual_write(24,self.modeNode3)
						blynk.virtual_write(25,self.pumpStateNode3)
						blynk.virtual_write(26,self.pumpStatusNode3)
						blynk.virtual_write(27,self.statusNode3)
						blynk.virtual_write(28,self.TimeNormalNode3)
						blynk.virtual_write(29,self.TimeDebugNode3) 
						stateBlynkRx = False
				else:
					if self.blynkPumpModeNode3 == self.pumpModeNode3 and self.blynkModeNode3 == self.modeNode3 and self.blynkPumpStateNode3 == self.pumpStateNode3 and self.blynkTimeNormalNode3 == self.TimeNormalNode3 and self.blynkTimeDebugNode3 == self.TimeDebugNode3:
						print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Case 3 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
						self.tempNode3 = rxTempNode3
						self.humNode3 = rxHumNode3
						self.pumpModeNode3 = rxPumpModeNode3	   
						self.modeNode3 = rxModeNode3         
						self.pumpStateNode3 = rxPumpStateNode3    
						self.pumpStatusNode3 = rxPumpStatusNode3   
						self.statusNode3 = rxStatusNode3
						self.TimeNormalNode3 = rxTimeNormalNode3
						self.TimeDebugNode3 = rxTimeDebugNode3
						print("send to blynk"+str(self.tempNode3)+","+str(self.humNode3)+","+str(self.pumpModeNode3)+","+str(self.modeNode3)+","+str(self.pumpStateNode3)+","+str(self.pumpStatusNode3)+","+str(self.statusNode3)+","+str(self.TimeNormalNode3)+","+str(self.TimeDebugNode3))
					
						blynk.virtual_write(21,self.tempNode3)
						blynk.virtual_write(22,self.humNode3)
						blynk.virtual_write(23,self.pumpModeNode3)
						blynk.virtual_write(24,self.modeNode3)
						blynk.virtual_write(25,self.pumpStateNode3)
						blynk.virtual_write(26,self.pumpStatusNode3)
						blynk.virtual_write(27,self.statusNode3)
						blynk.virtual_write(28,self.TimeNormalNode3)
						blynk.virtual_write(29,self.TimeDebugNode3) 
						stateBlynkRx = False
					else:
						print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Case 4 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
						self.tempNode3 = rxTempNode3
						self.humNode3 = rxHumNode3
						self.pumpModeNode3 = rxPumpModeNode3	   
						self.modeNode3 = rxModeNode3         
						self.pumpStateNode3 = rxPumpStateNode3    
						self.pumpStatusNode3 = rxPumpStatusNode3   
						self.statusNode3 = rxStatusNode3
						self.TimeNormalNode3 = rxTimeNormalNode3
						self.TimeDebugNode3 = rxTimeDebugNode3
						print("send to blynk"+str(self.tempNode3)+","+str(self.humNode3)+","+str(self.pumpModeNode3)+","+str(self.modeNode3)+","+str(self.pumpStateNode3)+","+str(self.pumpStatusNode3)+","+str(self.statusNode3)+","+str(self.TimeNormalNode3)+","+str(self.TimeDebugNode3))
					
						blynk.virtual_write(21,self.tempNode3)
						blynk.virtual_write(22,self.humNode3)
						blynk.virtual_write(23,self.pumpModeNode3)
						blynk.virtual_write(24,self.modeNode3)
						blynk.virtual_write(25,self.pumpStateNode3)
						blynk.virtual_write(26,self.pumpStatusNode3)
						blynk.virtual_write(27,self.statusNode3)
						blynk.virtual_write(28,self.TimeNormalNode3)
						blynk.virtual_write(29,self.TimeDebugNode3) 
						stateBlynkRx = False
			else:
				print("ConfirmReceive Error")		
			#current_data = "Time"+str(current_time)+" Data "+self.received_data 
			sleep(0.1)
			self.checkDataNode = 3
		else :
			self.checkDataNode = 0
			state = "ONE"
	def send_data(self, node):
		if node == 1:
			sleep(2)
			self.checkstatusNode1 = 1
			self.stateNode1 = self.checkstatusNode1 
			print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Send Node 1 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
			data = str(self.confirmNode1)+","+str(self.modeNode1)+","+str(self.TimeNormalNode1)+","+str(self.TimeDebugNode1)+","+str(self.stateNode1)
			print("Sending data:", data)
			data_length = len(data)
			data_to_send = str(int(self.destination_Node1,16)) + " " + str(int(self.localAddress_Gateway,16)) + " " + str(data_length) + " " + data
			print(data_to_send)
			print(data_to_send.split())
			self.write_payload(data_to_send)
			self.set_mode(MODE.TX)
			self.clear_irq_flags(TxDone=1)
			sleep(0.5) 
			self.set_mode(MODE.STDBY)
			self.set_mode(MODE.RXCONT)
			blynk.virtual_write(5,self.stateNode1)
			self.previousMillisNode1 = int(round(time.time() * 1000)) 
			self.flag = 1
		elif node == 2:
			sleep(2)
			self.checkstatusNode2 = 1
			self.stateNode2 = self.checkstatusNode2 
			print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Send Node 2 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
			data = str(self.confirmNode2)+","+str(self.modeNode2)+","+str(self.TimeNormalNode2)+","+str(self.TimeDebugNode2)+","+str(self.stateNode2)
			print("Sending data:", data)
			data_length = len(data)
			data_to_send = str(int(self.destination_Node2,16)) + " " + str(int(self.localAddress_Gateway,16)) + " " + str(data_length) + " " + data
			print(data_to_send)
			print(data_to_send.split())
			self.write_payload(data_to_send)
			self.set_mode(MODE.TX)
			self.clear_irq_flags(TxDone=1)
			sleep(0.5) 
			self.set_mode(MODE.STDBY)
			self.set_mode(MODE.RXCONT)
			blynk.virtual_write(15,self.stateNode2)
			self.previousMillisNode2 = int(round(time.time() * 1000)) 
			self.flag = 1
		elif node == 3:
			print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Send Node 3 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
			sleep(2)
			if self.pumpModeNode3 == 1:
				'''
				print("########################################### Mode AuTo ###########################################")
				if self.checkstatusNode1 == 1 and self.checkstatusNode2 == 1 and self.blynkUsageStateN1 == 1 and self.blynkUsageStateN2 == 1:#คอมเม้น self.checkstatusNode3 = 1 ต้องเช็คอันนี้ด้วนหรือเปล่า  
					print("########################################### Use Node1 and Node2 ###########################################")
					#AVERRAGE water Level
					self.averageWaterLevel = (self.waterLevelNode1+self.waterLevelNode2)/2
					if self.averageWaterLevel <= self.blynkWaterLevelStart:
						print("###################################### ON PUMP<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
						self.pumpStateNode3 = 1
					elif self.averageWaterLevel >= self.blynkWaterLevelStop:
						print("###################################### OFF PUMP<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
						self.pumpStateNode3 = 0
				elif self.checkstatusNode1 == 1 and self.blynkUsageStateN1 == 1:
					print("############################################### Use Node1 #################################################")
					if self.waterLevelNode1 <= self.blynkWaterLevelStart:
						print("#################################### ON PUMP<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
						self.pumpStateNode3 = 1
					elif self.waterLevelNode1 >= self.blynkWaterLevelStop:
						print("###################################### OFF PUMP<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
						self.pumpStateNode3 = 0
				elif self.checkstatusNode2 == 1 and self.blynkUsageStateN2 == 1:
					print("############################################### Use Node2 #################################################")
					if self.waterLevelNode2 <= self.blynkWaterLevelStart:
						print("###################################### ON PUMP<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
						self.pumpStateNode3 = 1
					elif self.waterLevelNode2 >= self.blynkWaterLevelStop:
						print("###################################### OFF PUMP<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
						self.pumpStateNode3 = 0
				else:
					self.pumpStateNode3 = 0
					#print("########################################### NOT ON button Usage Node1 or Node2 OR Node1 OFF OR Node2 OFF ###########################################")
				'''
				self.checkstatusNode3 = 1
				self.statusNode3 = self.checkstatusNode3
				#pumpModeNode3...modeNode3....pumpStateNode3....statusNode3....TimeNormalNode3....TimeDebugNode3
				data = str(self.confirmNode3)+","+str(self.pumpModeNode3)+","+str(self.modeNode3)+","+str(self.pumpStateNode3)+","+str(self.statusNode3)+","+str(self.TimeNormalNode3)+","+str(self.TimeDebugNode3)
				print("Sending data Node3:", data)
				data_length = len(data)
				data_to_send = str(int(self.destination_Node3,16)) + " " + str(int(self.localAddress_Gateway,16)) + " " + str(data_length) + " " + data
				print(data_to_send.split())
				self.write_payload(data_to_send)
				self.set_mode(MODE.TX)
				self.clear_irq_flags(TxDone=1)
				sleep(0.5) 
				self.set_mode(MODE.STDBY)
				self.set_mode(MODE.RXCONT)
				blynk.virtual_write(25,self.pumpStateNode3)
				blynk.virtual_write(26,self.pumpStatusNode3)
				blynk.virtual_write(27,self.statusNode3)
				self.previousMillisNode3 = int(round(time.time() * 1000)) 
			else:
				print("######################################### Mode Mannual ##########################################")
				self.checkstatusNode3 = 1
				self.statusNode3 = self.checkstatusNode3
				#pumpModeNode3...modeNode3....pumpStateNode3....statusNode3....TimeNormalNode3....TimeDebugNode3
				data = str(self.confirmNode3)+","+str(self.pumpModeNode3)+","+str(self.modeNode3)+","+str(self.pumpStateNode3)+","+str(self.statusNode3)+","+str(self.TimeNormalNode3)+","+str(self.TimeDebugNode3)
				print("Sending data Node3:", data)
				data_length = len(data)
				data_to_send = str(int(self.destination_Node3,16)) + " " + str(int(self.localAddress_Gateway,16)) + " " + str(data_length) + " " + data
				print(data_to_send.split())
				self.write_payload(data_to_send)
				self.set_mode(MODE.TX)
				self.clear_irq_flags(TxDone=1)
				sleep(0.5) 
				self.set_mode(MODE.STDBY)
				self.set_mode(MODE.RXCONT)
				blynk.virtual_write(27,self.statusNode3)
				self.previousMillisNode3 = int(round(time.time() * 1000))
			self.flag = 1
	
	def myDataa(self):
		#bme280_data = bme280.sample(bus,address)
		#temp = bme280_data.temperature
		print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
	def setupMode(self):
		blynk.run()
		rssi_value = self.get_rssi_value()
		status = self.get_modem_status()
		sys.stdout.flush()
	def checkStatusNode(self):
		##################################################### Node1 ################################################################################
		if self.modeNode1 == 1:
			currentMillisNode1 = int(round(time.time() * 1000)) # ดึงเวลาปัจจุบันในทุกครั้งในลูป
			if currentMillisNode1 - self.previousMillisNode1 >= self.TimeNormalNode1 * 60 * 1000 * 1.2:     #self.TimeNormalNode1*60*
				if(self.checkstatusNode1 == 0):  #update ค่า ขึ้นblynk
					self.checkstatusNode1 = 0
					self.stateNode1 = self.checkstatusNode1
					blynk.virtual_write(5,self.stateNode1)
					print(">>>>>>>>>>>>>>>>>>>>              TimeNormalNode1                <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
					print(">>>>>>>>>>>>>>>>>>>>                  NO PASS                    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
					print(">>>>>>>>>>>>>>>>>>>>checkstatusNode1"+str(self.checkstatusNode1)+" <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
				else:							#update ค่า ขึ้นblynk
					self.checkstatusNode1 = 0
					self.stateNode1 = self.checkstatusNode1
					blynk.virtual_write(5,self.stateNode1)
					print(">>>>>>>>>>>>>>>>>>>>              TimeNormalNode1                <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
					print(">>>>>>>>>>>>>>>>>>>>                   PASS                      <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
					print(">>>>>>>>>>>>>>>>>>>>checkstatusNode1"+str(self.checkstatusNode1)+" <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
				# อัปเดตค่า previousMillisSw เมื่อทำงานเสร็จสิ้น
				self.previousMillisNode1 = currentMillisNode1
		else:
			currentMillisNode1 = int(round(time.time() * 1000))  # ดึงเวลาปัจจุบันในทุกครั้งในลูป
			if currentMillisNode1 - self.previousMillisNode1 >= self.TimeDebugNode1 * 60 * 1000 * 1.2: #self.TimeDebugNode1*60*
				if(self.checkstatusNode1 == 0):  #update ค่า ขึ้นblynk
					self.checkstatusNode1 = 0
					self.stateNode1 = self.checkstatusNode1
					blynk.virtual_write(5,self.stateNode1)
					print(">>>>>>>>>>>>>>>>>>>>               TimeDebugNode1                <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
					print(">>>>>>>>>>>>>>>>>>>>                  NO PASS                    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
					print(">>>>>>>>>>>>>>>>>>>>checkstatusNode1"+str(self.checkstatusNode1)+" <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
				else:							#update ค่า ขึ้นblynk
					self.checkstatusNode1 = 0
					self.stateNode1 = self.checkstatusNode1
					blynk.virtual_write(5,self.stateNode1)
					print(">>>>>>>>>>>>>>>>>>>>               TimeDebugNode1                <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
					print(">>>>>>>>>>>>>>>>>>>>                   PASS                      <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
					print(">>>>>>>>>>>>>>>>>>>>checkstatusNode1"+str(self.checkstatusNode1)+" <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
				# อัปเดตค่า previousMillisSw เมื่อทำงานเสร็จสิ้น
				self.previousMillisNode1 = currentMillisNode1
		##################################################### Node2 ################################################################################
		if self.modeNode2 == 1:
			currentMillisNode2 = int(round(time.time() * 1000))  # ดึงเวลาปัจจุบันในทุกครั้งในลูป
			if currentMillisNode2 - self.previousMillisNode2 >= self.TimeNormalNode2*60*1000 * 1.2:     #self.TimeNormalNode2*60*
				if(self.checkstatusNode2 == 0):  #update ค่า ขึ้นblynk
					self.checkstatusNode2 = 0
					self.stateNode2 = self.checkstatusNode2
					blynk.virtual_write(15,self.stateNode2)
					print(">>>>>>>>>>>>>>>>>>>>              TimeNormalNode2                <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
					print(">>>>>>>>>>>>>>>>>>>>                  NO PASS                    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
					print(">>>>>>>>>>>>>>>>>>>>checkstatusNode2"+str(self.checkstatusNode2)+" <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
				else:							#update ค่า ขึ้นblynk
					self.checkstatusNode2 = 0
					self.stateNode2 = self.checkstatusNode2
					blynk.virtual_write(15,self.stateNode2)
					print(">>>>>>>>>>>>>>>>>>>>              TimeNormalNode2                <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
					print(">>>>>>>>>>>>>>>>>>>>                   PASS                      <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
					print(">>>>>>>>>>>>>>>>>>>>checkstatusNode2"+str(self.checkstatusNode2)+" <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
				# อัปเดตค่า previousMillisNode2 เมื่อทำงานเสร็จสิ้น
				self.previousMillisNode2 = currentMillisNode2
		else:
			currentMillisNode2 = int(round(time.time() * 1000))  # ดึงเวลาปัจจุบันในทุกครั้งในลูป
			if currentMillisNode2 - self.previousMillisNode2 >= self.TimeDebugNode2*60*1000 * 1.2: #self.TimeDebugNode2*60*
				if(self.checkstatusNode2 == 0):  #update ค่า ขึ้นblynk
					self.checkstatusNode2 = 0
					self.stateNode2 = self.checkstatusNode2
					blynk.virtual_write(15,self.stateNode2)
					print(">>>>>>>>>>>>>>>>>>>>               TimeDebugNode2                <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
					print(">>>>>>>>>>>>>>>>>>>>                  NO PASS                    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
					print(">>>>>>>>>>>>>>>>>>>>checkstatusNode2"+str(self.checkstatusNode2)+" <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
				else:							#update ค่า ขึ้นblynk
					self.checkstatusNode2 = 0
					self.stateNode2 = self.checkstatusNode2
					blynk.virtual_write(15,self.stateNode2)
					print(">>>>>>>>>>>>>>>>>>>>               TimeDebugNode2                <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
					print(">>>>>>>>>>>>>>>>>>>>                   PASS                      <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
					print(">>>>>>>>>>>>>>>>>>>>checkstatusNode2"+str(self.checkstatusNode2)+" <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
				# อัปเดตค่า previousMillisNode2 เมื่อทำงานเสร็จสิ้น
				self.previousMillisNode2 = currentMillisNode2
		##################################################### Node3 ################################################################################		
		if self.modeNode3 == 1:
			currentMillisNode3 = int(round(time.time() * 1000))  # ดึงเวลาปัจจุบันในทุกครั้งในลูป
			if currentMillisNode3 - self.previousMillisNode3 >= self.TimeNormalNode3*60*1000 * 1.2:     #self.TimeNormalNode3*60*
				if(self.checkstatusNode3 == 0):  #update ค่า ขึ้นblynk
					self.checkstatusNode3 = 0
					self.stateNode3 = self.checkstatusNode3
					blynk.virtual_write(27,self.stateNode3)
					print(">>>>>>>>>>>>>>>>>>>>              TimeNormalNode3                <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
					print(">>>>>>>>>>>>>>>>>>>>                  NO PASS                    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
					print(">>>>>>>>>>>>>>>>>>>>checkstatusNode3"+str(self.checkstatusNode3)+" <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
				else:							#update ค่า ขึ้นblynk
					self.checkstatusNode3 = 0
					self.stateNode3 = self.checkstatusNode3
					blynk.virtual_write(27,self.stateNode3)
					print(">>>>>>>>>>>>>>>>>>>>              TimeNormalNode3                <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
					print(">>>>>>>>>>>>>>>>>>>>                   PASS                      <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
					print(">>>>>>>>>>>>>>>>>>>>checkstatusNode3"+str(self.checkstatusNode3)+" <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
				# อัปเดตค่า previousMillisNode3 เมื่อทำงานเสร็จสิ้น
				self.previousMillisNode3 = currentMillisNode3
		else:
			currentMillisNode3 = int(round(time.time() * 1000))  # ดึงเวลาปัจจุบันในทุกครั้งในลูป
			if currentMillisNode3 - self.previousMillisNode3 >= self.TimeDebugNode3*60*1000 * 1.2: #self.TimeDebugNode3*60*
				if(self.checkstatusNode3 == 0):  #update ค่า ขึ้นblynk
					self.checkstatusNode3 = 0
					self.stateNode3 = self.checkstatusNode3
					blynk.virtual_write(27,self.stateNode3)
					print(">>>>>>>>>>>>>>>>>>>>               TimeDebugNode3                <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
					print(">>>>>>>>>>>>>>>>>>>>                  NO PASS                    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
					print(">>>>>>>>>>>>>>>>>>>>checkstatusNode3"+str(self.checkstatusNode3)+" <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
				else:							#update ค่า ขึ้นblynk
					self.checkstatusNode3 = 0
					self.stateNode3 = self.checkstatusNode3
					blynk.virtual_write(27,self.stateNode3)
					print(">>>>>>>>>>>>>>>>>>>>               TimeDebugNode3                <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
					print(">>>>>>>>>>>>>>>>>>>>                   PASS                      <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
					print(">>>>>>>>>>>>>>>>>>>>checkstatusNode3"+str(self.checkstatusNode3)+" <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
				# อัปเดตค่า previousMillisNode3 เมื่อทำงานเสร็จสิ้น
				self.previousMillisNode3 = currentMillisNode3
		# ให้รอสักเล็กน้อยเพื่อไม่ให้ลูปทำงานเร็วเกินไป
		time.sleep(0.01)
	def notifications(self):
		#blynk.sync_virtual(6,7,8,16,17,18,23,24,25,28,29,38,39,40,41,42)
		if self.checkstatusNode1 == 1 and self.tempNode1 >= 80 and self.flag == 1:
			print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Temp Node 1 Over !!! <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
			blynk.log_event("temperaturenotification","Temp Node 1 Over")
			self.flag = 0
		if self.checkstatusNode2 == 1 and self.tempNode2 >= 80 and self.flag == 1:
			print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Temp Node 2 Over !!! <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
			blynk.log_event("temperaturenotification","Temp Node 2 Over")
			self.flag = 0
		if self.checkstatusNode3 == 1 and self.tempNode3 >= 80 and self.flag == 1:
			print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Temp Node 3 Over !!! <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
			blynk.log_event("temperaturenotification","Temp Node 3 Over")
			self.flag = 0
		if self.checkstatusNode1 == 1 and self.humNode1 >= 90 and self.flag == 1:
			print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Hum Node 1 Over !!! <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
			blynk.log_event("humiditynotification","Hum Node 1 Over")
			self.flag = 0
		if self.checkstatusNode2 == 1 and self.humNode2 >= 90 and self.flag == 1:
			print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Hum Node 2 Over !!! <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
			blynk.log_event("humiditynotification","Hum Node 1 Over")
			self.flag = 0
		if self.checkstatusNode3 == 1 and self.humNode3 >= 90 and self.flag == 1:
			print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Hum Node 3 Over !!! <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
			blynk.log_event("humiditynotification","Hum Node 1 Over")
			self.flag = 0
		if self.checkstatusNode1 == 1 and self.checkstatusNode2 == 1 and self.blynkUsageStateN1 == 1 and self.blynkUsageStateN2 == 1 and self.flag == 1:
			print("########################################### Use Node1 and Node2 ###########################################")
			#AVERRAGE water Level
			self.averageWaterLevel = (self.waterLevelNode1+self.waterLevelNode2)/2
			if self.averageWaterLevel <= self.blynkWaterLevelStart:
				print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> WaterLevel  LOW  Over !!! <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
				blynk.log_event("lowwaterlevelnotification","WaterLevel  LOW  Over !!!")
			elif self.averageWaterLevel >= self.blynkWaterLevelStop:
				print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> WaterLevel  HIGH  Over !!! <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
				blynk.log_event("highwaterlevelnotification","WaterLevel  HIGH  Over !!!")
			self.flag = 0
		elif self.checkstatusNode1 == 1 and self.blynkUsageStateN1 == 1 and self.flag == 1:
			print("############################################### Use Node1 #################################################")
			if self.waterLevelNode1 <= self.blynkWaterLevelStart:
				print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> WaterLevel  LOW  Over !!! <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
				blynk.log_event("lowwaterlevelnotification","WaterLevel  LOW  Over !!!")
			elif self.waterLevelNode1 >= self.blynkWaterLevelStop:
				print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> WaterLevel  HIGH  Over !!! <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
				blynk.log_event("highwaterlevelnotification","WaterLevel  HIGH  Over !!!")
			self.flag = 0
		elif self.checkstatusNode2 == 1 and self.blynkUsageStateN2 == 1 and self.flag == 1:
			print("############################################### Use Node2 #################################################")
			if self.waterLevelNode2 <= self.blynkWaterLevelStart:
				print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> WaterLevel  LOW  Over !!! <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
				blynk.log_event("lowwaterlevelnotification","WaterLevel  LOW  Over !!!")
			elif self.waterLevelNode2 >= self.blynkWaterLevelStop:
				print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> WaterLevel  HIGH  Over !!! <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
				blynk.log_event("highwaterlevelnotification","WaterLevel  HIGH  Over !!!")
			self.flag = 0
		#else:
			#print("########################################### NOT ON button Usage Node1 or Node2 ###########################################")
		if self.pumpStatusNode3 ==  1 and self.flag == 1:
			print("########################################### PUMP NOT WORK ###########################################")
			#blynk.log_event("pumpnotworknotification","PUMP NOT WORK!!!")
			self.flag = 0
	def _lineNotify(self,payload,file=None):
		url = 'https://notify-api.line.me/api/notify'
		token = self.tokenLine
		print('..........................................................................')
		print(token)
		headers = {'Authorization':'Bearer '+token}
		return requests.post(url, headers=headers , data = payload, files=file)
		#ข้อความ
		#lineNotify('ข้อความ')
		#notifySticker(11,1)
		#notifyPicture("ที่อยู่รูปภาพ")
	#ข้อความ
	def lineNotify(self,message):
		payload = {'message':message}
		return self._lineNotify(payload)
	#สติกเกอร์
	def notifySticker(self,stickerID,stickerPackageID):
		payload = {'message':" ",'stickerPackageId':stickerPackageID,'stickerId':stickerID}
		return self._lineNotify(payload)
	#รูปภาพ
	def notifyPicture(self,url):
		payload = {'message':" ",'imageThumbnail':url,'imageFullsize':url}
		return self._lineNotify(payload)
	#ส่งแจ้งเตือน
	
	def start(self):
		blynk.sync_virtual(6,7,8,16,17,18,23,24,25,28,29,38,39,40,41,42,43,44)
		self.lineNotify('สวัสดี LoRa Rice ระบบเริ่มทำงาน')
		self.reset_ptr_rx()
		self.set_mode(MODE.RXCONT)
		state = "ONE"  # กำหนด initial state เป็น "WAITING"
		while True:
			try:
				currentMillisLcd = int(round(time.time() * 1000))  # ดึงเวลาปัจจุบันในทุกครั้งในลูป
				if currentMillisLcd - self.previousMillisLcd >= 1000: #self.TimeDebugNode3*60*
					if self.countLcd == 2 or self.countLcd == 3 or self.countLcd == 4:
						self.countSleep = self.countSleep+1
					if self.countSleep >=5:
						self.countLcd = 1
						lcd.clear()    
						lcd.write_string('  >>> HOME <<<')
						self.countSleep = 0
					self.previousMillisLcd = currentMillisLcd
				self.setupMode()
				self.checkStatusNode()
				if state == "ONE":  #อ่านค่าเซ็นเซอร์
					#blynk.log_message("test_event")
					self.setupMode()
					print(state)
					state = "TWO" 
				elif state == "TWO": ##นำค่าที่ได้รับมาจากNode มาตรวจสอบ และอัพเดทข้อมูลไปblynk และยืนยันกลับไปที่ node
					self.setupMode()
					print(state)
					if self.stateRx == True:
						self.checkDataAndUpdate()
					#else:
					#	self.checkstateNode1 = 0
					state = "THREE"
				elif state == "THREE": 
				
					state = "FOUR"
				elif state == "FOUR":               
					self.setupMode()
					print(state)
					if self.checkDataNode == 1 or self.checkDataNode == 2 or self.checkDataNode == 3 and self.confirmReceive == True:
						self.send_data(self.checkDataNode)
						self.stateRx = False
						self.checkDataNode = 0
					state = "FIVE"
				elif state == "FIVE":
					self.setupMode()
					print(state)
					self.notifications()
					state = "ONE"
			except Exception as e:
				print("System Errer : ",e)
				continue
	def startt(self):
		while True:
			bme280_data = bme280.sample(bus,address)
			temp = bme280_data.temperature
			print("temp = "+temp)
			sleep(5)
			# กระบวนการที่ต้องทำในทุก iteration
# กำหนดค่าต่างๆ และเริ่มต้น LoRa
lora = LoRaGateway(verbose=True)
lora.set_mode(MODE.STDBY)
lora.set_pa_config(pa_select=1)
lora.set_freq(923.0)  # ต้องกำหนดค่าตามที่ใช้งาน

# เริ่มต้นโปรแกรม
lora.start()

# save by jack 
#print("destination_rx :" ,hex(self.destination_rx))
#print("data_length_rx :" ,self.data_length_rx),
#datasend = self.received_data
#blynk.virtual_write(3,str(datasend))
#current_data = "Time"+str(current_time)+" Data "+self.received_data 
#print(current_data)
#with open("logfile.txt", "a") as log_file:
#	log_file.write(current_data + "\n")
