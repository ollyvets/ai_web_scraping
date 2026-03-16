import pandas as pd
import os

def export_to_csv(data: list[dict], filename: str = "leads_report.csv") -> str:
    """
    Exports the analyzed lead data to a CSV file.
    Demonstrates a basic reporting pipeline for the extracted intelligence.

    Args:
        data (list[dict]): A list of dictionaries containing analyzed company data 
                           (e.g., name, url, pain_points, pitch).
        filename (str): The desired name for the output CSV file. Defaults to "leads_report.csv".

    Returns:
        str: A status message indicating success and the file path, or an error message.
    """
    if not data:
        return "Warning: No data provided to export."

    try:
        # Define the output directory and ensure it exists
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, filename)
        
        # Convert the list of dictionaries into a pandas DataFrame
        df = pd.DataFrame(data)
        
        # Export to CSV without the index column
        df.to_csv(filepath, index=False, encoding='utf-8')
        
        return f"Success: Exported {len(data)} records to {filepath}"
    
    except Exception as e:
        return f"Error during export: {str(e)}"