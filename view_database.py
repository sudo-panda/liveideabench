import os
import sqlite3
import pandas as pd
import json

from .run import clean_text

# Define the database file path
DB_PATH = './data/ideabench.db'

def load_and_display_database():
    """
    Load the SQLite database and display its content as a DataFrame
    """
    # Check if the database file exists
    if not os.path.exists(DB_PATH):
        print(f"Error: Database file '{DB_PATH}' does not exist")
        return

    # Create a connection to the database
    conn = sqlite3.connect(DB_PATH)

    try:
        # Query all results
        query = "SELECT * FROM results ORDER BY timestamp DESC"
        df = pd.read_sql_query(query, conn)

        # Process JSON fields
        for json_col in ['critic_models', 'raw_critiques', 'parsed_scores', 
                         'critique_reasonings', 'error', 
                         'hallucination_scores', 'samples_for_hallucination']:
            if json_col in df.columns:
                df[json_col] = df[json_col].apply(
                    lambda x: json.loads(x) if pd.notna(x) and isinstance(x, str) else x
                )
        
        # Clean text fields
        df['idea'] = df['idea'].apply(lambda x: clean_text(x))
        df['full_response'] = df['full_response'].apply(lambda x: clean_text(x))
        df['raw_critiques'] = df['raw_critiques'].apply(
            lambda x: [clean_text(i) if isinstance(i, str) else i for i in x] if isinstance(x, list) else clean_text(x)
        )
        df['critique_reasonings'] = df['critique_reasonings'].apply(
            lambda x: [clean_text(i) if isinstance(i, str) else i for i in x] if isinstance(x, list) else clean_text(x)
        )

        # Print basic statistics
        print(f"Total records in the database: {len(df)}")
        print("\nBasic Statistics:")
        print(f"Unique prompt inputs: {df['prompt_input'].nunique()}")
        print(f"Number of idea model types: {df['idea_model'].nunique()}")
        
        if 'critic_models' in df.columns:
            unique_critics = set(e for lst in df['critic_models'].dropna() for e in (lst if isinstance(lst, list) else [lst]))
            print(f"Unique critic models: {unique_critics}")

        # Display an overview of the DataFrame
        print("\nData Preview:")
        # Select more meaningful columns for display
        display_columns = [
            'id', 'timestamp', 'prompt_input', 'idea_model', 'critic_models',
            'parsed_scores', 'first_was_rejected', 'hallucination_scores'
        ]
        preview_df = df[display_columns].head(10)
        
        print(preview_df)

        return df

    except sqlite3.Error as e:
        print(f"Error reading the database: {e}")

    finally:
        # Close the connection
        conn.close()

# Execute the main function
if __name__ == "__main__":
    print("Loading IdeaBench database...")
    df = load_and_display_database()
    os.makedirs('./csvs', exist_ok=True)
    df.to_csv('./csvs/view.csv')

    if df is not None:
        # More analysis code can be added here
        print("\n🎉Database loaded successfully! \n💡You can now run `stats.ipynb` to generate `data/data.parquet` which serves as input for the subsequent analysis notebooks....")

        # If interactive analysis is needed, the df variable can be kept
        # For example, you can uncomment the lines below to enable interactive analysis
        # import code
        # code.interact(local=locals())