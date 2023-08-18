#!/bin/bash

if [ ! -d .venv/ ]; then
    python -m venv ./.venv
    source .venv/bin/activate
    pip install -r requirements.txt
fi

sudo cp checktec.service /etc/systemd/system/checktec.service
sudo systemctl daemon-reload
sudo systemctl enable --now checktec.service
