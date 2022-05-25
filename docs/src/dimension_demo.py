import pytermgui as ptg


with ptg.WindowManager() as manager:
    manager.layout.add_slot()
    manager.add(ptg.Window("Some window", box="EMPTY"))
