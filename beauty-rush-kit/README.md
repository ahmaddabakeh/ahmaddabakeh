# Beauty Rush logo kit — handover notes

## What's in the folder
| Folder | Contents |
|---|---|
| `logo/` | Horizontal, stacked and BR monogram. Each comes in black, white, pink (`mono-f5b8c9`), burgundy (`mono-6b1f35`), on-pink and on-black versions, as SVG and high-resolution PNG. |
| `social/` | **`tiktok-profile-split.png`** (chosen profile picture: BEAUTY in black on pink, RUSH in pink on a black band, 1080 × 1080, readable from 32 px up). Alternates: `tiktok-profile.png` (BR) and `tiktok-profile-full-name.png`, each with a black version. Plus `live-banner-1920x1080.png`. |
| `web/` | `favicon.ico`, favicon and app-icon PNGs, `apple-touch-icon.png`, `site.webmanifest`, and `head-snippet.html` to paste into your website's `<head>`. |
| `presentation/` | `board.html`, the final identity board with mockups (social profile, mailer box, shopping bag, sticker, t-shirt, signage), and `board-full.png`. |
| `BRAND-GUIDELINES.md` | One-page usage guide: clear space, minimum sizes, colours, fonts and don'ts. |
| `source/` | Python scripts that rebuild every master from the Montserrat font file. |

## Design rationale
- A type-only wordmark in the spirit of the big beauty houses: confident and simple, with no clip-art.
- Candy pink and black own the TikTok feed and read at a glance on Live graphics.
- The BR monogram carries the brand where the full name would be too small.

## Test results (logo-design skill)
- `svg_audit.py`:
  - BR monogram: 99/100
  - App icon and favicon: 100/100
  - Horizontal and stacked: 91/100
- The only flag on the wordmarks is Montserrat's **Y**, whose arms are drawn about 1° off 60°. That's how the typeface designer drew it. Snapping it would make the Y inconsistent with the other letters, so it's left as designed.
- `preview_sheet.py`:
  - BR stays legible at 16 px.
  - Horizontal and stacked read from 32 px up.
  - Black, white, one-colour and pink versions all hold up.
- All masters are outlined vector paths: no live text, rasters, filters or masks.

## Open items
- **Trademark:** this kit doesn't include a trademark clearance. Before you print packaging, run a search for "Beauty Rush" in your country's trademark database (USPTO in the US) and do a reverse image search.
- **Ownability:** the wordmark is set in a stock font, so it's simple but easy to imitate. A subtle custom detail, such as a sharper R leg or a joined SH, would make it more distinctive and easier to protect.
- **Print colours:** get a printed proof of Candy Pink before large runs. Pinks shift a lot between printers.
- **Social handle:** the board's social mockup shows "@beautyrush" as a placeholder.
