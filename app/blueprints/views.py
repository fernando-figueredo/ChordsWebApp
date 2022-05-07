from flask import Flask, render_template, request
from app.blueprints.functions import *
import os
import youtube_dl
import librosa, librosa.display


def init_app(app):

    @app.route('/')
    def index():
        return render_template("home.html")

    @app.route('/extract', methods=['GET', 'POST'])
    def extract():
        
        '''
        try:
            os.remove('D:/GitHub/ChordsWebApp/app/static/audio.wav')
            os.remove('D:/GitHub/ChordsWebApp/chords.txt')
        except:
            print ("File not found") 
        '''
        link = request.form['musicName']

        '''
        #Extrai musica do YouTube
        baixaYoutube(link)
               
        #Separa Instrumental dos Vocais
        separaVocais()

        #Transcreve o acompanhamento
        chordsTranscreve()
        '''       

        #Link
        linkid = 'jAuVIm9zL_c'
        #linkid= get_id(link)
        print("ID do Video = ", linkid)
        
        #Formata os acordes para exibição
        os.chdir('D:/GitHub/ChordsWebApp')

        arquivotxt = open('chords.txt','r')
        arquivotxt = arquivotxt.read()
        arquivotxt = arquivotxt.rstrip('\n')
        dicAcordes = arquivotxt.split(' ')

        acordesUnicos = []
        listaBinaria = []
        for i in range (len(dicAcordes)-1):
            if dicAcordes[i] != dicAcordes[i+1]:
                dicAcordes[i] = dicAcordes[i].capitalize()
                acordesUnicos.append(dicAcordes[i])
                listaBinaria.append('1')
            else:
                listaBinaria.append('0')

        #O ultimo acorde sempre entra
        dicAcordes[len(dicAcordes)-1] = dicAcordes[len(dicAcordes)-1].capitalize()
        acordesUnicos.append(dicAcordes[len(dicAcordes)-1])

        #Primeiras e ultiams posicoes como espaços em branco
        acordesUnicos.insert(0,' ')
        acordesUnicos.append(' ')
        
        p=0
        tam=len(dicAcordes)

        '''
        print ("Dicionario de acordes: ", dicAcordes)
        print ("Acordes Unicos: ", acordesUnicos )
        print ("Lista Binaria: ", listaBinaria)
        '''

        os.chdir("D:/GitHub/ChordsWebApp/")
        x, sr = librosa.load('audio_Instruments.wav')
        tempo, beats = librosa.beat.beat_track(x, sr=sr, start_bpm=60, units='time')
        beats = beats.tolist()

        beatstxt = open('beatstxt.txt', 'w+')
        beatstxt.write(str(beats))

        #criando um ACE patern file
        ACEtxt = open('ACEtxt.txt', 'w+')
        for i in range (len(dicAcordes)):
            ACEtxt.write(str(beats[i]))
            ACEtxt.write('\t')
            ACEtxt.write(str(beats[i+1]))
            ACEtxt.write('\t')
            ACEtxt.write(dicAcordes[i])
            ACEtxt.write('\n')

        return render_template("video.html", linkid=linkid, listaBinaria=listaBinaria, tam=tam, acordesUnicos=acordesUnicos, p=p, beats=beats, tempo=tempo)

