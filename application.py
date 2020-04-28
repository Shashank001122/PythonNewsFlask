import json
import requests
from flask import Flask, render_template, request, jsonify, send_from_directory
from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException
from collections import Counter
#app = Flask(__name__)
application = app = Flask(__name__)
lines = []
with open('stopwords_en.txt') as f:
    lines = [line.rstrip() for line in f]


@app.route('/')
def index():
    return send_from_directory('static', 'osd.html')


@app.route('/wordcloudd3', methods=['GET'])
def wordcloud():
    newsapi = NewsApiClient(api_key="6c70eb3b2c36455ca87436fecbd77761")
    if request.method == 'GET':
        top_headlines = newsapi.get_top_headlines(
            country='us',
            language='en',
            page_size=30
        )
        mainstring = ""
    myList = []
    for i in top_headlines["articles"]:
        mainstring += i["title"]
    myDict = Counter(mainstring.split())
    for k, v in myDict.items():
        if k.lower() not in lines and k.isalpha():
            myList.append((k, v))
    myList.sort(key=lambda x: x[1], reverse=True)
    return jsonify({'res': myList[0:30]})


@app.route('/mainget', methods=['GET'])
def front():
    newsapi = NewsApiClient(api_key="6c70eb3b2c36455ca87436fecbd77761")
    if request.method == 'GET':
        top_headlines = newsapi.get_top_headlines(
            sources='fox-news,cnn',
            language='en',
        )
        return jsonify({'output2': top_headlines})


@app.route('/maingetimg', methods=['GET'])
def front1():
    newsapi = NewsApiClient(api_key="6c70eb3b2c36455ca87436fecbd77761")
    if request.method == 'GET':
        top_headlines = newsapi.get_top_headlines(
            country='us',
            language='en',
        )
        return jsonify({'output3': top_headlines})


@app.route('/processget', methods=['GET'])
def processget():
    newsapi = NewsApiClient(api_key="6c70eb3b2c36455ca87436fecbd77761")
    if request.method == 'GET':
        query = request.args.get('query')
        sources = request.args.get('sources')
        from_param = request.args.get('from_param')
        to = request.args.get('to')
        if query and sources != 'all' and from_param and to:
            try:
                output1 = newsapi.get_everything(q=query,
                                                 sources=sources,
                                                 from_param=from_param,
                                                 to=to,
                                                 language='en',
                                                 sort_by='publishedAt',
                                                 page_size=30)

                return jsonify({'output': output1})
            except NewsAPIException as err:
                print(err.args)
                return (jsonify({'erroroutput': err.args}))

        elif query and sources == 'all' and from_param and to :
            try:
                output1 = newsapi.get_everything(q=query,
                                                 from_param=from_param,
                                                 sources=None,
                                                 to=to,
                                                 language='en',
                                                 sort_by='publishedAt',
                                                 page_size=30)

                return jsonify({'output': output1})
            except NewsAPIException as err:
                return (jsonify({'erroroutput': err.args}))


@app.route('/sourcesget', methods=['GET'])
def sourceget():
    query = request.args.get('query')
    response = requests.get(
        "http://newsapi.org/v2/sources?apiKey=6c70eb3b2c36455ca87436fecbd77761&category=" + query + "&language=en&country=us")
    data = json.loads(response.text)

    arrid = []
    arrname = []
    for i in data["sources"]:
        arrid.append(i["id"])
        arrname.append(i["name"])
    return(jsonify({"name": arrname, "id": arrid}))


if __name__ == '__main__':
    app.run(debug=True)
