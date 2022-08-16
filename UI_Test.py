import pymel.core as pm

ui_file_path = pm.internalVar(usd=True) + r"Test/HardMeshWeight_UI.ui"
print(ui_file_path)
MainUI = pm.loadUI(uiFile=ui_file_path)
print(MainUI)

State_label = pm.text(MainUI + r"|gridLayout|State_label")
print(State_label)


def fix_weight_cmd(ignoreInputs):
    print("state_edit")
    # pm.scriptJob(killAll=True)
    pm.text(MainUI + r"|gridLayout|State_label", edit=True,
            label="State:Success!", bgc=[0, 1, 0])


pm.scriptJob(ct=["SomethingSelected", 'pm.text( MainUI + r"|gridLayout|State_label",edit=True,label="State:None",bgc=[0.27,0.27,0.27])'],
             parent=MainUI, permanent=True, killWithScene=True)


print(type(MainUI))
pm.showWindow(MainUI)
