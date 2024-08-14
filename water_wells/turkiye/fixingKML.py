
from files import input,output
import xml.etree.ElementTree as ET

def fix_all_unbound_prefixes(content):
    """Fixes common unbound prefix and namespace issues in KML content."""
    content = remove_schema_location(content)
    
    if 'xmlns' not in content:
        content = content.replace('<kml', '<kml xmlns="http://www.opengis.net/kml/2.2"')
    
    if 'xsi:' in content and 'xmlns:xsi=' not in content:
        content = content.replace('<Document ', '<Document xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ')
    
    return content

def remove_schema_location(content):
    """Removes the xsi:schemaLocation attribute from KML content."""
    if 'xsi:schemaLocation' in content:
        start = content.find('xsi:schemaLocation')
        end = content.find('>', start)
        content = content[:start] + content[end:]
    return content

def fix_kml_file(input_path, output_path):
    """Reads a KML file, applies fixes, and writes the fixed content to a new file."""
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            kml_content = file.read()

        # Apply the fixes
        fixed_content = fix_all_unbound_prefixes(kml_content)

        # Save the fixed content to a new file
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(fixed_content)

        # Verify the fixed file is correctly formatted
        tree = ET.parse(output_path)
        root = tree.getroot()
        print(f"Successfully fixed and verified: {output_path}")

    except ET.ParseError as e:
        print(f"Error parsing the file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
fix_kml_file(input, output)
