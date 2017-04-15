#!/bin/bash
# Description: This script ...
#
# Copyright (C) 2016 Synesis LLC. All rights reserved.
# Author Georgy Schapchits <georgy.schapchits@synesis.ru>, Synesis LLC www.synesis.ru.

NAME=magicrm

mkdir -p /etc/${NAME}/
mkdir -p /var/lib/${NAME}/
mkdir -p /var/log/${NAME}/

cp configs/default.conf /etc/${NAME}/${NAME}.conf
touch /var/log/${NAME}/${NAME}.log

chmod 666 /var/log/${NAME}/${NAME}.log
chmod -R 777 /var/lib/${NAME}