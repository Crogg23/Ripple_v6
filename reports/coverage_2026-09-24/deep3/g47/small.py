import pandas as pd, re
t = pd.read_csv("S08.csv", dtype=str, keep_default_na=False)
t["st"] = t.TITLE.str.extract(r",\s*([A-Z]{2})\s+\d{4}")
t["scale"] = t.TITLE.str.extract(r"1:([\d,]+)-scale")
print(t.st.value_counts(dropna=False).head(10).to_dict())
print(t.scale.value_counts(dropna=False).to_dict())
print(t.PUB_YEAR.value_counts().head(6).to_dict())
print(t.CREATED.str[:4].value_counts().to_dict())
print(t.TITLE.value_counts().head(5).to_dict())
print(t.FILESIZE.head(5).tolist())
i = pd.read_csv("S09.csv", dtype=str, keep_default_na=False)
print("ITIS rows", len(i), "distinct keys", i.ITIS_TAXON_UNIT_TYPES_KEY.nunique(), "kingdoms", i.KINGDOM_ID.value_counts().sort_index().to_dict())
print("distinct rank names", i.RANK_NAME.nunique(), "runs", i._SOURCE_RUN_ID.nunique(), "sha", i._SRC_SHA256.nunique(), "loaded", i.LOADED_TXT.unique()[:3])
print("update years", i.UPDATE_DATE.str[:4].value_counts().sort_index().to_dict())
# parent integrity: does every dir_parent_rank_id exist as a rank in the same kingdom?
keys = set(zip(i.KINGDOM_ID, i.RANK_ID))
bad = i[(i.DIR_PARENT_RANK_ID!="0") & ~i.apply(lambda r: (r.KINGDOM_ID, r.DIR_PARENT_RANK_ID) in keys, axis=1)]
print("dir parent missing in same kingdom:", len(bad), bad[["KINGDOM_ID","RANK_ID","RANK_NAME","DIR_PARENT_RANK_ID"]].to_string(index=False) if len(bad) else "")
bad2 = i[(i.REQ_PARENT_RANK_ID!="0") & ~i.apply(lambda r: (r.KINGDOM_ID, r.REQ_PARENT_RANK_ID) in keys, axis=1)]
print("req parent missing:", len(bad2))
print(i[i.UPDATE_DATE.str[:4]>="2020"][["KINGDOM_ID","RANK_ID","RANK_NAME","UPDATE_DATE"]].to_string(index=False))
