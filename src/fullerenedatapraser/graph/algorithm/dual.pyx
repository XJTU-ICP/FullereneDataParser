# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : dual.pyx
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

import numpy as np
cimport numpy as np
cimport cython

DTYPE = int
ctypedef np.int_t DTYPE_t

def dual(np.ndarray[DTYPE_t, ndim=2] D,
         int M,
         int N):
    return c_dual(D, M, N)

@cython.boundscheck(False)
@cython.nonecheck(False)
cdef  c_dual(np.ndarray[DTYPE_t, ndim=2] D,
             int M,
             int N):
    cdef np.ndarray[DTYPE_t, ndim = 2] V
    cdef np.ndarray[DTYPE_t, ndim= 2] A
    cdef int I = 0
    cdef int L, K, J
    cdef int IER
    cdef int JJ, II
    V = np.zeros((N, N), dtype=int)
    A = np.zeros((N, N), dtype=int)
    for L in range(M):
        for K in range(L):
            if D[K, L] == 0:
                continue
            for J in range(K):
                if D[J, K] == 0 or D[J, L] == 0:
                    continue
                if I + 1 > N:
                    continue
                V[0, I] = J
                V[1, I] = K
                V[2, I] = L
                I += 1
    IER = I - N
    print(IER, I, N, V)
    if IER != 0:
        raise BaseException

    for J in range(N):
        for I in range(J):
            K = 0
            for JJ in range(3):
                for II in range(3):
                    if V[II, I] == V[JJ, J]:
                        K += 1
            if K == 2:
                A[I, J] = 1
                A[J, I] = 1
    return A
