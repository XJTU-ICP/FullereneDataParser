# -*- coding: utf-8 -*-
# ====================================== #
# @Author  : Yanbo Han
# @Email   : yanbohan98@gmail.com
# @File    : dual.pyx
# ALL RIGHTS ARE RESERVED UNLESS STATED.
# ====================================== #

from libc.stdlib cimport free
import numpy as np

cimport

cimport
import numpy as np
from libc.stdlib cimport

free
numpy as np
import numpy as np
from libc.stdlib cimport

free

DTYPE = int
ctypedef np.int_t DTYPE_t


cdef extern from "planar_dual.hpp" namespace "dualgraph":
    cdef cppclass dual_graph_generator:
        int origin_size
        int *edge_origin
        int dual_size
        dual_graph_generator(int size, int* edge_origin) except +
        void privacy_get_graph_edge_num()
        int * privacy_get_dual_edges(int dual_size)

cdef extern from "planar_dual.cpp":
    pass

cdef class py_dual_graph_generator:
    cdef dual_graph_generator *c_dener
    cdef void * _data

    def __cinit__(self, int size, int[:,:] edge_origin):
        self.c_dener = new dual_graph_generator(size, &edge_origin[0,0])
    def __dealloc__(self):
        if self._data != NULL:
            free(self._data)

    def privacy_get_graph_edge_num(self):
        self.c_dener.privacy_get_graph_edge_num()

    def privacy_get_dual_edges(self, int dual_size):
        # cdef int[:] Y = np.zeros([dual_size*2],dtype=int)
        Y=np.asarray(<int[:dual_size,:2]> self.c_dener.privacy_get_dual_edges(dual_size))
        # np.set_array_base(Y,self)
        return Y

    def _privacy_get_dual_edges(self):
        dual_size=self.c_dener.dual_size
        # cdef int[:] Y = np.zeros([dual_size*2],dtype=int)
        Y=np.asarray(<int[:dual_size,:2]> self.c_dener.privacy_get_dual_edges(dual_size))
        # np.set_array_base(Y,self)
        return Y

    @property
    def origin_size(self):
        return self.c_dener.origin_size
    @property
    def dual_size(self):
        return self.c_dener.dual_size
