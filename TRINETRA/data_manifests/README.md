# data_manifests/
Subset CSVs (`sample_id, path, label, group, split, sha1`) written by `data_adapters/build_npz.py --manifest`, plus
`.sha256` files. **No raw data is ever committed here.** Name: `<dataset>_<subset>_seed0.csv`.
`tpd_index.csv` currently indexes the 736 materialized geo rows; `profiles/` stores generated profiles of the registry and geo tables.
EO manifests remain absent until the team attaches and converts those datasets on Kaggle.
<!-- END -->
