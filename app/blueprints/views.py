from __future__ import unicode_literals
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, redirect
from werkzeug.utils import secure_filename
import os
import pac

from subprocess import Popen, PIPE
import youtube_dl
from app.blueprints.forms import *
from app.blueprints.functions import *


def init_app(app):

    def load_user(id):
        return User.query.filter_by(id=id).first()

    @app.route('/')
    def index():
    
        return render_template("home.html")

    
    @app.route('/upload')
    def upload():
        return render_template("upload.html")

    @app.route('/video')
    def video():
        return render_template("video.html")

    @app.route('/uploader', methods=['GET', 'POST'])
    def uploader():
        if request.method == 'POST':
            f = request.files['file']
            f.save('app/static/audio.wav')
            pac.convert_wav_to_16bit_mono("app/static/audio.wav", "app/static/audio.wav")
            return redirect("/")

    @app.route('/extract', methods=['GET', 'POST'])
    def extract():
        link = request.form['musicName']

        ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',  
        }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        return redirect("/")

'''
    @app.route('/acordes', methods=['GET', 'POST'])
    def acordes():

        #idioma = request.form['idiomaSelec']
        #nomemusica = request.form['musicName']
         
        #Separa Instrumental dos Vocais
        separaVocais()

        #Separa os Vocais em Versos
        iteracoes = cortaVocais()
        print("Numero de audios: ", iteracoes)

        #Transcreve vocais com DeepSpeech
        deepTranscreve(iteracoes, idioma)
        
        #Separa Instrumental em Versos
        instrumental = cortaInstrumental()
        
        #Transcreve o acompanhamento
        chordsTranscreve(instrumental)
        
        #Junto tudo em uma Cifra
        formataCifra(nomemusica)
        
        os.chdir('D:/GitHub/ChordsWebApp')
        return send_file('../'+nomemusica+'_cifra.txt', as_attachment=True, cache_timeout=0)
'''

