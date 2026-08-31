# Joins on UEI  ·  2 datasets, 1 links

```mermaid
erDiagram
  FED_USASPENDING_CONTRACTS {
    col COUNTRY
    col NAICS
    col NAME
    id UEI
    col ZIP
  }
  PORTAL_SOC_TEXAS_OPEN_DATA_B8DDC96BFF {
    id UEI
  }
  FED_USASPENDING_CONTRACTS }o--o{ PORTAL_SOC_TEXAS_OPEN_DATA_B8DDC96BFF : "7"
```
