# patch_datetime.py
import os
import re

# Path to the database.py file
db_file_path = 'src/core/database.py'

# Read the file content
with open(db_file_path, 'r') as f:
    content = f.read()

# Import our datetime utility
import_statement = 'import json\nimport os\n'
new_import = 'import json\nimport os\nfrom ..utils.datetime_utils import datetime_json_dumps\n'
content = content.replace(import_statement, new_import)

# Replace json.dumps with our custom function
content = content.replace('json.dumps(doc)', 'datetime_json_dumps(doc)')
content = content.replace('json.dumps(document)', 'datetime_json_dumps(document)')

# Write the modified content back
with open(db_file_path, 'w') as f:
    f.write(content)

print("Database.py has been patched to handle datetime objects.")