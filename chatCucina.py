
import os
import io
import sys
import asyncio
import argparse
import pyaudio
import wave
import json
import librosa
import requests
from scipy.io import wavfile as wav
from scipy.fftpack import fft
import numpy as np
from mutagen.mp3 import MP3
from vosk import Model, KaldiRecognizer, SetLogLevel
from pygame import mixer
from pygame import time
from gtts import gTTS
from revChatGPT.V1 import Chatbot


gpt_response = ""
os.environ["CHATGPT_BASE_URL"] = "https://ai.fakeopen.com/api/"

def speech_to_text(speech_file):

    stt = ""

    wf = wave.open(speech_file, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        sys.exit(1)



    model = Model("/home/mikilinux/Desktop/ChefGPT/vosk-model-small-it-0.22")

    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    rec.SetPartialWords(True)

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        rec.AcceptWaveform(data)
            
       


   
    stt=json.loads(rec.Result())
    if stt== "":
     stt= json.loads(rec.PartialResult())
    return stt["text"]


async def ask_chat_gpt(prompt):
    global gpt_response
    chat  = Chatbot(config={
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJtaWNoZWxlLmlwcG9saXRpQG1lLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlfSwiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS9hdXRoIjp7InVzZXJfaWQiOiJ1c2VyLTIyTzZMRkpMano1ZzE4VDQzSWVnakwzRiJ9LCJpc3MiOiJodHRwczovL2F1dGgwLm9wZW5haS5jb20vIiwic3ViIjoiYXV0aDB8NjNjMTJiZGExMWQ2ZGU3ODY1MjA4Nzc3IiwiYXVkIjpbImh0dHBzOi8vYXBpLm9wZW5haS5jb20vdjEiLCJodHRwczovL29wZW5haS5vcGVuYWkuYXV0aDBhcHAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY5NTcyMzQxNiwiZXhwIjoxNjk2OTMzMDE2LCJhenAiOiJUZEpJY2JlMTZXb1RIdE45NW55eXdoNUU0eU9vNkl0RyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgbW9kZWwucmVhZCBtb2RlbC5yZXF1ZXN0IG9yZ2FuaXphdGlvbi5yZWFkIG9yZ2FuaXphdGlvbi53cml0ZSBvZmZsaW5lX2FjY2VzcyJ9.rkWhs5wg63ynnAPDtztFZQnKsnfiwzdJA0ATStJu_g3WxUEyhGkNAiqcL8DG9zi1GJ6LCg85DD3Os_dFX33cYhTxm8hqi-KpvXSJCuH-Qv6f-CFUPU_X8_0Rapg4YOyJAeiOtE9fSHhjsadj0piWAKMeXeLpFYspB0yWaHjCHI22LjppLaJ32Ol0Rh3kX3PbVAa_R9_4zeih-gCUjp9ZoxiFsBQVUMOqihKDckvqSY_SzJKaVCm87mwkmWR3j3oapisvoQ4feKaoMqhvW9PXD4co6FBf__M1EpN5cbqTdJnOo23UI-xVSlKA0X5KnaauEXVt5qh2DsyW1cyP0xZvgQ"
  }, conversation_id="938e9ef6-792e-458c-9447-0c0de1b1c604")
    
    for data in chat.ask(prompt ):
            response = data["message"]


    gpt_response=response

    return



def record_wav():
    form_1 = pyaudio.paInt16
    chans = 1
    samp_rate = 8000
    chunk = 4096
    record_secs = 7
    
    wav_output_filename = '/home/mikilinux/Desktop/ChefGPT/input.wav'

    audio = pyaudio.PyAudio()



    #os.system("pactl set-card-profile bluez_card.16_3C_FC_EB_81_D6 headset-head-unit")
    print("fine impostazione")
    print("Sto Registrando")
    riproduciMusica("domanda")
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                        input = True, \
                        frames_per_buffer=chunk)
                 

    frames = []

    # Loop through stream and append audio chunks to frame array.
    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        data = stream.read(chunk,exception_on_overflow = False)
        frames.append(data)

    print("Fine Registrazione")

    # Stop the stream, close it, and terminate the pyaudio instantiation.
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the audio frames as .wav file.
    wavefile = wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()
    #print("impostato a a2dp")
    #os.system("pactl set-card-profile bluez_card.16_3C_FC_EB_81_D6 a2dp-sink")
    #print("fine impostazione")
    return


