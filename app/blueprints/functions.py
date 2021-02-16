from pydub import AudioSegment
from pydub.silence import split_on_silence
import os


# Funções 
def separaVocais():
#Separa Instrumental dos Vocais
    os.chdir("D:/GitHub/ChordsWebApp/vocal-remover-master/")
    os.system("python inference.py --input D:/GitHub/ChordsWebApp/app/static/audio.wav")
    os.replace("D:/GitHub/ChordsWebApp/vocal-remover-master/audio_Instruments.wav", "D:/GitHub/ChordsWebApp/audio_Instruments.wav")
    os.replace("D:/GitHub/ChordsWebApp/vocal-remover-master/audio_Vocals.wav", "D:/GitHub/ChordsWebApp/audio_Vocals.wav")
    os.chdir("D:/GitHub/ChordsWebApp")
    print("Vocais separados!")
    
def separaVersos():
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
