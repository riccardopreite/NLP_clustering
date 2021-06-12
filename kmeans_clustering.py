from sklearn.cluster import KMeans
import numpy as np
import csv
import matplotlib.pyplot as plt
from kmodes.kmodes import KModes
import json
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

# #############################################################################

# Generate sample data
# input_file = '/content/drive/MyDrive/yelp_academic_dataset_business.csv'

def prepareData(nparray,coordinate,label,i):
    fullJson = nparray.tolist()
    coordJson = coordinate.tolist()
    labelJson = label.tolist()
    full = {
        'label' : labelJson,
        'data' : coordJson,
        'full' : fullJson
    }
    with open('json_from_server'+str(i)+'.json', 'w') as outfile:
        str_ = json.dumps(full,
                      indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
        outfile.write(to_unicode(str_))
    return full

def clean_main():
    new = [16,49,41,4,5,6,8,9,11,12,13,15,20,22,23,24,25,27,28,30,31,32,33,34,35,36,37,39,43,44,45,46,47,48,51,52,53,54,55,57,58,59]
    business_csv = './yelp_academic_dataset_business.csv'
    cluster = 9
    cluster_attr = 20
    origin,tokenizer = readCsvTokenizing(business_csv,new,"float32")
    kmeans,df,label,u_labels = k(data=origin,cluster=cluster)
    js = {}
    print("starting sub clustering...")
    for i in u_labels:
        if i == 8:
            #do control for reshape to make 1 cluster
            break
        kmeans2,df2,label2,u_labels2 = categoriesk(data=df[label == i],cluster=cluster_attr)
        kmeans2,df2,label2,u_labels2 = attrk(data=df2[label2 == i],cluster=cluster_attr,col=3)
        translated = []
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
        print("finito translating")

        translated = np.asarray(translated)
        js[str(i)] = prepareData(translated,translated[0:,:2],u_labels2,i)

    with open('json_from_server.json', 'w') as outfile:
        str_ = json.dumps(js,
                      indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
        outfile.write(to_unicode(str_))
    return js


def main():
    # latlon = [16,49]
    # attributes = [4,5,6,8,9,11,12,13,15,20,22,23,24,25,27,28,30,31,32,33,34,35,36,37,39,43,44,45,46,47,48,51,52,53,54,55,57,58,59]
    # new = [16,49,4,5,6,8,9,11,12,13,15,20,22,23,24,25,27,28,30,31,32,33,34,35,36,37,39,43,44,45,46,47,48,51,52,53,54,55,57,58,59]

    new = [16,49,41,4,5,6,8,9,11,12,13,15,20,22,23,24,25,27,28,30,31,32,33,34,35,36,37,39,43,44,45,46,47,48,51,52,53,54,55,57,58,59]
    business_csv = './yelp_academic_dataset_business.csv'
    cluster = 9
    cluster_attr = 20
    origin,tokenizer = readCsvTokenizing(business_csv,new,"float32")
    # for key in tokenizer:
    #     temp_cont = len(tokenizer[key])
    #     if temp_cont > cluster_attr:
    #         cluster_attr = temp_cont
    # cluster_attr = int(max/10)
    # print("TOKENI")
    # print(origin)

    kmeans,df,label,u_labels = k(data=origin,cluster=cluster)
    for i in u_labels:
        kmeans2,df2,label2,u_labels2 = categoriesk(data=df[label == i],cluster=cluster_attr)
        kmeans2,df2,label2,u_labels2 = attrk(data=df2[label2 == i],cluster=cluster_attr,col=3)
        translated = []
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
        print("finito translating")

        translated = np.asarray(translated)
        prepareData(translated,label2)
        # index = 0
        # while index < len(translated):
        #     print(translated[index,0])
        #     translated[index,0] = float(translated[index,0])
        #     translated[index,1] = float(translated[index,1])
        #     print(float(translated[index,0]))
        #     index = index + 1
        # print(translated[label2==0])
        toplot = np.asarray(translated[0:,:2],dtype="float32")
        # plotHover(kmeans2,toplot,cluster_attr,label2,u_labels2,translated[0:,2:])
        plot(kmeans2,toplot,cluster_attr,label2,u_labels2)

def k(data,cluster):

    kmeans = KMeans(n_clusters=cluster, init='k-means++', n_init=4,random_state=0, verbose=0)

    # print("INIZIO k")
    # label = kmeans.fit_predict(data)
    label = kmeans.fit_predict(data[0:,:2])
    u_labels = np.unique(label)

    # print("returning k")
    return kmeans,data,label,u_labels

def categoriesk(data,cluster):
    if len(data) < cluster:
        cluster = len(data)
    kmeans = KMeans(n_clusters=cluster, init='k-means++', n_init=5,random_state=0, verbose=0)

    # print("INIZIO categoriesk")
    label = kmeans.fit_predict(data[0:,2].reshape(-1, 1))
    u_labels = np.unique(label)
    # print("returning categoriesk")

    return kmeans,data,label,u_labels

def attrk(data,cluster,col):

    kmeans = KMeans(n_clusters=cluster, init='k-means++', n_init=5,random_state=0, verbose=0)

    # print("INIZIO attrk")
    label = kmeans.fit_predict(data[0:,col:])
    u_labels = np.unique(label)
    # print("returning attrk")

    return kmeans,data,label,u_labels
    # print(data[label==0])
    # print("INMEZZO")
    # print(data[label==1])
    # print("INMEZZO")
    # print(data[label==2])
    # print("INMEZZO")
    #
    # print(data[label==3])
    # print("INMEZZO")
    # print(data[label==4])
    # print("INMEZZO")
    #
    # print(data[label==5])
    # print("INMEZZO")
    #
    # print(data[label==6])
    # print("INMEZZO")
    #
    # print(data[label==7])



def checkDuality(lav,ori):
    unique, counts = np.unique(lav, return_counts=True)
    for i in counts:
        if i > 1:
            print("error")



def plotHover(kmeans,df,cluster,label,u_labels,names):

    #plotting the results:
    print(names)
    fig,ax = plt.subplots()
    c = np.random.randint(1,5,size=len(names))

    norm = plt.Normalize(1,4)
    cmap = plt.cm.RdYlGn
    for i in u_labels:
        sc = plt.scatter(df[label == i , 0] , df[label == i , 1] , label = i)

    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)
    def update_annot(ind):

        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        text = "{}, {}".format(" ".join(list(map(str,ind["ind"]))),
                               " ".join([str(names[n]) for n in ind["ind"]]))
        annot.set_text(text)
        annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
        annot.get_bbox_patch().set_alpha(0.4)


    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = sc.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    print("FINE")
    fig.canvas.mpl_connect("motion_notify_event", hover)
    plt.title("n_cluster: %d" %  cluster)
    plt.legend()
    plt.show()

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
                        # if key == 41:
                        #     string = row[key]
                        #     string = string.replace("'b","")
                        #     string = string.replace("'","")
                        #     stringvect = string.split(',')
                        #     if key not in tokenizer:
                        #         tokenizer[key] = {}
                        #         last_token[key] = 0
                        #     sub = []
                        #     for value in stringvect:
                        #
                        #         if value not in tokenizer[key]:
                        #             if len(tokenizer[key]) == 0:
                        #                 tokenizer[key][value] = 0
                        #             else:
                        #                 tokenizer[key][value] = last_token[key] + 1
                        #                 last_token[key] = last_token[key] + 1
                        #         sub.append(tokenizer[key][value])
                        #     print("DIOCANE")
                        #     print(sub)
                        #     sublist.append(np.asarray(sub))
                        #
                        # else:
                        #     key,tokenizer,last_token = addElement(key,tokenizer,last_token,row)
                        #     sublist.append(tokenizer[key][row[key]])
                        key,tokenizer,last_token = addElement(key,tokenizer,last_token,row)
                        sublist.append(tokenizer[key][row[key]])
                    else:
                        sublist.append(row[key])
                val.append(sublist)

            else:
                i = 1
        val = np.asarray(val)
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
    clean_main()
