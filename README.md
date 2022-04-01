# Bee-Geii-s
ENG : Program of our directed study "swarming detector".
FRA : Programme de notre projet tutoré "détecteur d'essaimage".

ENG : This README will first be in English and then translated into French.
FRA : Ce README sera d'abord en anglais puis traduit en français.

########## ENGLISH ##########

--- Description of the project ---

This project is a swarming detector.
A swarming is a natural phenomenom when bees leave their hive to create another one. 
This enable a bee colony to reproduce.

This directed study has been carry out by 3 students of University of Lorraine, France (Université de Lorraine, IUT de Saint-Dié).
This is a second year technical degree in Industrial IT and Electrical Engineering (DUT GEII) project.

The aim of the project is to send a sms to the beekeeper when a swarming occurs.

To carry out this project we use several components, here is a list :
  - Raspberry Pi Zero W
  - ADC (we use a MCP3008)
  - 2 potentiometers (100k)
  - Sound sensor (we use MAX4466)
  - Thermo-Hygrometer (we use HTU21)
  - Waveshare GSM/GPRS/GNSS/Bluetooth HAT for Raspberry Pi
  - Some wires
(The wiring will soon be publish)

We use a Raspberry Pi Zero W because it has less power consumption than the others Raspberry.
However the Pi Zero does not have analog inputs with an integreted ADC that is why we have the MCP3008.
The MCP3008 is used to convert analog signals coming from both the potentiometers and the sound sensor.
The two potentiometers are used to set the thresholds of the hysteresis. One of them set the low threshold the other one is the bandwidth. 

To enhance the project, we can add a force sensor underneath the hive. We can also change the way our program is call, this way we can, for instance, shutdown the system and boot up every 5 minutes. By making this, we will expand tremendously our system battery life.

--- How to install and run the project ---

•	Install Raspbian on the Raspberry and do the startup config
•	SSH activation : sudo raspi-config -> Interface Options -> SSH -> <Yes> -> <Ok>
•	SPI activation : sudo raspi-config -> Interface Options -> SPI -> <Yes> -> <Ok>
•	I2C activation : sudo raspi-config -> Interface Options -> I2C -> <Yes> -> <Ok>
•	Serial Port activation : sudo raspi-config -> Interface Options -> Serial Port -> <Yes> -> <Ok>
•	MCP3008 library download : sudo pip install adafruit-mcp3008
•	I2C library download : 
-	pip install smbus-cffi
-	pip install git+https://github.com/bivab/smbus-cffi.git
-	git clone https://github.com/bivab/smbus-cffi.git
-	python setup.py install
•	PySerial library download : pip install pyserial
•	CRON settings : crontab -e
* * * * * <program directory> && <Python interpreter directory> <program>
@reboot <program directory> && <Python interpreter directory> <startup program>
  
  
  

  
########## FRENCH ##########

--- Description du projet ---

Ce projet est un détecteur d'essaimage
Un essaimage est un phénomène naturel durant lequel des abeilles quittent leur ruche pour aller en fonder une autre. 
Cela permet à la colonie de se reproduire.

Ce projet tutoré a été réalisé par trois étudiants de l'Université de Lorraine (IUT de Saint-Dié).
Il s'agit d'un projet de deuxième année de DUT Génie Electrique et Informatique Industrielle.

Le but du projet est d'envoyer un SMS à l'apiculteur lorsqu'un essaimage se produit.

Pour mener à bien ce projet, nous avons utilisés différents composants, en voici la liste :
  - Raspberry Pi Zero W
  - CAN (MCP3008)
  - 2 potentiomètres (100k)
  - Capteur de son (MAX4466)
  - Capteur de température et d'hygrométrie (HTU21)
  - Waveshare GSM/GPRS/GNSS/Bluetooth HAT pour Raspberry Pi
  - Des fils
(Le câblage sera publié prochainement)

Nous utilisons un Raspberry Pi Zero W parce que sa consommation électrique est moindre par rapport aux autres Rapsberry.
Cependant, la Pi Zero n'a pas d'entrée analogique avec un CAN intégré, c'est pourquoi nous utilisons un MCP3008.
Le MCP3008 est utilisé pour convertir les signaux analogiques venants des potentiomètres et du capteur de son.
Les deux potentiomètres sont utilisés pour régler les seuils de l'hystérésis. L'un des potentiomètre régle le seuil bas, le second régle la largeur de bande.

Pour améliorer le projet, nous pouvons ajouter un capteur de force en dessous de la ruche. Nous pouvons également changer la façon dont notre programme est appelé, de cette façon nous pourrions, par example, éteindre le système et le relancer toutes les 5 minutes. En faisant cela, nous réduirons de manière très importante l'autonomie de notre système.

--- How to install and run the project ---

•	Installation de Raspbian sur la carte et faire la configuration de démarrage
•	Activation du SSH : sudo raspi-config -> Interface Options -> SSH -> <Oui> -> <Ok>
•	Activation du SPI : sudo raspi-config -> Interface Options -> SPI -> <Oui> -> <Ok>
•	Activation de l’I2C : sudo raspi-config -> Interface Options -> I2C -> <Oui> -> <Ok>
•	Activation du Serial Port : sudo raspi-config -> Interface Options -> Serial Port -> <Oui> -> <Ok>
•	Téléchargement de la bibliothèque MCP3008 : sudo pip install adafruit-mcp3008
•	Téléchargement de la bibliothèque I2C : 
-	pip install smbus-cffi
-	pip install git+https://github.com/bivab/smbus-cffi.git
-	git clone https://github.com/bivab/smbus-cffi.git
-	python setup.py install
•	Téléchargement de la bibliothèque Serial : pip install pyserial
•	Réglage du CRON : crontab -e
* * * * * <répertoire du programme> && <répertoire de l’interpréteur Python> <programme>
@reboot <répertoire du programme> && <répertoire de l’interpréteur Python> <programme>

