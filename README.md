# NetRadio component

This is a new Media_source that allows you to define a set of web radio stations (e.g., http://streams.greenhost.nl:8080/jazz) and then play them from a service call or by using a custom Lovelace card.


To install the Media Source component:
1. Copy __init__.py const.py manifest.json media_source.py to <config>/custom_components/netradio
2. Add a configuration in your configuration.yaml file like this:
  
> netradio:
>   radio: 
>     - url: 'http://streams.greenhost.nl:8080/jazz'
>       name: Concertzender Jazz
>     - url: 'http://icestreaming.rai.it/5.mp3'
>       name: RAI Radio Classica
>     - url: 'http://stream.srg-ssr.ch/m/rsc_de/mp3_128'
>       name: Radio Swiss Classic
>     - url: 'http://wshu.streamguys.org/wshu-classical-mp3'
>       name: WSHU
>     - url: 'https://streams-pfs.kqed.org/kqedradio-pfs?listenerid=cd0bc9c32b46bbe87b06480cabac29f7'
>       name: KQED
>     - url: 'http://kzsu-streams.stanford.edu/kzsu-1-256.mp3'
>       name: KZSU
  

To install the Custom Lovelace card (optional):

1. Copy netradio-card.js to <config>/www directory
2. Add netradio-card.js to your Lovelace resources (you need to activate advanced mode first).


You can play the radios from the Media Browser panel, or fron the Custom Lovelace Card, or by calling a service:

netradio.start_radio

with parameters:
entity_id - the media player to play the radio
radio_index - the number of the radio you want to play, starting from 0, in the list above.

E.g.:
{"entity_id": "media_player.bang_olufsen", "radio_index":0}


