from chromadb.api.types import QueryRequest, GetRequest

class QueryRequestOptional(QueryRequest, total=False):
    pass

class GetRequestOptional(GetRequest, total=False):
    pass
