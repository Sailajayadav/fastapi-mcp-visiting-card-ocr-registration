import requests
import pandas as pd

def download_excel_sheet(url, output_path):
    """
    Downloads an Excel sheet from the given URL and saves it to the specified output path.

    Args:
        url (str): The URL of the Excel sheet to download.
        output_path (str): The local file path where the Excel sheet will be saved.

    Returns:
        bool: True if download was successful, False otherwise.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        with open(output_path, 'wb') as file:
            file.write(response.content)

        print(f"Excel sheet downloaded successfully to {output_path}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading Excel sheet: {e}")
        return False

def read_excel_sheet(file_path):
    """
    Reads an Excel sheet from the given file path and returns the data as a pandas DataFrame.

    Args:
        file_path (str): The path to the Excel file.

    Returns:
        pd.DataFrame: The data from the Excel sheet.
    """
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print(f"Error reading Excel sheet: {e}")
        return None

if __name__ == "__main__":
    # Read the local contacts.xlsx file
    df = read_excel_sheet("contacts.xlsx")
    if df is not None:
        print("Contents of contacts.xlsx:")
        print(df)