import data_structure as ds

import utils


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
            if tag in ds.sign:
                start = file.tell() - 8
                file.seek(-8, 1)
                size = int.from_bytes(file.read(4))
                file.seek(4, 1)
                curAtom = ds.Atom(tag, start, size)
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
                

def main(fileDemage, fileTemplate):
    with open(fileDemage,'rb') as fileDemage, open(fileTemplate, 'rb') as fileTemplate:
        # limit = get_file_size(file1)
        # tree = create_atom_list(file1, limit)
        # for el in tree:
            # el.print_item()
        # print(fileDemage.name)
        make_key_file(fileDemage, fileTemplate)
 

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

def define_keyframes(file):
    """ stss = find_atom(tree, b'stss')
    stco = find_atom(tree, b'stco')
    stsz = find_atom(tree, b'stsz')
    if stss is not None:
        stss_data = make_list_stbl_atoms(file, stss[0])
        stco_data = make_list_stbl_atoms(file, stco[0])
        stsz_data = make_list_stbl_atoms(file, stsz[0], 4, 16)
        lt = list()
        for i in stss_data:
            lt.append((stco_data[i - 1], stsz_data[i - 1]))
        return lt     """
    limit = get_file_size(file)
    tree = create_atom_list(file, limit)
    stss = find_atom(tree, b'stss')
    stsz = find_atom(tree, b'stsz')
    stco = find_atom(tree, b'stco')
    if stss is not None:
        keyList = list()
        stss_data = make_list_stbl_atoms(file, stss[0])
        stsz_data = make_list_stbl_atoms(file, stsz[0], 4, 16)
        stco_data = make_list_stbl_atoms(file, stco[0])
        lt = [stsz_data[stss_data[i]-1] for i in range(0, len(stss_data))]
        minSize = min(lt)
        for i in range (0, len(stsz_data)):
            if stsz_data[i] > minSize:
                keyList.append((stco_data[i], stsz_data[i]))
        return keyList 
                                    

def find_pos_sizevalue(data, template, size=4):
   
    for i in range(0, len(data) - size + 1):
        if int.from_bytes(data[i:i + size]) == template - size - i:
            return i

def define_feature_key(file, size=60):
    
    limit = get_file_size(file)
    tree = create_atom_list(file, limit)
    lt = define_keyframes(file)
    first = lt[0]
    featureMatrix = [True for i in range(0, size)]
    stsz = find_atom(tree, b'stsz')
    stsz_data = make_list_stbl_atoms(file, stsz[0], 4, 16)
    file.seek(first[0])
    dataFirst = file.read(size)
    pos = find_pos_sizevalue(dataFirst, stsz_data[0])
    minSize = maxSize = lt[0][1]
    for current in lt:
        # file.seek(first[0])
        # dataFirst = file.read(size)
        if current[1] < minSize:
            minSize = current[1]
        elif current[1] > maxSize:
            maxSize = current[1]    
        file.seek(current[0])
        dataCurrent = file.read(size)
        featureMatrix = utils.metrika(dataFirst, dataCurrent, featureMatrix)
        dataFirst = dataCurrent
    return (dataFirst, featureMatrix, pos, minSize, maxSize)

def find_key_in_damage(fileDamage, fileExample):
    feature_key = define_feature_key(fileExample)
    limit = get_file_size(fileDamage)
    templateSize = len(feature_key[0])
    posSize = feature_key[2]
    pos = 0
    fileDamage.seek(pos)
    lt = list()
    while pos < limit - templateSize:
        currentData = fileDamage.read(templateSize)
        for i in range(0, templateSize):
            if feature_key[1][i]:
                if feature_key[0][i] != currentData[i]:
                    pos += 1
                    fileDamage.seek(pos)
                    break
        else:
            keySize = posSize + int.from_bytes(currentData[posSize:posSize + 4]) + 4
            if (pos + posSize + keySize <= limit) and (keySize > feature_key[3] - 100) and (keySize < feature_key[4] + 100):
                lt.append((pos, keySize))
                pos += (posSize + keySize)
            else:
                pos += 1
    return lt
     

    

def define_feature_differnce(file, tree):
    pass



main('562965', 'FILE0137.MOV')
        




   


