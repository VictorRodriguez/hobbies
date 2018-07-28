#!/usr/bin/env bats
# *-*- Mode: sh; c-basic-offset: 8; indent-tabs-mode: nil -*-*

@test "gdb coredump" {
    rm -rf /tmp/corefile-*
    rm -rf log.txt
    gcc -g main.c -o main
    ./main || :
    FILE=$(ls /tmp/corefile*)
    gdb ./main "$FILE" -x gdb_script.txt | grep "main.c:5"
    rm -rf /tmp/corefile-*
    rm -rf log.txt
    rm -rf main
}

