import pymel.core as pm


ui_file_path = pm.internalVar(usd=True) + r"Test/HardMeshWeight_UI.ui"
print(ui_file_path)
MainUI = pm.loadUI(uiFile=ui_file_path)
print(MainUI)

#x = pm.text( MainUI + r"|State_label",edit=True)



def fix_weight_cmd( ignoreInputs ):
    print("state_edit")
    pm.text( MainUI + r"|State_label",edit=True,label="OK!")
pm.showWindow( MainUI )