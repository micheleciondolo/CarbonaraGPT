# CarbonaraGPT
CarbonaraGPT Interface for Cooking Purposes.


Cosa serve :

hardware: 
- Raspberry Pi 3B minimo ( fa  schifo al cazzo, ma funziona)
- Alimentatore da almeno 3A!!
- Cassa bluetooth con microfono tipo questa  link: https://www.amazon.it/dp/B0B8X6FLVZ?psc=1&ref=ppx_yo2ov_dt_b_product_details
- tanta pazienza

  Software:
Se me lo chiedete posso pure passarvi la mia img già installata.
Altrimenti vi consiglio:
- Debian 12
- python3
- mpg123
- tutte le liberie python che servono : vosk, gTTs, revChatGPT e via dicendo.


Basta che lanciate il file chatCucina.py (python3 chatCucina.py), vedete se servono altre cose, compilate la sezione settings in alto nel file python e tutto DOVREBBE funzionare.
la sezione setttings si compila cosi:

bluetoothCard =  nome della scheda bluetooth trovate facendo pactl list , come nome della scheda.
mainFolder = cartella principale all'interno della quale ci sono tutti i file tra cui chatCucina.py
modelFolder = "vosk-model-small-it-0.22"

parlate su telegram con carbonaragpt_bot , poi leggete una guida e ricavatevi:

TELEGRAM_TOKEN  e 
TELEGRAM_CHAT_ID

per chat gpt.. create dal browser una conversazione. 
Poi ricavatevi Conversation id dal link della conversazione e access token tramite link  https://chat.openai.com/api/auth/session
quindi compilate 
ACCESS_TOKEN_CHATGPT e 
CONVERSATION_ID_CHATGPT 


Nella cartella dovete aggiungere la cartella italiana di vosk scaricabile qui https://alphacephei.com/vosk/models/vosk-model-small-it-0.22.zip chiamatela "vosk-model-small-it-0.22".
nella cartella di vosk cambiate la configurazione in modo che non sia una vera carretta : beam=1 e riducete la max-active!



Buone ricette.
