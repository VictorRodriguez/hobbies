#!/usr/bin/env bash
echo 1 > /proc/sys/kernel/sysrq
date
echo b > /proc/sysrq-trigger

