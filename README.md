# transcription-verification

To run the transcription verification using docker

```
docker run --name transcription-verification -d -p 5001:5001 \
      -v [local path to wavs and rhasspy jsons]:/data \
      csmyth76/transcription-verification
```
Access the appliction at:
```
http://0.0.0.0:5001/
```

The output file will be written to the local directory that contained the wav and json files.
<br>
<br>
<br>
TODO:
- detect and existing output file so that the process of verifying transcriptions can be stopped and restarted later
- list the files that have been transcribed along with the transcriptions; each item in the list should be a link that will allow the user to edit the transcription
- track words that are commonly changed in the transcription and provided a method to quickly change them in when verifying a transcritpion; this could be an option for auto update (possibly with highlights of the updates) or a button to automatically change them in the transcription 
