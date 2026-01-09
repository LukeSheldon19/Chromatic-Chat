DB_CONFIG = {
    # "host": "localhost", #may need to change back when creating knowledge base or testing -- Actually I don't think so
    "host": "host.docker.internal",  # Changed from "localhost"
    "port": 5432,
    "database": "vector_db",
    "user": "postgres",
    "password": "temp"
}

PGVECTOR_TABLE = "knowledge_base"
EMBEDDING_DIM = 384 