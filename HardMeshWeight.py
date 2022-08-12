import pymel.core as pm

vtx_all_inf_dict = {}  # 每個vtx包含所有影響權重值的字典
vtx_final_inf_dict = {}  # 過濾完後最後需要被處裡的字典

selected_point = pm.filterExpand(sm=31)  # 批次取得選到的vtx名稱
get_history = pm.listHistory(selected_point, lv=0)  # 讀取歷史紀錄
selected_skin = pm.ls(get_history, type="skinCluster")  # 取得skinCluster名稱

##===========檢測區==========##
# print("UI level:"inf_name_text_edit)
# print("History:", get_history)
print("get skin:", selected_skin[0])
# print("Influences:",vertex_inf)
print("Now select:", selected_point)
##===========檢測區==========##

##=========獲取乾淨權重字典區塊=============##

for single_vtx in selected_point:
    temp_dict = {}  # 每次配對影響名稱與數值的暫存字典
    loop_times = 0
    vertex_name = single_vtx
    vertex_inf = pm.skinCluster(
        selected_skin[0], query=True, inf=True)  # 取得該對象上的影響名稱
    vertex_weight = pm.skinPercent(
        selected_skin[0], single_vtx, query=True, value=True)  # 取得該對象的權重參數
    #print("Influences:",vertex_inf,vertex_weight)
    for q in vertex_inf:  # 將該vtx的影響與數值做配對
        temp_dict[q] = vertex_weight[loop_times]
        loop_times = loop_times + 1
    # 影響與權重值的配對作為值,vtx編號作為key,形成另一個字典
    vtx_all_inf_dict[vertex_name] = temp_dict

for vtx_key in vtx_all_inf_dict.items():  # 訪問每一個vtx
    temp_list = []  # 暫存的乾淨資訊列表
    inf = vtx_key[1].items()    # 取得vtx上,包含所有影響清單的字典

    for single_inf in inf:  # 訪問字典內每一個影響
        if single_inf[1] == 0:  # 判別權重值是否為0,不為0則將該影響名稱與數值加入暫存列表
            pass
        else:
            #print("inf", single_inf)
            temp_list.append(single_inf)
    vtx_final_inf_dict[vtx_key[0]] = temp_list  # 將該vtx過濾出的乾淨權重列表加入新的字典

##=========獲取乾淨權重字典區塊=============##


keisan_dict = {}    #統計每種[影響名稱,數值]的組合出現了幾次

for i in vtx_final_inf_dict.items():
    x = str(i[1])
    if x in keisan_dict :
        keisan_dict[str(i[1])] += 1
    else:
        keisan_dict[str(i[1])] = 1

# 找出最大值

set_name_list = []  #暫存名稱列表55
set_times_list = [] #暫存"次數"列表

for z in sorted(keisan_dict.items()):
    #print("keisan_dict:", z[0])
    set_name_list.append(z[0])
    set_times_list.append(z[1])

max_value = max(set_times_list)
max_value_index = set_times_list.index(max_value)

get_max_set = set_name_list[max_value_index]
print("Max set:",get_max_set)    #最多次重複的組合
print("Max set:",type(get_max_set))

for n in vtx_final_inf_dict.items():
    print(n[1])
    if str(n[1]) == get_max_set:
        print("Match!")
    else:
        print("Out!")