def record_wavSINO():
    form_1 = pyaudio.paInt16
    chans = 1
    samp_rate = 8000
    chunk = 4096
    record_secs = 5
    
    wav_output_filename = '/home/mikilinux/Desktop/ChefGPT/input2.wav'

    audio = pyaudio.PyAudio()

    print("Sto Registrando")
    riproduciMusica("domanda")

    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                        input = True, \
                        frames_per_buffer=chunk)
                 
  
    frames = []

    # Loop through stream and append audio chunks to frame array.
    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        data = stream.read(chunk,exception_on_overflow = False)
        frames.append(data)

    print("Fine Registrazione")

    # Stop the stream, close it, and terminate the pyaudio instantiation.
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the audio frames as .wav file.
    wavefile = wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()
    print("a2dp imposto")
    #os.system("pactl set-card-profile bluez_card.16_3C_FC_EB_81_D6 a2dp-sink")
    print("fine impostazione")
    return

def riproduci(text):
	
	#os.system("pactl set-card-profile bluez_card.16_3C_FC_EB_81_D6 a2dp-sink")
	tts = gTTS(text,lang = "it", slow = False)
	tts.save('/home/mikilinux/Desktop/ChefGPT/frase.mp3')
	mixer.music.load("/home/mikilinux/Desktop/ChefGPT/frase.mp3")
	mixer.music.play()	  
	audio=MP3("/home/mikilinux/Desktop/ChefGPT/frase.mp3")
	#print(audio.info.length)
	time.wait(int(audio.info.length)*1000+500)



def riproduciMusica(tipo):
	#os.system("pactl set-card-profile bluez_card.16_3C_FC_EB_81_D6 a2dp-sink")
	if tipo == "domanda" :
		mixer.music.load("/home/mikilinux/Desktop/ChefGPT/ping.mp3")
		mixer.music.play()	      	    

	if tipo == "attesa" :
		mixer.music.load("/home/mikilinux/Desktop/ChefGPT/wait.mp3")
		mixer.music.play()
	if tipo == "attesa2" :
		mixer.music.load("/home/mikilinux/Desktop/ChefGPT/polka.mp3")
		mixer.music.play()
	if tipo == "continuo" :
		mixer.music.load("/home/mikilinux/Desktop/ChefGPT/banana.mp3")
		mixer.music.play()



def boh(file):
	respuesta=""
	rate, data = wav.read(file)
	vc = np.fft.fft(data)
	abs_vc = np.absolute(vc)
	abs_vc = abs_vc[0:int(len(abs_vc)/2)]
	
	upper7000 = 0
	below7000 = 0
	below5000 = 0
	below3000 = 0
	total_energy = np.sum(abs_vc)
	
	for i in range(len(abs_vc)) :
		if i<3000 :
			below3000 += abs_vc[i]
			
		elif i<5000 and i>3000 :
			below5000 += abs_vc[i]
			
		elif i<7000 and i>5000:
			below7000 += abs_vc[i]
		elif i>7000:
			upper7000 += abs_vc[i]
			
	upper7000Rate = upper7000 / total_energy
	below7000Rate = below7000 / total_energy
	below5000Rate = below5000 / total_energy
	below3000Rate = below3000 / total_energy
	
	print(below3000Rate)
	print(below5000Rate)
	print(below7000Rate)
	print(upper7000Rate)
	print(upper7000)
	print(below7000)
	
	if below3000Rate + below5000Rate > 0.85 :
		respuesta="no"
		print("eh no")
	elif upper7000<100000000 and below7000<100000000 :
		respuesta="vuota"
		print("eh vuota")
	elif upper7000Rate + below7000Rate + below5000Rate > 0.50 :
		respuesta="yes"
		print("eh si")
	return respuesta

