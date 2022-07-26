import numpy as np
from pathlib import Path
from point import point

class node(object):
    '''
    *args:    The point of the node
    **kwargs: The property of the node
    '''
    dire = {'x': 0, 'y':1, 'z':2}
    def __init__(self, *args, **kwargs):
        # Define the point
        if len(args) < 3:
            raise Exception('The length of the points in a node should be higher than 3.')
        self.points = np.array(args)
        self.np     = len(args)
        self.lbound = (min(self.points[:, 0]), min(self.points[:, 1]), min(self.points[:, 2]))
        self.rbound = (max(self.points[:, 0]), max(self.points[:, 1]), max(self.points[:, 2]))
        for key, value in kwargs.items():
            setattr(self, key, value)

    # Gt means the whole grid in the selected region.
    def __gt__(self, other):
        if len(other) != 3:
            raise Exception('The length of the dimension must be 3.')
        return (self.lbound[0] >= other[0] and self.lbound[1] >= other[1] and self.lbound[2] >= other[2])

    # Lt means the whole grid in the selected region.
    def __lt__(self, other):
        if len(other) != 3:
            raise Exception('The length of the dimension must be 3.')
        return (self.rbound[0] <= other[0] and self.rbound[1] <= other[1] and self.rbound[2] <= other[2])

    # Ge means at least a part of the grid in the selected region.
    def __ge__(self, other):
        if len(other) != 3:
            raise Exception('The length of the dimension must be 3.')
        for point in self.points:
            if point[0] >= other[0] and point[1] >= other[1] and point[2] >= other[2]:
                return True
        return False

    # Le means at least a part of the grid in the selected region.
    def __le__(self, other):
        if len(other) != 3:
            raise Exception('The length of the dimension must be 3.')
        for point in self.points:
            if point[0] <= other[0] and point[1] <= other[1] and point[2] <= other[2]:
                return True
        return False

    def value(self, val=None, proj=None):
        if val is not None:
            val = getattr(self, val)
        else:
            val = 1

        # Judge if has already calculate it.
        if proj is not None:
            if hasattr(self, 'area'+proj):
                return getattr(self, 'area'+proj)*val
        else:
            if hasattr(self, 'area'):
                return getattr(self, 'area')*val

        if proj is not None:
            proj_column = self.dire[proj]
            proj_points = np.delete(self.points, proj_column, 1) 
            # 2-D Area in Projection
            area = 0
            for i in range(self.np):
                i1   = i + 1 - self.np*int(i/(self.np-1))
                area += proj_points[i, 0] * proj_points[i1, 1] - proj_points[i1, 0] * proj_points[i, 1]
            area = abs(area)/2
            setattr(self, 'area'+proj, area)
        else:
            points = self.points
            # 3-D Area
            a = (pow(((points[1, 1] - points[0, 1])
                *(points[-1, 2] - points[0, 2])
                -(points[-1, 1] - points[0, 1])
                *(points[1, 2] - points[0, 2])),2)
                +pow(((points[-1, 0] - points[0, 0])
                *(points[1, 2] - points[0, 2])
                -(points[1, 0] - points[0, 0])
                *(points[-1, 2] - points[0, 2])),2)
                +pow(((points[1, 0] - points[0, 0])
                *(points[-1, 1] - points[0, 1])
                -(points[-1, 0] - points[0, 0])
                *(points[1, 1] - points[0, 1])),2))
            # Use the first 3 point to determine the plane
            cosnx = (((points[1, 1] - points[0, 1])
                    *(points[-1, 2] - points[0, 2])
                    -(points[-1, 1] - points[0, 1])
                    *(points[1, 2] - points[0, 2]))
                    /pow(a, 1/2))
            cosny = (((points[-1, 0] - points[0, 0])
                    *(points[1, 2] - points[0, 2])
                    -(points[1, 0] - points[0, 0])
                    *(points[-1, 2] - points[0, 2]))
                    /pow(a, 1/2))
            cosnz = (((points[1, 0] - points[0, 0])
                    *(points[-1, 1] - points[0, 1])
                    -(points[-1, 0] - points[0, 0])
                    *(points[1, 1] - points[0, 1]))
                    /pow(a, 1/2))
            area  = 0
            for i in range(self.np):
                i1   = i + 1 - self.np*int(i/(self.np-1))
                area += (cosnz*(points[i, 0] * points[i1, 1] - points[i1, 0] * points[i, 1])
                        +cosnx*(points[i, 1] * points[i1, 2] - points[i1, 1] * points[i, 2])
                        +cosny*(points[i, 2] * points[i1, 0] - points[i1, 2] * points[i, 0]))
            area = abs(area)/2
            setattr(self, 'area', area)
        return area*val
        
if __name__ == '__main__':
    node_test = node(point(0, 0, 0), point(1, 0, 1), point(1, 1, 1), point(0, 1, 0), p=1)
    if node_test >= (0,0,0) and node_test <= (0.5,0.5,0.5):
        print('yes')
