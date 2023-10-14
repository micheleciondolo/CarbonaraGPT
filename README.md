CarbonaraGPT Interface for Cooking Purposes.
ADDED NAPOLETANO , PUGLIESE, SARDO AND ENGLISH COCKNEY! OMG!


FOR ANY QUESTION CONTACT ME or open issue.



-------------

Cosa serve :

hardware:

    Raspberry Pi 3B minimo ( fa schifo al cazzo, ma funziona)

    Alimentatore da almeno 3A!!

    Cassa bluetooth con microfono tipo questa link: https://www.amazon.it/dp/B0B8X6FLVZ?psc=1&ref=ppx_yo2ov_dt_b_product_details

    tanta pazienza

Software: Se me lo chiedete posso pure passarvi la mia img già installata. Altrimenti vi consiglio:

    Debian 12

    python3

    mpg123

    tutte le liberie python che servono : vosk, gTTs, revChatGPT e via dicendo.

Per prima cosa installate PipeWire e rendetelo il default per la gestione audio sul vostro raspberry (disattivate PulseAudio)
Poi collegate la cassa bluetooth tramite blueman-manager.
tramite "pactl list" dovreste vederla e dovrebbe avere 2 profili audio disponibili: a2dp-sink e headset-head-unit
Se non dovessero chiamarsi così è un casino. 


Poi basta che lanciate il file chatCucina.py (python3 chatCucina.py), vedete se servono altre cose, compilate la sezione settings in alto nel file python e tutto DOVREBBE funzionare. la sezione setttings si compila cosi:
DIALETTO PARLATO = dialetto che deve usare l'AI, non quello che dovete parlare voi, voi potete parlare solo italiano o inglese. Lei può rispondere in romano/napoletano/inglese (cockney)/sardo e pugliese. Scegliete una di queste stringhe e impostatela.
bluetoothCard = nome della scheda bluetooth trovate facendo pactl list , come nome della scheda.
mainFolder = cartella principale all'interno della quale ci sono tutti i file tra cui chatCucina.py 

parlate su telegram con carbonaragpt_bot , poi leggete una guida e ricavatevi:

TELEGRAM_TOKEN e TELEGRAM_CHAT_ID

per chat gpt.. create dal browser una conversazione. Poi ricavatevi Conversation id dal link della conversazione e access token tramite link https://chat.openai.com/api/auth/session quindi compilate ACCESS_TOKEN_CHATGPT e CONVERSATION_ID_CHATGPT

Nella cartella dovete aggiungere la cartella italiana di vosk scaricabile qui https://alphacephei.com/vosk/models/vosk-model-small-it-0.22.zip chiamatela "vosk-model-small-it-0.22". nella cartella di vosk cambiate la configurazione in modo che non sia una vera carretta : beam=1 e riducete la max-active!

IMPORTANTISSIMO: dopo aver installato revChatGPT andate su /usr/local/lib/python3.x/dist-packages/revChatGPT e modificate il file V1.py aggiungendo la seguente stringa dopo le import e le from..

os.environ["CHATGPT_BASE_URL"]="https://ai.fakeopen.com/api/"

altrimenti non funziona una mazza.

mi rendo conto che questa guida è scritta con i piedi, se vi servono ulteriori delucidazioni potete scrivermi su telegram @Luzzo1989.

Buone ricette.

--------------------------------------------------
--------------------------------------------------
--------------------------------------------------

ENGLISH VERSION:

What you need:

Hardware:

    Raspberry Pi 3B at a minimum (it's not great, but it works)
    
    Power supply of at least 3A!!
    
    Bluetooth speaker with a built-in microphone like this one: Link to Amazon
    
    Lots of patience

Software: If you ask, I can provide you with my pre-installed image. Otherwise, I recommend:
    
    Debian 12
    
    Python3
    
    mpg123

    All the necessary Python libraries: vosk, gTTs, revChatGPT, and so on.

First, install PipeWire and make it the default for audio management on your Raspberry Pi (disable PulseAudio). Then, connect the Bluetooth speaker via blueman-manager. By using "pactl list," you should see it, and it should have 2 available audio profiles: a2dp-sink and headset-head-unit. If they are named differently, it's a mess.

Then, just run the file chatCucina.py (python3 chatCucina.py). Check if you need anything else, fill out the settings section at the top of the Python file, and everything SHOULD work. The settings section is filled out as follows:

DIALETTO_PARLATO = the dialect that the AI should use, not the one you should speak. You can only speak Italian or English. It can respond in Roman/Neapolitan/English (Cockney)/Sardinian and Apulian. Choose one of these strings and set it.

bluetoothCard = the name of the Bluetooth card found by running pactl list, as the card's name.

mainFolder = the main folder in which all the files, including chatCucina.py, are located.

Talk on Telegram with carbonaragpt_bot, then read a guide and obtain:

TELEGRAM_TOKEN and TELEGRAM_CHAT_ID

For chat GPT, create a conversation from your browser. Then, get the Conversation ID from the conversation link and access token through the link here. Then, fill in ACCESS_TOKEN_CHATGPT and CONVERSATION_ID_CHATGPT.

In the folder, add the English folder of vosk, which you can download here https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip , and name it "vosk-model-small-en-us-0.15". In the vosk folder, change the configuration so that it's not too strict: set beam=1 and reduce the max-active!

EXTREMELY IMPORTANT: After installing revChatGPT, go to /usr/local/lib/python3.x/dist-packages/revChatGPT and modify the file V1.py by adding the following string after the imports:

os.environ["CHATGPT_BASE_URL"]="https://ai.fakeopen.com/api/"

Otherwise, it won't work at all.

I realize that this guide is not very well-written. If you need further clarification, feel free to write to me on telegram @Luzzo1989

Happy cooking!




--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

For any question don't hesitate and contact me on telegram @Luzzo1989
