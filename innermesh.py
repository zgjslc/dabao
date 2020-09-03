import pyvista as pv
import numpy as np
import glob

class buildmesh:
    def __init__(self):
        self.name = []
        self.data = []
        self.link = []
        self.wholelink = []
        self.meshtype = []
        self.firstpoint = []
    def get_num(self,line, keyword=', NODES='):
        line_in = line
        list1 = line_in.split(keyword)
        list1 = list1[1].split(',')
        list1 = list1[0].split()
        num = int(list1[0])
        return num


    def get_data(self,filename):
        self.name = []
        self.data = []
        self.link = []
        self.wholelink = []
        self.meshtype = []
        self.firstpoint = []
        with open(filename) as f:
            lines = f.readlines()
        if(lines[0].startswith('VARIABLES')):
            s = lines[0].split('VARIABLES="')
            s = s[1].split('"\n')
            a = s
            a = a[0].split('","')
            self.name = a[3:]
            for i in range(len(self.name)+3):
                self.data.append([])
        node_num = self.get_num(lines[1], ', NODES=')
        ele_num = self.get_num(lines[1], ', ELEMENTS=')
        a = len(self.data) - 3
        self.property = np.zeros((a,node_num))

        for index in range(2, 2+node_num):
            list1 = lines[index].split()
            for i in range(len(self.data)):
                self.data[i].append(float(list1[i]))

        for idx,index in enumerate(lines):
            if( 'ZONETYPE=FEQUADRILATERAL' in index):
                elenum = self.get_num(index, keyword=', ELEMENTS=')
                for i in range(idx+1,idx+elenum+1):
                    list1 = lines[i].split()
                    self.link = []
                    self.link.append(4)
                    self.link.append(int(list1[0]) - 1)
                    self.firstpoint.append(int(list1[0]) - 1)
                    self.link.append(int(list1[1]) - 1)
                    self.link.append(int(list1[2]) - 1)
                    self.link.append(int(list1[3]) - 1)
                    self.wholelink.append(self.link)
                    self.meshtype.append(9)
                List_mesh = np.array(self.wholelink)
                self.cells = np.hstack(List_mesh)
                List_y = np.array(self.data[1])
                List_x = np.array(self.data[0])
                List_z = np.array(self.data[2])
                self.points = np.column_stack((List_x, List_y, List_z))
                for i in range(len(self.data)-3):
                    self.property[i] = np.array(self.data[i + 3])
                self.offset = np.array(self.firstpoint)
                self.cell_type = np.array(self.meshtype)
        if(self.wholelink !=[]):
            return 1
        elif(self.wholelink ==[]):
            return 0




    def meshplot(self,filename):
        type = self.get_data(filename)
        if(type == 1):

            grid = pv.UnstructuredGrid(self.offset, self.cells, self.cell_type, self.points)
            grid.slice()
            for i in range(len(self.data) - 3):
                grid.point_arrays[self.name[i]] = self.property[i]
            return grid, self.name,type
        elif(type ==0):
            return 0, 0, type
if __name__ == "__main__":
    h =buildmesh()
    plotter = pv.Plotter()
    meshlist = []
    resultpath = 'C:\\Users\\Administrator\\Desktop\\BJ20191027\\RotFlow_Work\\cass12\\RESULT'
    filename1 = glob.glob(resultpath + '\\*.plt')
    for i in range(len(filename1)):
        if ('Rsu' in filename1[i]):
            grid,name,type =h.meshplot(filename1[i])

            if(type ==1):
                meshlist.append(grid)
    for mesh in meshlist:
        plotter.add_mesh(mesh)
    plotter.show()


