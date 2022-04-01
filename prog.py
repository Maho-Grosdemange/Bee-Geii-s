# version 5.0
# mise a jour : 01/04/2022

# Ce programmme a pour but d'etre appele par le service CRON toutes les cinq minutes
# Il integre la recuperation des valeurs de son, temperature et humidite
# Lorsqu'un essaimage est detecte, le systeme envoie un SMS
# Reglage du seuil bas et de la largeur de bande du seuil a hysteresis



# Bibliotheques globales
import time
import os

# Bibliotheque capteur son (MAX4466)
from spidev import SpiDev

# Bibliotheques capteur de temperature et d'hygrometrie
import board
import busio
from adafruit_htu21d import HTU21D

# Bibliotheques GSM Hat
import serial



class SMS:
    """La classe SMS crée des instances SMS avec les arguments suivants :
            - numero : numero de telephone vers lequel est envoye / duquel a ete envoye le sms
            - message : contenu du sms
            - date : date de creation ou de reception du sms
            - heure : heure de creation ou de reception du sms
            - mode : recu ou envoye (r ou s)
        Une instance de la classe sms possede les methodes suivantes :
        __init__ : constructeur pour un sms a envoyer
        received : constructeur pour un sms recu
        send : envoye le sms"""
    
    def __init__(self, numero, message, date = time.strftime("%Y", time.localtime())[2:] + time.strftime("/%m/%d", time.localtime()), heure = time.strftime("%H:%M:%S", time.localtime()), mode = "s"):
        self.date = date
        self.heure = heure
        self.numero = numero
        self.message = message
        self.mode = mode
        


    @classmethod
    def received(cls, sms):
        numero = sms[sms.find("REC UNREAD")+13 : sms.find("REC UNREAD")+25]
        message = sms[sms.find("REC UNREAD")+52 :].rstrip().rstrip("\n")
        date = sms[sms.find("REC UNREAD")+31 : sms.find("REC UNREAD")+39]
        heure = sms[sms.find("REC UNREAD")+40 : sms.find("REC UNREAD")+48]

        if (len(numero) == 12) and (len(message) >= 1) and (len(date) == 8) and (len(heure) == 8):
            return cls(numero, message, date, heure, "r")
    


    def send(self):
        print("message : {}\nnumber : {}".format(self.message, self.numero))
        write_at("+CMGF=1")
        get_at_response()
        write_at("+CMGS=\"{}\"".format(self.numero))
        get_at_response()
        msg = self.message + "\x1A"
        s.write(msg.encode())
        time.sleep(6)

        
# Copyright (c) 2016 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

