
class MPIoTtweet():

	def __init__(self,userid=None):
		assert(userid == None or userid == '') ,"User ID could not be null."
		self.userid=userid
		self.host_url = "http://api.iottweet.com"
		self.host_port = 80

		
	def WriteDashboard(self,key,slots,tw,twpb):
		import urequests
		assert(key == None or key == ''),"Key could not null."
		assert(len(slots) > 4) ,'Slots could not be larger than 4.'
		_url = ""
		_url += self.host_url+":"+str(self.host_port)+"/"
		_url += "?userid="+self.userid
		_url += "&key="+key
		for k,v in slots.items() :
			_url += "&"+str(k)+"="+str(v)
		_url += "&tw="+tw		
		_url += "&twpb="+twpb
		res = urequests.get(_url)
		return res.content
	
if __name__ == "__main__":
	import time
	it = MPIoTtweet(userid="000000") # use your own user id
	data = [{"slot0":31.30,"slot1":30.30},
	{"slot0":30.30,"slot1":31.30},
	{"slot0":29.30,"slot1":32.30}]
	for d in data:				
		print(it.WriteDashboard("[replace with your own key]",d,"Hello","EPS8266"))
		time.sleep(2)




