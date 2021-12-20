# singleton
instances = None
def singleton(cls):
    def getinstance(*args, **kwargs):
        global instances
        if not instances:
           instances = cls(*args, **kwargs)
        return instances
    return getinstance
 
@singleton
class MyClass():
    a = 1
 
A = MyClass()
B = MyClass()
 
#print (len(A))
print (A is B)
