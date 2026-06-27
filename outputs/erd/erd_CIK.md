# Joins on CIK  ·  2 datasets, 1 links

```mermaid
erDiagram
  FED_SEC_EDGAR_COMPANY_TICKERS {
    id CIK
  }
  FED_SEC_EDGAR_FINANCIALS {
    id CIK
    id EIN
    col NAME
    col SIC
  }
  FED_SEC_EDGAR_COMPANY_TICKERS }o--o{ FED_SEC_EDGAR_FINANCIALS : "4,822"
```
