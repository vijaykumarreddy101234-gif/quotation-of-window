#!/bin/bash
# Publishes this app to Firebase Hosting (raviraja-quotations.web.app / .firebaseapp.com). Run in Google Cloud Shell.
set -e
rm -rf ~/rrsite && git clone -q -b gh-pages https://github.com/vijaykumarreddy101234-gif/quotation-of-window.git ~/rrsite && cd ~/rrsite
cat > firebase.json <<'J'
{"hosting":{"public":".","ignore":["firebase.json","fb.sh","**/.*","README.md","firestore.rules"],
 "headers":[{"source":"**/*.@(html|js|webmanifest)","headers":[{"key":"Cache-Control","value":"no-cache"}]}]}}
J
firebase --version
firebase deploy --only hosting --project raviraja-quotations --non-interactive && echo "RR_DEPLOY_OK"
