from flask import send_file
from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_silence
from subprocess import Popen, PIPE
import os
import pac


# Funções 
def baixaYoutube():
    print("Baixando do youtube...")

#Baixa a música a partir do Youtube ID


def separaVocais():
#Separa Instrumental dos Vocais
    os.chdir("D:/GitHub/ChordsWebApp/vocal-remover-master/")
    os.system("python inference.py --input D:/GitHub/ChordsWebApp/app/static/audio.wav")
    print("parou!!!")
    print("Vocais separados!")
    os.replace("D:/GitHub/ChordsWebApp/vocal-remover-master/audio_Instruments.wav", "D:/GitHub/ChordsWebApp/audio_Instruments.wav")
    os.replace("D:/GitHub/ChordsWebApp/vocal-remover-master/audio_Vocals.wav", "D:/GitHub/ChordsWebApp/audio_Vocals.wav")
    os.chdir("D:/GitHub/ChordsWebApp")
    
def cortaInstrumental():
    song = AudioSegment.from_wav("audio_Vocals.wav")

    print("Carregou musica!")

    chunks = detect_silence(song, min_silence_len=400, silence_thresh=-45, seek_step=1)

    instrumental = AudioSegment.from_wav("audio_Instruments.wav")
    #lista do instrumental separado
    acomp=[]

    for i in range (len(chunks)):
        for j in range (2):
            if j == 0:
                ji=1 # ji = j invertido
            else:
                ji=0
  
            try:
                #recorta o instrumental referentes aos silencios e aos versos intercaladamente
                acomp.append(instrumental[(chunks[i][j]):(chunks[i+j][ji])])

                print("Exportando instrumental_{0}.wav".format(2*i+j))
                acomp[(2*i)+j].export(
                    "./instrumental/instrumental_{0}.wav".format(2*i+j),
                    bitrate = "16",format = "wav"
                    )
             
            except:
                print("Instrumental Separado!")
    return (2*i+j)

def chordsTranscreve():
    os.chdir("D:/GitHub/ChordsWebApp/")
    #Converte a taxa de amostragem do áudio para 16Kb mono
    pac.convert_wav_to_16bit_mono("D:/GitHub/ChordsWebApp/audio_Instruments.wav", "D:/GitHub/ChordsWebApp/audio_Instruments.wav")
    os.chdir("chords")
    os.system("python split.py D:/GitHub/ChordsWebApp/audio_Instruments.wav")
    os.replace("chords.txt", "D:/GitHub/ChordsWebApp/chords.txt")

def formataCifra(nomemusica):
    os.chdir('D:/GitHub/ChordsWebApp')
    
    try:
        os.remove("cifra_final.txt")
    except:
        print("nada acontece feijoada")

    chords = open ('chords.txt','r')
    chords = chords.read()
    acordes = chords.split('\n')

    #remove acordes iguais consecutivos
    for a in range (len(acordes)):

        acordes[a] = acordes[a].split(' ')

        acordes[a].reverse()
        for z in range(len(acordes[a])-1):
            if acordes[a][z] == acordes[a][z+1]:
                acordes[a][z] = '  '
        acordes[a].reverse()

    lyrics = open ('lyrics.txt','r')
    lyrics = lyrics.read()
    letra = lyrics.split('\n')

    print("LEN letra: " + str(len(letra)))
    print("LEN ACORDES: " + str(len(acordes)))

    #Intercala Cifra e Letra
    cifra = open ('cifra.txt','a')
    cifra.write('\t\t\t\t\tCIFRA: ' + nomemusica)
    cifra.write('\n \n \n')
    cifra.write(str(acordes[0]))
    cifra.write('\n')
    cifra.write('(introdução) \n' + '\n ') 
    for x in range (len(letra)-1):
        cifra = open ('cifra.txt','a')
        cifra.write(' \n ' + str(acordes[2*x+1]) +' ' + str(acordes[2*x+2]))
        cifra.write(' \n ' + letra[x] + '\n')
        cifra.close()

    cifra = open ('cifra.txt','r')
    cifra = cifra.read()

    cifra = cifra.replace("b'","")
    cifra = cifra.replace("'","")
    cifra = cifra.replace("[","")
    cifra = cifra.replace("]","")
    cifra = cifra.replace(",","")
    cifra = cifra.replace("\\n","")

    cifra_f = open(nomemusica + '_cifra.txt', 'w')
    cifra_f.write(cifra)
    cifra_f.close()
    os.remove("cifra.txt")
    
