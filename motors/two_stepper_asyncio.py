from machine import Pin
import time
import uasyncio as asyncio

CCW_8_STEP_SEQ = -1
CCW_4_STEP_SEQ = -2
CW_8_STEP_SEQ = 1
CW_4_STEP_SEQ = 2
PIN_MAP = {"D1":5,"D2":4,"D3":0,"D4":2,"D5":14,"D6":12,"D7":13,"D8":15,"SCL":5,"SDA":4,"SCK":14,"MISO":12,"MOSI":13,"SS":15}


SEQ = [[1,0,0,1],
		[1,0,0,0],
		[1,1,0,0],
		[0,1,0,0],
		[0,1,1,0],
		[0,0,1,0],
		[0,0,1,1],
		[0,0,0,1]]
		
STEP_FORMULAR = {-1:(8,4076,5.625),
			-2:(4,2038,11.25),
			1:(8,4096,5.625),
			2:(4,2038,11.25)}
		
STEP_COUNT = len(SEQ)
#		self.dir_err = "Invalid direction value"
#		self.wt_err="waiting time must be an integer between 2 and 20.(Lower is faster)"
		 
async def step(rnd=1,direction=2,waiting_time=2):
	info_touple = STEP_FORMULAR[direction]		
	max_rev = info_touple[1]*rnd
	await _step(max_rev,direction,waiting_time)
	
async def _div(v1,v2):
	res=(0,0)
	if v2 >= v1 :
		return (0,v1)
	vt = v1 - v2
	m = 1
	while vt > v2 :
		vt = vt - v2
		m +=1
	return (m,vt)
	
async def angular_step(angle=90,direction=2,waiting_time=2,bi_direction=False,pins=[]):
	info_touple = STEP_FORMULAR[direction]	
	rnd,angle = await _div(angle,360)
	max_rev = info_touple[1]*rnd + angle * info_touple[1] // 360
	rev = 0
	step_counter = 0
	if bi_direction :
		direction = -1 * direction
	while rev < max_rev: 
		for pin in range(0,4):
			step_val = SEQ[step_counter][pin]
			pins[pin].value(step_val)
		step_counter += direction
		if (step_counter >= STEP_COUNT):
			step_counter = 0
		if (step_counter < 0):
			step_counter = STEP_COUNT + direction	
		await asyncio.sleep_ms(waiting_time)
		rev += 1				

async def step_a():
	pins = []
	st_a = ["D1","D2","D3","D4"]
	for i in range(0,4):
		pins.append(Pin(PIN_MAP[st_a[i]],Pin.OUT))
	await angular_step(angle=360,direction=2,waiting_time=2,pins=pins)
	asyncio.sleep_ms(1000)
	await angular_step(angle=360,direction=-2,waiting_time=2,pins=pins) 					

async def step_b():		
	pins = []
	st_b = ["D5","D6","D7","D8"]
	for i in range(0,4):
		pins.append(Pin(PIN_MAP[st_b[i]],Pin.OUT))
	await angular_step(angle=360,direction=-2,waiting_time=2,pins=pins)
	asyncio.sleep_ms(1000) 
	await angular_step(angle=360,direction=2,waiting_time=2,pins=pins)					


async def main(delay):
	await asyncio.sleep(delay)
				
loop = asyncio.get_event_loop()
loop.create_task(step_a())	
loop.create_task(step_b())
loop.run_until_complete(main(30))
#loop.run_forever()
loop.close()		 				 			
