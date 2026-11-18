# Al-Bahaar website (rebuild)

Static rebuild of www.albahaar.com — plain HTML/CSS/JS, no build step.

| File | Purpose |
|---|---|
| `index.html` | Home: hero, hours, story, highlights, popular dishes, reviews, reservations |
| `menu.html` | Full menu (12 categories, 95 items) with sticky category tabs |
| `about.html` | Story, Ismail family, Chef Mahmoud, private events, reviews |
| `contact.html` | Contact info, inquiry form (opens email), FAQ, map |
| `privacy.html` | Privacy policy |
| `menu-data.js` | **Edit prices/dishes here** — all menu content |
| `site.js` | Shared header, footer, reviews, reservation block, contact details & hours (`SITE`) |
| `styles.css` | Theme (colors/fonts in `:root`) |

Images still load from the current Webflow CDN; download them into `albahaar/images/` before the old site is shut down.

Preview locally: `python3 -m http.server -d albahaar 8000`, then open http://localhost:8000.
