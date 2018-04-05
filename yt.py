from flask import Flask, request, redirect
from flask_restful import Resource, Api, reqparse
import youtube_dl
import os

app = Flask(__name__)
api = Api(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    return response

class ICY(Resource):
    def get(self):
        return "Hello World!"

class YTD(Resource):
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('ytd', type=str)
        res = parser.parse_args()
        url = res.ytd

        ydl = youtube_dl.YoutubeDL({'outtmpl': "%(uploader)s-%(title)s.%(ext)s"})

        with ydl:
            result = ydl.extract_info(url, download=True)
        fn = ydl.prepare_filename(result)

        if 'entries' in result:
            video = result['entries'][0]
        else:
            video = result

        if os.path.exists(fn):
            fn = fn
        elif os.path.exists(os.path.splitext(fn)[0] + '.mkv'):
            fn = os.path.splitext(fn)[0] + '.mkv'
        else:
            fn = "Error: file doesn't exist"

        metadata = {'title': video['title'], 'uploader': video['uploader'],
                    'webpage url': video['webpage_url'], 'file name': fn}

        return metadata


api.add_resource(YTD, '/api', endpoint='api')
api.add_resource(ICY, '/')

if __name__ == '__main__':
    app.run()
