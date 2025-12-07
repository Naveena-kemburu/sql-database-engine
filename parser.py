import re
from typing import Dict, Any, List, Optional

class SQLParser:
    """Parse and validate SQL query strings."""
    
    COMPARISON_OPERATORS = ['>=', '<=', '!=', '=', '>', '<']
    
    def parse(self, query: str) -> Dict[str, Any]:
        """Parse a SQL query string."""
        query = query.strip()
        if not query:
            raise ValueError("Empty query provided")
        
        is_count = 'COUNT(' in query.upper()
        
        select_match = re.search(r'SELECT\s+(.*?)\s+FROM', query, re.IGNORECASE)
        if not select_match:
            raise ValueError("Invalid SQL syntax: Missing SELECT or FROM clause")
        
        select_clause = select_match.group(1).strip()
        
        from_match = re.search(r'FROM\s+(\w+)', query, re.IGNORECASE)
        if not from_match:
            raise ValueError("Invalid SQL syntax: Missing FROM clause")
        
        table_name = from_match.group(1).strip()
        
        where_clause = None
        where_match = re.search(r'WHERE\s+(.*?)(?:\s*;\s*)?$', query, re.IGNORECASE)
        if where_match:
            where_clause = self._parse_where(where_match.group(1).strip())
        
        if is_count:
            select_cols = self._parse_count(select_clause)
        else:
            select_cols = self._parse_select_cols(select_clause)
        
        return {
            'select_cols': select_cols,
            'from_table': table_name,
            'where_clause': where_clause,
            'is_count': is_count,
            'count_column': select_cols if is_count else None
        }
    
    def _parse_select_cols(self, select_str: str) -> List[str]:
        """Parse column names from SELECT clause."""
        if select_str.strip() == '*':
            return ['*']
        cols = [col.strip() for col in select_str.split(',')]
        return cols
    
    def _parse_count(self, select_str: str) -> Optional[str]:
        """Parse COUNT function and extract column name."""
        count_match = re.search(r'COUNT\s*\(\s*(\*|\w+)\s*\)', select_str, re.IGNORECASE)
        if not count_match:
            raise ValueError("Invalid COUNT syntax")
        return count_match.group(1).strip()
    
    def _parse_where(self, where_str: str) -> Dict[str, Any]:
        """Parse WHERE clause condition."""
        operator = None
        for op in self.COMPARISON_OPERATORS:
            if op in where_str:
                operator = op
                break
        
        if not operator:
            raise ValueError("Invalid WHERE clause: No comparison operator found")
        
        parts = where_str.split(operator, 1)
        if len(parts) != 2:
            raise ValueError("Invalid WHERE clause syntax")
        
        column = parts[0].strip()
        value_str = parts[1].strip()
        
        if value_str.startswith("'") and value_str.endswith("'"):
            value = value_str[1:-1]
        elif value_str.startswith('"') and value_str.endswith('"'):
            value = value_str[1:-1]
        else:
            try:
                value = float(value_str)
                if value.is_integer():
                    value = int(value)
            except ValueError:
                value = value_str
        
        return {
            'column': column,
            'operator': operator,
            'value': value
        }
