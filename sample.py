from cgnsreader import cgnsRead

# A sample to get the 
fn = './CRHmodel-10.02.012@03000.cgns'
a = cgnsRead(fn, HEAD=['Pressure', 'SkinFrictionX', 'SkinFrictionY', 'SkinFrictionZ'],
                 TAIL=['Pressure', 'SkinFrictionX', 'SkinFrictionY', 'SkinFrictionZ'],
                 MIDDLE=['Pressure', 'SkinFrictionX', 'SkinFrictionY', 'SkinFrictionZ'])

nList_head = a.HEAD.nList()
# nList_middle = a.MIDDLE.nList()
# nList_tail = a.TAIL.nList()

# Calculate the pressure
box1_h_l = (206.54, -1.7403027430452744, 0.4)
box1_h_u = (209.54, 1.8, 4)

a.HEAD.cal('Pressure', lb=box1_h_l, rb=box1_h_u, proj='x')
a.HEAD.cal(lb=box1_h_l, rb=box1_h_u, proj=None)


