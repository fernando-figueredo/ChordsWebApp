# ChordsWebApp
 Web Application to automatic musical Chords and Lyrics Transcription
 ---
 
 ## Enviroment
Python 3.8.5

```bash
pip install -r requirements.txt
```

## Running

```bash
flask run #runs app
```
Open in a Web browser
Website: http://localhost:5000


## Screenshots

Homepage:
![chordswebapp1](https://user-images.githubusercontent.com/45243859/133005967-449d9182-e4c2-4ae5-8eae-688bb76eebb3.PNG)

Transcription Page:
![chordswebapp2](https://user-images.githubusercontent.com/45243859/133005969-e95e48ee-6621-49f2-902c-a77e997c99bf.PNG)

## Structure
```bash
─Transcrição de áudio
│   ├───app
│   ├───blueprints
│   │   └───__pycache__
│   ├───ext
│   │   └───__pycache__
│   ├───static
│   │   ├───css
│   │   └───images
│   ├───STT
│   │   └───Vosk
│   ├───templates
│   └───__pycache__
└───model
    └───ivector
```
