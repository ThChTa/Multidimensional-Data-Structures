import os

def combine_files(file1_path, file2_path, output_path):
    try:
        # Read content from the first file
        with open(file1_path, 'r') as file1:
            content1 = file1.read()

        # Read content from the second file
        with open(file2_path, 'r') as file2:
            content2 = file2.read()

        # Combine the content of the two files
        combined_content = content1 + '\n\n' + content2

        # Write the combined content to the specified output file
        with open(output_path, 'w') as output_file:
            output_file.write(combined_content)

        print(f"Files combined successfully. Output saved to {output_path}")

    except Exception as e:
        print(f"Error combining files: {e}")

# Example usage
path1 = r'C:\Users\Thomas\Desktop\Multidimensional-Data-Structures\trees\r-tree.py'
path2 = r'C:\Users\Thomas\Desktop\Multidimensional-Data-Structures\lsh\lsh.py'
output_path = r'C:\Users\Thomas\Desktop\Multidimensional-Data-Structures\output_path.py'

combine_files(path1, path2, output_path)
