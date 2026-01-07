from fmodule import dbFunctions
from fmodule import vectorFunctions
from fmodule import preprocessingFunctions

CSV_PATH = "data/clean_combined_dataset.csv"
TEXT_COLUMN = "text"
LABEL_COLUMN = "label"

# -------------------- #

def similarity_search_sum_labels(conn, query_emb, k=30):
    """
    Returns the sum of labels for the top-k most similar documents
    using cosine distance. Smaller distance = more similar.
    """
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT SUM(label) AS total_label
            FROM (
                SELECT label
                FROM knowledge_base
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            ) AS top_k;
            """,
            (query_emb, k)
        )

        result = cur.fetchone()
        return result[0] if result else 0


# -------------------- #

q1 = "God I hate you so much, please never text my phone again!" #high negative sentiment

q2 = "Yesterday was so much fun! I'd love it so much if you would come with me another time." #high positive sentiment

q3 = "I am going to the store, I will see you later." #neutral sentiment

# -------------------- #

q1_preprocessed = preprocessingFunctions.clean_text(q1)
q1_embedding = vectorFunctions.generate_embeddings([q1_preprocessed])[0]

q2_preprocessed = preprocessingFunctions.clean_text(q2)
q2_embedding = vectorFunctions.generate_embeddings([q2_preprocessed])[0]

q3_preprocessed = preprocessingFunctions.clean_text(q3)
q3_embedding = vectorFunctions.generate_embeddings([q3_preprocessed])[0]

conn = dbFunctions.get_db_connection()

try:
    q1_score = similarity_search_sum_labels(conn, q1_embedding)
    print(q1_score)

    q2_score = similarity_search_sum_labels(conn, q2_embedding)
    print(q2_score)

    q3_score = similarity_search_sum_labels(conn, q3_embedding)
    print(q3_score)
finally:
    dbFunctions.close_db_connection(conn)