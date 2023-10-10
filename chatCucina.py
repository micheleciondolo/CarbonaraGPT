import os
import io
import sys
import asyncio
import argparse
import wave
import json
import requests
import subprocess
import time
from vosk import Model, KaldiRecognizer, SetLogLevel
from gtts import gTTS
from revChatGPT.V1 import Chatbot


gpt_response = ""
os.environ["CHATGPT_BASE_URL"] = "https://ai.fakeopen.com/api/"

# SETTINGS
bluetoothCard = ""
mainFolder = ""
modelFolder = "vosk-model-small-it-0.22"
TELEGRAM_TOKEN = "
TELEGRAM_CHAT_ID = ""
ACCESS_TOKEN_CHATGPT = ""

def get_profilo_audio():
	risultino= str(subprocess.check_output(['sh' , mainFolder+'/profiloattivo.sh']))
	print(risultino)
	return risultino

def speech_to_text(speech_file):

    stt = ""

    wf = wave.open(speech_file, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        print(str(wf.getnchannels()) +" "+ str(wf.getsampwidth())+" "+ str(wf.getcomptype()))
        sys.exit(1)

    model = Model(mainFolder + "/" + modelFolder)

    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    rec.SetPartialWords(True)

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        rec.AcceptWaveform(data)

    stt = json.loads(rec.Result())
    if stt == "":
        stt = json.loads(rec.PartialResult())
    return stt["text"]


async def ask_chat_gpt(prompt):
    global gpt_response
    chat = Chatbot(
        config={"access_token": ACCESS_TOKEN_CHATGPT},
        conversation_id=CONVERSATION_ID_CHATGPT,
    )

    for data in chat.ask(prompt):
        response = data["message"]

    gpt_response = response

    return



def recordVeloce(path,secondi):
	print("Inizio rec")
	subprocess.run(["arecord", "-d",  secondi  ,"-f","S16_LE",path])
	print("Fine rec")

def riproduciVeloce(path):
	subprocess.run(["mpg123", "play",  path])

	
def riproduciVeloceNoWait(path):
	subprocess.Popen(["mpg123", "play",  path])


	
def riproduciVeloceNoWait2(path,volume):
	subprocess.Popen(["mpg123", "-f","-"+volume,  path])
	

def riproduci(text):

	tts = gTTS(text, lang="it", slow=False)
	tts.save(mainFolder + "/frase.mp3")
	riproduciVeloce(mainFolder + "/frase.mp3")
	
def riproduciRipeti(text):

	tts = gTTS(text, lang="it", slow=False)
	tts.save(mainFolder + "/frase2.mp3")
	riproduciVeloce(mainFolder + "/frase2.mp3")


def riproduciMusica(tipo):
	if tipo == "domanda":
		riproduciVeloce(mainFolder + "/ping.mp3")
	if tipo == "attesa":
		riproduciVeloceNoWait(mainFolder + "/wait.mp3")
	if tipo == "attesa2":
		riproduciVeloceNoWait(mainFolder + "/polka.mp3")
	if tipo == "ricetta":
		riproduciVeloceNoWait2(mainFolder + "/banana2.mp3","2000")

def inviatelegram(stringa):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={stringa}"
    print(requests.get(url).json())



def ripeti(stringa):
	gisa=False
	esclamazione = speech_to_text(mainFolder + "/input2.wav")
	if esclamazione == stringa:
		gisa=True
	print(esclamazione)
	return gisa
	
def closePreviousMusic():
	subprocess.run(["pkill", "mpg123"])

def setta_profilo_audio(stringa):
	subprocess.run(["pactl", "set-card-profile",  bluetoothCard  ,stringa])
	while stringa not in get_profilo_audio():
		time.sleep(100)


def main():

    setta_profilo_audio("a2dp-sink")
    riproduci("Dimme la tua domanda de cucina zio! Se vuoi parlà de altri cazzi, dimme ALTRO!")

    riproduciMusica("domanda")
    setta_profilo_audio("headset-head-unit")

    recordVeloce(mainFolder+"/input.wav","7")
    print("risetto")
    setta_profilo_audio("a2dp-sink")
    riproduci("perfetto! ora aspetta che è na carretta!")
    closePreviousMusic()
    riproduciMusica("attesa2")
    boolAltro = False
    question = speech_to_text(mainFolder + "/input.wav")
    print("Domandona: {0}".format(question))
    closePreviousMusic()
    riproduci("Me hai chiesto: " + question + "! benissimo fratè!")
    if question == "altro":
    	boolAltro = True
    if boolAltro == True:
    	riproduci("Dimme tutto zio!")
    	riproduciMusica("domanda")
    	setta_profilo_audio("headset-head-unit")
    	recordVeloce(mainFolder+"/input.wav","7")
    	setta_profilo_audio("a2dp-sink")
    	riproduci("perfetto! ora aspetta che è na carretta!")
    	closePreviousMusic()
    	riproduciMusica("attesa2")
    	question = speech_to_text(mainFolder + "/input.wav")
    	print("Domandona: {0}".format(question))
    	riproduci("Me hai chiesto: " + question + "! benissimo fratè!")
    
    riproduci("Attendi sennò te sbrocco! Te deve da risponde l'intelligenza artificiale")
    riproduciMusica("attesa")
    asyncio.run(ask_chat_gpt(question + ". Devi rispondere in stretto dialetto romano però!"))
    print("Risposta: {0}".format(gpt_response))
    closePreviousMusic()
    riproduciMusica("ricetta")
    if boolAltro == False:
    	inviatelegram("Ecco la tua ricetta: {0}".format(gpt_response))
    	frasi = gpt_response.split("\n")
    	print("numero frasi "+str(len(frasi)))
    	numFrase = 0
    	frasiDaRipetere=0
    	arrayFrasi=[]
    	for frase in frasi:

    		if len(frase) < 2:
    			continue
    		notripeti = False
    		numFrase = numFrase + 1
    		riproduci(frase)
    		print("numero frase "+str(numFrase))
    		if(numFrase==len(frasi)):
    			print("finito")
    			break
                	
    		notripeti = ("INGREDIENTI" in frase.upper()or "ISTRUZIONI" in frase.upper() or frase.endswith(":") or frase.startswith("-")or numFrase == 1 or numFrase == len(frasi))
    		print("da ripetere? " +str(not notripeti))
    		if notripeti == False:
    			frasiDaRipetere=frasiDaRipetere+1
    			arrayFrasi.append(frase)
    			if frasiDaRipetere==3 or numFrase== len(frasi):
    				frasiDaRipetere=0
    				riproduciRipeti("se non hai capito dimmi ripeti! te ripeto le ultime.")
    				closePreviousMusic()
    				riproduciMusica("domanda")
    				setta_profilo_audio("headset-head-unit")
    				recordVeloce(mainFolder+"/input2.wav","5")
    				setta_profilo_audio("a2dp-sink")
    				riproduci("Ok!")
    				riproduciMusica("ricetta")
    				if ripeti("ripeti"):
    					for frasetta in arrayFrasi:
    						riproduci(frasetta)
    					arrayFrasi=[]
    					riproduci("se non hai capito sticazzi! continuo lo stesso")
    else:
    	riproduci(gpt_response)
    closePreviousMusic()	
    riproduci("ho finito zio! se vuoi chiudere l'applicazione dimmi chiudi, altrimenti non dire nulla e ricomincio. Se beccamo")
    riproduciMusica("domanda")
    setta_profilo_audio("headset-head-unit")
    recordVeloce(mainFolder+"/input2.wav","5")
    #record_wavSINO()
    setta_profilo_audio("a2dp-sink")
    	
    if ripeti("chiudi"):
    	sys.exit("chiusa con successo")
    else:
    	main()
    	


if __name__ == "__main__":
    main()
