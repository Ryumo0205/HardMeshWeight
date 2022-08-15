import pymel.core as pm
import pymel.core.uitypes as pmui
import pymel.core.windows as pmw

ui_file_path = pm.internalVar(usd=True) + r"Test/HardMeshWeight_UI.ui"
print(ui_file_path)
MainUI = pm.loadUI(uiFile=ui_file_path)
print(MainUI)

x = pm.textField( MainUI + r"|lineEdit",query=True)


def fix_weight_cmd( ignoreInputs ):
    print("state_edit")
pm.showWindow( MainUI )