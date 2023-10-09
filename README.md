<<<<<CarbonaraGPT Interface for Cooking Purposes.

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

Basta che lanciate il file chatCucina.py (python3 chatCucina.py), vedete se servono altre cose, compilate la sezione settings in alto nel file python e tutto DOVREBBE funzionare. la sezione setttings si compila cosi:

bluetoothCard = nome della scheda bluetooth trovate facendo pactl list , come nome della scheda. mainFolder = cartella principale all'interno della quale ci sono tutti i file tra cui chatCucina.py modelFolder = "vosk-model-small-it-0.22"

parlate su telegram con carbonaragpt_bot , poi leggete una guida e ricavatevi:

TELEGRAM_TOKEN e TELEGRAM_CHAT_ID

per chat gpt.. create dal browser una conversazione. Poi ricavatevi Conversation id dal link della conversazione e access token tramite link https://chat.openai.com/api/auth/session quindi compilate ACCESS_TOKEN_CHATGPT e CONVERSATION_ID_CHATGPT

Nella cartella dovete aggiungere la cartella italiana di vosk scaricabile qui https://alphacephei.com/vosk/models/vosk-model-small-it-0.22.zip chiamatela "vosk-model-small-it-0.22". nella cartella di vosk cambiate la configurazione in modo che non sia una vera carretta : beam=1 e riducete la max-active!

IMPORTANTISSIMO: dopo aver installato revChatGPT andate su /usr/local/lib/python3.x/dist-packages/revChatGPT e modificate il file V1.py aggiungendo la seguente stringa dopo le import e le from..

os.environ["CHATGPT_BASE_URL"]="https://ai.fakeopen.com/api/"

altrimenti non funziona una mazza.

mi rendo conto che questa guida è scritta con i piedi, se vi servono ulteriori delucidazioni potete scrivermi sul forum.

Buone ricette.

--------------------------------------------------
--------------------------------------------------
--------------------------------------------------



Here are the translated instructions in English:

What you need:

Hardware:

    Raspberry Pi 3B minimum (it's not great, but it works).
    Power supply of at least 3A!!
    Bluetooth speaker with a microphone, like this one: link.
    Lots of patience.

Software:

If you ask me, I can even pass you my pre-installed image. Otherwise, I recommend:

    Debian 12
    Python 3
    mpg123
    All the Python libraries you need: vosk, gTTs, revChatGPT, and so on.

Just launch the file chatCucina.py (python3 chatCucina.py), see if you need anything else, fill out the settings section at the top of the Python file, and everything SHOULD work. The settings section is filled out like this:

    bluetoothCard = the name of the Bluetooth card found by running pactl list as the card name.
    mainFolder = the main folder where all the files, including chatCucina.py, are located.
    modelFolder = "vosk-model-small-it-0.22"

Chat on Telegram with carbonaragpt_bot, then read a guide and get:

    TELEGRAM_TOKEN and TELEGRAM_CHAT_ID

For Chat GPT, create a conversation in your browser. Then, get the Conversation ID from the conversation link and the Access Token through the link here. Then fill out ACCESS_TOKEN_CHATGPT and CONVERSATION_ID_CHATGPT.

In the folder, add the Italian folder of Vosk, which you can download here link, and name it "vosk-model-small-it-0.22". In the Vosk folder, change the configuration so it's not too heavy: beam=1 and reduce max-active!

VERY IMPORTANT: After installing revChatGPT, go to /usr/local/lib/python3.x/dist-packages/revChatGPT and modify the V1.py file by adding the following string after the imports and from statements:



os.environ["CHATGPT_BASE_URL"]="https://ai.fakeopen.com/api/"

Otherwise, it won't work at all.

I realize that this guide is written a bit roughly. If you need further clarification, you can write to me on the forum.

Happy cooking!
