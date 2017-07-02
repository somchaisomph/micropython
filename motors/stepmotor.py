from machine import Pin
import time
'''
reference : https://arduino-info.wikispaces.com/SmallSteppers
'''
class Model_28BYJ_48():
	CCW_8_STEP_SEQ = -1
	CCW_4_STEP_SEQ = -2
	CW_8_STEP_SEQ = 1
	CW_4_STEP_SEQ = 2
	PIN_MAP = {"D1":5,"D2":4,"D3":0,"D4":2,"D5":14,"D6":12,"D7":13,"D8":15,"SCL":5,"SDA":4,"SCK":14,"MISO":12,"MOSI":13,"SS":15}
	
	def __init__(self,pins=[]):
		self.pins = []
		for i in range(0,4):
			self.pins.append(Pin(self.PIN_MAP[pins[i]],Pin.OUT))

		self.seq = [[1,0,0,1],
				[1,0,0,0],
				[1,1,0,0],
				[0,1,0,0],
				[0,1,1,0],
				[0,0,1,0],
				[0,0,1,1],
				[0,0,0,1]]
		
		self.step_formular = {-1:(8,4076,5.625),
					-2:(4,2038,11.25),
					1:(8,4096,5.625),
					2:(4,2038,11.25)}
		
		self.step_count = len(self.seq)
		self.dir_err = "Invalid direction value"
		self.wt_err="waiting time must be an integer between 2 and 20.(Lower is faster)"
		 
	def step(self,rnd=1,direction=2,waiting_time=2):
		assert (direction in [-1,-2,1,2]),self.dir_err
		assert (2 <= waiting_time <= 20) ,self.wt_err
	
		info_touple = self.step_formular[direction]		
		max_rev = info_touple[1]*rnd
		self._step(max_rev,direction,waiting_time)
	

	def angular_step(self,angle=90,direction=2,waiting_time=2,bi_direction=False):
		assert (direction in [-1,-2,1,2]),self.dir_err
		assert (2 <= waiting_time <= 20) ,self.wt_err
		info_touple = self.step_formular[direction]	
		rnd,angle = self._div(angle,360)
		max_rev = info_touple[1]*rnd + angle * info_touple[1] // 360
		self._step(max_rev,direction,waiting_time)
		if bi_direction :
			self._step(max_rev,-direction,waiting_time)
			
	
	def _step(self,max_rev,direction,wait_time):
		rev = 0
		step_counter = 0
		while rev < max_rev: 
			for pin in range(0,4):
				step_val = self.seq[step_counter][pin]
				self.pins[pin].value(step_val)
 
			step_counter += direction
 
			# If we reach the end of the sequence
  			# start again
  			
			if (step_counter >= self.step_count):
				step_counter = 0
			if (step_counter < 0):
				step_counter = self.step_count + direction
 			
			# Wait before moving on
			time.sleep_ms(wait_time)
			rev += 1
	
	def _div(self,v1,v2):
		res=(0,0)
		if v2 >= v1 :
			return (0,v1)
		vt = v1 - v2
		m = 1
		while vt > v2 :
			vt = vt - v2
			m +=1
		return (m,vt)
		
if __name__ == "__main__":
	st_mot = Model_28BYJ_48(["D1","D2","D3","D4"])
	for i in range(4):
		st_mot.angular_step(angle=120,direction=-2,waiting_time=2)
		time.sleep(1) 
		st_mot.angular_step(angle=120,direction=2,waiting_time=2)
		time.sleep(1) 			
