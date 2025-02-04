import os

from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core.node_parser import SentenceSplitter, SemanticSplitterNodeParser
from llama_index.core.indices.query.query_transform import HyDEQueryTransform
from llama_index.core.query_engine import TransformQueryEngine

import cloudpickle

from dotenv import load_dotenv

from wise_chain.init_defaults import init_llamaindex_defaults
from storyline_wise.ingestion.confluence.llama_index.llama import get_pages_for_space

env_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "../../.env"))
print("env_path:", env_path)
success = load_dotenv(env_path)
assert success, "Failed to load .env file"

space_name = "***"
PERSIST_DIR = f"./storage_{space_name}"
pickle_dir = f"./pickle_{space_name}"


init_llamaindex_defaults(team="My Name", use_case="Storyline prototype")


if not os.path.exists(PERSIST_DIR):
    if not os.path.isdir(pickle_dir):
        os.makedirs(pickle_dir)
    # load the documents and create the index
    documents = get_pages_for_space(space_name)

    with open(f"{pickle_dir}/documents.pkl", "wb") as f:
        cloudpickle.dump(documents, f)

    # splitter = SemanticSplitterNodeParser(
    #     buffer_size=1, breakpoint_percentile_threshold=95
    # )
    index = VectorStoreIndex.from_documents(
        documents, transformations=[SentenceSplitter(chunk_size=512)]
    )
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)
print("Index loaded")

query_engine = index.as_query_engine()

hyde = HyDEQueryTransform(include_original=True)
hyde_query_engine = TransformQueryEngine(query_engine, hyde)
response = query_engine.query("Does Wise do any Causal Inference?")
print(response)
