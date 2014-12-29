__author__ = 'korzen'



class smth:
    def __init__(self, id, parent_id = None):
        self.id = id
        self.parent_id = parent_id
        self.childs = []

s = smth(1)
s2 = smth(2,1)
s.childs.append(s2)
s3 = smth(3,2)
s2.childs.append(s3)

print s.childs[0].childs[0].id
