# HPCvasp
## A simple High-throughput calculation tool for vasp and supposed to running on tianhe2 HPC
    you can set calculation type in config/workflow.json;
    vasp software path and other env can set in config/condor.ini
    then just run "python vasp.py --process $num_of_process --qsize $num_of_qsize" and --other paras, or, if you write all paras in config, you can just use "python vasp.py" to run.
