"""Compare EIA source workbook sheets (f8612024.zip) with warehouse pulls (out_S02..S06.csv)."""
import zipfile, io, pandas as pd
z = zipfile.ZipFile('f8612024.zip')
spec = {
 'Distribution_Systems_2024.xlsx': ('out_S02.csv', 0),
 'Utility_Data_2024.xlsx': ('out_S03.csv', 1),
 'Dynamic_Pricing_2024.xlsx': ('out_S04.csv', 2),
 'Net_Metering_2024.xlsx': ('out_S05.csv', 2),
 'Non_Net_Metering_Distributed_2024.xlsx': ('out_S06.csv', 1),
}
for f, (csvf, hdr) in spec.items():
    w = pd.read_csv(csvf, low_memory=False)
    x = pd.ExcelFile(io.BytesIO(z.read(f)))
    print('=====', f, 'warehouse rows', len(w), 'states in wh', w['STATE'].nunique())
    wkeys = set(zip(w['UTILITY_NUMBER'].astype('Int64').astype(str), w['STATE'].astype(str)))
    for sh in x.sheet_names:
        d = pd.read_excel(x, sh, header=None, skiprows=hdr + 1, dtype=str)
        # year col 0; keep rows with a 4-digit year
        d = d[d[0].astype(str).str.fullmatch(r'\d{4}')]
        if 'State Level' in sh:
            print('  sheet', sh, 'rows', len(d), '(state totals)')
            continue
        # find utility number and state columns by position
        if f.startswith('Net_Metering') or f.startswith('Non_Net'):
            un, st = d[2], d[1]
        else:
            un, st = d[1], d[3] if not f.startswith('Dynamic') else d[4]
        keys = list(zip(un.astype(str), st.astype(str)))
        miss = [k for k in keys if k not in wkeys]
        print('  sheet', sh, 'rows', len(d), 'missing from warehouse', len(miss), miss[:8])
