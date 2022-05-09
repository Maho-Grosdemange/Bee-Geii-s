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

To wire the system you need to follow the document "cablage.png".
The you need to wire the sound sensor to the Channel 0 of the ADC and the potentiometers to the channels 1 and 2.

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
  */1 */1 */1 */1 */1 <program directory> && <Python interpreter directory> <program>
@reboot <program directory> && <Python interpreter directory> <startup program>
  
When a swarming occurs, the system send a SMS to the beekeeper.
You can also send a SMS to the system with the several commands :
  
    !lire_temperature               :   send the temperature
    
    !lire_humidite                  :   send back the humidity
    
    !lire_son                       :   send back sound value
    
    !lire_date ou !lire_heure       :   send back date and hour
    
    !lire_seuils                    :   send back of the thresholds
    
    !modif_seuils <seuilb> <seuilh> :   change the thresholds with the values in the SMS.
                                        This command execute the !bloquer_seuils command.
                                        
    !bloquer_seuils                 :   lock the thresholds.
                                        The program will no longer read the potentiometers values.
                                        
    !debloquer_seuils               :   unlock the thresholds.
                                        The program will read the potentiometers values.
                                        
    !lire_numeros                   :   send back the list of numbers to which the system should send a SMS when a swarming occurs (phonebook.txt).
    
    !ajouter_numero <numero>        :   add the number into the numbers list (phonebook.txt).
                                        Send back the number if it has been add or a message to say the number is already in the list.
                                
    !retirer_numero <numero>        :   remove the number into the numbers list (phonebook.txt).
                                        Send back the number if it has been remove or a message to say the number is not in the list.

    !lire_temps                     :   send back the monostable threshold value.

    !modif_temps <valeur>           :   change the monostable threshold value.
                                        Send back the modify value.
  

  
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

  To wire the system you need to follow the document "cablage.png".
The you need to wire the sound sensor to the Channel 0 of the ADC and the potentiometers to the channels 1 and 2.
  
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
  */1 */1 */1 */1 */1 <répertoire du programme> && <répertoire de l’interpréteur Python> <programme>
@reboot <répertoire du programme> && <répertoire de l’interpréteur Python> <programme>

Lorsqu'un essaimage a lieu, le système doit envoyer un SMS a l'apiculteur.
  Vous pouvez également envoyer un SMS au système avec les commandes suivantes :
  
    !lire_temperature               :   envoi de la temperature
    
    !lire_humidite                  :   envoi de l'humidite
    
    !lire_son                       :   envoi de la valeur du son
    
    !lire_date ou !lire_heure       :   envoi de la date et heure du module
    
    !lire_seuils                    :   envoi des seuils (seuilh et seuilb de l'hysteresis) du systeme
    
    !modif_seuils <seuilb> <seuilh> :   change les seuils avec les valeurs passees en parametre dans le sms (valeurs en %).
                                        Cette commande execute en meme temps !bloquer_seuils
                                        
    !bloquer_seuils                 :   bloque les seuils.
                                        Le programme n'ira plus lire la valeur des potentiometres mais lira les valeurs stockes dans le fichier param.txt
                                        
    !debloquer_seuils               :   debloque les seuils.
                                        Le programme ira lire la valeur des potentiometres
                                        
    !lire_numeros                   :   envoi de la liste des numeros auxquels envoyer un message en cas d'essaimage (liste contenue dans phonebook.txt)
    
    !ajouter_numero <numero>        :   ajoute le numero passe en parametre par sms a la liste des numeros contenue dans phonebook.txt.
                                        Envoi le numero si le numero a ete ajoute, Numero deja dans la liste si le numero est deja dans la liste
                                
    !retirer_numero <numero>        :   retire le numero passe en parametre par sms de la liste des numeros contenue dans phonebook.txt
                                        Envoi le numero si le numero a ete retire, Numero non present dans la liste si le numero n'etait pas dans la liste

    !lire_temps                     :   envoi de la valeur du seuil de temps du monostable

    !modif_temps <valeur>           :   change le seuil de temps du monostable.
                                        Envoi la valeur modifiee
  
