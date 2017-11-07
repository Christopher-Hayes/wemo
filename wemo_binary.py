import requests

class wemo_binary:
	url="http://10.22.22.1:49152/upnp/control/basicevent1"

	headerGet = {'SOAPACTION':'"urn:Belkin:service:basicevent:1#GetBinaryState"','Content-Type':'text/xml: charset="utf-8"','Accept':''}
	bodyGet = '<?xml version="1.0" encoding="utf-8"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:GetBinaryState xmlns:u="urn:Belkin:service:basicevent:1"></u:GetBinaryState></s:Body></s:Envelope>'

	headerSet = {'SOAPACTION':'"urn:Belkin:service:basicevent:1#SetBinaryState"','Content-Type':'text/xml: charset="utf-8"','Accept':''}
	bodySet1 = '<?xml version="1.0" encoding="utf-8"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:SetBinaryState xmlns:u="urn:Belkin:service:basicevent:1"><BinaryState>'
	bodySet2 = '</BinaryState></u:SetBinaryState></s:Body></s:Envelope>'

	def getState(self):
		response = requests.post(self.url, data=self.bodyGet, headers=self.headerGet)
		content = response.content
		index = content.index("<BinaryState>")+13
		state = content[index:index+1]
		return state

	def setState(self, s):

		response = requests.post(self.url, data=(self.bodySet1+str(1 if s else 0) + self.bodySet2), headers=self.headerSet)
		content = response.content
		index = content.index("<BinaryState>")+13
		state = content[index:index+1]
		return state

	def __repr__(self):
		return "Switch: " + ("ON" if self.getState() == "1" else "OFF")
