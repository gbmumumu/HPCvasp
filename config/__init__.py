#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from utils.spath import SPath

_config_root = SPath(os.path.abspath(__file__)).parent
_condor = _config_root / "condor.ini"
_workflow = _config_root / "workflow.json"

CONDOR = _condor.read_ini()
WORKFLOW = _workflow.read_json()

if __name__ == '__main__':
    pass
