from sklearn.cluster import KMeans
import numpy as np
import csv
import matplotlib.pyplot as plt
#from kmodes.kmodes import KModes
import json
import io
import pickle

try:
    to_unicode = unicode
except NameError:
    to_unicode = str

# #############################################################################

# Generate sample data
# input_file = '/content/drive/MyDrive/yelp_academic_dataset_business.csv'
def loadModel(filename):
    return pickle.load(open(filename, 'rb'))

def saveModel(model):
    filename = 'finalized_model.sav'
    pickle.dump(model, open(filename, 'wb'))

def saveFile(data,name):
    with open(name, 'w') as outfile:
        str_ = json.dumps(data,
                      indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
        outfile.write(to_unicode(str_))

def prepareData(nparray,coordinate,label,unique_labels,i):
    fullJson = nparray.tolist()
    coordJson = []
    for lab in unique_labels:
        coordJson.append(coordinate[label == lab].tolist())
    labelJson = unique_labels.tolist()
    full = {
        'label' : labelJson,
        'data' : coordJson,
        'full' : fullJson
    }
    saveFile(full,'json_from_server'+str(i)+'.json')
    return full

def main():
    # new = [16,49,41,4,5,6,8,9,11,12,13,15,20,22,23,24,25,27,28,30,31,32,33,34,35,36,37,39,43,44,45,46,47,48,51,52,53,54,55,57,58,59]
    new = [16,49,4,5,6,8,9,11,12,13,15,20,22,23,24,25,27,28,30,31,32,33,34,35,36,37,39,43,44,45,46,47,48,51,52,53,54,55,57,58,59]
    business_csv = './yelp_academic_dataset_business.csv'
    cluster = 9
    cluster_attr = 25
    origin,tokenizer = readCsvTokenizing(business_csv,new,"float32")
    kmeans,df,label,u_labels = k(data=origin,cluster=cluster)
    js = {}
    print("starting sub clustering...")
    kmeans_sub = KMeans(n_clusters=cluster_attr, init='k-means++', n_init=5,random_state=0, verbose=0)
    kmeans_sub_1 = KMeans(n_clusters=1, init='k-means++', random_state=0, verbose=0)
    for i in u_labels:
        print("start "+str(i)+" cluster")
        if len(df[label == i]) == 1:
            print("1")
            # kmeans2,df2,label2,u_labels2 = categoriesk(kmeans_sub_1,data=df[label == i])

            kmeans2,df2,label2,u_labels2 = attrk(kmeans_sub_1,data=df[label==i],col=2)

        else:

            # kmeans2,df2,label2,u_labels2 = categoriesk(kmeans_sub,data=df[label == i])
            kmeans2,df2,label2,u_labels2 = attrk(kmeans_sub,data=df[label==i],col=2)
        print("end "+str(i)+" cluster")
        translated = []
        js[str(i)] = []
        for elem in df2:
            outtemp=[]
            outtemp.append(float(elem[0]))
            outtemp.append(float(elem[1]))
            init = 2
            while init < len(new):
                for key in tokenizer[new[init]]:
                    if str(tokenizer[new[init]][key]) == elem[init]:
                        temp = key
                        outtemp.append(temp)
                        break
                init = init + 1
            translated.append(outtemp)
        print("finito treanslating cluster " + str(i))
        translated = np.asarray(translated)
        js[str(i)] = prepareData(translated,df2[0:,:2],label2,u_labels2,i)
    saveFile(js,'json_from_server.json')
    saveModel(kmeans_sub)
    return js

def k(data,cluster):

    kmeans = KMeans(n_clusters=cluster, init='k-means++', n_init=4,random_state=0, verbose=0)

    label = kmeans.fit_predict(data[0:,:2])
    u_labels = np.unique(label)

    return kmeans,data,label,u_labels

def categoriesk(model,data):

    label = model.fit_predict(data[0:,2].reshape(-1, 1))
    u_labels = np.unique(label)

    return model,data,label,u_labels

def attrk(model,data,col):

    label = model.fit_predict(data[0:,col:])
    u_labels = np.unique(label)

    return model,data,label,u_labels




def plot(kmeans,df,cluster,label,u_labels):

    #plotting the results:
    for i in u_labels:
        plt.scatter(df[label == i , 0] , df[label == i , 1] , label = i)
    print("FINE")
    plt.title("n_cluster: %d" %  cluster)
    plt.legend()
    plt.show()


def readCsvTokenizing(input_file,column,type):
    with open(input_file, 'r') as inp:
        val = []
        tokenizer = {}
        last_token = {}
        rd = csv.reader(inp)
        cont_token = 0
        i = 0
        for row in rd:
            if i != 0:
                sublist = []
                for key in column:

                    if key != 16 and key != 49:
                        key,tokenizer,last_token = addElement(key,tokenizer,last_token,row)
                        sublist.append(tokenizer[key][row[key]])
                    else:
                        sublist.append(row[key])
                val.append(sublist)

            else:
                i = 1
        val = np.asarray(val)
        saveFile(tokenizer,"tokenizer.json")
        return val,tokenizer

def addElement(key,tokenizer,last_token,row):
    try:
        json_object = json.loads(row[key])
    except ValueError as e:
        if key not in tokenizer:
            tokenizer[key] = {}
            last_token[key] = 1
        if row[key] not in tokenizer[key]:
            if len(tokenizer[key]) == 0:
                tokenizer[key][row[key]] = 1
            else:
                tokenizer[key][row[key]] = last_token[key] + 1
                last_token[key] = last_token[key] + 1
        return key,tokenizer,last_token
    for keyd in json_object:
        key,tokenizer,last_token = addElement(json_object[keyd],tokenizer,last_token,row)
        return key,tokenizer,last_token


if __name__ == "__main__":
    main()
