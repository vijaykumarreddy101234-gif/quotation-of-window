#!/bin/bash
# Publishes this app to Firebase Hosting. Run in Google Cloud Shell (after gcloud auth login).
set -e
rm -rf ~/rrsite && git clone -q -b gh-pages https://github.com/vijaykumarreddy101234-gif/quotation-of-window.git ~/rrsite
python3 ~/rrsite/fbdeploy.py ~/rrsite
