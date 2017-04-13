#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Author Georgy Schapchits <gogi.soft.gm@gmail.com>.

def get_default_config_toml():
    return '''
[general]
    ## Show progress for long operations
    progress = true

    ## Ignore all errors
    # force=true

[remove]
    ## Follow the symlinks
    # symlinks = true

    ## Not save removed elements in trash dir
    # no_trash = true

    ## Recursive remove the dir
    # recursive = true

    ## Regexp template for removed files
    # regexp = ".*"

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
    "general: {
        "progress": true,
        "force": true,
    },
    "remove": {
        "regexp": null,
        "symlinks": true,
        "no_trash": false,
        "recursive": true,
        "empty_dir": true,
        "retention": "P1D"
    },
    "restore": {
        "conflict_resolve": "SKIP"
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