#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from utils.spath import SPath


class _Lattice:
    def __init__(self, latt):
        self._latt = np.around(
            np.asarray(latt).reshape((3, 3)), decimals=6
        )

    def get_latt_len(self):
        return [np.linalg.norm(x) for x in self._latt]

    @property
    def a(self):
        return self.get_latt_len()[0]

    @property
    def b(self):
        return self.get_latt_len()[1]

    @property
    def c(self):
        return self.get_latt_len()[2]

    @property
    def lattice(self):
        return self._latt

    @property
    def inv_lattice(self):
        return np.linalg.inv(self._latt)

    def get_cart_coords(self, frac_coords):
        return np.dot(np.array(frac_coords), self._latt)

    def get_frac_coords(self, cart_coords):
        return np.dot(np.array(cart_coords), self.inv_lattice())

    def reciprocal_lattice(self):
        return _Lattice(2 * np.pi * np.linalg.inv(self._latt).T)

    def reciprocal_lattice_crystallographic(self):
        return _Lattice(self.reciprocal_lattice().lattice / (2 * np.pi))


class POSCAR:
    def __init__(self, title='', scale=1.0,
                 lattice=None, coords=None, is_cart=True):
        pass

    @classmethod
    def from_file(cls, filepath: SPath, **kwargs):
        for line in filepath.readline_text(**kwargs):
            pass


if __name__ == '__main__':
    pass
