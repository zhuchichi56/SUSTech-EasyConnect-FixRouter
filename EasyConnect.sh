#!/usr/bin/expect
set timeout 10

spawn sudo python fixRouter.py
expect "password:"
send "xxxxxxxx\r"
interact

