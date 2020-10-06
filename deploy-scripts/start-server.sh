#!/usr/bin/env bash
cd $DEPLOY_DIR
python manage runserver 127.0.0.1:9010 &
