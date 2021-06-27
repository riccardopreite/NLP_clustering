import pandas as pd
import numpy as np
import json
try:
    to_unicode = unicode
except NameError:
    to_unicode = str



# df.replace(np.nan, '', regex=True) #this code will replace all the nan (Null) values with an empty string for the entire dataframe


def saveFile(data,name):
    with open(name, 'w') as outfile:
        # str_ = json.dumps(data,
        #               indent=4, sort_keys=True,
        #               separators=(',', ': '), ensure_ascii=False)
        outfile.write(to_unicode(data))

def dummy_encoding(encoded,data,name):
    if name == "latitude" or name == "longitude":
        print(name)
        encoded = pd.concat([encoded, data], axis=1)
    elif type(data) == pd.core.frame.DataFrame:
        for key in data:
            encoded = dummy_encoding(encoded,data[key],key)
    else:
        data = cleanData(pd.DataFrame(data),name)
        temp_df = pd.get_dummies(data,prefix=name)
        encoded = pd.concat([encoded, temp_df], axis=1)

        print("finish encoding " + str(name))

    return encoded


def cleanData(data,name):
    temp_data = []
    for index in data.index:

        temp = data.loc[index,name].replace("b'","")
        temp = temp.replace('b"',"")
        temp = temp.replace(' ',"")
        temp = temp[:-1].split(",")
        temp_data.append(temp)

    lent = range(0, len(temp_data))
    data = pd.DataFrame(data=temp_data,index=lent)
    data = data.fillna('')
    return data


def read_df(csv_file):
    df_full = pd.read_csv(csv_file)
    key_to_remove = ['business_id', 'name','address','city','state','postal_code','stars','review_count','is_open','hours','attributes']
    position_df = pd.concat([df_full["longitude"], df_full["latitude"]],axis=1)

    df = df_full.drop(key_to_remove, axis=1)
    length = len(df.index)

    temp = df.isna().sum()
    items = temp.items()
    for tupla in items:
        key = tupla[0]
        value = tupla[1]
        # print(length-value)
        if(length-value < 50000):
            df = df.drop(key, axis=1)

    df = df.drop("hours.Monday", axis=1)
    df = df.drop("hours.Tuesday", axis=1)
    df = df.drop("hours.Wednesday", axis=1)
    df = df.drop("hours.Thursday", axis=1)
    df = df.drop("hours.Friday", axis=1)
    df = df.drop("hours.Saturday", axis=1)
    df = df.drop("hours.Sunday", axis=1)
    df = df.drop("attributes.WiFi", axis=1)
    df = df.drop("attributes.BikeParking", axis=1)
    cat = df.pop("categories")
    df["categories"] = cat

    print("START ENCODING ATTRIBUTES & CATEGORIES, COLUMNS TO ENCODE: "+ str(df.columns))
    df = df.fillna('')
    attr = pd.DataFrame()
    attr = pd.DataFrame(dummy_encoding(attr,df,""))

    print("FINISHED DUMMY_ENCODING, PRINTING ATTRIBUTES & CATEGORIES...")
    print(attr.info())

    print("CHECKING FOR NULL VALUE...")
    nan_encoded = attr.isna().sum()
    items = nan_encoded.items()
    for tupla in items:
        if(tupla[1] > 0):
            print("ERROR")
    print("FINISHED CHECKING")


    lat_column = attr.pop('latitude')
    lon_column = attr.pop('longitude')

    attr.insert(0, 'latitude', lat_column)
    attr.insert(0, 'longitude', lon_column)
    print("inserted column")
    column = attr.iteritems()
    print(attr.columns)
    i = 0
    for name, values in column:
    # for key in column:
        if "categories" in name:
            break
        i = i + 1
    print("categories index start from " + str(i))
    return attr.values,i,attr.columns

if __name__ == "__main__":
    business_csv = './yelp_academic_dataset_business.csv'
    read_df(business_csv)
