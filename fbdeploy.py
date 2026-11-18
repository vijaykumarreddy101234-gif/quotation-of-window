#!/usr/bin/env python3
"""Publish this folder to Firebase Hosting (site raviraja-quotations) using the gcloud login. Run in Cloud Shell."""
import gzip, hashlib, json, os, subprocess, sys, urllib.request
SITE = "raviraja-quotations"; API = "https://firebasehosting.googleapis.com/v1beta1/"
TOK = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode().strip()
H = {"Authorization": "Bearer " + TOK, "X-Goog-User-Project": SITE}
def call(method, url, body=None, raw=None, ctype="application/json"):
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    r = urllib.request.Request(url, data=data, method=method, headers={**H, "Content-Type": ctype})
    try:
        with urllib.request.urlopen(r) as f: t = f.read().decode(); return json.loads(t) if t.strip() else {}
    except urllib.error.HTTPError as e: print("HTTP", e.code, url, e.read().decode()[:800]); sys.exit(1)
root = sys.argv[1] if len(sys.argv) > 1 else "."
files = {}
for n in ["index.html", "manifest.webmanifest", "sw.js", "icon-180.png", "icon-192.png", "icon-512.png"]:
    gz = gzip.compress(open(os.path.join(root, n), "rb").read(), mtime=0); files["/" + n] = (hashlib.sha256(gz).hexdigest(), gz)
cfg = {"headers": [{"glob": "**/*.@(html|js|webmanifest)", "headers": {"Cache-Control": "no-cache"}}]}
v = call("POST", API + f"sites/{SITE}/versions", {"config": cfg})["name"]; print("version", v)
p = call("POST", API + v + ":populateFiles", {"files": {k: h for k, (h, _) in files.items()}})
need = set(p.get("uploadRequiredHashes", [])); up = p.get("uploadUrl")
for k, (h, gz) in files.items():
    if h in need: call("POST", up + "/" + h, raw=gz, ctype="application/octet-stream"); print("uploaded", k)
call("PATCH", API + v + "?update_mask=status", {"status": "FINALIZED"})
call("POST", API + f"sites/{SITE}/releases?versionName=" + v, {})
print("RR_DEPLOY_OK https://raviraja-quotations.web.app  https://raviraja-quotations.firebaseapp.com")
