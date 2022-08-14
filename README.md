# 輔助說明
## 實現的功能說明
假設使用者選取到了100個vtx，其中99個vtx的權重**組合**為 [("Spine",1.0)]，只有1個vtx的權重值為 [("Spine",0.5),("Chest",0.5)]，程式能自動判斷出 [("Spine",1.0)] 這組權重是該100個vtx內的**多數權重組合**，並自動將那1個vtx的權重修正成 [("Spine",1.0)]。


----------
## 最終指令需要的資料

```python
# 此指令可以一次修改多個vertex,transformValue可接受一個內含多個tuple(influenceName,weight)組成的list
pm.skinPercent("物件名稱字串", ["vtx[001],"...], transformValue=[("influence名稱",weight數值)...])
```
實際上大概會長這樣
```python
pm.skinPercent("skinCluster1", ["vtx[001]","vtx[002]","vtx[003]"], transformValue=[("Chest",0.1),("Spine1",0.5),("Spine2",0.4)])
```

--------
## vtx_clear_inf_dict的結構說明與由來
我使用迴圈執行兩個方法獲得每個vtx上的Influence名稱與weight數值

`skinCluste()`可以返回vtx上的所有Influence名稱

例如`['Pivot', 'Spine', 'Chest', 'Neck',...]`

`skinPercent()`此方法查詢模式下可以返回所有的weight數值，但不包含Influence名稱

例如`[0.0, 0.2616, 0.33303, 0.23566, 0.0, 0.0, 0.0001,...]`

接下來我必須過濾資料，我不需要weight數值為0的資料，但我不能直接將list內為0的元素刪除，因為這兩個list的長度相同，直接刪除將會打亂順序，無法正確的配對。

如以上方兩個list為例，將會是

|索引|名稱|數值|
|----|----|---|
|0|Pivot|0.0|
|1|Spine|0.2616|
|2|Chest|0.33303|
|3|Neck|0.23566|

所以我選擇先將資料配對，得到紀錄每個vertex含有的Influence名稱與數值，得到以下字典，即使weight是0也包含
```python
#   每個VertexName裡面包含了該檔案內所有的Influence的weight,即使數值是0也包含在內
vtx_all_inf_dict = {
    "VertexName":{"InfluenceName":float,"InfluenceName":float,"InfluenceName":float,"InfluenceName":float,"InfluenceName":float,...},
    "VertexName":{"InfluenceName":float,"InfluenceName":float,"InfluenceName":float,"InfluenceName":float,"InfluenceName":float,...},
    "VertexName":{"InfluenceName":float,"InfluenceName":float,"InfluenceName":float,"InfluenceName":float,"InfluenceName":float,...}...
}
```
實際上會長得像這樣
```python
vtx_all_inf_dict = {
    "vtx[001]":{"Top":0.0564,"L_Arm":0.5561,"Chest":0.0,"Spine1":0.0,"Spine2":0.0,...},
    "vtx[002]":{"Top":0.0564,"L_Arm":0.5561,"Chest":0.0,"Spine1":0.0,"Spine2":0.0,...},
    "vtx[003]":{"Top":0.02556,"L_Arm":0.0255,"Chest":0.05256,"Spine1":0.001,"Spine2":0.0,...},...
    }
```

再來是過濾資訊，我不需要weight為0的資訊，所以我將數值0以外的資訊放到另一個字典，成為真正所需資訊的字典**vtx_clear_inf_dict**

## 找出哪個權重值組合是正確的

出現最多次的組合即是所需要的正確資料，我需要訪問字典內的key(就是vertex)的值，將值轉為字串作為統計用字典**count_dict**的key，次數作為值。

```python
vtx_clear_inf_dict = {
    "vtx[001]":{"Top":0.0564,"L_Arm":0.5561,"Chest":0.0,"Spine1":0.0,"Spine2":0.0,...},
    "vtx[002]":{"Top":0.0564,"L_Arm":0.5561,"Chest":0.0,"Spine1":0.0,"Spine2":0.0,...},
    "vtx[003]":{"Top":0.02556,"L_Arm":0.0255,"Chest":0.05256,"Spine1":0.001,"Spine2":0.0,...},...
    }
# 使用上方的字典組合統計後,得到下方字典
count_dict = {
    '{"Top":0.0564,"L_Arm":0.5561,"Chest":0.0,"Spine1":0.0,"Spine2":0.0,...}':次數,
    '{"Top":0.02556,"L_Arm":0.0255,"Chest":0.05256,"Spine1":0.001,"Spine2":0.0,...}':次數,
    ....
}
 ```   
最後使用`max()`返回正確的組合儲存到變數`get_max_set`

## 找出需要被修正的vertex

因為上面使用`max()`得出的組合，資料型態為字串，為了比對，需要將vtx_clear_inf_dict儲存的**vertex上含有的權重組合**轉成字串，再與get_max_set比對

只要遇到比對成功的組合，就直接從vtx_clear_inf_dict取出該組合，然後`break`

最後只要將資料填入指令即可

## **成果影片**
![說明](https://media.giphy.com/media/gOjNzjy55SonpvcDBP/giphy.gif)


-------------
## 0813下課後的提問
雖然功能已達成，但還是想提問老師

如上述所示，取得資料的過程中已經把資料轉成字串的形式，想知道在python中是否有不依靠套件的方式把資料從字串轉回原本的型態?

例如:
```python
'{"Top":0.0564,"L_Arm":0.5561,"Chest":0.0,"Spine1":0.0,"Spine2":0.0,...}:48'
###轉變回字典
{"Top":0.0564,"L_Arm":0.5561,"Chest":0.0,"Spine1":0.0,"Spine2":0.0,...}':48
```

