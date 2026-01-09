DB_CONFIG = {
    # "host": "localhost",
    "host": "host.docker.internal",  # Changed from "localhost"
    "port": 5432,
    "database": "vector_db",
    "user": "postgres",
    "password": "temp"
}

PGVECTOR_TABLE = "knowledge_base"
EMBEDDING_DIM = 384 