class MCP3008:
    """La classe MCP3008 sert a recuperer les informations du CAN.
    Un objet de type MCP3008 possede 3 methodes : open, read et close."""

    def __init__(self, bus = 0, device = 0):
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()
        self.spi.max_speed_hz = 1000000
        
    def open(self):
        """Sert a activer la communication SPI a une frequence maximale de 1MHz."""
        
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = 1000000
        
    def read(self, channel = 0):
        """Sert a recuperer les donnees envoyees par la liaison SPI.
        Prend en parametre la voie du MCP3008 qui doit etre lue par la fonction."""
        
        adc = self.spi.xfer([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data
    
    def close(self):
        """Sert a clore la communication SPI."""
        
        self.spi.close()



def current_milli_time():
    """Fonction retournant le temps en ms ecoule depuis epoch (1er Janvier 1970)"""
    
    return round(time.time() * 1000)



def read_MAX4466(adc, channel, sample_window, start_millis):
    """Fonction retournant la valeur crete a crete du signal lu par le MAX4466.
    Le capteur pouvant amplifier un signal entre 20Hz et 20kHz, on lis les valeurs pendant 50ms (periode max theorique du signal).
    On recupere ensuite le max et le min du signal pour retourner la valeur crete a crete.
    Durant le temps de recuperation des donnees, environ 125 valeurs sont recuperes.
    adc = objet de type MCP3008 (voir class MCP3008)
    channel = canal du CAN (adc) que l'on souhaite lire
    sample_window = temps durant lequel on veux recuperer les valeurs
    start_millis = temps en ms ecoule depuis le 1er Janvier 1970"""

    signalMax = 0
    signalMin = 1024
    sample_list = []

    while (current_milli_time() - start_millis < sample_window):
        sample_list.append(adc.read(channel = 0))   #on recupere le plus de donnees possible pendant 50ms

    for sample in sample_list:  #on cherche le min et le max
        if (sample < 1024):
            if (sample > signalMax):
                signalMax = sample        
            elif (sample < signalMin):
                signalMin = sample
    return signalMax - signalMin #on retourne la valeur crete a crete



def get_at_response(sleep = 0.5):
    """Retourne la reponse du modem (lecture de la liaison serie) avec au prealable un temps de pause passe en parametre (0.5s par defaut)"""
    
    #give modem enough time to reply
    time.sleep(sleep)
    r = s.read_all()
    if not r:
        return ""
    r = r.decode()
    return r



def write_at(cmd):
    """Sert a ecrire sur la liaison serie le message passe en parametre"""
    
    cmd = b"AT" + cmd.encode("UTF-8") + b"\r\n"
    s.write(cmd)



def get_new_sms(sleep = 0.5):
    """Sert a demander les nouveaux sms recus"""
    
    #s.write(b"ATE0\r\n")
    write_at("+CMGF=1")
    time.sleep(0.1)
    write_at("+CMGL=\"REC UNREAD\"")
    #s.write(b"ATE1\r\n")
    return get_at_response()



def command(sms, seuilb, seuilh, SEUILS_BLOQUES, phonebook, temps_mono):
    """Sert a la gestion des commandes envoyees par sms. La reponse a une commande se fait par sms a celui qui l'a envoyee.
    12 commandes sont possibles :
    
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
                                        Envoi la valeur modifiee"""


    if "!lire_temperature" == sms.message:
        print("temp")
        message = "Temperature dans la ruche : {:.2f}C".format(temperature_value)
        
    elif "!lire_humidite" == sms.message:
        print("humid")
        message = "Taux d'humidite dans la ruche : {:.2f}%".format(humidite_value)

    elif "!lire_son" == sms.message:
        print("son")
        message = "Valeur du son a l'exterieur de la ruche : {:.2f}%".format(sound_value/10.23)

    elif "!lire_date" == sms.message or "!lire_heure" == sms.message:
        print("date") 
        message = "Date et heure du systeme : {} {}".format(sms.date, sms.heure)

    elif "!lire_seuils" == sms.message:
        print("lire seuils")
        message = "Seuil bas {:.2f}%\nSeuil haut {:.2f}%".format(seuilb/10.23, seuilh/10.23)

    elif "!modif_seuils" == sms.message.split()[0]:
        print("modif seuils")
        
        if float(sms.message.split()[1])*10.23 < float(sms.message.split()[2])*10.23:
            seuilb = float(sms.message.split()[1])*10.23
            seuilh = float(sms.message.split()[2])*10.23
            SEUILS_BLOQUES = True
            message = "Les seuils ont ete changes :\nSeuil bas {:.2f}%\nSeuil haut {:.2f}%".format(seuilb/10.23, seuilh/10.23)
        else:
            message = "Le seuil bas doit etre inferieur au seuil haut"

    elif "!bloquer_seuils" == sms.message:
        print("bloquer seuils")
        SEUILS_BLOQUES = True
        message = "Seuils bloques"

    elif "!debloquer_seuils" == sms.message:
        print("debloquer_seuils")
        SEUILS_BLOQUES = False
        message = "Seuils debloques"
        
    elif "!lire_numeros" == sms.message:
        print("lire numeros")
        message = "Liste de numeros ({}) :\n".format(len(phonebook))
        for numero in phonebook:
            message += "\n{}".format(numero)

    elif "!ajouter_numero" == sms.message.split()[0]:
        print("ajouter numero")
        IS_IN_LIST = False
        for numero in phonebook:
            if sms.message.split()[1] == numero:
                IS_IN_LIST = True
                
        if not IS_IN_LIST:
            phonebook.append(sms.message.split()[1])
            message = "Le numero {} a ete ajoute a la liste".format(sms.message.split()[1])
        else:
            message = "Le numero {} est deja dans la liste".format(sms.message.split()[1])

    elif "!retirer_numero" == sms.message.split()[0]:
        print("retirer numero")
        IS_IN_LIST = False
        for numero in phonebook:
            if sms.message.split()[1] == numero:
                IS_IN_LIST = True
  
        if IS_IN_LIST:
            phonebook.remove(sms.message.split()[1])
            message = "Le numero {} a ete retire de la liste".format(sms.message.split()[1])
        else:
            message = "Le numero {} n'est pas dans la liste".format(sms.message.split()[1])

    elif "!lire_temps" == sms.message:
        print("lire temps")
        message = "Le temps minimum avant de declarer un essaimage est de {} minutes".format(temps_mono)


    elif "!modif_temps" == sms.message.split()[0]:
        print("modifier temps")
        temps_mono = sms.message.split()[1]
        message = "Le temps minimum avant de declarer un essaimage est maintenant de {} minutes".format(temps_mono)
        
        
    else:
        message = None

    if message:
        sms_list.append(SMS(sms.numero, message))
        sms_list[-1].send()

    return(seuilb, seuilh, SEUILS_BLOQUES, phonebook, temps_mono)

    

def get_temp():
    
    return sensor.temperature


    
def get_humid():
    
    return sensor.relative_humidity



def get_son():

    #On lit la valeur du capteur de son via le CAN (canal 0, pendant 50ms)
    return read_MAX4466(adc, channel = 0, sample_window = 50, start_millis = current_milli_time())   



def get_date():
    
    date = time.strftime("%a %d %b %Y %H:%M:%S", time.gmtime())
    
    for i in range(0,12):
        date = date.replace(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][i], ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "November", "December"][i])
    for i in range(0,7):
        date = date.replace(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][i], ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"][i])

    return date



