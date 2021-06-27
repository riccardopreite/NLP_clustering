from flask import Flask, render_template, flash, request, Response,jsonify,make_response
import os.path
import json
import pandas as pd
import kmeans_clustering_more_sliced
app = Flask(__name__,static_url_path='', static_folder='./')
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'

json_from_server = {}
@app.route('/get_stat')
def get_stat():
    savenewfull()
    calc_stat()
    with open('json/statistics.json') as data_file:
        data_loaded = json.load(data_file)
        return make_response(data_loaded)

@app.route('/calc_stat')
def calc_stat():
    print("calculating statistics...")
    statistic_json = {}
    with open('json/full.json') as data_file:
        data_loaded = json.load(data_file)
        for lat in data_loaded:
            statistic_json[lat] = {}
            for cat in data_loaded[lat]:
                statistic_json[lat][cat] = {}
                for attr in data_loaded[lat][cat]:
                    statistic_json[lat][cat][attr] = {}
                    total = 0
                    for vect in data_loaded[lat][cat][attr][0]:
                        for elem in vect:
                            if type(elem) == type(""):
                                total = total + 1
                                if elem not in statistic_json[lat][cat][attr]:
                                    statistic_json[lat][cat][attr][elem] = 1
                                else:
                                    statistic_json[lat][cat][attr][elem] = statistic_json[lat][cat][attr][elem] + 1
                    for elem in statistic_json[lat][cat][attr]:
                        statistic_json[lat][cat][attr][elem] = (statistic_json[lat][cat][attr][elem] / total) * 100
        print("statistics calulated")

        kmeans_clustering_more_sliced.saveFile(statistic_json,"json/statistics.json")

        # with open('json/statistics.json') as data_file:
        #     data_loaded = json.load(data_file)
        #     return make_response(data_loaded)


def savenewfull():
    i = 0
    json_to_send = {}
    while i < 9:
        with open('json/lat&lon_'+str(i)+'.json') as data_file:
            json_to_send['lat_lon_'+str(i)] = json.load(data_file)

        i = i + 1
    kmeans_clustering_more_sliced.saveFile(json_to_send,"json/full.json")

@app.route('/call')
def call():
    print("start reclustering")
    kmeans_clustering_more_sliced.main()
    print("sending results")
    savenewfull()
    calc_stat()
    with open('json/full.json') as data_file:
        json_from_server["cluster"] = json.load(data_file)
        with open('json/statistics.json') as statistic_file:
            json_from_server["statistics"] = json.load(statistic_file)

            return make_response(json_from_server)



@app.route('/getlat_lon')
def getlat():
    print("sending saved cluster")
    savenewfull()
    calc_stat()
    json_from_server = {}

    with open('json/full.json') as data_file:
        json_from_server["cluster"] = json.load(data_file)
        with open('json/statistics.json') as statistic_file:
            json_from_server["statistics"] = json.load(statistic_file)

            return make_response(json_from_server)


def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)

        return open(src).read()
    except IOError as exc:
        return str(exc)

@app.route('/')
def index():
    content = get_file('html/test.html')
    return Response(content, mimetype="text/html")





def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))
if __name__ == '__main__':
    # json_from_server = kmeans_clustering.clean_main()
    # print("finished")
    app.run(debug=True, port=3000, host='0.0.0.0')
