from flask import Flask, render_template, request, redirect, url_for, flash, send_file, redirect
from werkzeug.utils import secure_filename
import os
import pac

from subprocess import Popen, PIPE
from app.blueprints.forms import *
from app.blueprints.functions import *


def init_app(app):

    def load_user(id):
        return User.query.filter_by(id=id).first()

    @app.route('/')
    def index():
        try: 
            transcricao = open('Lyrics.txt','r')
            transcricao = transcricao.read()
        except:
            transcricao = ""
        return render_template("home.html", transcricao=transcricao)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = loginForm()

        if form.validate_on_submit():
            print(form.username.data)
            print(form.password.data)
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.password == form.password.data:
                login_user(user, remember=form.rememberMe.data)
                flash("Login realizado com Sucesso. Bem-Vindo(a) " + user.name)
                return redirect(url_for('index'))

            else:
                flash("Usuário ou Senha Inválidos.")

        else:
            print(form.errors)

        return render_template("login.html", form=form)

    @app.route("/logout")
    def logout():
        logout_user()
        flash("Logout Realizado.")
        return redirect(url_for('login'))

    @app.route('/solicitacao')
    def solicitacao():
        return render_template("solicitacao.html")
    
    @app.route('/upload')
    def upload():
        return render_template("upload.html")

    @app.route('/uploader', methods=['GET', 'POST'])
    def uploader():
        if request.method == 'POST':
            f = request.files['file']
            f.save('app/static/audio.wav')
            pac.convert_wav_to_16bit_mono("app/static/audio.wav", "app/static/audio.wav")
            return redirect("/")

    @app.route('/transcreve', methods=['GET', 'POST'])
    def transcreve():
        os.system("python app/STT/Vosk/transcribe.py app/static/audio.wav")
        return send_file("../Transcrição.txt", as_attachment=True, cache_timeout=0)
    
    @app.route('/acordes', methods=['GET', 'POST'])
    def acordes():
        #Separa Instrumental dos Vocais
        separaVocais()

        #Separa os Vocais em Versos
        iteracoes = cortaVocais()
        print("Numero de audios: ", iteracoes)

        #Transcreve vocais com DeepSpeech
        deepTranscreve(iteracoes)

        #Separa Instrumental em Versos
        cortaInstrumental()
        
        #Trnascreve o acompanhamento
        chordsTranscreve(iteracoes)

        transcricao = open('Lyrics.txt','r')
        transcricao = transcricao.read()

        return render_template("home.html",transcricao=transcricao)
    
    @app.route('/gravacao', methods=['GET', 'POST'])
    def gravacao():
        return render_template("gravacao.html")
    
    @app.route('/save-record', methods=['POST'])
    def save_record():
        app.logger.debug(request.files['file'].filename) 
        return render_template("gravacao.html")
    
    @app.route('/uploads', methods=['POST'])
    def save_audio():
        rawAudio = request.get_data()
        audioFile = open('RecordedFile.wav', 'wb')
        audioFile.write(rawAudio)
        audioFile.close()
        return speech_to_text()

