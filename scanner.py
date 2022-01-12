from os import popen
from os import system


def ipBox():
	message=popen("nslookup img").read()
	line=message.splitlines()[1]
	start=0
	for i in line:
		if i.isdigit():
			start=line.find(i)
			break;
	return line[start:]

def findIpInLocalPing(ping):
	line=ping.splitlines()[1]
	start=0
	for i in line:
		if i.isdigit():
			start=line.find(i)
			break;
	end=start+1
	for index in range(start,len(line)):
		i=line[index]
		if not(i.isdigit() or i=="."):
			end=index+1
			break;


	return line[start:end]
def lastPoint(string):
	while string.endswith("."):
		string=string[:-1]
	return len(string)-1


def scanIp(plage, printOn=False, time=100, cls=True, printNotConnected=False):
	ping=[]
	result=[]
	baseIp=ipBox()
	baseIp=baseIp[:lastPoint(baseIp)]
	if printOn:
		if cls:
			system("cls")
		print("Scan lancé...")
		for i in range(plage+1):
			ping.append(popen("ping -w "+str(time)+" "+baseIp+str(i)).read())
			if "perte 100%" not in ping[i]:
				result.append(findIpInLocalPing(ping[i]))
				print(result[len(result)-1]+" Connected")
			elif printNotConnected:
				print(findIpInLocalPing(ping[i])+" Not Connected")
	else:
		for i in range(plage+1):
			ping.append(popen("ping -w "+ str(time)+" "+baseIp+str(i)).read())
			if "perte 100%" not in ping[i]:
				result.append(findIpInLocalPing(ping[i]))
	return result

if __name__=="__main__":
	try:
		while(True):
			try:
				plage=int(input("Combien d'entré ?\n"))
			except ValueError:
				print("Saisissez un nombre.")
				continue
			break
		scanIp(plage,printOn=True)
	finally:
		system("pause")


