import psycopg2
from psycopg2.extras import execute_batch
from config.db_config import DB_CONFIG, PGVECTOR_TABLE, EMBEDDING_DIM

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def close_db_connection(conn):
    if conn:
        conn.close()

def create_vector_table(conn):
    conn.autocommit = True
    query = f"""
        CREATE EXTENSION IF NOT EXISTS vector;

        CREATE TABLE IF NOT EXISTS {PGVECTOR_TABLE} (
            id SERIAL PRIMARY KEY,
            content TEXT,
            embedding VECTOR({EMBEDDING_DIM}),
            label INT
        );
    """
    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()

def insert_embeddings(conn, rows):
    """
    rows: List of tuples -> (text, embedding, label)
    """
    query = f"""
    INSERT INTO {PGVECTOR_TABLE} (text, embedding, label)
    VALUES (%s, %s, %s)
    """
    with conn.cursor() as cur:
        execute_batch(cur, query, rows, page_size=1000)
        conn.commit()