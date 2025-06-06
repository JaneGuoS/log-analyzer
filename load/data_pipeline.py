import os
import time

#Data Loaders
from llama_index.core import SimpleDirectoryReader
from llama_index.readers.github import GithubClient,GithubRepositoryReader
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter
#Indices and Storage
import pymongo
from llama_index.storage.kvstore.mongodb import MongoDBKVStore as MongoDBCache
from llama_index.storage.docstore.mongodb import MongoDocumentStore
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
#Pipeline
from llama_index.core.ingestion import IngestionPipeline, IngestionCache, DocstoreStrategy
#Vector Embedding Model
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

print('Initialize')
MONGODB_URL          = os.getenv('MONGODB_URL')
MONGODB_DBNAME       = os.getenv('MONGODB_DBNAME')
MONGODB_CLIENT       = pymongo.MongoClient(MONGODB_URL)
MONGODB_CACHE        = IngestionCache(cache=MongoDBCache(mongo_client=MONGODB_CLIENT, db_name = MONGODB_DBNAME))
MONGODB_DOCSTORE     = MongoDocumentStore.from_uri(uri=MONGODB_URL, db_name = MONGODB_DBNAME)

LOGS_DIR             = os.getenv('LOGS_DIR')

EMBED_MODEL          = 'BAAI/bge-small-en-v1.5'
EMBEDDINGS           = HuggingFaceEmbedding(model_name=EMBED_MODEL)

print('->Ingestion Data Sources:')
print('  LOGS_DIR(SimpleDirectoryReader)  = '+LOGS_DIR)
print('->Embedding Model:')
print('  HuggingFaceEmbedding','->',EMBED_MODEL)
print('->Storage:')
print('  MongoDB','->',MONGODB_DBNAME)

def ingest_logs():
  print('->Ingest Logs')
  start         = time.time()
  splitter      = SentenceSplitter(separator=",", chunk_size=2000,chunk_overlap=20)
  documents     = SimpleDirectoryReader(LOGS_DIR,
                                        filename_as_id = True).load_data()
  pipeline      = IngestionPipeline(
                        transformations   = [splitter,EMBEDDINGS],
                        vector_store      = MongoDBAtlasVectorSearch(
                                              mongodb_client  = MONGODB_CLIENT,
                                              db_name         = MONGODB_DBNAME,
                                              collection_name = 'logs_collection',
                                              index_name      = 'default'),
                        cache             = MONGODB_CACHE,
                        docstore          = MONGODB_DOCSTORE,
                        docstore_strategy = DocstoreStrategy.UPSERTS,
                  )
  nodes         = pipeline.run(documents = documents)
  end           = time.time()
  print(f'  Total Time = {end-start}', f'Total Documents = {len(documents)}', f'Total Nodes = {len(nodes)}')


  print('->Ingest Dev Guide')
  start         = time.time()
  pipeline      = IngestionPipeline(
                        transformations   = [EMBEDDINGS], 
                        vector_store      = MongoDBAtlasVectorSearch(
                                              mongodb_client  = MONGODB_CLIENT,
                                              db_name         = MONGODB_DBNAME,
                                              collection_name = 'devguide_collection',
                                              index_name      = 'devguide_idx'),
                        cache             = MONGODB_CACHE,
                        docstore          = MONGODB_DOCSTORE,
                        docstore_strategy = DocstoreStrategy.UPSERTS,
                  )
  nodes         = pipeline.run(documents = documents)
  end           = time.time()
  print(f'  Total Time = {end-start}', f'Total Documents = {len(documents)}', f'Total Nodes = {len(nodes)}')

ingest_logs()

print('Manually create atlas vector search index:','default')