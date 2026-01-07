import pandas as pd
from fmodule import dbFunctions
from fmodule import vectorFunctions

CSV_PATH = "data/clean_combined_dataset.csv"
TEXT_COLUMN = "text"
LABEL_COLUMN = "label"

# -------------------- #

temp_df = pd.read_csv(CSV_PATH)
texts = temp_df[TEXT_COLUMN].astype(str).tolist()
labels = temp_df[LABEL_COLUMN].astype(int).tolist()

embeddings = vectorFunctions.generate_embeddings(texts)
rows = list(zip(embeddings, labels))

# -------------------- #

conn = dbFunctions.get_db_connection()
try:
    dbFunctions.create_vector_table(conn)
    dbFunctions.insert_embeddings(conn, rows)
finally:
    dbFunctions.close_db_connection(conn)

print(f"Inserted {len(rows)} rows into PGVector DB.")

# -------------------- #