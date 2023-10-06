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
bluetoothCard = "bluez_card.16_3C_FC_EB_81_D6"
mainFolder = "/home/mikilinux/Desktop/ChefGPT"
modelFolder = "vosk-model-small-it-0.22"
TELEGRAM_TOKEN = "6669718176:AAEPsciRzWejO4noo_nQiZ3PY1IvE-lWGdw"
TELEGRAM_CHAT_ID = "17107215"
ACCESS_TOKEN_CHATGPT = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJtaWNoZWxlLmlwcG9saXRpQG1lLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlfSwiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS9hdXRoIjp7InVzZXJfaWQiOiJ1c2VyLTIyTzZMRkpMano1ZzE4VDQzSWVnakwzRiJ9LCJpc3MiOiJodHRwczovL2F1dGgwLm9wZW5haS5jb20vIiwic3ViIjoiYXV0aDB8NjNjMTJiZGExMWQ2ZGU3ODY1MjA4Nzc3IiwiYXVkIjpbImh0dHBzOi8vYXBpLm9wZW5haS5jb20vdjEiLCJodHRwczovL29wZW5haS5vcGVuYWkuYXV0aDBhcHAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY5NTcyMzQxNiwiZXhwIjoxNjk2OTMzMDE2LCJhenAiOiJUZEpJY2JlMTZXb1RIdE45NW55eXdoNUU0eU9vNkl0RyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgbW9kZWwucmVhZCBtb2RlbC5yZXF1ZXN0IG9yZ2FuaXphdGlvbi5yZWFkIG9yZ2FuaXphdGlvbi53cml0ZSBvZmZsaW5lX2FjY2VzcyJ9.rkWhs5wg63ynnAPDtztFZQnKsnfiwzdJA0ATStJu_g3WxUEyhGkNAiqcL8DG9zi1GJ6LCg85DD3Os_dFX33cYhTxm8hqi-KpvXSJCuH-Qv6f-CFUPU_X8_0Rapg4YOyJAeiOtE9fSHhjsadj0piWAKMeXeLpFYspB0yWaHjCHI22LjppLaJ32Ol0Rh3kX3PbVAa_R9_4zeih-gCUjp9ZoxiFsBQVUMOqihKDckvqSY_SzJKaVCm87mwkmWR3j3oapisvoQ4feKaoMqhvW9PXD4co6FBf__M1EpN5cbqTdJnOo23UI-xVSlKA0X5KnaauEXVt5qh2DsyW1cyP0xZvgQ"
CONVERSATION_ID_CHATGPT = "938e9ef6-792e-458c-9447-0c0de1b1c604"

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
		riproduciVeloce(mainFolder + "/wait.mp3")

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
	
def restart():

    print("argv was",sys.argv)
    print("sys.executable was", sys.executable)
    print("restart now")
    os.execv(sys.executable, ['python3'] + sys.argv)

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
    boolAltro = False
    question = speech_to_text(mainFolder + "/input.wav")
    print("Domandona: {0}".format(question))
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
    	question = speech_to_text(mainFolder + "/input.wav")
    	print("Domandona: {0}".format(question))
    	riproduci("Me hai chiesto: " + question + "! benissimo fratè!")
    
    riproduci("Attendi sennò te sbrocco! Te deve da risponde l'intelligenza artificiale")
    riproduciMusica("attesa")
    asyncio.run(ask_chat_gpt(question + ". Devi rispondere in stretto dialetto romano però!"))
    print("Risposta: {0}".format(gpt_response))
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
    				
    				riproduciMusica("domanda")
    				setta_profilo_audio("headset-head-unit")
    				recordVeloce(mainFolder+"/input2.wav","5")
    				setta_profilo_audio("a2dp-sink")
    				riproduci("Ok!")
    				if ripeti("ripeti"):
    					for frasetta in arrayFrasi:
    						riproduci(frasetta)
    					arrayFrasi=[]
    					riproduci("se non hai capito sticazzi! continuo lo stesso")
    else:
    	riproduci(gpt_response)
    	
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
