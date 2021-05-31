#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import pathlib
import shutil
import os
import yaml
import json


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

    def copy_to(self, des):
        if not isinstance(des, SPath):
            des = SPath(des)
        assert self.is_file() and not self.is_empty()
        if self.parent == des.parent:
            have = list(self.parent.rglob(des.name + '*'))
            if have:
                n = len(have)
                des.rename(f"{self.parent / des.name}_{n}")
        try:
            shutil.copy(str(self), str(des))
        except shutil.SameFileError:
            return

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

    def read_json(self):
        if ".json" == self.suffix:
            with self.open() as f:
                return json.load(f)
        return None

    def _read_ini(self):
        if ".ini" == self.suffix:
            configs = configparser.ConfigParser()
            configs.read(str(self))
            return configs
        return None

    def get_configs_from_ini(self, section, option, dtype=""):
        cfg = self._read_ini()
        if cfg is not None:
            if not dtype:
                return cfg.get(section, option)
            elif cfg == "int":
                return cfg.getint(section, option)
            elif cfg == "float":
                return cfg.getfloat(section, option)
            elif cfg == "boolean":
                return cfg.getboolean(section, option)
            else:
                raise TypeError
        return None

    def read_yaml(self):
        if self.suffix == ".yaml":
            configs = yaml.safe_load(self.open().read())
            return configs
        return None


if __name__ == "__main__":
    pass
