class MyContextManager:
    def __int__(self):
        print("in init")

    def __enter__(self):
        print("in enter")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("in exit")
        print("exc_type ", exc_type)
        print("exc_val", exc_val)
        print("exc_tb", exc_tb)

with MyContextManager() as my_context:
    print("do job") # przed tym pojawia sie "in enter"
    raise KeyError("Seba")

"""
in enter
do job
in exit

"""