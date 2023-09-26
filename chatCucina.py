
import os
import io
import sys
import asyncio
import argparse
import pyaudio
import wave
import json



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



    model = Model("vosk-model-small-it-0.22")

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
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJtaWNoZWxlLmlwcG9saXRpQG1lLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlfSwiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS9hdXRoIjp7InVzZXJfaWQiOiJ1c2VyLTIyTzZMRkpMano1ZzE4VDQzSWVnakwzRiJ9LCJpc3MiOiJodHRwczovL2F1dGgwLm9wZW5haS5jb20vIiwic3ViIjoiYXV0aDB8NjNjMTJiZGExMWQ2ZGU3ODY1MjA4Nzc3IiwiYXVkIjpbImh0dHBzOi8vYXBpLm9wZW5haS5jb20vdjEiLCJodHRwczovL29wZW5haS5vcGVuYWkuYXV0aDBhcHAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY5NDI3NjI0MywiZXhwIjoxNjk1NDg1ODQzLCJhenAiOiJUZEpJY2JlMTZXb1RIdE45NW55eXdoNUU0eU9vNkl0RyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgbW9kZWwucmVhZCBtb2RlbC5yZXF1ZXN0IG9yZ2FuaXphdGlvbi5yZWFkIG9yZ2FuaXphdGlvbi53cml0ZSBvZmZsaW5lX2FjY2VzcyJ9.j2mKdmywluYyT2ik1kQvURIgbk8wSnOu9nF5hMdPLKcT_oQhEOhadrrJzoYZ06qVhrHnxMFH_B37MNcGaOQSvs8W6l0BlfdhEsj6iVHFprzg3dLED7wmuV5mY-3M7nAjW85lbTCdZJIv4jj3RtI7ysebIaY1CgXMbcPg7rJS4Cr6Nd7THEsdxcW2SxnrxblKSwSrUOSLxUMsNrlQzuUmIK7O6QoCNalUd_sv0yiM1t-pRJcL01oQmvPH0S-hmh4xM9kc6xBuuGSTuW1Qh3QCQyifBfVC9GjtpPvRK787o8jCYk03Evny6SrFnwTTTIRmM9wIhp9J06ttLyRVPkYbjA"
  }, conversation_id="938e9ef6-792e-458c-9447-0c0de1b1c604")
    
    for data in chat.ask(prompt ):
            response = data["message"]


    gpt_response=response

    return



def record_wav():
    form_1 = pyaudio.paInt16
    chans = 1
    samp_rate = 16000
    chunk = 4096
    record_secs = 7

    wav_output_filename = 'input.wav'

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

    return


def record_wavSINO():
    form_1 = pyaudio.paInt16
    chans = 1
    samp_rate = 16000
    chunk = 4096
    record_secs = 3
    
    wav_output_filename = 'input2.wav'

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

    return

def riproduci(text):

	tts = gTTS(text,lang = "it", slow = False)
	tts.save('frase.mp3')
	mixer.init()
	mixer.music.load("frase.mp3")
	mixer.music.play()
	while mixer.music.get_busy():
	   time.wait(100)  # ms

				 

def riproduciMusica(tipo):

	if tipo == "domanda" :
		mixer.music.load("ping.mp3")
		mixer.music.play()	      	    
		while mixer.music.get_busy():
	 	  time.wait(100)  # ms
	if tipo == "attesa" :
		mixer.music.load("wait.mp3")
		mixer.music.play()
	if tipo == "attesa2" :
		mixer.music.load("polka.mp3")
		mixer.music.play()
	if tipo == "continuo" :
		mixer.music.load("banana.mp3")
		mixer.music.play()

def main():

    while True:

        riproduci("Dimme la tua domanda de cucina zio! Se vuoi parlà de altri cazzi, dimme ALTRO!")
        record_wav()
        riproduci("perfetto! ora aspetta che è na carretta!")
        riproduciMusica("attesa2")
        boolAltro=False

        question = speech_to_text("input.wav")
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
               record_wav()     
               riproduci("perfetto! ora aspetta che è na carretta!")
               riproduciMusica("attesa2")
               question = speech_to_text("input.wav")
               #question =  input("Please enter something: ")
               print("Domandona: {0}".format(question))               
               riproduci("Me hai chiesto: "+question+"! benissimo fratè!")


        riproduci("Attendi sennò te sbrocco! Te deve da risponde l'intelligenza artificiale")
        riproduciMusica("attesa")
        asyncio.run(ask_chat_gpt(question+ ". Devi rispondere in stretto dialetto romano però!"))
	#mixer.music.stop()
        print("Risposta: {0}".format(gpt_response)) 
        text_file = open("ricetta.txt", "w")
        text_file.write("Risposta: {0}".format(gpt_response))
        text_file.close()
        if boolAltro==False:
            boll=False;
            frasi = gpt_response.split("\n")
            stoppatutto=False
            

            for frase in frasi:
                  if stoppatutto :
                    break
                  if len(frase) <2 :
                    continue
                  boll=False
               
                    
                  while boll==False:
                      riproduci(frase)
                      
                      if "INGREDIENTI" in frase.upper() or "ISTRUZIONI" in frase.upper() or frase.startswith('-'):
                           break
                      riproduci("Continuo?")
                      record_wavSINO()
                      riproduci("ok!")
                      riproduciMusica("continuo")

                      question2 = speech_to_text("input2.wav")

                      print(question2)
                
                      if question2 == "si" or question2 == "sì" :
                        print("continuo")
                        boll=True
                        
                      if question2 == "fine" or question2 == "stop" :
                            stoppatutto=True
                            break
        else:
            boll=False;
            frasi = gpt_response.split(".")
            stoppatutto=False
            

            for frase in frasi:
                  if stoppatutto :
                    break
                  if len(frase) <2 :
                    continue
                  boll=False
               
                    
                  while boll==False:
                      riproduci(frase)
                      
                    #  if "INGREDIENTI" in frase.upper() or "ISTRUZIONI" in frase.upper() or frase.startswith('-'):
                    #       break
                      riproduci("Continuo?")
                      record_wavSINO()
                      riproduci("ok!")
                      riproduciMusica("continuo")

                      question2 = speech_to_text("input2.wav")

                      print(question2)
                
                      if question2 == "si" or question2 == "sì" :
                        print("continuo")
                        boll=True
                        
                      if question2 == "fine" or question2 == "stop" :
                            stoppatutto=True
                            break



      



if __name__ == "__main__":
    main()

