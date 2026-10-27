# Beauty Rush — Logo Guidelines

## 1. The logo
- **Idea:** heavy black capitals on candy pink. Simple, loud and instantly recognisable on a TikTok Live, and confident enough to sit next to the beauty brands you sell.
- **Versions:**
  - **Horizontal** (main logo): website, Live banners, signage, email.
  - **Stacked:** square spaces such as mailer boxes, shipping inserts, stickers and merch.
  - **BR monogram:** TikTok profile picture, favicon, app icon, and anywhere under 64 px.
- **Files:**
  - `logo/*.svg` for screens and printers. They're vector, so they scale to any size.
  - `logo/*.png` for quick use in apps and Canva.
  - `social/` for the TikTok profile picture and Live banner.
  - `web/` for website icons.

## 2. Clear space
Keep empty space around the logo equal to **half the height of the capital letters** on every side. The space grows and shrinks with the logo. Never place text, stickers or graphics inside it.

## 3. Minimum size
| Version | Screen | Print |
|---|---|---|
| Horizontal | 120 px wide | 30 mm wide |
| Stacked | 64 px wide | 18 mm wide |
| BR monogram | 16 px (use `web/favicon.svg`) | 6 mm |

Below these sizes, switch to the BR monogram.

## 4. Colour
| Name | HEX | RGB | CMYK (approx.) | Pantone (nearest, approx.) |
|---|---|---|---|---|
| Candy Pink | #F5B8C9 | 245 184 201 | 0 25 18 4 | 182 C |
| Ink Black | #141012 | 20 16 18 | 60 40 40 100 (rich black) | Black 6 C |
| White | #FFFFFF | 255 255 255 | 0 0 0 0 | — |
| Burgundy (accent) | #6B1F35 | 107 31 53 | 0 71 51 58 | 7421 C |

The CMYK and Pantone values are starting points. Ask your printer for a printed proof before a large run.

**Approved logo and background pairs**, with contrast ratios:
- Ink Black on Candy Pink (main pairing): 11.3:1
- Ink Black on White: 18.9:1
- Candy Pink on Ink Black: 11.3:1
- Burgundy on Candy Pink: 6.7:1, for accents and secondary packaging
- White on Ink Black or on Burgundy

On photos, use the black or white version on a calm area, or place the logo on a solid Candy Pink panel.

## 5. Typography
- **Logo:** Montserrat ExtraBold, converted to outlines. Never retype the logo; always use the files.
- **Headlines on graphics:** Montserrat ExtraBold or Black, all capitals.
- **Body text:** Montserrat Regular or Medium.
- **Licence:** Montserrat is under the SIL Open Font License. It's free for commercial and logo use and downloads from Google Fonts.

## 6. Don'ts
Don't:
- stretch, squash or rotate the logo
- recolour it outside the palette, or use pink on white (too little contrast)
- add shadows, outlines, gradients, glitter or other effects
- rearrange BEAUTY and RUSH, or change the spacing
- place it on busy backgrounds without a pink or black panel
- recreate the wordmark by typing it

## 7. Master files
Master SVGs are in `logo/`. The `source/` folder holds the scripts that generated them, so the files can be rebuilt exactly.
