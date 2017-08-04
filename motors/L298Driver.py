from machine import Pin, PWM
import utime as time

class PinMap():
	WMOS_D1_MINI = {"D1":5,"D2":4,"D3":0,"D4":2,"D5":14,"D6":12,"D7":13,"D8":15,"SCL":5,"SDA":4,"SCK":14,"MISO":12,"MOSI":13,"SS":15}
	

class L298Driver():
	def __init__(self,ena,enb,in1,in2,in3,in4):
		self.ENA = Pin(ena,Pin.OUT)
		self.ENB = Pin(enb,Pin.OUT)		
		self.A1 = PWM(Pin(in1,Pin.OUT))
		self.A2 = PWM(Pin(in2,Pin.OUT))		
		self.B1 = PWM(Pin(in3,Pin.OUT))
		self.B2 = PWM(Pin(in4,Pin.OUT))				

	def motor_a_on(self):
		self.ENA.on()
		
	def motor_b_on(self):
		self.ENB.on()
	
	def motor_a_off(self):
		self.ENA.off()
	
	def motor_b_off(self):
		self.ENB.off()

	def enable(self):
		self.motor_a_on()
		self.motor_b_on()
		
	def disable(self):
		self.motor_a_off()
		self.motor_b_off()
		
	
	def motor_a_forward(self,speed=200):
		#self.A1.on()
		self.A1.duty(speed)
		self.A2.duty(0)
			
	def motor_b_forward(self,speed=200):
		self.B1.duty(speed)
		self.B2.duty(0)

	def motor_a_backward(self,speed=200):
		self.A1.duty(0)
		self.A2.duty(speed)
			
	def motor_b_backward(self,speed=200):
		self.B1.duty(0)
		self.B2.duty(speed)

	def motor_a_stop(self):
		self.A1.duty(0)
		self.A2.duty(0)
			
	def motor_b_stop(self):
		self.B1.duty(0)
		self.B2.duty(0)

	def forward(self,duration,speed):
		self.motor_a_forward(speed)
		self.motor_b_forward(speed)
		time.sleep(duration)
		self.stop()		

	
	def backward(self,duration,speed):
		self.motor_a_backward(speed)
		self.motor_b_backward(speed)
		time.sleep(duration)
		self.stop()		
		
	def turn_left(self,duration,speed):
		self.motor_a_backward(speed)
		self.motor_b_forward(speed)
		time.sleep(duration)
		self.stop()		
		
		
	def turn_right(self,duration,speed):
		self.motor_a_forward(speed)
		self.motor_b_backward(speed)
		time.sleep(duration)
		self.stop()		


		
	def stop(self):
		self.motor_a_stop()
		self.motor_b_stop()

if __name__ == "__main__":
	l298 = L298Driver(ena = PinMap.WMOS_D1_MINI["D3"],enb=PinMap.WMOS_D1_MINI["D5"],in1=PinMap.WMOS_D1_MINI["D4"],in2=PinMap.WMOS_D1_MINI["D8"],in3=PinMap.WMOS_D1_MINI["D7"],in4=PinMap.WMOS_D1_MINI["D6"])
	l298.enable()
	l298.forward(5)
	l298.backward(5)
	l298.turn_left(5)
	l298.turn_right(5)
	l298.disable()
