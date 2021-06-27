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
                elif str(elem) != '0.0' and str(elem) != '0':
                    if columns[label_index] != "categories_":
                        vect.append(columns[label_index])
                label_index = label_index + 1

            categories_json[cat_key][attr_key][0].append(vect)

    return categories_json



def main():
    #cluster lat lon is right 9 different cluster
    cluster = 9
    cluster_attr = 4
    cluster_categories = 15

        #LAT&LON MODEL
    kmeans = KMeans(n_clusters=cluster, init='k-means++', n_init=4,random_state=0, verbose=0)
        #ATTRIBUTE MODEL
    kmeans_sub_attr = KMeans(n_clusters=cluster_attr, init='k-means++', n_init=3,random_state=0, verbose=0)
        #CATEGORIES MODEL
    kmeans_sub_cate = KMeans(n_clusters=cluster_categories, init='k-means++', n_init=3,random_state=0, verbose=0)
        #ONE ELEMENT MODEL
    kmeans_sub_1 = KMeans(n_clusters=1, init='k-means++', random_state=0, verbose=0)

    business_csv = './yelp_academic_dataset_business.csv'
    np_data, start_categories_index,columns = read_df.read_df(business_csv)
    print("returned data from csv, starting clustering from lat&lon")

    kmeans,df,label,u_labels = k(kmeans,data=np_data,cluster=cluster)
    print("finished clustering from lat&lon")
    del np_data

    print("starting sub clustering...")
    for i in u_labels:
        categories_json = {}
        print("start "+str(i)+" cluster")
        if len(df[label == i]) == 1:
            print("starting categories clustering")
            df_cat,label_cat,u_labels_cat = categoriesk(kmeans_sub_1,data=df[label == i],start_categories_col=start_categories_index)
            for lab in u_labels_cat:
                print("starting attribute sub clustering")
                df_attr,label_attr,u_labels_attr = attrk(kmeans_sub_1,data=df_cat,start_categories_col=start_categories_index)
                print("fixing data, removing 0 value...")
                categories_json = translateCluster(categories_json,lab,u_labels_attr,df_attr,label_attr,columns)
                print("fixed data, ended attribute sub clustering lat&lon: " +str(i) + " categories: " + str(lab))

        else:
            print("starting categories clustering")

            df_cat,label_cat,u_labels_cat = categoriesk(kmeans_sub_cate,data=df[label==i],start_categories_col=start_categories_index)
            for lab in u_labels_cat:
                print("starting attribute sub clustering lat&lon: " +str(i) + " categories: " + str(lab))
                df_attr,label_attr,u_labels_attr = attrk(kmeans_sub_attr,data=df_cat[lab==label_cat],start_categories_col=start_categories_index)
                print("fixing data, removing 0 value...")
                categories_json = translateCluster(categories_json,lab,u_labels_attr,df_attr,label_attr,columns)
                print("fixed data, ended attribute sub clustering lat&lon: " +str(i) + " categories: " + str(lab))

        saveFile(categories_json,"json/lat&lon_"+str(i)+".json")
        categories_json = {}
        print("end "+str(i)+" cluster")
    return True

def k(model,data,cluster):
    #Predict only on first two columns, lat&lon
    label = model.fit_predict(data[0:,:2])
    u_labels = np.unique(label)

    return model,data,label,u_labels

def categoriesk(model,data,start_categories_col):
    #Predict only on last columns, categories
    label = model.fit_predict(data[0:,start_categories_col:])
    u_labels = np.unique(label)

    return data,label,u_labels


def attrk(model,data,start_categories_col):
    #Predict only on middle columns, attributes
    label = model.fit_predict(data[0:,2:start_categories_col])
    u_labels = np.unique(label)

    return data,label,u_labels

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
