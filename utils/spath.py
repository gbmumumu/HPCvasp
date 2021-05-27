#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
import os

import pandas


class SPath(type(pathlib.Path())):
    def rm_file(self):
        assert self.is_file() and self.exists()
        self.unlink()

    def force_rmdir(self):
        assert self.exists()
        try:
            self.rmdir()
        except OSError:
            for i in self.rglob("*"):
                if i.is_dir():
                    i.force_rmdir()
                else:
                    i.unlink()
        else:
            return
        finally:
            self.rmdir()

    def copy(self, des):
        import shutil

        if not isinstance(des, SPath):
            des = SPath(des)
        assert self.is_file()
        try:
            shutil.copy(str(self), str(des))
        except shutil.SameFileError:
            return
        if self.parent == des.parent:
            have = list(self.parent.rglob(self.name))
            if have:
                n = len(have)
                self.rename(f"{self.parent / self.name}_{n}")
        return

    def walk(self, pattern='*', depth=1, is_file=True):
        assert self.is_dir()

        for j in self.rglob(pattern):
            if len(j.parts) == len(self.parts) + depth:
                if all([is_file, j.is_file()]) or all([not is_file, not j.is_file()]):
                    yield j

    def readline_text(self, encoding='utf-8', errors='ignore'):
        with self.open(mode='r', encoding=encoding, errors=errors) as f:
            for line in f:
                yield line.strip('\n')

    def add_to_text(self, data, encoding='utf-8', errors='ignore'):
        if not isinstance(data, str):
            raise TypeError('data must be str, not %s' %
                            data.__class__.__name__)
        with self.open(mode='a+', encoding=encoding, errors=errors) as f:
            if not data.endswith('\n'):
                data += '\n'
            return f.write(data)

    def is_empty(self):
        return os.path.getsize(self) == 0






if __name__ == "__main__":
    pass
