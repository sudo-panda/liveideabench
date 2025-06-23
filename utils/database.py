"""
Database Management Module

Uses SQLite for data storage, supporting concurrent access from multiple processes.
"""

import os
import sqlite3
import json
import threading
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database file path
DB_PATH = './data/ideabench.db'

# Ensure the database directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Thread lock for protecting the connection pool
_lock = threading.Lock()

# Connection pool - one connection per thread
_connection_pool = {}


def get_connection() -> sqlite3.Connection:
    """Get the database connection for the current thread"""
    thread_id = threading.get_ident()
    
    with _lock:
        if thread_id not in _connection_pool:
            conn = sqlite3.connect(DB_PATH, timeout=30.0)
            conn.row_factory = sqlite3.Row  # Allows row objects to be accessed by column name
            _connection_pool[thread_id] = conn
            return conn
        return _connection_pool[thread_id]


def close_all_connections() -> None:
    """Close all database connections"""
    with _lock:
        for conn in _connection_pool.values():
            conn.close()
        _connection_pool.clear()


def init_database() -> None:
    """Initialize the database structure"""
    logger.info("Initializing database...")

    conn = get_connection()
    cursor = conn.cursor()
    
    # Create the results table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        prompt_input TEXT NOT NULL,
        idea_model TEXT NOT NULL,
        critic_models TEXT NOT NULL,
        idea TEXT NOT NULL,
        full_response TEXT NOT NULL,          -- Full response
        first_was_rejected INTEGER DEFAULT 0, -- Flag indicating if the model rejected the request initially
        first_reject_response TEXT,           -- Stores the reason for the initial rejection
        idea_gen_config TEXT NOT NULL,        -- Configuration for idea gen in JSON format
        hallucination_scores TEXT,            -- Stores hallucination scores in JSON format
        samples_for_hallucination TEXT,       -- Stores samples for hallucination detection in JSON format
        raw_critiques TEXT NOT NULL,
        parsed_scores TEXT,                   -- Scores stored in JSON format
        critique_reasonings TEXT,             -- Reasoning process of the critic model
        error TEXT                            -- Potential error messages
    )
    ''')
    
    # Create indexes to speed up queries
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_prompt_input_model ON results (prompt_input, idea_model)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON results (timestamp)')
    
    conn.commit()

def insert_idea(idea_data: Dict[str, Any]) -> int:
    """Insert a new idea into the database

    Args:
        idea_data: Dictionary containing the idea data

    Returns:
        The ID of the newly inserted record
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Extract and process data
    timestamp = datetime.now().isoformat()
    prompt_input = idea_data.get('prompt_input', '')
    idea_model = idea_data.get('idea_model', '')
    idea = idea_data.get('idea', '')
    full_response = idea_data.get('full_response', '')
    first_was_rejected = idea_data.get('first_was_rejected', 0)
    if isinstance(first_was_rejected, bool):
        first_was_rejected = 1 if first_was_rejected else 0
    first_reject_response = idea_data.get('first_reject_response')
    idea_gen_config = json.dumps(idea_data.get('idea_gen_config', {}))
    hallucination_scores = json.dumps(idea_data.get('hallucination_scores', {}))
    samples_for_hallucination = json.dumps(idea_data.get('samples_for_hallucination', []))

    assert prompt_input != "", "The prompt input must be provided"
    assert idea_model != "", "The idea model must be provided"
    assert idea != "", "The idea must be provided"
    assert full_response != "", "The full response must be provided"

    try:
        cursor.execute('''
        INSERT INTO results 
        (timestamp, prompt_input, idea_model, idea, idea_gen_config, 
         full_response, first_was_rejected, first_reject_response, 
         hallucination_scores, samples_for_hallucination,
         critic_models, raw_critiques, parsed_scores, critique_reasonings, error)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, prompt_input, idea_model, idea, idea_gen_config, 
              full_response, first_was_rejected, first_reject_response,
              hallucination_scores, samples_for_hallucination,
              "[]", "[]", "[]", "[]", "[]"))

        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        logger.error(f"Database insertion error: {str(e)}")
        conn.rollback()
        raise

