import operator
import pymel.core as pm


vtx_all_inf_dict = {}  # 每個vtx包含所有影響權重值的字典
vtx_clear_inf_dict = {}  # 過濾完後最後需要被處裡的字典

selected_point = pm.filterExpand(sm=31)  # 批次取得選到的vtx名稱
get_history = pm.listHistory(selected_point, lv=0)  # 讀取歷史紀錄
selected_skin = pm.ls(get_history, type="skinCluster")  # 取得skinCluster名稱

##=========獲取乾淨權重字典區塊=============##

for one_vtx in selected_point:
    temp_dict = {}  # 每次配對InfluenceName與Weight的暫存字典
    counter = 0
    vertex_name = one_vtx
    vertex_inf = pm.skinCluster(
        selected_skin[0], query=True, inf=True)  # 取得該對象上的所有影響名稱
    vertex_weight = pm.skinPercent(
        selected_skin[0], one_vtx, query=True, value=True)  # 取得該對象的所有權重數值
    #print("Influences:",vertex_inf,vertex_weight)
    for q in vertex_inf:  # 將該vtx的影響與數值做配對
        temp_dict[q] = vertex_weight[counter]
        counter = counter + 1
    # 影響與權重值的配對作為值,vtx編號作為key,形成另一個字典
    vtx_all_inf_dict[vertex_name] = temp_dict

for vtx in vtx_all_inf_dict.items():  # 訪問字典裡的每一個vtx
    temp_list = []  # 暫存的乾淨資訊列表
    inf = vtx[1].items()    # 取得vtx上,包含所有影響清單的字典

    for single_inf in inf:  # 訪問字典內每一個影響
        if single_inf[1] == 0:  # 判別權重值是否為0,不為0則將該影響名稱與數值加入暫存列表
            pass
        else:
            #print("inf", single_inf)
            temp_list.append(single_inf)
    vtx_clear_inf_dict[vtx[0]] = temp_list  # 將該vtx過濾出的乾淨權重列表加入新的字典

##=========獲取乾淨權重字典區塊=============##

##===========檢測區==========##
# print("UI level:"inf_name_text_edit)
# print("History:", get_history)
# print("get skin:", selected_skin[0])
# print("Influences:",vertex_inf)
# print("Now select:", selected_point)
##===========檢測區==========##

count_dict = {}    #統計每種[影響名稱,數值]的組合出現了幾次
vtx_name_list = []  #判斷有問題的vtx名稱的列表
set_name_list = []  #暫存組合名稱列表
set_times_list = [] #暫存"次數"列表
final_tuple = None    #存放最後執行指令需要的tuple組合

for i in vtx_clear_inf_dict.items():
    x = str(i[1]) 
    if x in count_dict :
        count_dict[str(i[1])] += 1
    else:
        count_dict[str(i[1])] = 1

# 得到值最大的key
get_max_set = max(count_dict.items(), key=operator.itemgetter(1))[0] 
print("get_max_set:",get_max_set,type(get_max_set))

#   搜尋所有vertex找出不符合的vertex
for n in vtx_clear_inf_dict.items():
    y = str(n[0]) # 記錄此次的vtx名稱
    if str(n[1]) == get_max_set:    #將權重組合轉成字串與"次數最多的key"比對
        pass
    else:
        vtx_name_list.append(y) #將不符合的vtx加入最後需要被修正的list

#如果list是空的就不執行修改
if vtx_name_list == []:
    print("All Clear ! ")
else:    
    print("Wrong vtx:",vtx_name_list)
    pm.select(vtx_name_list)    #在視窗中選擇到並顯示有問題的點

    #重新再取一次正確的權重值組合
    for g in vtx_clear_inf_dict.items():
        m = str(g[1])  
        if m == get_max_set:    #將取到的組合轉成字串跟get_max_set比對
            final_tuple = g[1]  #直接將比對成功的組合取出(g[1]是含多個權重值組合tuple的list)
            break
        else:
            pass
    print(final_tuple)

    # 把有問題的vertex的權重值改成final_tuple
    # 此指令可以一次修改多個vertex,transformValue可接受一個內含多個tuple(influenceName,weight)組成的list
    pm.skinPercent(selected_skin[0], vtx_name_list, transformValue=final_tuple)

    print(vtx_all_inf_dict)