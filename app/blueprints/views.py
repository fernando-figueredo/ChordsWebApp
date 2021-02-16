from flask import Flask, render_template, request, redirect, url_for, flash, send_file, redirect
from flask_login import login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

from app.ext.auth import lm

from app.blueprints.forms import *
from app.blueprints.functions import *
from app.tables import *


def init_app(app):

    @lm.user_loader
    def load_user(id):
        return User.query.filter_by(id=id).first()

    @app.route('/')
    def index():
        try: 
            transcricao = open('Transcrição.txt','r')
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
    @login_required
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
            return redirect("/")

    @app.route('/transcreve', methods=['GET', 'POST'])
    def transcreve():
        os.system("python app/STT/Vosk/transcribe.py app/static/audio.wav")
        return send_file("../Transcrição.txt", as_attachment=True, cache_timeout=0)
    
    @app.route('/acordes', methods=['GET', 'POST'])
    def acordes():
    #Separa Instrumental dos Vocais
       # os.chdir("D:/GitHub/ChordsWebApp/vocal-remover-master/")
      #  os.system("python inference.py --input D:/GitHub/ChordsWebApp/app/static/audio.wav")
       # os.replace("D:/GitHub/ChordsWebApp/vocal-remover-master/audio_Instruments.wav", "D:/GitHub/ChordsWebApp/audio_Instruments.wav")
      #  os.replace("D:/GitHub/ChordsWebApp/vocal-remover-master/audio_Vocals.wav", "D:/GitHub/ChordsWebApp/audio_Vocals.wav")
      #  os.chdir("D:/GitHub/ChordsWebApp")

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

        return render_template("home.html")
    
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

