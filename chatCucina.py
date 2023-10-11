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
TELEGRAM_TOKEN = ""
TELEGRAM_CHAT_ID = ""
ACCESS_TOKEN_CHATGPT = ""
CONVERSATION_ID_CHATGPT=""


DIALETTO_PARLATO="romano" #OPZIONI romano/napoletano/sardo/pugliese/english




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

	tts = gTTS(text, lang=codice_lang, slow=False)
	tts.save(mainFolder + "/frase.mp3")
	riproduciVeloce(mainFolder + "/frase.mp3")


def getFrasi(dialetto):
    global intro,carretta,dimmitutto,attendi,mehaichiesto1,mehaichiesto2,ripetiz,sticazzi,finito
    
    if dialetto == "romano":
        intro = "Dimme la tua domanda de cucina zio! Se vuoi parlà de altri cazzi, dimme ALTRO!"
        carretta="perfetto! ora aspetta che è na carretta!"
        dimmitutto="Dimme tutto zio!"
        attendi="Attendi sennò te sbrocco! Te deve da risponde l'intelligenza artificiale"
        mehaichiesto1="Me hai chiesto: "
        mehaichiesto2="! benissimo fratè!"
        ripetiz="se non hai capito dimmi ripeti! te ripeto le ultime."
        sticazzi="se non hai capito sticazzi! continuo lo stesso"
        finito="ho finito zio! se vuoi chiudere l'applicazione dimmi chiudi, altrimenti non dire nulla e ricomincio. Se beccamo"
    elif dialetto == "pugliese":
        intro = "Diceme 'a tue domande de cucina, fratè. Si vuoi parlare 'e atre robìe, diceme 'altrò!"
        carretta = "Perfetto! Aro aspetta ca è lentissime!"
        dimmitutto = "Diceme tutto amico!"
        attendi = "Attendi, sennò ti meno! Te deve risponde l'intelligenza artificiale"
        mehaichiesto1 = "Mi hai chiesto: "
        mehaichiesto2 = "! benissimo fratè!"
        ripetiz = "si nun hai capito, diceme ripeti! Te ripeto 'e l'urtime."
        sticazzi = "si nun hai capito, non me ne frega 'n cazzo! continuo lo stesso"
        finito = "ho finito amico! si vuoi chiudere l'applicazione, diceme chiudi, aiat a non dì niente e ricomincio."
    elif dialetto == "napoletano":
        intro = "Diceme 'a tue domanda 'e cucina, frate. Si vuoi parla 'e atre robè, diceme 'altrò!"
        carretta = "Perfetto! Aro aspetta ca è lentissimo!"
        dimmitutto = "Diceme tutto amico!"
        attendi = "Attendi, sennò te meno! Te deve da risponde l'intelligenza artificiale"
        mehaichiesto1 = "M'hai chiesto: "
        mehaichiesto2 = "! benissimo frate!"
        ripetiz = "se nun hai capito, diceme ripeti! Te ripeto 'e 'e sciute."
        sticazzi = "se nun hai capito, non me ne frega un cazzo! jamme 'o stesso"
        finito = "ho finito amico! si vuoi chiudere l'applicazione, diceme chiudi, aiat a non dicere niente e ricomincio."
    elif dialetto == "sardo":
        intro = "Dime sa tue domanda de cuina, frade. Si boles faeddare de atres cosas, dime 'altrò!"
        carretta = "Perfetu! Aiat a no istare fintzes issolu!"
        dimmitutto = "Dime totu amigu!"
        attendi = "Atendi, a no ti meno! Isso deve rispondere sa intellìgitzia artificiale."
        mehaichiesto1 = "Mi hai chiestu: "
        mehaichiesto2 = "! benissimu frade!"
        ripetiz = "si no hats capidu, dime repiti! T'appo istadu chiare les ùrtimas."
        sticazzi = "si no hats capidu, no me ne frega un cazzo! sigho s'istessu."
        finito = "ho finido amigu! si boles serrare s'aplicatzione, dime serrare, aiat a no faeddare nada e torro a iniziare."
    elif dialetto == "english":
        intro = "Please ask me a cooking question bro!"
        carretta = "Now wait. I am slow as fuck"
        dimmitutto = "Now you can tell me, motherfucker!"
        attendi = "Now you must wait for the artificial intelligence. Understand bro? Relax loser."
        mehaichiesto1 = "You asked me: "
        mehaichiesto2 = "! Alright, yo man!"
        ripetiz = "If you didn't understand, say repeat! I'll repeat for this time bro."
        sticazzi = "If you didn't understand I dont fucking care! I'll go on."
        finito = "Ended bro. If you want to close the script say close, otherwise don't say anything"
    else:
        print("error")



