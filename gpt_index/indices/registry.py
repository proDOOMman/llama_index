"""Index registry."""

from typing import Any, Dict, Type

from gpt_index.constants import DATA_KEY, TYPE_KEY
from gpt_index.data_structs.data_structs_v2 import (
    KG,
    ChatGPTRetrievalPluginIndexDict,
    ChromaIndexDict,
    CompositeIndex,
    DeepLakeIndexDict,
    EmptyIndex,
    FaissIndexDict,
    IndexDict,
    IndexGraph,
    IndexList,
    KeywordTable,
    MilvusIndexDict,
    MyScaleIndexDict,
    OpensearchIndexDict,
    PineconeIndexDict,
    QdrantIndexDict,
    SimpleIndexDict,
    V2IndexStruct,
    WeaviateIndexDict,
)
from gpt_index.data_structs.struct_type import IndexStructType
from gpt_index.data_structs.table_v2 import PandasStructTable, SQLStructTable
from gpt_index.indices.base import BaseGPTIndex
from gpt_index.indices.empty.base import GPTEmptyIndex
from gpt_index.indices.keyword_table.base import GPTKeywordTableIndex
from gpt_index.indices.knowledge_graph.base import GPTKnowledgeGraphIndex
from gpt_index.indices.list.base import GPTListIndex
from gpt_index.indices.struct_store.pandas import GPTPandasIndex
from gpt_index.indices.struct_store.sql import GPTSQLStructStoreIndex
from gpt_index.indices.tree.base import GPTTreeIndex
from gpt_index.indices.vector_store.base import GPTVectorStoreIndex

INDEX_STRUCT_TYPE_TO_INDEX_STRUCT_CLASS: Dict[IndexStructType, Type[V2IndexStruct]] = {
    IndexStructType.TREE: IndexGraph,
    IndexStructType.LIST: IndexList,
    IndexStructType.KEYWORD_TABLE: KeywordTable,
    IndexStructType.SIMPLE_DICT: SimpleIndexDict,
    IndexStructType.DICT: FaissIndexDict,
    IndexStructType.WEAVIATE: WeaviateIndexDict,
    IndexStructType.PINECONE: PineconeIndexDict,
    IndexStructType.QDRANT: QdrantIndexDict,
    IndexStructType.MILVUS: MilvusIndexDict,
    IndexStructType.CHROMA: ChromaIndexDict,
    IndexStructType.OPENSEARCH: OpensearchIndexDict,
    IndexStructType.VECTOR_STORE: IndexDict,
    IndexStructType.SQL: SQLStructTable,
    IndexStructType.PANDAS: PandasStructTable,
    IndexStructType.KG: KG,
    IndexStructType.EMPTY: EmptyIndex,
    IndexStructType.COMPOSITE: CompositeIndex,
    IndexStructType.CHATGPT_RETRIEVAL_PLUGIN: ChatGPTRetrievalPluginIndexDict,
    IndexStructType.DEEPLAKE: DeepLakeIndexDict,
    IndexStructType.MYSCALE: MyScaleIndexDict,
}


INDEX_STRUCT_TYPE_TO_INDEX_CLASS: Dict[IndexStructType, Type[BaseGPTIndex]] = {
    IndexStructType.TREE: GPTTreeIndex,
    IndexStructType.LIST: GPTListIndex,
    IndexStructType.KEYWORD_TABLE: GPTKeywordTableIndex,
    IndexStructType.VECTOR_STORE: GPTVectorStoreIndex,
    IndexStructType.SQL: GPTSQLStructStoreIndex,
    IndexStructType.PANDAS: GPTPandasIndex,
    IndexStructType.KG: GPTKnowledgeGraphIndex,
    IndexStructType.EMPTY: GPTEmptyIndex,
}


def load_index_struct_from_dict(struct_dict: Dict[str, Any]) -> "V2IndexStruct":
    type = struct_dict[TYPE_KEY]
    data_dict = struct_dict[DATA_KEY]
    cls = INDEX_STRUCT_TYPE_TO_INDEX_STRUCT_CLASS[type]
    return cls.from_dict(data_dict)


def load_index_from_dict(index_dict: Dict[str, Any], **kwargs: Any) -> "BaseGPTIndex":
    type = index_dict[TYPE_KEY]
    data_dict = index_dict[DATA_KEY]
    cls = INDEX_STRUCT_TYPE_TO_INDEX_CLASS[type]
    return cls.load_from_dict(data_dict, **kwargs)


def save_index_to_dict(index: BaseGPTIndex) -> dict:
    index_dict = {
        TYPE_KEY: index.index_struct.get_type(),
        DATA_KEY: index.save_to_dict(),
    }
    return index_dict
