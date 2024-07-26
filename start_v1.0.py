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
    def add_subAtoms(self, subAtoms)
        self.subAtoms.extend(subAtoms)


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

       
# def tag_to_hexstr(st):
#     return '0x'+''.join([str(hex(ord(i)))[2:4] for i in (st)])

def create_atoms(hex_file):
    struc = []
    for atom in sign:
        start = hex_file.find(binascii.unhexlify(sign[atom][1]), 4)
        while start > 0:
            struc.append(Atom(atom, start - 4,int.from_bytes(hex_file[start - 4:start])))
            start = hex_file.find(binascii.unhexlify(sign[atom][1]), start+1)
            # print(start)
            # start +=1
    return struc        



sign = {
    'ftyp': [1, '66747970'],
    'mdat': [0, '6d646174'],
    'free': [0, '66726565'],
    'moov': [1, '6d6f6f76'],
    'trak': [1, '7472616b'],
    'tkhd': [0, '746b6864'],
    'mdia': [1, '6d646961'],
    'mdhd': [0, '6d646864'],
    'hdlr': [0, '68646c72'],
    'minf': [1, '6d696e66'],
    'vmhd': [0, '766d6864'],
    'dinf': [0, '64696e66'],
    'stbl': [1, '7374626c'],
    'stsd': [0, '73747364'],
    'stts': [0, '73747473'],
    'ctts': [0, '63747473'],
    'stsc': [0, '73747363'],
    'stsz': [0, '7374737a'],
    'stco': [0, '7374636f'],
    'stss': [0, '73747373'],
    'sdtp': [0, '73647470']


}


with open('1.mp4', 'rb') as file1:
    str_1 = file1.read()
    struc = create_atoms(str_1)
for st in struc:
    if st.chunk_name() == 'stsc':
        stsc_obj = Stsc(st.name, st.start, st.size, str_1[st.start:st.start + st.size])
        print(stsc_obj.chunks_offset(str_1[st.start:st.start + st.size]))    


