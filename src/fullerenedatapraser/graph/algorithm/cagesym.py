# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : cagesym.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

import numpy as np

def search_addon(ADJ:np.ndarray,n:int,condition_for_vertex=None,mask=None,searched=None):
    """

    Parameters
    ----------
    ADJ:np.ndarray
        Adjecant Matrix of Cage Graph.
    n:int
        Addons to do.
    condition_for_vertex:
        not used
    Returns
    -------
    List of vertex for addons.
    """
    assert len(ADJ.shape)==2
    assert ADJ.shape[0]==ADJ.shape[1]
    assert ADJ.shape[0]%2==0
    natoms=ADJ.shape[0]
    assert isinstance(n,int), "`n` must be an integer and n>=1 !"
    if mask is None:
        mask=[]
    if searched is None:
        searched=[]
    else:
        searched=searched
    if n>1:
        for item in get_vertex_class_lists(ADJ,mask):
            # iter for each class of vertex
            ADJ_use = ADJ.copy()

            addonlist=[]
            addoni=min(item)
            ADJ_use[addoni,:]=0
            ADJ_use[:,addoni]=0
            addonlist.append(addoni)
            for subaddons in search_addon(ADJ_use,n-1,mask=[*mask,addoni],searched=searched):
                yield [addoni,*subaddons]
            searched.extend(item)

    elif n==1:
        for item in get_vertex_class_lists(ADJ,mask):
            result=min(item)
            if result not in searched:
                yield [min(item)]
            else:
                pass
    else:
        raise RuntimeError("Unkown error in searching addons of cages, got n<=0!")




def get_vertex_class_lists(ADJ,mask:list):
    natoms=ADJ.shape[0]
    nocc=int(natoms/2)
    p = np.zeros([natoms, natoms])
    val,vec = np.linalg.eigh(ADJ)

    for i in range(natoms):
        for j in range(natoms):
            for l in range(nocc):
                p[i][j] += 2 * vec[i][l] * vec[j][l]

    cc = np.array([np.sort(np.array(list(i))) for i in np.round(p * ADJ, 8)])
    cc_norm = np.linalg.norm(cc, axis=-1)
    cc_mat = (cc[None, :, :] * cc[:, None, :]).sum(-1) / ((cc_norm[None, :] * cc_norm[:, None])+0.001)

    vertex_class = np.unique(cc_mat, axis=-1, return_index=True, return_inverse=True)
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
    from fullerenedatapraser.io.xyz import simple_read_xyz_xtb
    from fullerenedatapraser.molecular.fullerene import FullereneFamily
    from ase.visualize import view

    np.set_printoptions(threshold=np.inf)
    np.set_printoptions(linewidth=500)

    atoms = list(simple_read_xyz_xtb(r"C:\Work\CODE\DATA\fullerxTBcal\xTBcal\opted\C60\C60_000001812opted.xyz"))[-1]

    # view(atoms)

    f = FullereneFamily(spiral=1812, atoms=atoms)
    f = f.get_fullerenecage()
    D = f.atomADJ
    # D[1,:]=0
    # D[:,1]=0
    # for i in range(3,60):
    #     D[i,:]=0
    #     D[:,i]=0
    # print(D)
    # [print(item) for item in get_vertex_class_lists(D,mask=[])]
    addonslist=search_addon(D,4)
    for position in addonslist:
        print(position)
