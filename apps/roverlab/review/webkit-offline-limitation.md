# WebKit offline verification limitation

The installed macOS WebKit 2359 runner completes the three mission journeys, rule-driven failure, save/continue/reset, and relay-link checks. Its default keyboard behavior requires Option+Tab to reach links/buttons; the suite follows that native convention when plain Tab leaves the document body focused.

Direct opening of `public/index.html` works with all HTTP and HTTPS requests blocked. This verifies that the local game has no required external network dependency.

Hosted offline reload remains **unverified in WebKit**. Two targeted runs reached an active service-worker controller and confirmed all nine core resources in `roverlab-v1`, including `index.html`, scripts, styles, icon, font, and manifest. Calling Playwright `context.setOffline(true)` followed by `page.reload()` nevertheless returned:

```text
page.reload: WebKit encountered an internal error
```

The same automated offline setting also blocks a direct `file://` navigation before the app runs. The evidence points to a limitation of this local automated WebKit setup, but does not establish offline Safari compatibility. Chromium passes hosted offline reload both locally and on the production URL.

The default browser suite continues to attempt this check. To run the remaining WebKit checks while preserving the limitation explicitly in its report, set `ROVERLAB_SKIP_WEBKIT_OFFLINE=1`; the result is recorded as **SKIPPED**, never passed. No browser installation or operating-system network change was performed.
