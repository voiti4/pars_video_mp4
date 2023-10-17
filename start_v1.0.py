class Atom:
    
    def __init__(self, name, start, size):
        self.name = name
        self.start = start
        self.size = size
    def __str__(self):
        return f'name-{self.name} start-{self.start} size-{self.size}'    

def file_to_hexstr(file_name):
    with open(file_name, 'rb') as file:
        bytes = file.read()
    hex_list = []
    for b in bytes:
        if int(b) < 16:
            hex_list.append(f'0{hex(b)[2:]}')
        else:
            hex_list.append(hex(b)[2:])
    return ''.join(hex_list)


def create_atoms(hex_str):
    structure = []
    len_str = len(hex_str)
    i = 0
    flag = False
    while i < len_str:
        for key in sign:
            if hex_str.startswith(sign[key][1], i):
                structure.append(Atom(key, i // 2 - 4, hex_str[i - 8:i]))
                flag = True
                if sign[key][0] == 0:
                    i += int(hex_str[i - 8:i], 16)
                else:
                    i += 1
                break
        if flag:
            flag = False
        else:
            i += 1                
    return structure
        
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
# struc = create_atoms(file_to_hexstr('1.mp4'))
# for st in struc:
#    print(st)
with open('2.mp4', 'rb') as file:
    bytes = file.read()
i = 0
len_str = len(bytes)
while i :=bytes.find(b'\x74\x72\x61\x6b', i, len_str):
    print(i)
    i += 1
    pass
pass