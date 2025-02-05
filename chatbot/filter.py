import pandas as pd


def initial_filtering(file_path, filters):
    """
    Performs an initial filtering of the courses based on key parameters:
    - University name
    - Field name (e.g., Engineering, Business, etc.)
    - University location
    - Degree program type

    The filtering is case-insensitive and trims extra whitespace.

    Args:
        file_path (str): Path to the Excel file.
        filters (dict): Dictionary containing filtering criteria with keys:
            "university name", "field type", "location", "degree program type"

    Returns:
        pd.DataFrame: Filtered DataFrame after applying the initial filters.
    """
    # Load the Excel file
    df = pd.read_excel(file_path, sheet_name="Sheet1")

    # Normalize the columns for string comparison
    for col in ["university_name", "field_name", "location", "degree_program"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower()

    print("Initial course count:", df.shape[0])

    # Apply the University Name filter if provided
    if filters.get("university name"):
        uni_filter = filters["university name"].strip().lower()
        df = df[df["university_name"].notna() & (df["university_name"] == uni_filter)]
        print("After university name filter:", df.shape[0])

    # Apply the Field Type filter if provided (e.g., Engineering)
    if filters.get("field type"):
        field_filter = filters["field type"].strip().lower()
        df = df[df["field_name"].notna() & (df["field_name"] == field_filter)]
        print("After field type filter:", df.shape[0])

    # Apply the University Location filter if provided
    if filters.get("location"):
        location_filter = filters["location"].strip().lower()
        df = df[df["location"].notna() & (df["location"] == location_filter)]
        print("After location filter:", df.shape[0])

    # Apply the Degree Program Type filter if provided
    if filters.get("degree program type"):
        degree_filter = filters["degree program type"].strip().lower()
        df = df[df["degree_program"].notna() & (df["degree_program"] == degree_filter)]
        print("After degree program type filter:", df.shape[0])

    return df



