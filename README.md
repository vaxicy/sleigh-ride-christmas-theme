# Sleigh Ride Christmas Theme

Version 1.0.0. Pine green #244C3D and warm cream #F7EEDF, with static Santa sleigh artwork above the native Google logo. The approved GPT-generated icon is a red sleigh carrying one gift, exported only as logo/logo128.png.

Load this root folder from chrome://extensions with Developer mode enabled. The manifest references ordinary and high-DPI background PNGs in images/.

Store assets include two 1280×800 screenshots and promo tiles at 440×280 and 1400×560. The first screenshot retains the real installed Chrome tab, address bar and native Chinese interface. Personal bookmarks, extension icons and avatars are covered with matching background colors; the page avatar area follows the original gradient row by row. The full image is scaled proportionally and padded with theme green. The introduction is an English HTML/CSS render. The store generator preserves the native screenshot instead of overwriting it.

The wide promo embeds the same cleaned real screenshot; its surrounding copy remains English. The small promo uses the approved sleigh icon. The introduction background #E6E9EC is outside the theme palette. Source artwork is in source/. Logo candidate contact sheet is in logo-candidates/. Store listing copy is in store-assets/store-description.txt.

Run scripts/generate-store-assets.py with Pillow, Playwright and installed Chromium to regenerate the icon and store artwork. The script uses locally installed Chromium. Logo generation used the built-in image generator with the selected concept 1 reference and the prompt to produce a standalone transparent red sleigh, cream gift and gold bow and runners.
