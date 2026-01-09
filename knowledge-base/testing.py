from fmodule import dbFunctions
from fmodule import vectorFunctions
from fmodule import preprocessingFunctions

CSV_PATH = "data/clean_combined_dataset.csv"
TEXT_COLUMN = "text"
LABEL_COLUMN = "label"

# -------------------- #

q1 = "God I hate you so much, please never text my phone again!" #high negative sentiment

q2 = "Yesterday was so much fun! I'd love it so much if you would come with me another time." #high positive sentiment

q3 = "I am going to the store, I will see you later." #neutral sentiment

# -------------------- #

model, tokenizer = vectorFunctions.load_embedding_model_and_tokenizer()

q1_preprocessed = preprocessingFunctions.clean_text(q1)
q1_embedding = vectorFunctions.generate_embeddings([q1_preprocessed])[0]

q2_preprocessed = preprocessingFunctions.clean_text(q2)
q2_embedding = vectorFunctions.generate_embeddings([q2_preprocessed])[0]

q3_preprocessed = preprocessingFunctions.clean_text(q3)
q3_embedding = vectorFunctions.generate_embeddings([q3_preprocessed])[0]

conn = dbFunctions.get_db_connection()

try:
    q1_score = dbFunctions.similarity_search_sum_labels(conn, q1_embedding)
    print(q1_score)

    q2_score = dbFunctions.similarity_search_sum_labels(conn, q2_embedding)
    print(q2_score)

    q3_score = dbFunctions.similarity_search_sum_labels(conn, q3_embedding)
    print(q3_score)
finally:
    dbFunctions.close_db_connection(conn)