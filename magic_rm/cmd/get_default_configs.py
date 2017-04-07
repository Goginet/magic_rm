#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Author Georgy Schapchits <gogi.soft.gm@gmail.com>.

def get_default_config_toml():
    return '''
[remove]
    ## Follow the symlinks
    # symlinks = true

    ## Recursive remove the dir
    # recursive = true

    ## Remove empty dir
    # empty_dir = true

    ### File retention time in the trash
    ### formats: P1Y1M1D (1 year, 1 month, 1 day), PT1H1M1S (1 hour, 1 minute, 1 sec)
    # retention = P1D

[restore]
    ## Police for resolve conflict (REPLACE|SKIP)
    conflict_resolve="SKIP"

[logger]
    ## Logging level (DEBUG|INFO|WARNING|ERROR)
    log_level = "DEBUG"

    ## Verbose level (DEBUG|INFO|WARNING|ERROR)
    verbose_level = "DEBUG"

    ## Logger format (JSON|TOML)
    mode = "JSON"

    ## Log file path
    file_path = "magic_rm.log"

[trash]
    ## Path to the trash dir
    path = "trash"
'''

def get_default_config_json():
    return '''
{
    "remove": {
        "symlinks": true,
        "recursive": true,
        "empty_dir": true,
        "retention": "P1D"
    },
    "restore": {
        "conflict_resolve": true
    },
    "logger": {
        "log_level": "DEBUG",
        "verbose_level": "DEBUG",
        "mode": "JSON",
        "file_path": "magic_rm.log"
    },
    "trash": {
        "path": "trash",
    }
}
'''