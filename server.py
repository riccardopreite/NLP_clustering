from flask import Flask, render_template, flash, request, Response,jsonify,make_response
import os.path
import json
import kmeans_clustering_more_sliced
app = Flask(__name__,static_url_path='', static_folder='./')
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'

json_from_server = {}

@app.route('/call')
def call():
    print("start reclustering")
    kmeans_clustering.main()
    print("sending results")
    with open('json_from_server.json') as data_file:
        data_loaded = json.load(data_file)
        return make_response(data_loaded)

@app.route('/get')
def get():
    print("sending saved cluster")
    with open('json_from_server.json') as data_file:
        data_loaded = json.load(data_file)
        return make_response(data_loaded)

@app.route('/getlat_lon')
def getlat():
    print("sending saved cluster")
    # i = 0
    # json_to_send = {}
    # while i < 9:
    #     with open('lat&lon_'+str(i)+'.json') as data_file:
    #         json_to_send['lat_lon_'+str(i)] = json.load(data_file)
    #
    #     i = i + 1
    # kmeans_clustering_more_sliced.saveFile(json_to_send,"full.json")
    # return make_response(json_to_send)

    with open('full.json') as data_file:
        data_loaded = json.load(data_file)
        return make_response(data_loaded)


@app.route('/getsingle')
def getsingle():
    print("sending saved cluster 7")
    with open('json_from_server7.json') as data_file:
        data_loaded = json.load(data_file)
        return make_response(data_loaded)

@app.route('/gettokenizer')
def gettokenizer():
    print("sending tokenizer dict")
    with open('tokenizer.json') as data_file:
        data_loaded = json.load(data_file)
        return make_response(data_loaded)




@app.route('/')
def index():
    content = get_file('test.html')
    return Response(content, mimetype="text/html")


    def get_file(filename):  # pragma: no cover
        try:
            src = os.path.join(root_dir(), filename)

            return open(src).read()
        except IOError as exc:
            return str(exc)


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))
if __name__ == '__main__':
    # json_from_server = kmeans_clustering.clean_main()
    # print("finished")
    app.run(debug=True, port=3000, host='0.0.0.0')
