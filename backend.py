from flask import Flask, request, render_template, send_file
from pytube import YouTube
from moviepy.editor import AudioFileClip
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    try:
        yt = YouTube(url)
        video_stream = yt.streams.filter(only_audio=True).first()
        video_file = video_stream.download(filename='temp.mp4')

        # MP4 dosyasını MP3 formatına dönüştür
        video_clip = AudioFileClip(video_file)
        mp3_file = 'output.mp3'
        video_clip.write_audiofile(mp3_file)
        video_clip.close()
        os.remove(video_file)

        return send_file(mp3_file, as_attachment=True)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
