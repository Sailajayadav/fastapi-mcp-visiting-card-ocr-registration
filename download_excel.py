import requests

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

# Example usage:
# download_excel_sheet("https://example.com/contacts.xlsx", "contacts.xlsx")