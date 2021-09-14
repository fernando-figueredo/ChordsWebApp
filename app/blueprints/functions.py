from urllib.parse import urlparse, parse_qs
import youtube_dl
import os
import pac


# Funções 
def baixaYoutube(link):
    print("Baixando do youtube...")

    #Baixa a música a partir do Youtube ID
    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'wav',
    'preferredquality': '192',  
    }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(link, download=False)
        video_title = info_dict.get('title', None)

    path = f'D:/GitHub/ChordsWebApp/app/static/audio.wav'

    ydl_opts.update({'outtmpl':path})

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

def separaVocais():
#Separa Instrumental dos Vocais
    os.chdir("D:/GitHub/ChordsWebApp/vocal-remover-master/")
    os.system("python inference.py --input D:/GitHub/ChordsWebApp/app/static/audio.wav")
    print("parou!!!")
    print("Vocais separados!")
    os.replace("D:/GitHub/ChordsWebApp/vocal-remover-master/audio_Instruments.wav", "D:/GitHub/ChordsWebApp/audio_Instruments.wav")
    os.replace("D:/GitHub/ChordsWebApp/vocal-remover-master/audio_Vocals.wav", "D:/GitHub/ChordsWebApp/audio_Vocals.wav")
    os.chdir("D:/GitHub/ChordsWebApp")
    
def chordsTranscreve():
    os.chdir("D:/GitHub/ChordsWebApp/")
    #Converte a taxa de amostragem do áudio para 16Kb mono
    pac.convert_wav_to_16bit_mono("D:/GitHub/ChordsWebApp/audio_Instruments.wav", "D:/GitHub/ChordsWebApp/audio_Instruments.wav")
    os.chdir("chords")
    os.system("python split.py D:/GitHub/ChordsWebApp/audio_Instruments.wav")
    os.replace("chords.txt", "D:/GitHub/ChordsWebApp/chords.txt")

def get_id(url):
    u_pars = urlparse(url)
    quer_v = parse_qs(u_pars.query).get('v')
    if quer_v:
        return quer_v[0]
    pth = u_pars.path.split('/')
    if pth:
        return pth[-1]
