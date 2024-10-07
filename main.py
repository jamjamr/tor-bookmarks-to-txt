import json
import os

def parse_bookmarks(bookmark_data):
    """
    Recursively parse bookmark data and return a list of formatted bookmarks and folders.
    Skip empty folders (those without bookmarks or subfolders with bookmarks).
    """
    result = []
    
    # Check if the current item is a folder with children
    if 'children' in bookmark_data:
        folder_name = bookmark_data.get('title', '').strip()
        folder_contents = []
        
        # Recursively parse each child (could be folders or bookmarks)
        for child in bookmark_data['children']:
            folder_contents.extend(parse_bookmarks(child))
        
        # Only add the folder if it has contents (non-empty, containing bookmarks or valid subfolders)
        if folder_contents:
            result.append('---------')  # Folder separator
            result.append(f"Folder: {folder_name}")
            result.extend(folder_contents)
    
    # If the item is a bookmark (has a URL), add it
    elif bookmark_data.get('uri'):
        bookmark_title = bookmark_data.get('title', 'Untitled')
        bookmark_url = bookmark_data['uri']
        result.append(f"{bookmark_title} - {bookmark_url}")
    
    return result

def convert_bookmarks_to_txt(json_file, txt_file):
    # Read the bookmarks JSON data
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Parse the bookmarks recursively
    bookmarks = parse_bookmarks(data)
    
    # Write the parsed data to a .txt file
    with open(txt_file, 'w', encoding='utf-8') as file:
        for line in bookmarks:
            file.write(line + '\n')

def get_file_name():
    """
    Prompt the user for a file name and assume .json if no extension is provided.
    Automatically generate the output file name with .txt extension.
    """
    file_name = input("Enter the Tor bookmark backup file name (without or with extension): ").strip()
    
    # Assume .json extension if none is provided
    if '.' not in file_name:
        file_name += '.json'
    
    return file_name

# Main logic
json_file_path = get_file_name()  # Get input file name from the user

# Automatically generate output file name by changing extension to .txt
txt_file_path = os.path.splitext(json_file_path)[0] + '.txt'

convert_bookmarks_to_txt(json_file_path, txt_file_path)

print(f"Bookmarks have been successfully written to {txt_file_path}")
