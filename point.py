from collections import UserList


class point(tuple):
    def __new__(cls, x, y, z, **kwargs):
        return tuple.__new__(cls, (x,y,z))
        
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class pointList(UserList):
    def __init__(self):
        pass

    def pop(self):
        pass

if __name__ == '__main__':
    pl = []
    pl = [point(1,2,3,pl=pl), point(4,5,6,pl=pl)]
    pl[0].id
