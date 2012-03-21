import socket
import os


def fcfs(bu):
	wtime=0
	for key,(sno,size) in sorted(bu.iteritems(),key=lambda x:x[1][0]):
		print "waiting time for process",key,"is:",wtime
		wtime+=size

def sjf(bu):
	wtime=0
	for key,(sno,size) in sorted(bu.iteritems(),key=lambda x:x[1][1]):
		print "waiting time for process",key,"is:",wtime
		wtime+=size

def bjf(bu):
	wtime=0
	priority=0
	i=0
	for key,(sno,size) in sorted(bu.iteritems(), key=lambda x: x[1][1]):
		priority=sno+i
		bu[key]=sno,size,priority
		i+=1
	for key,(sno,size,priority) in sorted(bu.iteritems(), key=lambda x: x[1][2]):
		print "waiting time to process",key,"is:",wtime
		wtime+=size


def roundrobin(bu):
	wt=[0 for i in range(len(bu))]
	tat=[]
	count=[0 for i in range(len(bu))]
	maxsize=0
	for sno,size in bu.itervalues():
		print "Burst time for process p",sno,"=",size,"*10^-9"
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
	for row in Rrobin:
		print row
	for j in range (0,len(bu)):
		for i in range(0,count[j]-1):
			for k in range (0,len(bu)):
				if k!=j:
					wt[j]+=Rrobin[k][i]
		for k in range (0,j):
			wt[j]+=Rrobin[k][count[j]-1]
	for i in range (0,len(bu)):
		print "Waiting Time for process P",i+1,"=",wt[i]
	twt=0.0
	sum1=0.0
	for i in range(0,len(bu)):
		twt=twt+wt[i]
		#tat.append(b[i]+wt[i])
		#sum1+=tat[i]
	awt=twt/n
	sum1=sum1/n
	print "Total Waiting Time=",twt
	print "Average Waiting Time=",awt
	#print "Average turnaround time=",sum1

if __name__ == "__main__":
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind(("", 5000))
	server_socket.listen(5)

	print "TCPServer Waiting for client on port 5000"

	bu={}
	n=3
	while 1:
		client_socket, address = server_socket.accept()
		print "I got a connection from ", address
		for i in range(0,3):
		        data = client_socket.recv(512)
		        if ( data == 'q' or data == 'Q'):
				client_socket.close()
				break;
			else:
				size=os.path.getsize(data)
				bu[data]=i,size
				print bu
		break
	print "ROUND ROBIN SCHEDULING"
	fcfs(bu)
	sjf(bu)
	roundrobin(bu)
	bjf(bu)
