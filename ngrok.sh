#!/bin/bash

systemctl start httpd
systemctl restart httpd
ngrok http 5000

