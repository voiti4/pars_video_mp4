import structure_analysis as sa

import data_structure as ds

import utils

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
        if atomList[atom.get_name()][0] == 1:
            curAtom = ds.Atom(atom.get_name())
            if atom.subAtoms:
                subAtoms = create_repaired_tree(atom.subAtoms, atomList)
                curAtom.add_subAtoms(subAtoms)
            repairedTree.append(curAtom)    
    return repairedTree

def clone_template_data():
    pass

def main(fileDemage, fileTemplate):
    with open(fileDemage,'rb') as fDemage, open(fileTemplate, 'rb') as fTemplate:
        lim = sa.get_file_size(fTemplate)
        treeTemplate = sa.create_atom_list(fTemplate, lim)
        tree = create_repaired_tree(treeTemplate, ds.sign)
    print (tree)

main('562965', 'FILE0137.MOV')