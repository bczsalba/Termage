import pytermgui as ptg

with ptg.WindowManager() as manager:
    manager.layout.add_slot("Body")
    manager.add(
        ptg.Window(
            ptg.inspect(ptg.inspect),
            box="EMPTY",
        ),
    )
