# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : cagesym.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

import numpy as np
import tqdm


def _search_addon(ADJ:np.ndarray,n:int,mask=None,searched=None):
    """

    Parameters
    ----------
    ADJ:np.ndarray
        Adjecant Matrix of Cage Graph.
    n:int
        Addons to do.
    Returns
    -------
    List of vertex for addons. **With repeated!!!**
    """
    assert len(ADJ.shape)==2
    assert ADJ.shape[0]==ADJ.shape[1]
    assert ADJ.shape[0]%2==0
    natoms=ADJ.shape[0]
    if searched is None:
        searched = []
    searched_main=searched.copy()
    assert isinstance(n,int), "`n` must be an integer and n>=1 !"
    if mask is None:
        mask=[]
    if n>1:
        for item in get_vertex_class_lists(ADJ,mask):
            # iter for each class of vertex
            ADJ_use = ADJ.copy()
            searched_sub = searched_main.copy()

            addonlist=[]
            addoni=min(item)
            ADJ_use[addoni,:]=0
            ADJ_use[:,addoni]=0
            addonlist.append(addoni)
            for subaddons in search_addon(ADJ_use,n-1,mask=[*mask,addoni],searched=searched_sub):
                yield [addoni,*subaddons]
            # searched_main.extend(item)

    elif n==1:
        for item in get_vertex_class_lists(ADJ,mask):
            result=min(item)
            if result not in searched_main:
                yield [min(item)]
            else:
                pass
    else:
        raise RuntimeError("Unkown error in searching addons of cages, got n<=0!")

def search_addon(ADJ:np.ndarray,n:int,mask=None,searched=None):
    """
    See Also `_search_addon()`

    """
    return np.unique(np.sort(np.array(list(_search_addon(ADJ,n,mask,searched))), axis=-1), axis=0)


def get_vertex_class_lists(ADJ,mask:list,order=None):
    natoms=ADJ.shape[0]
    nocc=int(natoms/2)
    natoms = ADJ.shape[0]
    nocc = int(natoms / 2)
    val, vec = np.linalg.eigh(ADJ)
    if not order:
        order = natoms//4*2
    else:
        pass
    result = vec @ np.diag(val ** order) @ np.linalg.inv(vec)
    # Use graph transmittion multiple methods for graph symmetry.
    cc = np.array([np.sort(np.array(list(i))) for i in result])
    cc_mat = cc #(cc[None, :, :] * cc[:, None, :]).sum(-1)
    val_max=cc_mat.max()
    vertex_class = np.unique(np.round(cc_mat/val_max,6), axis=0, return_index=True, return_inverse=True)
    # Uniform the value to regulate range for unique() function. Otherwise the double values will show differences.
    vertex_class_t = list(np.where(vertex_class[-1] == vertex_class[-1][item])[0] for item in vertex_class[-2])

    vertex_class_flitered=[]
    for item in vertex_class_t:
        flag=0
        for imask in mask:
            if imask in item or flag:
                flag=1
                break
        if not flag:
            vertex_class_flitered.append(item)
    return vertex_class_flitered

if __name__ == '__main__':
    # import ase.build
    # import numpy as np
    from fullerenedataparser.io.xyz import simple_read_xyz_xtb
    from fullerenedataparser.molecular.fullerene import FullereneFamily
    from ase.visualize import view
    import os


    np.set_printoptions(threshold=np.inf)
    np.set_printoptions(linewidth=500)

    atoms = list(simple_read_xyz_xtb(r"C:\Work\CODE\DATA\fullerxTBcal\xTBcal\opted\C44\C44_000000001opted.xyz"))[-1]
    outputfile=r"C60_1.txt"
    output=False

    # view(atoms)

    f = FullereneFamily(spiral=1, atoms=atoms)
    f = f.get_fullerenecage()
    D = f.atomADJ
    #
    print(get_vertex_class_lists(D,[]))
    # if os.path.exists(outputfile) and output:
    #     os.remove(outputfile)
    #
    # addonslist=search_addon(D,4)
    #
    # # print(len(addonslist))
    # # print(np.unique(np.sort(np.array(addonslist), axis=-1), axis=0))
    # # print(len(np.unique(np.sort(np.array(addonslist), axis=-1), axis=0)))
    # print(addonslist,file=open(outputfile,"a"))
