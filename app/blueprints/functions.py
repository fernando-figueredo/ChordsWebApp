from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_silence
from subprocess import Popen, PIPE
import os


# Funções 
def separaVocais():
#Separa Instrumental dos Vocais
    os.chdir("D:/GitHub/ChordsWebApp/vocal-remover-master/")
    os.system("python inference.py --input D:/GitHub/ChordsWebApp/app/static/audio.wav")
    print("parou!!!")
    print("Vocais separados!")
    os.replace("D:/GitHub/ChordsWebApp/vocal-remover-master/audio_Instruments.wav", "D:/GitHub/ChordsWebApp/audio_Instruments.wav")
    os.replace("D:/GitHub/ChordsWebApp/vocal-remover-master/audio_Vocals.wav", "D:/GitHub/ChordsWebApp/audio_Vocals.wav")
    os.chdir("D:/GitHub/ChordsWebApp")
    
    
def cortaVocais():
    #Separa os Vocais por Versos
    # Define a function to normalize a chunk to a target amplitude.
    def match_target_amplitude(aChunk, target_dBFS):
        ''' Normalize given audio chunk '''
        change_in_dBFS = target_dBFS - aChunk.dBFS
        return aChunk.apply_gain(change_in_dBFS)

    # Load your audio.  
    song = AudioSegment.from_wav("audio_Vocals.wav")

    chunks = split_on_silence (
        # Use the loaded audio.
        song, 
        # Specify that a silent chunk must be at least or 200 ms long.
        min_silence_len = 400,
        # Consider a chunk silent if it's quieter than -40 dBFS.
        silence_thresh = -45
    )

    # Process each chunk with your parameters
    for i, chunk in enumerate(chunks):
        # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
        silence_chunk = AudioSegment.silent(duration=500)

        # Add the padding chunk to beginning and end of the entire chunk.
        audio_chunk = silence_chunk + chunk + silence_chunk

        # Normalize the entire chunk.
        normalized_chunk = match_target_amplitude(audio_chunk, -20.0)

        # Export the audio chunk with new bitrate.
        print("Exporting verso_{0}.wav".format(i))
        normalized_chunk.export(
            ".//versos/verso_{0}.wav".format(i),
            bitrate = "64",
            format = "wav"
        )
    print("Versos separados!")
    return (i)

def deepTranscreve(i):
    os.chdir("D:/GitHub/ChordsWebApp/")
    for j in range(i):
        stdout= Popen("deepspeech --model deepspeech/deepspeech-0.9.3-models.pbmm --scorer deepspeech/deepspeech-0.9.3-models.scorer --audio versos/verso_" + str(j) + ".wav", shell=True, stdout=PIPE).stdout
        output=stdout.read()
        print(output)
        with open("Lyrics.txt", "a+") as text_file:
            text_file.write("\n" + str(output))
    print("Transcrição dos vocais finalizada!")
    try: 
        transcricao = open('Lyrics.txt','r')
        transcricao = transcricao.read()
    except:
        transcricao = ""

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