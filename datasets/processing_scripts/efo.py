import os
import numpy as np
import pandas as pd
import json


# Read EFO (in json format)
efo = json.load(open("/n/data1/hms/dbmi/zitnik/lab/users/mli/PrimeKG/efo.json"))
print("Number of keys", efo.keys())
print("Number of things in the `graphs` dict", len(efo["graphs"]))
print("Number of things in the `graphs` dict, 0th element", len(efo["graphs"][0]))

# Retrieve UMLS & MONDO terms only
efo_ids = []
efo_labels = []
efo_mondo_xref = []
efo_umls_xref = []
for n in efo["graphs"][0]["nodes"]:
    if "EFO" in n['id']: 
        if 'meta' in n:
            if 'xrefs' in n['meta']:
                n_id = n['id']
                n_mondo = None
                n_umls = None
                for x in [k['val'] for k in n['meta']['xrefs']]: 
                    if "MONDO" in x: 
                        if "MONDO:" in x: n_mondo = str(int(x.split("MONDO:")[1]))
                        elif "MONDO_" in x: n_mondo = str(int(x.split("MONDO_")[1]))
                    if "UMLS" in x: n_umls = x.split("UMLS:")[1]
                
                # Keep only EFO terms with either/both MONDO or UMLS
                if n_mondo == None and n_umls == None: continue
                efo_ids.append(n_id.rsplit("/", 1)[1])
                efo_labels.append(n['lbl'])
                efo_mondo_xref.append(n_mondo)
                efo_umls_xref.append(n_umls)
                print(n_mondo, n_umls)
print("Number of items", len(efo_ids))

# Restructure as a dataframe
efo_terms = pd.DataFrame.from_dict({'id': efo_ids,
                                    'label': efo_labels,
                                    'mondo': efo_mondo_xref,
                                    'umls': efo_umls_xref})
print(efo_terms)
assert len(efo_terms['id'].tolist()) == len(efo_terms.drop_duplicates()['id'].tolist())

# Save dataframe
efo_terms.to_csv('/n/data1/hms/dbmi/zitnik/lab/users/mli/PrimeKG/efo_terms.csv', index=False)