def update_critique(idea_id: int, critique_data: Dict[str, Any]) -> None:
    """Update an existing idea with critique data

    Args:
        idea_id: The ID of the idea to update
        critique_data: Dictionary containing the critique data
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Get exisiting critique data
    cursor.execute('SELECT * FROM results WHERE id = ?', (idea_id,))
    existing_data = cursor.fetchone()
    if not existing_data:
        logger.error(f"No record found with ID {idea_id}")
        raise ValueError(f"No record found with ID {idea_id}")
    
    critic_models = json.loads(existing_data['critic_models'] if existing_data['critic_models'] else "[]")
    raw_critiques = json.loads(existing_data['raw_critiques'] if existing_data['raw_critiques'] else "[]")
    parsed_scores = json.loads(existing_data['parsed_scores'] if existing_data['parsed_scores'] else "[]")
    critique_reasonings = json.loads(existing_data['critique_reasonings'] if existing_data['critique_reasonings'] else "[]")
    errors = json.loads(existing_data['error'] if existing_data['error'] else "[]")
    
    
    
    # Extract and process data
    critic_model = critique_data.get('critic_model', '')
    raw_critique = critique_data.get('raw_critique', '')
    parsed_score = critique_data.get('parsed_scores', {})
    critique_reasoning = critique_data.get('critique_reasonings')
    error = critique_data.get('error', '')

    if error != "": 
        assert critic_model != "", "The critic model must be provided"
        assert raw_critique != "", "The raw critiques must be provided"
        assert parsed_score != {}, "The parsed scores must be provided"

        critic_models.append(critic_model)
        raw_critiques.append(raw_critique)
        parsed_scores.append(parsed_score)
        critique_reasonings.append(critique_reasoning)

        try:
            cursor.execute('''
            UPDATE results 
            SET critic_models = ?, raw_critiques = ?, parsed_scores = ?, critique_reasonings = ?
            WHERE id = ?
            ''', (critic_models, raw_critiques, parsed_scores, critique_reasonings,
                  idea_id))

            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Database update error: {str(e)}")
            conn.rollback()
            raise
    else:
        errors.append(error)

        try:
            # Update errors column
            cursor.execute('''
            UPDATE results
            SET error = ?
            WHERE id = ?
            ''', (json.dumps(errors), idea_id))
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Database update error: {str(e)}")
            conn.rollback()
            raise

def save_result(result_data: Dict[str, Any]) -> int:
    """Save an evaluation result to the database

    Args:
        result_data: Dictionary containing the evaluation results

    Returns:
        The ID of the newly inserted record
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Extract and process data
    timestamp = datetime.now().isoformat()
    prompt_input = result_data.get('prompt_input', '')
    idea_model = result_data.get('idea_model', '')
    idea = result_data.get('idea', '')
    full_response = result_data.get('full_response', '')
    
    # Handle parsing results
    critic_models = None
    raw_critiques = None
    parsed_scores = None
    critique_reasonings = None
    error = None
    hallucination_scores = None
    samples_for_hallucination = None
    if 'critic_models' in result_data and result_data['critic_models']:
        critic_models = json.dumps(result_data['critic_models'])
    if 'raw_critiques' in result_data and result_data['raw_critiques']:
        raw_critiques = json.dumps(result_data['raw_critiques'])
    if 'parsed_scores' in result_data and result_data['parsed_scores']:
        parsed_scores = json.dumps(result_data['parsed_scores'])
    if 'critique_reasonings' in result_data and result_data['critique_reasonings']:
        critique_reasonings = json.dumps(result_data['critique_reasonings'])
    if 'error' in result_data and result_data['error']:
        error = json.dumps(result_data['error'])
    if 'hallucination_scores' in result_data and result_data['hallucination_scores']:
        hallucination_scores = json.dumps(result_data['hallucination_scores'])
    if 'samples_for_hallucination' in result_data and result_data['samples_for_hallucination']:
        samples_for_hallucination = json.dumps(result_data['samples_for_hallucination'])
    
    # Get rejection status
    first_was_rejected = result_data.get('first_was_rejected', 0)
    if isinstance(first_was_rejected, bool):
        first_was_rejected = 1 if first_was_rejected else 0
    first_reject_response = result_data.get('first_reject_response')
    
    try:
        cursor.execute('''
        INSERT INTO results 
        (timestamp, prompt_input, idea_model, critic_models, idea, raw_critiques, 
         parsed_scores, critique_reasonings, error, full_response, 
         first_was_rejected, first_reject_response, hallucination_scores, samples_for_hallucination)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            timestamp, prompt_input, idea_model, critic_models, idea, raw_critiques,
            parsed_scores, critique_reasonings, error, full_response, 
            first_was_rejected, first_reject_response, hallucination_scores, samples_for_hallucination
        ))
        
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        logger.error(f"Database insertion error: {str(e)}")
        conn.rollback()
        raise


def check_duplicate_entries(keyword: str, idea_model: str, limit: int = 6) -> bool:
    """Check if a sufficient number of records exist for the same keyword and model combination

    Args:
        keyword: The keyword
        idea_model: The idea model name
        limit: The maximum record count limit

    Returns:
        True if the record count meets or exceeds the limit, False otherwise
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT COUNT(*) as count FROM results 
    WHERE prompt_input = ? AND idea_model = ?
    ''', (keyword, idea_model))
    
    result = cursor.fetchone()
    count = result['count'] if result else 0
    
    return count >= limit


