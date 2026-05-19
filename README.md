# pandemics-tracking

Hand-curated catalog of major pandemics and epidemics from antiquity to present, parallel in spirit to `earthquakes`, `spaceweather`, `famines-tracking`, and `flood-data`.

## What's in it

`pandemics.csv` — ~36 major events with columns:

- `start_year`, `end_year` — duration; deaths spread evenly across years for active-deaths analyses
- `name` — common scholarly designation
- `region`
- `deaths_estimate` — published consensus where one exists, otherwise scholarly midpoint
- `sources_notes` — source author or attribution

Coverage: Plague of Athens (430 BC) → mpox (2022). Includes the major plague pandemics, cholera pandemics (1817–1923 numbered 1–6), flu pandemics (1889, 1918, 1957, 1968, 1976, 2009), HIV/AIDS, COVID-19, and notable regional epidemics like the 1545 Cocoliztli outbreak in Mesoamerica.

## Detection-bias caveats

| Era | Catalog completeness |
|---|---|
| Pre-1500 | Anecdotal — only the very largest and best-attested events. Death tolls are orders of magnitude. |
| 1500–1850 | Concentrated on European and Eastern Mediterranean events; non-Western pandemics underrepresented. |
| 1850–1950 | Improving with germ theory and global health institutions. Cholera pandemics are well-documented. |
| 1950–present | WHO-monitored; near-complete for events killing ≥1000 globally. |

Treat any cross-era comparison with these caveats in mind. For statistical work, the same regime-based detrending applied in the `correlations` repo applies here.

## Sources

Compiled from:
- Hays, J. N. (2005). *Epidemics and Pandemics: Their Impacts on Human History.*
- Snowden, F. M. (2019). *Epidemics and Society: From the Black Death to the Present.*
- WHO disease outbreak news (https://www.who.int/emergencies/disease-outbreak-news)
- Our World in Data pandemic mortality dataset (https://ourworldindata.org/pandemics)
- Acuña-Soto, R. et al. (2002). *Megadrought and megadeath in 16th century Mexico.* Emerging Infectious Diseases.
- Fenn, E. A. (2001). *Pox Americana: The Great Smallpox Epidemic of 1775–82.*

Death-toll estimates differ widely across sources for pre-1900 events; this CSV uses scholarly midpoint estimates. For active research, consult Our World in Data's underlying dataset.

## Intended use

This repo is the data source for the pandemic correlation tests in [`Biblejustin/correlations`](https://github.com/Biblejustin/correlations).
