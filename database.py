import sys
import mysql.connector
import pandas as pd

# Load the dataset from Kaggle
chembl_csv = pd.read_csv("chembl.csv")
# Read in the unique IDs for the compounds
molregno_list = list(chembl_csv["COMPOUND_ID"])
chembl_columns = chembl_csv.columns.tolist()
# Rename the 2nd column to allow for merging later
chembl_columns[1] = "molregno"
chembl_csv.columns = chembl_columns

# Connect to MySQL databse
db = mysql.connector.connect(
    host=sys.argv[1],
    user=sys.argv[2],
    password=sys.argv[3],
    database=sys.argv[4],
)

# Labels for the compound_properties table
comp_prop_labels = ["molregno", "mw_freebase", "alogp", "hba", "hbd", "psa", "rtb", "ro3_pass", "num_ro5_violations", "cx_most_apka", "cx_most_bpka", "cx_logp", "cx_logd", "molecular_species", "full_mwt", "aromatic_rings", "heavy_atoms", "qed_weighted", "mw_monoisotopic", "full_molformula", "hba_lipinski", "hbd_lipinski", "num_lipinski_ro5_violations", "np_likeness_score"]
cursor = db.cursor()

# Gather the data from the compound_properties table
placeholders = ','.join(['%s']*len(molregno_list))
query = f"SELECT * FROM compound_properties WHERE molregno IN ({placeholders})"
cursor.execute(query, molregno_list)
result = cursor.fetchall()

# Disconnect from MySQL and cleanup
cursor.close()
db.close()
db.disconnect()

# Convert to pandas DataFrame
dataset = pd.DataFrame(result, columns=comp_prop_labels)

# Cleanup bad columns
cols_to_drop = {}
for i in dataset:
    # Delete features with more than 30% nan values
    if pd.isna(dataset[i]).sum() / len(dataset) > 0.2:
        cols_to_drop[i] = None

    # Delete String columns
    if type(dataset[i][0]) == str or type(dataset[i][0]) == chr:
        cols_to_drop[i] = None

cols_to_drop = list(cols_to_drop.keys())
dataset.drop(cols_to_drop, axis=1, inplace=True)
print(f"Dropped {len(cols_to_drop)} columns:", cols_to_drop)
print("Drop criteria: Null rate above 30%; string values\n")

# Cleanup bad rows
rows_to_drop = {}
for j in dataset.index:
    if pd.isna(dataset.iloc[j]).sum():
        for col in pd.isna(dataset.iloc[j]).index[pd.isna(dataset.iloc[j]).values]:
            # If the null rate for the column is below 1%, we delete the row
            if pd.isna(dataset[col]).sum() / len(dataset) < 0.01:
                rows_to_drop[j] = None
                break

rows_to_drop = list(rows_to_drop.keys())
dataset.drop(rows_to_drop, inplace=True)
print(f"Dropped {len(rows_to_drop)} rows:", rows_to_drop)
print("Drop criteria: Row has null and the corresponding column's null rate is less than 1%\n")

# Convert to standard numeric types
dataset = dataset.apply(lambda c: pd.to_numeric(c) if c.dtype == object else c)

# Fill in cx_most_bpka with the median, not the mean, because cx_most_bpka is skewed
dataset.fillna({"cx_most_bpka": dataset["cx_most_bpka"].median()}, inplace=True)

# Merge with original data and cleanup
dataset = dataset.merge(chembl_csv, on="molregno", how="inner")
dataset.drop(["molregno", "Unnamed: 0", "SOURCES", "SMILES", "PCT_INHIB_3D7_PFLDH", "PCT_INHB_DD2"], axis=1, inplace=True)

# Save dataset and don't include the index column
print("Saving to dataset.csv ...")
dataset.to_csv("dataset.csv", index=False)
print("Saved to dataset.csv")