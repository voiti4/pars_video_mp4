import binascii

import utils


class Atom:
    
    def __init__(self, name, start, size, subAtoms=None):
        self.name = name
        self.start = start
        self.size = size
        if subAtoms is None:
            self.subAtoms = list()
        else:
            self.subAtoms = subAtoms    
    def __str__(self):
        return f'name-{self.name} start-{self.start} size-{self.size}'
    def get_name(self):
        return self.name
    def get_start(self):
        return self.start
    def get_size(self):
        return self.size 
    def add_subAtoms(self, subAtoms):
        self.subAtoms.extend(subAtoms)
    def print_item(self, level=0):
        str = '-' * level
        print(f'{str}{self}')
        if self.subAtoms:
            level += 1
            for atom in self.subAtoms:
                atom.print_item(level)    


class Stsc(Atom):

    def __init__(self, name, start, size, stsc):
        super().__init__(name, start, size)
        i = int.from_bytes(stsc[12:16])
        self.entery_count = i
    def chunks_offset(self, stsc):
        map_chank = dict()
        for i in range(self.entery_count):
            map_chank[str(int.from_bytes(stsc[self.start + 16 + i * 12:self.start + 20 + i * 12]))] = map_chank.get(str(int.from_bytes(stsc[self.start + 16 + i * 12:self.start + 20 + i * 12])), 0) + int.from_bytes(stsc[self.start + 20 + i * 12:self.start + 24 + i * 12])
        return map_chank

         
sign = {
    b'ftyp': [1, '66747970'],
    b'mdat': [0, '6d646174'],
    b'free': [0, '66726565'],
    b'moov': [1, '6d6f6f76'],
    b'trak': [1, '7472616b'],
    b'tkhd': [0, '746b6864'],
    b'mdia': [1, '6d646961'],
    b'mdhd': [0, '6d646864'],
    b'hdlr': [0, '68646c72'],
    b'minf': [1, '6d696e66'],
    b'vmhd': [0, '766d6864'],
    b'dinf': [0, '64696e66'],
    b'stbl': [1, '7374626c'],
    b'stsd': [0, '73747364'],
    b'stts': [0, '73747473'],
    b'ctts': [0, '63747473'],
    b'stsc': [0, '73747363'],
    b'stsz': [0, '7374737a'],
    b'stco': [0, '7374636f'],
    b'stss': [0, '73747373'],
    b'sdtp': [0, '73647470']


}


def get_file_size(fileobject):
    fileobject.seek(0,2) # move the cursor to the end of the file
    size = fileobject.tell()
    fileobject.seek(0,0)
    return size

def create_atom_list(file, limit):
    atoms = list()
    curPos = 0
    while (curPos<limit):
        curAtom = None
        try:
            tag = file.read(4)
            if tag in sign:
                start = file.tell() - 8
                file.seek(-8, 1)
                size = int.from_bytes(file.read(4))
                file.seek(4, 1)
                curAtom = Atom(tag, start, size)
                if tag != b'mdat':
                    subAtoms = create_atom_list(file, size - 8)
                    curAtom.add_subAtoms(subAtoms)
            else:
                file.seek(-3, 1)
        except EOFError:
            print('eof')
            break
        if curAtom is not None:
            curPos += curAtom.get_size()
            atoms.append(curAtom)
        else:
            curPos += 1
    return atoms          
                

def main(file):
    with open(file, 'rb') as file1:
        limit = get_file_size(file1)
        tree = create_atom_list(file1, limit)
        # for el in tree:
            # el.print_item()
        print(define_feature_key(file1, tree))
 

def find_atom(tree, tag):
    for el in tree:
        if el.get_name() == tag:
            return [el.get_start(), el.get_size()]
        elif el.subAtoms:
            return find_atom(el.subAtoms, tag)

def make_list_stbl_atoms(file, start, step=4, offset=12):
    start += offset
    file.seek(start)
    count = int.from_bytes(file.read(step))
    lt = list()
    for i in range(1, count):
        lt.append(int.from_bytes(file.read(step)))
    return lt

def define_keyframes(file, tree):
    stss = find_atom(tree, b'stss')
    stco = find_atom(tree, b'stco')
    stsz = find_atom(tree, b'stsz')
    if stss is not None:
        stss_data = make_list_stbl_atoms(file, stss[0])
        stco_data = make_list_stbl_atoms(file, stco[0])
        stsz_data = make_list_stbl_atoms(file, stsz[0], 4, 16)
        lt = list()
        for i in stss_data:
            lt.append((stco_data[i - 1], stsz_data[i - 1]))
        return lt    
                       
def metrika(data1, data2, template):
    length = min(len(data1), len(data2))
    for i in range(0, length):
        if template[i]:
            if data1[i] != data2[i]:
                template[i] = False
    return template               

def define_feature_key(file, tree, size=64):
    lt = define_keyframes(file, tree)
    first = lt[0]
    featureMatrix = [True for i in range(0, size)]
    j = 0
    for current in lt:
        file.seek(first[0])
        dataFirst = file.read(size)
        file.seek(current[0])
        dataCurrent = file.read(size)
        featureMatrix = metrika(dataFirst, dataCurrent, featureMatrix)
        j += 1
    return featureMatrix    



     

def define_feature_differnce(file, tree):
    pass



main('FILE0137.MOV')
        




   