def data_saving(path, txt, mode):
    """Fonction servant a sauvegarder les donnees dans un fichier.
    path = chemin du fichier ou il faut sauvegarder les donnees
    txt = message a sauvegarder
    mode = mode d'ouverture du fichier"""

    data_file = open(path, mode)
    #data_file.write(str(t) + '\n' + str(cpt) + '\n' + str(int(mono)))
    data_file.write(txt)
    data_file.close()



def data_recovery(path):
    """Fonction servant a recuperer les donnees sauvegardees par la fonction data_saving()
    path = chemin du fichier ou l'on veut recuperer les donnees
    Retourne une liste des elements sauvegardes dans le fichier"""
   
    file = open(path, "rt")
    data = file.readlines()
    file.close()
    return list(map(lambda s: s.strip(), data))

# Main

SMS_RECEIVED = False
temps_echantillon = 1 #minutes

adc = MCP3008()

i2c = busio.I2C(board.SCL, board.SDA)
sensor = HTU21D(i2c)

s = serial.Serial("/dev/ttyS0", 115200)
s.write(b"ATE0\r\n")

param = data_recovery("./param.txt")
phonebook = data_recovery("./phonebook.txt")

for p in param:
    print("{}".format(p))

if param[0] == "True":
    SEUILS_BLOQUES = True
else:
    SEUILS_BLOQUES = False

if SEUILS_BLOQUES:
    seuilb = float(param[1])
    seuilh = float(param[2])

else:
    seuilb = adc.read(channel = 1)  #Seuil bas - Lecture de la valeur du potentiometre
    bandwidth = adc.read(channel = 2)
    seuilh = seuilb + bandwidth / 5           #Seuil haut

cpt = int(param[3])

if param[4] == "True":
    mono = True
else:
    mono = False

if param[5] == "True":
    alarm = True
else:
    alarm = False

temps_mono = int(param[6])


#On lit les valeurs des capteurs
sound_value = get_son()
temperature_value = get_temp()
humidite_value = get_humid()

sms_list = []


  

#Gestion du seuil a hysteresis
if sound_value >= seuilh:
    cpt += temps_echantillon
    mono = True

if(sound_value < seuilh) and (sound_value > seuilb) and (mono == True):
    cpt += temps_echantillon

if sound_value <= seuilb:
    cpt = 0
    mono = False


if cpt >= temps_mono:
    alarm = True     #Essaimage en cours
else :
    alarm = False       #Pas d'essaimage

#alarm = True
if alarm:
    for numero in phonebook:
        date = time.strftime("%Y", time.localtime())[2:] + time.strftime("/%m/%d", time.localtime())
        heure = time.strftime("%H:%M:%S", time.localtime())
        message = "ESSAIMAGE DETECTE\nDate : {} {}\nDepuis {} minutes\nTemperature : {:.2f}C\nHumidite : {:.2f}%".format(date, heure, cpt, temperature_value, humidite_value)
        sms_list.append(SMS(numero, message))
        sms_list[-1].send()


raw_sms = get_new_sms()
raw_sms = raw_sms.replace("\r\n", "")
raw_sms = raw_sms.replace("OK", "")
raw_sms = raw_sms.split("+CMGL")
raw_sms = list(filter(lambda a: a != "", raw_sms))

for sms in raw_sms:
    if SMS.received(sms):
        sms_list.append(SMS.received(sms))

for sms in sms_list:
    print("Date : {}".format(sms.date))
    print("Heure : {}".format(sms.heure))
    print("Numero : {}".format(sms.numero))
    print("Message : {}".format(sms.message))
    print("\n")

for sms in sms_list:
    if sms.message[0] == "!":
        command_return = command(sms, seuilb, seuilh, SEUILS_BLOQUES, phonebook, temps_mono)
        SEUILS_BLOQUES = command_return[2]
        if SEUILS_BLOQUES:
            seuilb = command_return[0]
            seuilh = command_return[1]
        phonebook = command_return[3]
        temps_mono = command_return[4]

sms_txt = ""

for sms in sms_list:
    sms_txt += "{}\t{}\t{}\t{}\t{}\n".format(sms.mode, sms.date, sms.heure, sms.numero, sms.message)

data_saving("./sms.log", sms_txt, "a")
data_saving("./data.log", "\t".join([time.strftime("%Y", time.localtime())[2:] + time.strftime("/%m/%d", time.localtime()),
                                     time.strftime("%H:%M:%S", time.localtime()), str(seuilb), str(seuilh), str(cpt), str(mono), str(alarm), str(temps_mono),
                                     str(temperature_value), str(humidite_value), str(sound_value)]) + "\n", "a")


data_saving("./param.txt", "\n".join([str(SEUILS_BLOQUES), str(seuilb), str(seuilh), str(cpt), str(mono), str(alarm), str(temps_mono)]), "w")
data_saving("./phonebook.txt", "\n".join(phonebook), "w")

#s.write(b"AT+CMGD=1,3\r\n")
#time.sleep(25)
s.close()
