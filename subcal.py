#Ruben C. Vasquez
# macOS:desktop rubenvasquez$ python subcal.py 55.0.95.254/19
#function below is getting the ip address and splitting it into different sections


import sys
#we will be getting the ip from the console. 
#Couldn't figure out how to get it from the insert function
(ipAddress, cidrString) = sys.argv[1].split('/')
address = ipAddress.split('.')
c = int(cidrString)


#I'm separating the address so it will be easier to identify their class
ipFormat = [int(address[0]),int(address[1]),int(address[2]), int(address[3])]
firstSection = ipFormat[0]
secondSection = ipFormat[1]
thirdSection = ipFormat[2]
fourthSection = ipFormat[3]


#the function below is getting the subnet mask
subNetMask = [0, 0, 0, 0]
for i in range(c):
	subNetMask[i/8] = subNetMask[i/8] + (1 << (7 - i % 8))
	
	
#assigning a temp variable
temp = []


#creating a for loop to add to the temp variable
for i in range(4): temp.append(int(address[i]) & subNetMask[i])
free = list(temp)
cal = 32 - c
#creating another for loop
for i in range(cal): free[3 - i/8] = free[3 - i/8] + (1 << (i % 8))


#after, we will be getting the host
ipHost = {"first":list(temp), "last":list(free)}
ipHost["first"][3] += 4 
ipHost["last"][3] -= 1
ipHost["count"] = 0


#lastly, creating one more for loop to find the address range, might be off by a few numbers,
#there is a bug somewhere
for i in range(4):
    ipHost["count"] += (ipHost["last"][i] - ipHost["first"][i]) * 2**(8*(3-i))
    
    
#finds the classful networks
if firstSection < 127 and firstSection > 1:
	print "Classful Network Address:",ipFormat[0],".0.0.0"
	print "Classful Broadcast Address:",ipFormat[0],".255.255.255" 
	#decided it will be easier to group together the classful stuff together
elif firstSection > 128 and firstSection < 191:
	print "Classful Network Address:",ipFormat[0],".",ipFormat[1],".","0.0"
	print "Classful Broadcast Address:",ipFormat[0],".",ipFormat[1],".","255.255"
elif firstSection > 192 and firstSection < 223:
	print "Classful Network Address:",ipFormat[0], ".",ipFormat[1],".",ipFormat[2],".","0"
	print "Classful Broadcast Address:",ipFormat[0], ".",ipFormat[1],".",ipFormat[2],".","255"
elif firstSection > 224:
	print "Classful Network Address:",ipFormat[0], ".",ipFormat[1],".",ipFormat[2],".", ipFormat[3]
	print "Classful Broadcast Address:",ipFormat[0], ".",ipFormat[1],".",ipFormat[2],".", ipFormat[3]
	
	
#now we just print everything
print "Address:", ipAddress
print "Subnet mask:", ".".join(map(str, subNetMask))
print "Subnet:", ".".join(map(str, temp))
print "Subnet Broadcast:", ".".join(map(str, free))
print "Host Range within subnet: ", ".".join(map(str, ipHost["first"])),"-",".".join(map(str, ipHost["last"]))
print "Host Count: ", ipHost["count"]


#lastly, we're going to give our class letter
if firstSection < 127:
  print ("class A")
elif firstSection < 191 and firstSection > 128:
	print ("class B")
elif firstSection > 192 and firstSection < 223:
	print ("class C") 
elif firstSection  > 224:
	print ("class D")
