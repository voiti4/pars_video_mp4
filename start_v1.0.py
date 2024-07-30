import binascii


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
        for el in tree:
            el.print_item()
        print(find_atom(tree, b'stsz'))    

def find_atom(tree, tag):
    for el in tree:
        if el.get_name() == tag:
            return [el.get_start(), el.get_size()]
        elif el.subAtoms:
            find_atom(el.subAtoms, tag)


main('1.mp4')
        




   


