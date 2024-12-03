import os
import mimetypes


import os

class DatasetTypeDetector:
    VALID_IMAGE_EXTENSIONS = {
        ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff",
        ".webp", ".svg", ".heif", ".heic", ".cr2", ".nef",
        ".arw", ".dng"
    }
    
    LABEL_FILE_EXTENSIONS = {".txt", ".xml", ".json", ".yaml"}
    
    def __init__(self, path):
        self.path = path

    def is_image_classification_dataset(self):
        """
        Detect if the provided path is a valid image classification dataset.
        """
        if not os.path.exists(self.path):
            return False

        subdirs = [d for d in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, d))]
        if not subdirs:
            return False

        # Check if each subdirectory represents a class with only valid images and no labels
        for subdir in subdirs:
            subdir_path = os.path.join(self.path, subdir)

            if not self._is_class_subdirectory(subdir_path):
                return False

        return True

    def _is_class_subdirectory(self, path):
        """
        Check if a directory contains only image files and no label files.
        """
        for root, _, files in os.walk(path):
            for file in files:
                if self._is_label_file(file) or not self._is_valid_image_file(file):
                    return False
        return True

    def _is_valid_image_file(self, filename):
        """
        Check if a file is a valid image based on its extension.
        """
        _, ext = os.path.splitext(filename)
        return ext.lower() in self.VALID_IMAGE_EXTENSIONS

    def _is_label_file(self, filename):
        """
        Check if a file is a label or annotation file based on its extension.
        """
        _, ext = os.path.splitext(filename)
        return ext.lower() in self.LABEL_FILE_EXTENSIONS

    def contains_label_files(self, path):
        """
        Check if the dataset contains label files like .txt, .xml, .json, or .yaml.
        """
        for root, _, files in os.walk(path):
            for file in files:
                if self._is_label_file(file):
                    return True
        return False
    
    def contains_metadata_file(self):
        """
        Check if the dataset contains metadata files like .csv, .txt, or .pt.
        """
        metadata_extensions = {".csv", ".txt", ".pt"}
        for root, _, files in os.walk(self.path):
            for file in files:
                if os.path.splitext(file)[1].lower() in metadata_extensions:
                    return True
        return False

    
def print_folder_structure(path, indent=""):
    """
    Print the folder structure of the given path in a tree-like format.

    Args:
        path (str): The root directory path.
        indent (str): The indentation used for formatting the structure.
    """
    # Get the list of files and directories
    items = sorted(os.listdir(path))

    for i, item in enumerate(items):
        item_path = os.path.join(path, item)
        # Check if it's the last item to adjust the visual display
        if i == len(items) - 1:
            prefix = "└── "
            next_indent = indent + "    "
        else:
            prefix = "├── "
            next_indent = indent + "│   "

        # Print the current item
        if os.path.isdir(item_path):
            print(f"{indent}{prefix}{item}/")
            print_folder_structure(item_path, next_indent)
        else:
            print(f"{indent}{prefix}{item}")
            
def print_folder_structure_short(path, indent="", max_items=5):
    """
    Print the folder structure of the given path in a tree-like format,
    displaying up to max_items per directory.

    Args:
        path (str): The root directory path.
        indent (str): The indentation used for formatting the structure.
        max_items (int): Maximum number of items to display per folder level.
    """
    # Get the list of files and directories
    items = sorted(os.listdir(path))

    # Determine how many items to display, limited to max_items
    items_to_display = items[:max_items]
    more_items = len(items) > max_items

    for i, item in enumerate(items_to_display):
        item_path = os.path.join(path, item)

        # Check if it's the last item to adjust the visual display
        if i == len(items_to_display) - 1 and not more_items:
            prefix = "└── "
            next_indent = indent + "    "
        else:
            prefix = "├── "
            next_indent = indent + "│   "

        # Print the current item
        if os.path.isdir(item_path):
            print(f"{indent}{prefix}{item}/")
            print_folder_structure_short(item_path, next_indent, max_items)
        else:
            print(f"{indent}{prefix}{item}")

    # If there are more items, indicate them with '...'
    if more_items:
        print(f"{indent}└── ... ({len(items) - max_items} more items)")


# Example usage:
path = r"M:\Datasets\coco128-seg"
detector = DatasetTypeDetector(path)

if detector.is_image_classification_dataset():
    print(f"{path} is a valid image classification dataset.")
    if detector.contains_metadata_file():
        print("It also contains metadata files.")
else:
    print(f"{path} is not a valid image classification dataset.")
    
# print(f"Folder structure for '{path}':")
# print_folder_structure_short(path)