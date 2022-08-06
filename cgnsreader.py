import h5py
import re
from pathlib import Path
from point import point
from node import node
import math


class cgnsSection(object):

    # Section in the CGNS file

    def __init__(self, h5file: h5py.File, section, attrs):
        # Judge the section name of the HDF file
        sec_re     = re.compile(section) 
        sec_name   = None
        for ikey in h5file['Base'].keys():
            temp_re = sec_re.search(ikey)
            if temp_re is not None:
                sec_name = ikey
                break
        if sec_name is None:
            raise Exception('The section %s is not exist in the CGNS file.' % section)
        self.section = h5file['Base/'+sec_name]
        self.attrs   = attrs
        self.sname   = sec_name
        # Judge the name of the solution
        solu_re = re.compile(r'Solution\d+')
        self.soluName = None
        for ikey in self.section.keys():
            temp_re = solu_re.search(ikey)
            if temp_re is not None:
                self.soluName = temp_re.group(0)
                break
        if self.soluName is None:
            raise Exception('The solution is not exist in the CGNS file.')

    def pList(self):
        if hasattr(self, '_pList'):
            return getattr(self, '_pList')

        X = self.section['GridCoordinates/CoordinateX'][' data'][:]
        Y = self.section['GridCoordinates/CoordinateY'][' data'][:]
        Z = self.section['GridCoordinates/CoordinateZ'][' data'][:]

        self._pList = []
        for i in range(len(X)):
            self._pList.append(point(X[i], Y[i], Z[i]))

        return self._pList

    def nList(self):
        if hasattr(self, '_nList'):
            return getattr(self, '_nList')

        if not hasattr(self, '_pList'):
            self.pList()

        conn = self.section[self.sname+'/ElementConnectivity/ data'][:]
        conn = list(conn)
        vardict = {}
        self._nList = []
        for i in range(len(self.attrs)):
            vardict[self.attrs[i]] = self.section[self.soluName+'/'+self.attrs[i]+'/ data'][:]

        for i in range(len(vardict[self.attrs[0]])):
            point_num = conn.pop(0)
            point_list = []
            varnode = []
            for ikey in range(len(self.attrs)):
                varnode.append(vardict[self.attrs[ikey]][i])
            node_dict = dict(zip(vardict.keys(), varnode))
            for i_n in range(point_num):
                pnum = conn.pop(0)
                point_list.append(self._pList[pnum-1])
            self._nList.append(node(*point_list, **node_dict))
            # print(point_list, node_dict)

        return self._nList

    def cal(self, *var, lb=None, rb=None, proj=None):
        if not hasattr(self, '_nList'):
            return getattr(self, '_nList')
        val = 0
        for inode in self._nList:
            if len(var) == 1:
                val += inode.value('Pressure', proj=proj)
            else:
                val += math.sqrt((inode.value('SkinFrictionX') ** 2 + inode.value('SkinFrictionY') ** 2 +
                                 inode.value('SkinFrictionZ') ** 2))
        print(val)




class cgnsRead(object):
    """
    The Group of the CGNS file:
    1. The data restore at group BASE.
    2. The section was saved at BASE in different section. /BASE/[SECTION]
    3. The solution was saved at the section. /BASE/[SECTION]/[SOLUTION1]/[VARIABLE]
    4. GRID was saved at Grid location. /BASE/[SECTION]/GridCoordinates
    5. Node information was saved at /BASE/[SECTION]/[SECTION]/ElementConnectivity
    fn: - name of the CGNS file.
    kwargs: - key: section name.
            - value: variables name.
    """
    def __init__(self, fn, **kwargs):
        self.TAIL = None
        self.MIDDLE = None
        self.HEAD = None
        fn = Path(fn).expanduser().resolve()
        self.file = h5py.File(fn, 'r')
        for key, value in kwargs.items():
            setattr(self, key+'_value', value)
            setattr(self, key, self.getGroup(key))

    def getGroup(self, secname):
        return cgnsSection(self.file, secname, getattr(self, secname+'_value'))


if __name__ == '__main__':
    path = '~/tt/ttp.cgns'
    a = cgnsRead(path, **{'HEAD': ['Pressure']})
    p = a.HEAD.nList()
    print(p)
