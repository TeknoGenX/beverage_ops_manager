import io
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any

def export_to_excel(data: List[Dict[str, Any]], filename: str = None) -> bytes:
    """
    Export a list of dictionaries to an Excel file in memory.

    Args:
        data (List[Dict[str, Any]]): List of data to export.
        filename (str, optional): Filename for the Excel file. If None, uses a timestamp.

    Returns:
        bytes: The Excel file as bytes.
    """
    if not data:
        raise ValueError("Data is empty.")

    df = pd.DataFrame(data)
    output = io.BytesIO()
    if not filename:
        filename = f"laporan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Laporan')
    output.seek(0)
    return output.read()