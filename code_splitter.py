import sqlparse
from typing import List

class SQLCodeSplitter:
    def __init__(self, chunk_size: int = 2000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_sql_code(self, sql_code: str) -> List[str]:
        # Format and clean the SQL code
        formatted_sql = sqlparse.format(sql_code, reindent=True, keyword_case='upper')
        
        # Split into statements
        statements = sqlparse.split(formatted_sql)
        
        chunks = []
        current_chunk = ""
        
        for statement in statements:
            if len(current_chunk) + len(statement) <= self.chunk_size:
                current_chunk += statement + "\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = statement + "\n"
                
        if current_chunk:
            chunks.append(current_chunk)
            
        # Add overlap between chunks
        overlapped_chunks = []
        for i in range(len(chunks)):
            if i > 0:
                # Add some context from the previous chunk
                overlap_start = max(0, len(chunks[i-1]) - self.chunk_overlap)
                current_chunk = chunks[i-1][overlap_start:] + chunks[i]
            else:
                current_chunk = chunks[i]
            overlapped_chunks.append(current_chunk)
            
        return overlapped_chunks