/* Offline support for the installed app: keeps the app and its PDF/Excel tools on the phone */
const CACHE = "raviraja-v10";
const SHELL = ["./", "./index.html", "./manifest.webmanifest", "./icon-192.png", "./icon-512.png", "./icon-180.png"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const req = e.request, url = new URL(req.url);
  const lib = url.origin === location.origin || /^(cdnjs\.cloudflare\.com|fonts\.(googleapis|gstatic)\.com)$/.test(url.hostname) || (url.hostname === "www.gstatic.com" && url.pathname.startsWith("/firebasejs/"));
  if (req.method !== "GET" || !lib || url.pathname.startsWith("/api/")) return;    // never cache live data (cloud database, sign-in)
  if (req.mode === "navigate") {                                                    // app page: network first, offline fallback
    e.respondWith(fetch(req).then(r => { const c = r.clone(); caches.open(CACHE).then(x => x.put("./index.html", c)); return r; })
      .catch(() => caches.match("./index.html")));
    return;
  }
  e.respondWith(caches.match(req).then(hit => {                                     // libraries, fonts, icons: cache first
    const net = fetch(req).then(r => { if (r.ok || r.type === "opaque") { const c = r.clone(); caches.open(CACHE).then(x => x.put(req, c)); } return r; }).catch(() => hit);
    return hit || net;
  }));
});
