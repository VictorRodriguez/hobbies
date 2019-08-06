#!/usr/bin/env bash

# Redirect stdout ( > ) into a named pipe ( >() ) running "tee"
exec > >(tee -i logfile.txt)

# Without this, only stdout would be captured - i.e. your
# log file would not contain any error messages.
exec 2>&1

ssh -p 2222 root@127.0.0.1 'date'
ssh -p 2222 root@127.0.0.1 'echo 1 > /proc/sys/kernel/sysrq'
ssh -p 2222 root@127.0.0.1 'echo b > /proc/sysrq-trigger'