def query_results(filters: Optional[Dict[str, Any]] = None, 
                 limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """Query results based on filter conditions

    Args:
        filters: Dictionary of filter conditions
        limit: Maximum number of records to return

    Returns:
        List of results
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM results"
    params = []
    
    if filters:
        conditions = []
        for key, value in filters.items():
            if key in ['prompt_input', 'idea_model', 'critic_models', 'first_was_rejected']:
                conditions.append(f"{key} = ?")
                params.append(value)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
    
    query += " ORDER BY timestamp DESC"
    
    if limit:
        query += f" LIMIT {limit}"
    
    cursor.execute(query, params)
    
    results = []
    for row in cursor.fetchall():
        result_dict = dict(row)

        if result_dict.get('critic_models'):
            try:
                result_dict['critic_models'] = json.loads(result_dict['critic_models'])
            except json.JSONDecodeError:
                pass

        if result_dict.get('raw_critiques'):
            try:
                result_dict['raw_critiques'] = json.loads(result_dict['raw_critiques'])
            except json.JSONDecodeError:
                pass
        
        # Parse JSON fields
        if result_dict.get('parsed_scores'):
            try:
                result_dict['parsed_scores'] = json.loads(result_dict['parsed_scores'])
            except json.JSONDecodeError:
                pass

        if result_dict.get('critique_reasonings'):
            try:
                result_dict['critique_reasonings'] = json.loads(result_dict['critique_reasonings'])
            except json.JSONDecodeError:
                pass

        if result_dict.get('error'):
            try:
                result_dict['error'] = json.loads(result_dict['error'])
            except json.JSONDecodeError:
                pass

        if result_dict.get('hallucination_scores'):
            try:
                result_dict['hallucination_scores'] = json.loads(result_dict['hallucination_scores'])
            except json.JSONDecodeError:
                pass

        if result_dict.get('samples_for_hallucination'):
            try:
                result_dict['samples_for_hallucination'] = json.loads(result_dict['samples_for_hallucination'])
            except json.JSONDecodeError:
                pass
                
        results.append(result_dict)
    
    return results


def export_to_csv(output_path: str) -> None:
    """Export the database to a CSV file

    Args:
        output_path: The output path for the CSV file
    """
    import pandas as pd
    
    conn = get_connection()
    
    # Read all results
    df = pd.read_sql_query("SELECT * FROM results", conn)
    
    # Process JSON fields
    for json_col in ['critic_models', 'raw_critiques', 'parsed_scores', 
                     'parsed_reasonings', 'critique_reasonings', 'error', 
                     'hallucination_scores', 'samples_for_hallucination']:
        if json_col in df.columns:
            df[json_col] = df[json_col].apply(
                lambda x: json.loads(x) if x and isinstance(x, str) else x
            )
    
    # Export to CSV
    df.to_csv(output_path, index=False)
    logger.info(f"Successfully exported data to {output_path}")


def check_and_add_column() -> None:
    """Check and add new columns to the existing table"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get the current table structure
    cursor.execute("PRAGMA table_info(results)")
    columns = [column[1] for column in cursor.fetchall()]
    
    # Check if the critique_reasoning column exists
    if 'critique_reasoning' not in columns:
        logger.info("Adding critique_reasoning column to results table")
        cursor.execute("ALTER TABLE results ADD COLUMN critique_reasoning TEXT")
        conn.commit()


# Initialize the database
init_database()

# Check and update table structure
check_and_add_column()