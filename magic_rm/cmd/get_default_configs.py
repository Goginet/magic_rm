#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Author Georgy Schapchits <gogi.soft.gm@gmail.com>.

def get_default_config_toml():
    return '''
[remove]
    # force = true
    # interactive = true
    # recursive = true
    # empty_dir = true
    # no_remove = true

    ### File retention time in the trash
    ### formats: P1Y1M1D (1 year, 1 month, 1 day), PT1H1M1S (1 hour, 1 minute, 1 sec)
    # retention = P1D

[restore]
    # force = true

[logger]
    log_level = "ERROR"
    verbose_level = "WARNING"
    mode = "JSON"
    file_path = "magic_rm.log"

[trash]
    # no_trash = true
    path = "trash"
'''

def get_default_config_json():
    return '''
{
    "remove": {
        // "force": true,
        // "interactive": true,
        // "recursive": true,
        // "empty_dir": true,
        // "no_remove": true,
        // "retention": "P1D"
    },
    "restore": {
        // "force": true
    },
    "logger": {
        "log_level": "ERROR",
        "verbose_level": "WARNING",
        "mode": "JSON",
        "file_path": "magic_rm.log"
    },
    "trash": {
        // "no_trash": true,
        "path": "trash",
    }
}
'''