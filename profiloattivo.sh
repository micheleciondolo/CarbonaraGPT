pactl list cards | awk -v RS='' '/bluez/' | awk -F': ' '/Profilo attivo/ { print $2 }'
