# daria-lash.com tooling

- Source of truth: this repo (github.com/marino143/beauty-by-daria). cPanel account `lbdaria` pulls it into
  `~/repositories/beauty-by-daria` and `.cpanel.yml` copies files into `public_html`.
- Deploy: commit, then `tools/deploy.sh` (push + cPanel pull + deploy). Token: `~/.openclaw/secrets/daria-lash/cpanel.env`
  (expires 2027-11-17). Use host s040.cubrad.eu:2083; cpanel.codigit.hr has an expired certificate.
- Service pages are generated: `python3 tools/gen_pages.py` (reads prices from index.html). New top-level dirs must be
  added to `.cpanel.yml`.
- Bazna cijena (Pravilnik NN 132/2026): on a price change publish a NEW CSV in `cjenik/` by 11:00 that day, named
  `99025973_27718974341_Kozmeticki_salon_Obrez_20_Sesvete-Soblinec_Beauty_by_Daria_1_USLUGE_1_GGGGMMDD_SSMM.csv`,
  columns `naziv;maloprodajna;posebni oblik;bazna`, UTF-8, `;`. Update links in index.html, en/, de/, cjenik/index.html;
  keep the replaced CSV for 15 days.
