from sklearn.cluster import KMeans
import numpy as np
import csv
import matplotlib.pyplot as plt
import read_df
# import pandas as pd
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

# def translateCluster(categories_json,lab,u_labels_attr,df_attr,label_attr,columns):
#     cat_key = "categories_"+str(lab)
#     categories_json[cat_key] = {}
#
#     for attribute_cluster in u_labels_attr:
#         attr_key = "attribute_"+str(attribute_cluster)
#         categories_json[cat_key][attr_key] = []
#         top_index = 0
#         temp = df_attr[attribute_cluster == label_attr].tolist()
#         for row in temp:
#             label_index = 0
#             for elem in row:
#                 categories_json[cat_key][attr_key].append([])
#                 if label_index < 2:
#                     categories_json[cat_key][attr_key][top_index].append(elem)
#                 elif elem != 0 and elem != '0':
#                     if columns[label_index] != "categories_":
#                         categories_json[cat_key][attr_key][top_index].append(columns[label_index])
#
#                 label_index = label_index + 1
#             top_index = top_index + 1
#     return categories_json

def translateCluster(categories_json,lab,u_labels_attr,df_attr,label_attr,columns):
    cat_key = "categories_"+str(lab)
    categories_json[cat_key] = {}

    for attribute_cluster in u_labels_attr:
        attr_key = "attribute_"+str(attribute_cluster)
        categories_json[cat_key][attr_key] = []
        temp = df_attr[attribute_cluster == label_attr].tolist()
        categories_json[cat_key][attr_key].append([])
        for row in temp:
            label_index = 0
            vect = []
            for elem in row:
                if label_index < 2:
                    vect.append(elem)
                elif elem != 0 and elem != '0':
                    if columns[label_index] != "categories_":
                        vect.append(columns[label_index])
                label_index = label_index + 1

            categories_json[cat_key][attr_key][0].append(vect)

    return categories_json


def preparenewData(nparray,label,unique_labels,latlon_cluster,cat_cluster):
    fullJson = []
    for lab in unique_labels:
        fullJson.append(nparray[label==lab].tolist())
    labelJson = unique_labels.tolist()
    full = {
        'label' : labelJson,
        'full' : fullJson
    }
    saveFile(full,'json_from_server_'+str(latlon_cluster)+'_'+str(cat_cluster)+'.json')
    return full




def main():

    cluster = 9
    cluster_attr = 5
    cluster_categories = 15
    business_csv = './yelp_academic_dataset_business.csv'


    # np_data, origin_df,start_categories_index,columns = read_df.read_df(business_csv)
    np_data, start_categories_index,columns = read_df.read_df(business_csv)


    print("returned data from csv, starting clustering from lat&lon")
    kmeans,df,label,u_labels = k(data=np_data,cluster=cluster)
    del np_data
    print("finished clustering from lat&lon")

    js = {}
    print("starting sub clustering...")
    kmeans_sub_attr = KMeans(n_clusters=cluster_attr, init='k-means++', n_init=3,random_state=0, verbose=0)
    kmeans_sub_cate = KMeans(n_clusters=cluster_categories, init='k-means++', n_init=3,random_state=0, verbose=0)
    kmeans_sub_1 = KMeans(n_clusters=1, init='k-means++', random_state=0, verbose=1)

    df_cat,label_cat,u_labels_cat = categoriesk(kmeans_sub_1,data=df[label == 8],col=start_categories_index)


    for i in u_labels:

        print("start "+str(i)+" cluster")
        if len(df[label == i]) == 1:
            print("1")
            print("starting categories clustering")

            df_cat,label_cat,u_labels_cat = categoriesk(kmeans_sub_1,data=df[label == i],col=start_categories_index)

            categories_json = {}
            for lab in u_labels_cat:
                print("starting attribute sub clustering")
                df_attr,label_attr,u_labels_attr = attrk(kmeans_sub_1,data=df_cat,col=start_categories_index)
                print("fixing data, removing 0 value...")
                categories_json = translateCluster(categories_json,lab,u_labels_attr,df_attr,label_attr,columns)

            saveFile(categories_json,"lat&lon_"+str(i)+".json")

        else:
            print("starting categories clustering")

            df_cat,label_cat,u_labels_cat = categoriesk(kmeans_sub_cate,data=df[label==i],col=start_categories_index)

            categories_json = {}
            for lab in u_labels_cat:
                print("starting attribute sub clustering lat&lon: " +str(i) + " categories: " + str(lab))
                df_attr,label_attr,u_labels_attr = attrk(kmeans_sub_attr,data=df_cat[lab==label_cat],col=start_categories_index)
                print("fixing data, removing 0 value...")
                categories_json = translateCluster(categories_json,lab,u_labels_attr,df_attr,label_attr,columns)
                print("fixed data, ended attribute sub clustering lat&lon: " +str(i) + " categories: " + str(lab))
            saveFile(categories_json,"lat&lon_"+str(i)+".json")
            # categories_json = {}


        print("end "+str(i)+" cluster")
    return js

def k(data,cluster):

    kmeans = KMeans(n_clusters=cluster, init='k-means++', n_init=4,random_state=0, verbose=0)

    label = kmeans.fit_predict(data[0:,:2])
    u_labels = np.unique(label)

    return kmeans,data,label,u_labels

def categoriesk(model,data,col):
    if len(data) == 1:
        model = KMeans(n_clusters=1, init='k-means++', n_init=3,random_state=0, verbose=0)
    label = model.fit_predict(data[0:,col:])
    u_labels = np.unique(label)

    return data,label,u_labels


def attrk(model,data,col):
    if len(data) == 1:
        model = KMeans(n_clusters=1, init='k-means++', n_init=3,random_state=0, verbose=0)
    label = model.fit_predict(data[0:,2:col])
    u_labels = np.unique(label)

    return data,label,u_labels

def oldcategoriesk(model,data):

    label = model.fit_predict(data[0:,2].reshape(-1, 1))
    u_labels = np.unique(label)

    return model,data,label,u_labels

def oldattrk(model,data,col):

    label = model.fit_predict(data[0:,col:])
    u_labels = np.unique(label)

    return model,data,label,u_labels




def plot(df,cluster,label,u_labels):

    #plotting the results:
    for i in u_labels:
        plt.scatter(df[label == i , 0] , df[label == i , 1] , label = i)
    print("FINE")
    plt.title("n_cluster: %d" %  cluster)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
