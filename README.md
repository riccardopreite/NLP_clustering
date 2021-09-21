# Artificial intelligence course project 2020/21
## Natural Language Processing on Yelp dataset

Yelp Dataset is a collection of date from every source about business activity. It consist on 6 different dataset:
* business.json
* review.json
* user.json
* tip.json
* photo.json 
* checkin.json

In this project only **business.json** was used to make a model that can create different cluster based on certain parameters:

* Position (Latitude&Longitude)
* Categories (Restaurant, Bar, ecc)
* Attributes (Accepts credit card, parking, ecc)

## From json to csv
To train the model **Scikit-learn** has been used, especially kmeans clustering. The initial problem was that a json can contain other json inside. A conversion from json to csv
was necessary to create a single column for each possibily key in the json. Yelp leave in the documentation a link to a github repo to convert json to csv and with some examples:
https://github.com/Yelp/dataset-examples






## Clustering

The goal was to obtain different cluster of cluster with this shape:
* Cluster_lat_lon:
  * Cluster_categories:
    - Cluster attributes  

### Position cluster

This was the first partition of the project but this needed just few try to find out the right number of cluster. 
When this number was low distant points were in the same cluster and when the number of cluster was to high it was possible to see some cluster separated that could be only one. 
The number found for the cluster_lat_lon is **9** with a cluster that has only one point because is an outlier.

### Categories and Attributes cluster

Another two subdivision were needed because the hardware used for the training was very limited.
A stable situatuion has been found using **15 categories cluster** and for each one another subclustering is applied for a total number of **4 attributes cluster**. These number were the best approximation due to the poor hardware but it seems to produce decent results.



## Final works

The project is divided in two part:
* A server in python that train the model and host a web site to see the results;
* A JavaScript web site to see on a chart the results and retrain the model.


### To install packages:
```console
smog@maryjane:~$ pip3 install .
```

### To Run server:

```console
smog@maryjane:~$ python3 server.py
```
#### To use front-end view:
  http://localhost:3000/

### To Run only k-means:

```console
smog@maryjane:~$ python3 kmeans_clustering_more_sliced.py
```

# Preview
![testo alt](/foto/home.png "Screenshoot of the results on website")