def inviatelegram(stringa) :
    TOKEN = "6669718176:AAEPsciRzWejO4noo_nQiZ3PY1IvE-lWGdw"
    chat_id = "17107215"
    message = stringa
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    print(requests.get(url).json())


def main():
    mixer.init()
    rispostina="gisa"
    os.system("pactl set-card-profile bluez_card.16_3C_FC_EB_81_D6 a2dp-sink")
    while True:
        riproduci("Dimme la tua domanda de cucina zio! Se vuoi parlà de altri cazzi, dimme ALTRO!")
        os.system("pactl set-card-profile bluez_card.16_3C_FC_EB_81_D6 headset-head-unit")
        time.wait(1000)
        print("settato")
        record_wav()
        os.system("pactl set-card-profile bluez_card.16_3C_FC_EB_81_D6 a2dp-sink")
        riproduci("perfetto! ora aspetta che è na carretta!")
        #riproduciMusica("attesa2")
        boolAltro=False

        question = speech_to_text("/home/mikilinux/Desktop/ChefGPT/input.wav")
        #question =  input("Please enter something: ")
        print("Domandona: {0}".format(question))
        riproduci("Me hai chiesto: "+question+"! benissimo fratè!")
        # Send text to ChatGPT.

        if question == "chiudi" :
            break
        if question == "altro" :
            boolAltro=True
        if boolAltro ==True :
               riproduci("Dimme tutto zio!")
               os.system("pactl set-card-profile bluez_card.16_3C_FC_EB_81_D6 headset-head-unit")
               time.wait(1000)
               record_wav()
               os.system("pactl set-card-profile bluez_card.16_3C_FC_EB_81_D6 a2dp-sink")
               riproduci("perfetto! ora aspetta che è na carretta!")
               #riproduciMusica("attesa2")
               question = speech_to_text("/home/mikilinux/Desktop/ChefGPT/input.wav")
               #question =  input("Please enter something: ")
               print("Domandona: {0}".format(question))               
               riproduci("Me hai chiesto: "+question+"! benissimo fratè!")


        riproduci("Attendi sennò te sbrocco! Te deve da risponde l'intelligenza artificiale")
        riproduciMusica("attesa")
        asyncio.run(ask_chat_gpt(question+ ". Devi rispondere in stretto dialetto romano però!"))
        print("Risposta: {0}".format(gpt_response))
        inviatelegram("Ecco la tua ricetta: {0}".format(gpt_response))
        if boolAltro==False:
            
            frasi = gpt_response.split("\n")
            numFrase=0
            for frase in frasi:
            	  notripeti=False
            	  numFrase=numFrase+1
            	  if len(frase) <2:
            	  	continue
            	  riproduci(frase)
            	  notripeti= "INGREDIENTI" in frase.upper() or "ISTRUZIONI" in frase.upper() or frase.startswith('-') or numFrase == 1 or numFrase==len(frasi)
            	  if notripeti == False :
                  	riproduci("ripeto!")
                  	riproduci(frase)
                  	riproduci("hai capito fratè! continuo!")




        else:
        	riproduci(gpt_response)
        riproduci("ho finito zio! se vuoi chiudere l'applicazione dimmi chiudi, altrimenti ricomincio. Se beccamo")
        os.system("pactl set-card-profile bluez_card.16_3C_FC_EB_81_D6 headset-head-unit")
        time.wait(1000)
        record_wavSINO()
        os.system("pactl set-card-profile bluez_card.16_3C_FC_EB_81_D6 a2dp-sink")
        question2 = speech_to_text("/home/mikilinux/Desktop/ChefGPT/input2.wav")
        print(question2)
        if question2=="chiudi" :
        	quit()
         


      



if __name__ == "__main__":
    main()

