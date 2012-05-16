import socket
import os
import time
import re
import numpy as np
import matplotlib.pyplot as plt

#graph plot function

def plot(param):
    data = [ ("FCFS", param[0]), ("SJF", param[1]),
            ("R.Robin", param[2]), ( "BJF", param[3])]
    N = len( data )
    x = np.arange(1, N+1)
    y = [ num for (s, num) in data ]
    labels = [ s for (s, num) in data ]
    width = 1
    bar1 = plt.bar( x, y, width, color="y" )
    plt.ylabel( 'Throughput/Average Waiting Time' )
    plt.xticks(x + width/2.0, labels )
    plt.show()

#timestamp functions

def timestampit(func):
	def decorate(*args,**kwargs):
		decorate.timestamp=time.time()
		return func(*args,**kwargs)
	return decorate
@timestampit

def test():
	'''timestamp'''

#First Come First Serve Function

def fcfs(bu):
	twt=0.0
	wtime=0
	avgwt=0.0
	for key,(sno,size) in sorted(bu.iteritems(),key=lambda x:x[1][0]):
		print "waiting time for process",key,"is:",wtime
		wtime+=size
		twt=twt+wtime
	avgwt=twt/5
	print "Average Waiting Time for FCFS is", avgwt
	test()
	return test.timestamp, avgwt

#Shortest Job Function

def sjf(bu):
	wtime=0
	twt=0.0
	avgwt=0.0
	for key,(sno,size) in sorted(bu.iteritems(),key=lambda x:x[1][1]):
		print "waiting time for process",key,"is:",wtime
		wtime+=size
		twt=twt+wtime
	avgwt=twt/5
	print "Average Waiting Time for SJF is", avgwt
	test()
	return test.timestamp,avgwt

#Best Job First Function

def bjf(bu):
	wtime=0
	twt=0.0
	priority=0
	avgwt=0.0
	i=0
	for key,(sno,size) in sorted(bu.iteritems(), key=lambda x: x[1][1]):
		priority=sno+i
		bu[key]=sno,size,priority
		i+=1
	global client_sockets
	test()
	for key,(sno,size,priority) in sorted(bu.iteritems(), key=lambda x: x[1][2]):
		print "waiting time to process",key,"is:",wtime
		wtime+=size
		twt=twt+wtime
		fp=open(key,'r')
		content=fp.read()
		client_sockets[sno].send(content)
	avgwt=twt/5
	print "Average Waiting Time for Best Job First is", avgwt
	return test.timestamp,avgwt

#Round Robin Function

def roundrobin(bu):
	wt=[0 for i in range(len(bu))]
	twt=0.0
	count=[0 for i in range(len(bu))]
	maxsize=0
	for sno,size in bu.itervalues():
		if maxsize<size:
			maxsize=size
	tq=10
	m=maxsize/tq+1
	Rrobin=[[0 for col in range(m)]for row in range(len(bu))]
	for sno,size in bu.itervalues():
		j=0;
		while size>0:
			if size>=tq:
				size-=tq
				Rrobin[sno][j]=tq
			else:
				Rrobin[sno][j]=size
				size=0
			j+=1
		count[sno]=j
	for j in range (0,len(bu)):
		for i in range(0,count[j]-1):
			for k in range (0,len(bu)):
				if k!=j:
					wt[j]+=Rrobin[k][i]
		for k in range (0,j):
			wt[j]+=Rrobin[k][count[j]-1]
	twt=0.0
	avgwt=0.0
	for i in range(0,len(bu)):
		twt=twt+wt[i]
	avgwt=twt/5
	print "Average Waiting Time for Round Robin is ",avgwt
	test()
	return test.timestamp, avgwt

#Main block

if __name__ == "__main__":
	#creating server socket
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind(("", 5000))
	server_socket.listen(5)
	print "TCPServer Waiting for client on port 5000"

	bu={}
	client_sockets={}
	throughput={}
	param={}
	arrival={}
	response={}
	awt={}

	#accepting 5 requests from various clients

	for i in range(0,5):
		client_socket, address = server_socket.accept()
		client_sockets[i]=client_socket
		print "I got a connection from ", address
                data = client_socket.recv(512)
		search = re.search('^GET [\w/.0-9-_]+', data)
		filename = search.group(0)[5:]
		size=os.path.getsize(filename)
		bu[filename]=i,size
	print "input data set is", bu

	#First Come First Serve

	print "First Come First Serve"
	test()
	arrival[0]= test.timestamp
	response[0], awt[0] = fcfs(bu)

	#Shortest Job First	
	
	print "Shortest Job First"	
	test()
	arrival[1]= test.timestamp
	response[1],awt[1]=sjf(bu)
	
	#Round Robin
 
	print "Round Robin"
	test()
	arrival[2]= test.timestamp
	response[2],awt[2]=roundrobin(bu)

	#Best Job First

	print "Best Job First"
	test()
	arrival[3]= test.timestamp
	response[3],awt[3]=bjf(bu)
	
	for i in range(0,4):
		throughput[i]= 5/(response[i]-arrival[i])
		param[i]=throughput[i]/awt[i]
	plot(param)