def getGlobalFrasi(dialetto):
    global ingredientiString,istruzioniString,altroString,ripetiString,chiudiString,devirisp1,devirisp2,ecco,modelFolder,codice_lang
    if dialetto !="english" :
        ingredientiString="INGREDIENTI"
        istruzioniString="ISTRUZIONI"
        altroString = "altro"
        ripetiString="ripeti"
        chiudiString="chiudi"
        devirisp1=". Devi rispondere in stretto dialetto "
        devirisp2=" però!"
        ecco="Ecco la tua ricetta:"
        modelFolder="vosk-model-small-it-0.22"
        codice_lang="it"
    elif dialetto == "english":
        ingredientiString="INGREDIENTS"
        istruzioniString="INSTRUCTIONS"
        altroString = "other"
        ripetiString="repeat"
        chiudiString="close"
        devirisp1=". Please answer in strict london slang "
        devirisp2=" bro!"
        ecco="Here is your recipe:"
        modelFolder="vosk-model-small-en-us-0.15"
        codice_lang="en"
 
    else:
        print("error")

	
def riproduciRipeti(text):

	tts = gTTS(text, lang=codice_lang, slow=False)
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
    

    getFrasi(DIALETTO_PARLATO)
    getGlobalFrasi(DIALETTO_PARLATO)
    setta_profilo_audio("a2dp-sink")
    riproduci(intro)

    riproduciMusica("domanda")
    setta_profilo_audio("headset-head-unit")

    recordVeloce(mainFolder+"/input.wav","7")
    print("risetto")
    setta_profilo_audio("a2dp-sink")
    riproduci(carretta)
    closePreviousMusic()
    riproduciMusica("attesa2")
    boolAltro = False
    question = speech_to_text(mainFolder + "/input.wav")
    print("Domandona: {0}".format(question))
    closePreviousMusic()
    riproduci(mehaichiesto1 + question + mehaichiesto2)
    if question == altroString:
    	boolAltro = True
    if boolAltro == True:
    	riproduci(dimmetutto)
    	riproduciMusica("domanda")
    	setta_profilo_audio("headset-head-unit")
    	recordVeloce(mainFolder+"/input.wav","7")
    	setta_profilo_audio("a2dp-sink")
    	riproduci(carretta)
    	closePreviousMusic()
    	riproduciMusica("attesa2")
    	question = speech_to_text(mainFolder + "/input.wav")
    	print("Domandona: {0}".format(question))
    	riproduci(mehaichiesto1 + question + mehaichiesto2)
    
    riproduci(attendi)
    riproduciMusica("attesa")
    asyncio.run(ask_chat_gpt(question + devirisp1+DIALETTO_PARLATO+devirisp2))
    print("Risposta: {0}".format(gpt_response))
    closePreviousMusic()
    riproduciMusica("ricetta")
    if boolAltro == False:
    	inviatelegram(ecco+" {0}".format(gpt_response))
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
                	
    		notripeti = (ingredientiString in frase.upper()or istruzioniString in frase.upper() or frase.endswith(":") or frase.startswith("-")or numFrase == 1 or numFrase == len(frasi))
    		print("da ripetere? " +str(not notripeti))
    		if notripeti == False:
    			frasiDaRipetere=frasiDaRipetere+1
    			arrayFrasi.append(frase)
    			if frasiDaRipetere==3 or numFrase== len(frasi):
    				frasiDaRipetere=0
    				riproduciRipeti(ripetiz)
    				closePreviousMusic()
    				riproduciMusica("domanda")
    				setta_profilo_audio("headset-head-unit")
    				recordVeloce(mainFolder+"/input2.wav","5")
    				setta_profilo_audio("a2dp-sink")
    				riproduci("Ok!")
    				riproduciMusica("ricetta")
    				if ripeti(ripetiString):
    					for frasetta in arrayFrasi:
    						riproduci(frasetta)
    					arrayFrasi=[]
    					riproduci(sticazzi)
    else:
    	riproduci(gpt_response)
    closePreviousMusic()	
    riproduci(finito)
    riproduciMusica("domanda")
    setta_profilo_audio("headset-head-unit")
    recordVeloce(mainFolder+"/input2.wav","5")
    #record_wavSINO()
    setta_profilo_audio("a2dp-sink")
    	
    if ripeti(chiudiString):
    	sys.exit("chiusa con successo")
    else:
    	main()
    	


if __name__ == "__main__":
    main()