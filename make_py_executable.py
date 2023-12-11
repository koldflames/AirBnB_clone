import os

def make_py_files_executable(directory='.'):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                # Check if the file is not already executable
                if not os.access(file_path, os.X_OK):
                    # Add executable permission to the file
                    os.chmod(file_path, os.stat(file_path).st_mode | 0o111)

if __name__ == "__main__":
    make_py_files_executable()

