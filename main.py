# Dependencies and Setup
import pandas as pd
import numpy as np
import sys
from functools import reduce
from collections import OrderedDict, Counter

# Raw data file
file_to_load = "Resources/purchase_data.csv"

# Read purchasing file and store into pandas data frame
purchase_data = pd.read_csv(file_to_load)
purchase_data=pd.DataFrame(purchase_data)
print(purchase_data.head())

print(purchase_data.columns)
#print(purchase_data["Item Name"])
#print(type(purchase_data),purchase_data.count)

### Total Number of Players:
print("### Total Number of Players:")
total_players=pd.DataFrame({"Total Players":purchase_data['SN'].unique().shape[0]},index=["T"])
print(total_players)
### Purchasing Analysis (Total):
print("### Purchasing Analysis (Total):")
column_names=["Number of Unique Items","Average Price","Number of Purchases","Total Revenue"]
values=[purchase_data["Item ID"].unique().shape[0],\
         purchase_data["Price"].mean(),\
                purchase_data.shape[0],\
                   purchase_data["Price"].sum()   \
                      ]
aa=[{column_names[i]:values[i] for i in range(4)} ]
#print(aa)
Purchasing_Analysis_Total=pd.DataFrame(aa)
Purchasing_Analysis_Total.rename(index={0:"T"},inplace=True)
pd.set_option('precision',2)
print(Purchasing_Analysis_Total)
###Gender Demographics:
print("###Gender Demographics:")
Gender_data=purchase_data[['SN','Age','Gender']].drop_duplicates() # value_counts()
tot=Gender_data.shape[0]
Gender_data1=Gender_data.groupby("Gender").count()
Gender_data1.rename(columns={"SN":"count","Age":"percentage"},inplace=True)
Gender_data1["percentage"]=Gender_data1["count"]/tot
Gender_data1["percentage"] = pd.Series(["{0:.2f}%".format(val * 100) for val in Gender_data1["percentage"]], index = Gender_data1["percentage"].index)
print(Gender_data1)
###Purchasing Analysis (Gender):
print("###Purchasing Analysis (Gender): ('Average Purchase Total per Person by Gender' is abreviated as 'APTpP_Gender')")
Purchase_Gender=purchase_data.groupby(['Gender'])
Gender_groups_count=purchase_data.groupby(['Gender','SN']).size().groupby('Gender').count()
column_names=["PurchaseCount","AveragePrice","TotalValue","APTpP_Gender"]
values=[Purchase_Gender["Purchase ID"].count(),\
         Purchase_Gender["Price"].mean(),\
                Purchase_Gender["Price"].sum(),\
                   Purchase_Gender["Price"].sum()/Gender_groups_count ]
#values=Series.to_frame
values=[value.to_frame() for value in values]
#pd.concat combine list of data_frames to a bigger DataFrame: 
# https://stackoverflow.com/questions/44327999/python-pandas-merge-multiple-dataframes
df_merged_gender = reduce(lambda  left,right: pd.merge(left,right,left_index=True,right_index=True), values)
df_merged_gender.columns=column_names
print(df_merged_gender)         

###Age Demographics
print("###Age Demographics:('Average Purchase Total per Person by Age Group' is abbreviated as 'APTpP_Age')")
age_bins = [0, 9.90, 14.90, 19.90, 24.90, 29.90, 34.90, 39.90, 99999]
group_names = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

purchase_data["Age group"]=pd.cut(purchase_data["Age"],age_bins,labels=group_names)
purchase_age=purchase_data.groupby(["Age group"])
age_groups_count=purchase_data.groupby(["Age group","SN"]).size().groupby("Age group").count()

del values
values=[purchase_age["Purchase ID"].count(),\
         purchase_age["Price"].mean(),\
                purchase_age["Price"].sum(),\
                   purchase_age["Price"].sum()/age_groups_count ]
values=[value.to_frame() for value in values]
df_merged_age = reduce(lambda  left,right: pd.merge(left,right,left_index=True,right_index=True), values)
df_merged_age.columns=column_names
df_merged_age.rename(columns={"APTpP_Gender":"APTpP_Age"},inplace=True)
#df_merged["APTpP_Age"]=purchase_age["Price"].sum()/age_groups_count
print(df_merged_age)

###Top Spenders
print("###Top Spenders:")
Purchase_spender=purchase_data.groupby("SN")
Top_spenders=Purchase_spender["Price"].sum().sort_values(ascending=False)[0:5]

del values
values=[]
for i in range(5):
    #https://stackoverflow.com/questions/22691010/how-to-print-a-groupby-object
   ss=Purchase_spender.get_group(Top_spenders.index[i])["Price"]
   values.append({"Purchase Count":ss.count(),"Average Purchase Price":ss.mean(),"Total Purchase Value":ss.sum()})

df_merged_Top_Spenders=pd.DataFrame(values,index=Top_spenders.index)

print(df_merged_Top_Spenders)


###Most Popular Items
print("###Most Popular Items:")
Purchase_item=purchase_data.groupby("Item ID")
Top_items=Purchase_item["Purchase ID"].count().sort_values(ascending=False)[0:5]
del values
values=[]
for i in range(5):
    #https://stackoverflow.com/questions/22691010/how-to-print-a-groupby-object
   ss=Purchase_item.get_group(Top_items.index[i])["Price"]
   ss0=Purchase_item.get_group(Top_items.index[i])["Item Name"]
   ##align the dictionary and produece ordered DataFrame
   #https://stackoverflow.com/questions/44365209/generate-a-pandas-dataframe-from-ordereddict?rq=1
   values.append(OrderedDict({"Item Name":ss0.values[0],"Purchase Count":ss.count(),"item Price":ss.values[0],"TotalPurchaseValue":ss.sum()}))   

col = Counter()
for k in values:
    col.update(k)
df_merged_Top_Items=pd.DataFrame(values,index=Top_items.index,columns=col.keys())
print(df_merged_Top_Items)


###Most Profitable Items
print("###Most Profitable Items")
Purchase_item=purchase_data.groupby("Item ID")
Top_items=Purchase_item["Price"].sum().sort_values(ascending=False)[0:5]
del values
values=[]
for i in range(5):
    #https://stackoverflow.com/questions/22691010/how-to-print-a-groupby-object
   ss=Purchase_item.get_group(Top_items.index[i])["Price"]
   ss0=Purchase_item.get_group(Top_items.index[i])["Item Name"]
   ##align the dictionary and produece ordered DataFrame
   #https://stackoverflow.com/questions/44365209/generate-a-pandas-dataframe-from-ordereddict?rq=1
   values.append(OrderedDict({"Item Name":ss0.values[0],"Purchase Count":ss.count(),"item Price":ss.values[0],"TotalPurchaseValue":ss.sum()}))   
col = Counter()
for k in values:
    col.update(k)
df_merged_Top_Items=pd.DataFrame(values,index=Top_items.index,columns=col.keys())
print(df_merged_Top_Items)

#print(Purchase_Gender["Price"].sum())
#in addition to the .drop_duplicates(which can be labelled (1)) method, 
#there are other ways to calculate Gender-population,here are two ways:
#(2): aa=Purchase_Gender['SN'].unique()
#     Gender_population2=pd.Series([len(s) for s in aa],index=aa.index) 
#(3): Gender_population3=purchase_data.groupby(['Gender','SN']).size().groupby('Gender').count()
########### Age Demographics################





