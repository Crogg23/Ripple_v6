import requests, time
url = "https://campaignfinance.cdn.sos.ca.gov/dbwebexport.zip"
out = "raw_downloads/ca_dbwebexport.zip"
with requests.get(url, stream=True, timeout=300) as r:
    r.raise_for_status()
    total = int(r.headers.get('content-length', 0))
    done = 0
    t0 = time.time()
    with open(out, 'wb') as f:
        for chunk in r.iter_content(1<<20):
            f.write(chunk)
            done += len(chunk)
            if done % (50*1<<20) < (1<<20):
                print(f"{done/1e6:.0f}MB / {total/1e6:.0f}MB  {time.time()-t0:.0f}s", flush=True)
    print("DONE", done, flush=True)
