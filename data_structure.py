class Atom:
    
    def __init__(self, name, start=0, size=0, subAtoms=None):
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
    b'mdat': [1, '6d646174'],
    b'free': [0, '66726565'],
    b'moov': [1, '6d6f6f76'],
    b'mvhd': [1, '6d766864'],
    b'trak': [1, '7472616b'],
    b'tkhd': [1, '746b6864'],
    b'mdia': [1, '6d646961'],
    b'mdhd': [1, '6d646864'],
    b'hdlr': [0, '68646c72'],
    b'minf': [1, '6d696e66'],
    b'vmhd': [1, '766d6864'],
    b'dinf': [1, '64696e66'],
    b'dref': [1, '64726566'],
    b'stbl': [1, '7374626c'],
    b'stsd': [1, '73747364'],
    b'stts': [1, '73747473'],
    b'ctts': [0, '63747473'],
    b'stsc': [1, '73747363'],
    b'stsz': [0, '7374737a'],
    b'stco': [0, '7374636f'],
    b'stss': [0, '73747373'],
    b'co64': [0, '636f3634']


}