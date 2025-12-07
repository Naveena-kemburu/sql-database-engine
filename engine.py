import csv
from typing import Dict, List, Any, Optional
from parser import SQLParser

class SQLEngine:
    """Execute SQL queries on in-memory data."""
    
    def __init__(self):
        self.data = []
        self.columns = []
        self.parser = SQLParser()
    
    def load_csv(self, file_path: str) -> None:
        """Load CSV file into memory."""
        try:
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f)
                self.columns = reader.fieldnames
                self.data = list(reader)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise Exception(f"Error loading CSV file: {str(e)}")
    
    def execute(self, query: str) -> List[Any]:
        """Parse and execute a SQL query."""
        try:
            parsed = self.parser.parse(query)
            filtered_data = self._apply_where(parsed['where_clause'])
            
            if parsed['is_count']:
                return self._count(filtered_data, parsed['count_column'])
            else:
                return self._project(filtered_data, parsed['select_cols'])
        except Exception as e:
            raise Exception(f"Query execution failed: {str(e)}")
    
    def _apply_where(self, where_clause: Optional[Dict]) -> List[Dict]:
        """Filter rows based on WHERE clause."""
        if where_clause is None:
            return self.data
        
        column = where_clause['column']
        operator = where_clause['operator']
        value = where_clause['value']
        
        if column not in self.columns:
            raise ValueError(f"Column '{column}' does not exist")
        
        filtered = []
        for row in self.data:
            if self._evaluate_condition(row[column], operator, value):
                filtered.append(row)
        return filtered
    
    def _evaluate_condition(self, cell_value: str, op: str, target_value: Any) -> bool:
        """Evaluate a comparison condition."""
        try:
            if isinstance(target_value, (int, float)):
                cell_value = float(cell_value)
            
            if op == '=':
                return cell_value == target_value
            elif op == '!=':
                return cell_value != target_value
            elif op == '>':
                return float(cell_value) > float(target_value)
            elif op == '<':
                return float(cell_value) < float(target_value)
            elif op == '>=':
                return float(cell_value) >= float(target_value)
            elif op == '<=':
                return float(cell_value) <= float(target_value)
            return False
        except (ValueError, TypeError):
            return False
    
    def _project(self, data: List[Dict], columns: List[str]) -> List[Dict]:
        """Select specific columns from rows."""
        if columns == ['*']:
            return data
        
        for col in columns:
            if col not in self.columns:
                raise ValueError(f"Column '{col}' does not exist")
        
        result = []
        for row in data:
            result.append({col: row[col] for col in columns})
        return result
    
    def _count(self, data: List[Dict], column: str) -> int:
        """Count rows or non-null values in a column."""
        if column == '*':
            return len(data)
        
        if column not in self.columns:
            raise ValueError(f"Column '{column}' does not exist")
        
        return sum(1 for row in data if row.get(column))
    
    def format_result(self, result: Any) -> str:
        """Format query result for display."""
        if isinstance(result, int):
            return str(result)
        elif isinstance(result, list):
            if not result:
                return "No results"
            
            if isinstance(result[0], dict):
                columns = list(result[0].keys())
                lines = ["  ".join(columns)]
                for row in result:
                    lines.append("  ".join(str(row.get(col, "")) for col in columns))
                return "\n".join(lines)
        return str(result)
