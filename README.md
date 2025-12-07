# SQL Database Engine

A mini in-memory SQL query engine built from scratch in Python. This project demonstrates core database concepts including data loading, query parsing, filtering, projection, and aggregation.

## Project Overview

This is a simplified SQL query engine that supports a subset of SQL functionality. It loads data from CSV files into memory and allows users to execute SQL queries through an interactive command-line interface (REPL).

### Features

- **Data Loading**: Load CSV files into in-memory data structures
- **SQL Parsing**: Parse and validate SQL queries
- **Query Execution**: Execute SELECT, WHERE, and COUNT() queries
- **Interactive CLI**: Read-Eval-Print Loop for query execution
- **Error Handling**: Comprehensive error messages for invalid queries

## Setup Instructions

### Requirements

- Python 3.7 or higher
- No external dependencies required (uses standard library only)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Naveena-kemburu/sql-database-engine.git
cd sql-database-engine
```

2. Ensure Python 3.7+ is installed:
```bash
python --version
```

### Running the Application

1. Start the CLI:
```bash
python cli.py
```

2. Load a CSV file at the prompt:
```
Enter CSV file path: data/users.csv
```

3. Execute SQL queries:
```
SQL> SELECT * FROM users
SQL> SELECT name, age FROM users WHERE age > 30
SQL> SELECT COUNT(*) FROM users
```

4. Exit the application:
```
SQL> exit
```

## Supported SQL Grammar

This engine supports a simplified subset of SQL with the following syntax:

### SELECT Clause

Select all columns:
```sql
SELECT * FROM table_name
```

Select specific columns:
```sql
SELECT col1, col2, col3 FROM table_name
```

### WHERE Clause

Filter rows with a single condition using supported operators:
- `=` (equals)
- `!=` (not equals)
- `>` (greater than)
- `<` (less than)
- `>=` (greater than or equal)
- `<=` (less than or equal)

Examples:
```sql
WHERE age > 30
WHERE country = 'USA'
WHERE salary != 50000
```

### COUNT() Aggregation

Count all rows:
```sql
SELECT COUNT(*) FROM table_name
```

Count non-null values in a column:
```sql
SELECT COUNT(column_name) FROM table_name
```

With WHERE clause:
```sql
SELECT COUNT(*) FROM users WHERE age > 25
```

### Complete Query Examples

```sql
SELECT * FROM employees
SELECT name, email FROM users WHERE country = 'Canada'
SELECT age, salary FROM employees WHERE salary >= 60000
SELECT COUNT(*) FROM products
SELECT COUNT(phone) FROM contacts WHERE status = 'active'
```

## Project Structure

```
sql-database-engine/
├── parser.py          # SQL parsing logic
├── engine.py          # Query execution engine
├── cli.py             # Command-line interface (REPL)
├── data/
│   ├── users.csv        # Sample CSV file for testing
│   └── products.csv    # Sample CSV file for testing
├── README.md          # This file
└── requirements.txt   # Python dependencies (empty for this project)
```

## Module Details

### parser.py

Responsible for parsing SQL queries and extracting:
- SELECT clause (column names or *)
- FROM clause (table/file name)
- WHERE clause (condition with operator and value)
- COUNT() function detection

Returns a dictionary representation of the parsed query.

### engine.py

Implements the query execution logic:
- Data loading from CSV files
- Row filtering based on WHERE conditions
- Column projection for SELECT
- COUNT() aggregation
- Result formatting

### cli.py

Provides the interactive command-line interface:
- Prompts user for CSV file path
- Reads and executes SQL queries
- Displays results in a formatted manner
- Handles user input validation
- Allows graceful exit

## Error Handling

The engine provides clear error messages for:
- Invalid SQL syntax
- Non-existent columns
- Non-existent table/file
- Invalid comparison operators
- Type mismatches in WHERE clauses

## Testing

Sample CSV files are provided in the `data/` directory:
- `users.csv`: Contains user data (id, name, email, age, country)
- `products.csv`: Contains product data (id, product_name, price, quantity)

Run test queries using these files to validate the engine.

## Limitations

- Only one WHERE condition is supported (no AND/OR)
- No JOIN operations
- No GROUP BY or HAVING clauses
- No ORDER BY or LIMIT clauses
- No UPDATE or DELETE operations
- Case-sensitive column and operator matching

## Author

Built as a Partnr GPP (Global Placement Program) task.

## License

This project is open source and available under the MIT License.
