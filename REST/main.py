from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
from fastapi.concurrency import run_in_threadpool

from fmodule import dbFunctions
from fmodule import vectorFunctions
from fmodule import preprocessingFunctions

class QueryRequest(BaseModel):
    query: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- Open DB connection and load embedding model and tokenizer on startup ---- #
    app.state.conn = dbFunctions.get_db_connection()
    vectorFunctions.load_embedding_model_and_tokenizer()
    yield
    # ---- Close DB connection on shutdown ---- #
    dbFunctions.close_db_connection(app.state.conn)

app = FastAPI(lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/query")
async def query(request: QueryRequest):
    try:
        # Run blocking code in threadpool
        query_processed = await run_in_threadpool(
            preprocessingFunctions.clean_text,
            request.query
        )

        query_embedding = await run_in_threadpool(
            lambda: vectorFunctions.generate_embeddings([query_processed])[0]
        )

        result = await run_in_threadpool(
            dbFunctions.similarity_search_sum_labels,
            app.state.conn,
            query_embedding
        )

        return {"result": result}

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Query failed: {str(e)}"
        )   