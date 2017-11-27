import requests

class wemo_binary:
	URL = "http://10.22.22.1:49152/upnp/control/basicevent1"
    # get xml
	HEADER_GET = {'SOAPACTION':'"urn:Belkin:service:basicevent:1#GetBinaryState"','Content-Type':'text/xml: charset="utf-8"','Accept':''}
	BODY_GET = '<?xml version="1.0" encoding="utf-8"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:GetBinaryState xmlns:u="urn:Belkin:service:basicevent:1"></u:GetBinaryState></s:Body></s:Envelope>'
    # SET xml
	HEADER_SET = {'SOAPACTION':'"urn:Belkin:service:basicevent:1#SetBinaryState"','Content-Type':'text/xml: charset="utf-8"','Accept':''}
	BODY_SET1 = '<?xml version="1.0" encoding="utf-8"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:SetBinaryState xmlns:u="urn:Belkin:service:basicevent:1"><BinaryState>'
	BODY_SET2 = '</BinaryState></u:SetBinaryState></s:Body></s:Envelope>'
    # get
	def getState(self):
		response = requests.post(self.URL, data=self.BODY_GET, headers=self.HEADER_GET)
		content = response.content
		index = content.index("<BinaryState>")+13
		state = content[index:index+1]
		return state
    # set
	def setState(self, s):
		response = requests.post(self.URL, data=(self.BODY_SET1+str(1 if s else 0) + self.BODY_SET2), headers=self.HEADER_SET)
		content = response.content
		index = content.index("<BinaryState>")+13
		state = content[index:index+1]
		return state
    # print
	def __repr__(self):
		return "Switch: " + ("ON" if self.getState() == "1" else "OFF")
