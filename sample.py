from cgnsreader import cgnsRead

# A sample to get the 
fn = '~/data_gt/CRHmodel-10.02.012@03000.cgns'
a = cgnsRead(fn, HEAD=['Pressure', 'SkinFrictionX', 'SkinFrictionY', 'SkinFrictionZ'],
                 TAIL=['Pressure', 'SkinFrictionX', 'SkinFrictionY', 'SkinFrictionZ'])
nList_head = a.HEAD.nList()
nList_tail = a.TAIL.nList()
# Calculate the pressure
box1_h_l = (0, -0.5, 0.5); box1_h_u   = (5, 0.5, 1.5)
box1_t_l = (205, -0.5, 0.5); box1_t_u =  (210, 0.5, 1.5)
pre_div1 = 0
pre_div_all = 0
for inode in nList_head:
    pre_div_all += inode.value('Pressure',proj='x')
    if inode > box1_h_l and inode < box1_h_u:
        pre_div1 += inode.value('Pressure',proj='x')
for inode in nList_tail:
    pre_div_all -= inode.value('Pressure',proj='x')
    if inode > box1_t_l and inode < box1_t_u:
        pre_div1 -= inode.value('Pressure', proj='x')
print(pre_div1, pre_div_all)
