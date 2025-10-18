import os
import re

is_test_run = True

def rename_files_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            new_filename = re.sub(r'(\d{4})-(\d{2})-(\d{2})', r'\3-\2-\1', filename)
            if new_filename != filename:
                old_file_path = os.path.join(directory, filename)
                new_file_path = os.path.join(directory, new_filename)
                if is_test_run:
                    print(f"Would rename: {old_file_path} to {new_file_path}")
                else:
                    os.rename(old_file_path, new_file_path)
                    print(f"Renamed: {old_file_path} to {new_file_path}")

if __name__ == "__main__":
    target_directory = 'path/to/your/directory'  # Change this to your target directory
    rename_files_in_directory(target_directory)
