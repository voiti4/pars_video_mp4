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
    b'ftyp': [1, 'const'],
    b'mdat': [1, 'var'],
    b'free': [0, 'var'],
    b'moov': [1, 'var'],
    b'mvhd': [1, 'const'],
    b'trak': [1, 'var'],
    b'tkhd': [1, 'const'],
    b'mdia': [1, 'var'],
    b'mdhd': [1, 'const'],
    b'hdlr': [1, 'const'],
    b'minf': [1, 'var'],
    b'vmhd': [1, 'const'],
    b'dinf': [1, 'const'],
    b'dref': [1, 'const'],
    b'stbl': [1, 'var'],
    b'stsd': [1, 'const'],
    b'stts': [1, 'var'],
    b'ctts': [0, 'var'],
    b'stsc': [1, 'var'],
    b'stsz': [1, 'var'],
    b'stco': [1, 'var'],
    b'stss': [0, 'var'],
    b'co64': [1, 'var']


}