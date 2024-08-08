import structure_analysis as sa

import data_structure as ds

def make_key_file(fileDamage, fileTemplate):
   
    keyFrames = sa.find_key_in_damage(fileDamage, fileTemplate)
    name = 'KeyFrame_' + fileDamage.name
    with open(name,'wb') as fileTarget:
        for key in keyFrames:
            fileDamage.seek(key[0])
            fileTarget.write(fileDamage.read(key[1]))

def create_repaired_tree(tree, atomList):
    repairedTree = list()
    for atom in tree:
        if atom.subAtoms is not None:
            create_repaired_tree(atom, atomList)
        else:
            if atomList[atom.get_name()][0][0] == 1:
                repairedTree.append(ds.Atom(atom.get_name()))    
    return repairedTree             