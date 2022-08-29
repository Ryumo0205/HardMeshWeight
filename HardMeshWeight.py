# -*- coding: utf-8 -*-

import operator
import pymel.core as pm

#20220819修正:簡化資料結構減少效能消耗,新增進度條UI

ui_file_path = pm.internalVar(usd=True) + r"HardMeshWeight/HardMeshWeight_UI.ui"
print(ui_file_path)
MainUI = pm.loadUI(uiFile=ui_file_path)
print(MainUI)
State_label = pm.text(MainUI + r"|gridLayout|State_label",edit=True)
loading_bar = pm.progressBar(MainUI + r"|loading_bar",edit=True,progress=0)
loading_value = 0


def fix_weight_cmd(ignoreInputs):
    fix_weight()


def fix_weight():

    try:
        vtx_all_inf_dict = {}  # 每個vtx包含所有影響權重值的字典
        vtx_clear_inf_dict = {}  # 過濾完後最後需要被處裡的字典
        count_dict = {}    #統計每種[影響名稱,數值]的組合出現了幾次
        vtx_name_list = []  #判斷有問題的vtx名稱的列表
        final_tuple = None    #存放最後執行指令需要的tuple組合

        selected_point = pm.filterExpand(sm=31)  # 批次取得選到的vtx名稱
        selected_skin = pm.ls(sl=True)
        get_history = pm.listHistory(selected_skin, lv=0)  # 讀取歷史紀錄
        skin_name = pm.ls(get_history, type="skinCluster")  # 取得skinCluster名稱

        ##=========獲取乾淨權重字典區塊=============##

        #進度條最大值
        bar_maxinum = float(len(selected_point))
        print(bar_maxinum)

        for one_vtx in enumerate(selected_point):
            loading_value =  one_vtx[0] / bar_maxinum *100
            pm.progressBar(MainUI + r"|loading_bar",edit=True,progress=loading_value)

            temp_dict = {}  # 每次配對InfluenceName與Weight的暫存字典
            counter = 0
            vertex_name = one_vtx[1]
            vertex_inf = pm.skinCluster(
                skin_name[0], query=True, inf=True)  # 取得該對象上的所有影響名稱
            vertex_weight = pm.skinPercent(
                skin_name[0], vertex_name, query=True, value=True)  # 取得該對象的所有權重數值
            #print("Influences:",vertex_inf,vertex_weight)
            for q in vertex_inf:  # 將該vtx的影響與數值做配對
                temp_dict[q] = vertex_weight[counter]
                counter = counter + 1
            # 影響與權重值的配對作為值,vtx編號作為key,形成另一個字典
            vtx_all_inf_dict[vertex_name] = temp_dict
        pm.progressBar(MainUI + r"|loading_bar",edit=True,progress=100)


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

        ##===========================================##

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
            #   顯示無修正的結果
            print("No fixed vertices ! ")
            pm.text(MainUI + r"|gridLayout|State_label", edit=True,
                label="State:No fixed vertices", bgc=[1, 1, 0])
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
            print("final_inf:",final_tuple)

            # 此指令可以一次修改多個vertex,transformValue可接受一個內含多個tuple(influenceName,weight)組成的list
            pm.skinPercent(skin_name[0], vtx_name_list, transformValue=final_tuple)
            pm.text(MainUI + r"|gridLayout|State_label", edit=True,
                label="State:Success!", bgc=[0, 1, 0])
    except:
        pm.warning("please select vertices.")


pm.scriptJob(ct=["SomethingSelected", 'pm.text( MainUI + r"|gridLayout|State_label",edit=True,label="State:None",bgc=[0.27,0.27,0.27])'],
             parent=MainUI, permanent=True, killWithScene=True) #監聽是否選到新物件,選到新物件就更新UI顯示
pm.scriptJob(ct=["SomethingSelected", 'pm.progressBar(MainUI + r"|loading_bar",edit=True,progress=0)'],
             parent=MainUI, permanent=True, killWithScene=True)

if __name__ == "__main__":

    pm.showWindow(MainUI)