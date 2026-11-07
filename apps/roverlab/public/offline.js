/* Optional offline support. Direct file opening needs no service worker. */
(function () {
  'use strict';
  if (/^(https?:)$/.test(location.protocol)) {
    const manifest = document.createElement('link');
    manifest.rel = 'manifest';
    manifest.href = './manifest.webmanifest';
    document.head.appendChild(manifest);
  }
  if ('serviceWorker' in navigator && /^(https?:)$/.test(location.protocol)) {
    window.addEventListener('load', function () {
      navigator.serviceWorker.register('./sw.js', { updateViaCache: 'none' }).catch(function () {
        // Private browsing or unsupported hosting must never stop the game.
      });
    });
  }
}());
