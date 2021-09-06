from __future__ import unicode_literals
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
from urllib.parse import urlparse, parse_qs
import os
import pac

from subprocess import Popen, PIPE
import youtube_dl
from app.blueprints.forms import *
from app.blueprints.functions import *

def init_app(app):

    @app.route('/')
    def index():
        return render_template("home.html")

    @app.route('/video', methods=['GET', 'POST'])
    def video():
        return render_template("video.html")

    @app.route('/extract', methods=['GET', 'POST'])
    def extract():

        try:
            os.remove('D:/GitHub/ChordsWebApp/app/static/audio.wav')
        except:
            print ("File not found") 

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
        def get_id(url):
            u_pars = urlparse(url)
            quer_v = parse_qs(u_pars.query).get('v')
            if quer_v:
                return quer_v[0]
            pth = u_pars.path.split('/')
            if pth:
                return pth[-1]
        
        linkid= get_id(link)
        print("ID do Video = ", linkid)
        
        os.chdir('D:/GitHub/ChordsWebApp')

        arquivotxt = open ('chords.txt','r')
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

        #O ultimo sempre entra
        dicAcordes[len(dicAcordes)-1] = dicAcordes[len(dicAcordes)-1].capitalize()
        acordesUnicos.append(dicAcordes[len(dicAcordes)-1])

        #Primeiras e ultiams posicoes como espaços em branco
        acordesUnicos.insert(0,' ')
        acordesUnicos.append(' ')
        
        p=0
        tam=len(dicAcordes)
        print ("Dicionario de acordes: ", dicAcordes)
        print ("Acordes Unicos: ", acordesUnicos )
        print ("Lista Binaria: ", listaBinaria)


        return render_template("video.html", linkid=linkid, listaBinaria=listaBinaria, tam=tam, acordesUnicos=acordesUnicos, p=p)

