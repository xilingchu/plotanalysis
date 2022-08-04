from cgnsreader import Cal

fn = './opt0.cgns'

# pressure_HEAD:
box_h_l = (-0.14390611062777214, -1.7403027430452744, 0.7)
box_h_u = (2.4, 1.8, 4)
Cal().preHead(fn, box_h_l, box_h_u)

# pressure_TAIL:
box_t_l = (206.573, -1.7403027430452744, 0.7)
box_t_u = (209.113, 1.8, 4)
Cal().preTail(fn, box_t_l, box_t_u)

# skinfriction_HEAD:
box_h_l = (-0.14390611062777214, -1.7403027430452744, 0.7)
box_h_u = (2.4, 1.8, 4)
Cal().skinHead(fn, box_h_l, box_h_u)

# skinfriction_MIDDLE:
box1_m_l = (12.2, -1.7, 0.2)
box1_m_u = (62, 1.8, 4)
box2_m_l = (12.2, -1.7, 0.2)
box2_m_u = (62, 1.8, 0.4)
box3_m_l = (12.2, -1.7, 0.2)
box3_m_u = (196.8, 1.8, 0.4)
# Cal().skinMiddle(fn, box1_m_l, box1_m_u, box2_m_l, box2_m_u, box3_m_l, box3_m_u)

# skinfriction_TAIL:
box_t_l = (206.573, -1.7403027430452744, 0.7)
box_t_u = (209.113, 1.8, 4)
Cal().skinTail(fn, box_t_l, box_t_u)

