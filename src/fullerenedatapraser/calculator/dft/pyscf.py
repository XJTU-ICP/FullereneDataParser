# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : pyscf.py
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

import numpy
import numpy as np

from pyscf import gto

mol = gto.M(atom='O 0 0 0; h 0 -0.757 0.587; h 0 0.757 0.587', basis='cc-pvdz')
auxmol = gto.M(atom='O 0 0 0; h 0 -0.757 0.587; h 0 0.757 0.587', basis='weigend')
pmol = mol + auxmol
nao = mol.nao_nr()
naux = auxmol.nao_nr()
eri3c = numpy.empty((nao, nao, naux))
pi = 0
for i in range(mol.nbas):
    pj = 0
    for j in range(mol.nbas):
        pk = 0
        for k in range(mol.nbas, mol.nbas + auxmol.nbas):
            shls = (i, j, k)
            buf = pmol.intor_by_shell('int3c2e_sph', shls)
            di, dj, dk = buf.shape
            eri3c[pi:pi + di, pj:pj + dj, pk:pk + dk] = buf
            pk += dk
        pj += dj
    pi += di

eri2c = numpy.empty((naux, naux))
pk = 0
for k in range(mol.nbas, mol.nbas + auxmol.nbas):
    pl = 0
    for l in range(mol.nbas, mol.nbas + auxmol.nbas):
        shls = (k, l)
        buf = pmol.intor_by_shell('int2c2e_sph', shls)
        dk, dl = buf.shape
        eri2c[pk:pk + dk, pl:pl + dl] = buf
        pl += dl
    pk += dk


def get_vhf(mol, dm, *args, **kwargs):
    naux = eri2c.shape[0]
    nao = mol.nao_nr()
    rho = numpy.einsum('ijp,ij->p', eri3c, dm)
    rho = numpy.linalg.solve(eri2c, rho)
    jmat = numpy.einsum('p,ijp->ij', rho, eri3c)
    kpj = numpy.einsum('ijp,jk->ikp', eri3c, dm)
    pik = numpy.linalg.solve(eri2c, kpj.reshape(-1, naux).T)
    kmat = numpy.einsum('pik,kjp->ij', pik.reshape(naux, nao, nao), eri3c)
    return jmat - kmat * .5


mf = scf.RHF(mol)
mf.verbose = 0
mf.get_veff = get_vhf
print('E(DF-HF) = %.12f, ref = %.12f' % (mf.kernel(), scf.density_fit(mf).kernel()))
