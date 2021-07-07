from __future__ import unicode_literals
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, redirect
from werkzeug.utils import secure_filename
from urllib.parse import urlparse, parse_qs
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

    @app.route('/video', methods=['GET', 'POST'])
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
        try:
            os.remove('D:/GitHub/ChordsWebApp/app/static/audio.wav')
        except:
            print ("File not found") 

        link = request.form['musicName']

        #Extrai musica do YouTube
        baixaYoutube()

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
        
        #Separa Instrumental dos Vocais
        separaVocais()

        #Transcreve o acompanhamento
        chordsTranscreve()

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
        return render_template("video.html", linkid=linkid)

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
        chordsTranscreve()
        
        #Junto tudo em uma Cifra
        formataCifra(nomemusica)
        
        os.chdir('D:/GitHub/ChordsWebApp')
        return send_file('../'+nomemusica+'_cifra.txt', as_attachment=True, cache_timeout=0)
'''
