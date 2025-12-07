from engine import SQLEngine

def main():
    """Main CLI loop for SQL queries."""
    engine = SQLEngine()
    
    print("\n=== SQL Database Engine ===")
    print("Type 'exit' or 'quit' to exit")
    print("")
    
    csv_path = input("Enter CSV file path: ").strip()
    
    try:
        engine.load_csv(csv_path)
        print(f"Successfully loaded {csv_path}")
        print(f"Columns: {', '.join(engine.columns)}")
    except Exception as e:
        print(f"Error loading file: {e}")
        return
    
    while True:
        try:
            query = input("\nSQL> ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            
            result = engine.execute(query)
            formatted = engine.format_result(result)
            print(f"Result:\n{formatted}")
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
