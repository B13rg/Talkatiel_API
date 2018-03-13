import os
import socket
import requests

hostname = "127.0.0.1"
port = 5002



def runtests():
	print("TEST\t\tRESULT")
	print("---------------------------")
	result=test_pingServer()
	print("Ping\t\t{0}".format(result))
	result=test_https()
	print("SSL\t\t{0}".format(result))
	result=test_getTop()
	print("GET Top\t\t{0}".format(result))
	result=test_getNew()
	print("GET New\t\t{0}".format(result))
	result=test_getHot()
	print("GET Hot\t\t{0}".format(result))
	result=test_postPost()
	print("POST Posts\t{0}".format(result))
	result=test_postUser()
	print("POST User\t{0}".format(result))


def test_pingServer():
	sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = sock.connect_ex((hostname, port))
	if(not result):
		return "PASSED"
	return "FAILED"

def test_https():
	try:
		contents = requests.get("https://"+hostname+":"+str(port)+"/Posts/Top")
		statusCode=contents.status_code/100
		if(statusCode==2):
			return "PASSED"
	except:
		return "FAILED"
	return "FAILED"

def test_getTop():
	try:
		contents = requests.get("http://"+hostname+":"+str(port)+"/Posts/Top")
		statusCode=contents.status_code/100
		if(statusCode==2):
			return "PASSED"
	except:
		return "FAILED"
	return "FAILED"

def test_getNew():
	try:
		contents = requests.get("http://"+hostname+":"+str(port)+"/Posts/New")
		statusCode=contents.status_code/100
		if(statusCode==2):
			return "PASSED"
	except:
		return "FAILED"
	return "FAILED"

def test_getHot():
	try:
		contents = requests.get("http://"+hostname+":"+str(port)+"/Posts/Hot")
		statusCode=contents.status_code/100
		if(statusCode==2):
			return "PASSED"
	except:
		return "FAILED"
	return "FAILED"

def test_postPost():
	try:
		contents = requests.post("http://"+hostname+":"+str(port)+"/Posts", 
			data={"title": "343434","content": "sdfsdfsdfsdf", "userID": 9 } )
		statusCode=contents.status_code/100
		if(statusCode==2):
			return "PASSED"
	except:
		return "FAILED"
	return "FAILED"

def test_postUser():
	try:
		contents = requests.post("http://"+hostname+":"+str(port)+"/Users", 
			data={"userID": 343434,"phone": "5419796673", "deviceID": "qwasd asdasdasdasc 34523", "admin": 0 } )
		statusCode=contents.status_code/100
		if(statusCode==2):
			return "PASSED"
	except:
		return "FAILED"
	return "FAILED"





runtests()