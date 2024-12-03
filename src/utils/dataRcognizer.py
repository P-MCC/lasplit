import os
import mimetypes


class DatasetTypeDetector:
    VALID_IMAGE_EXTENSIONS = {
        ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff",
        ".webp", ".svg", ".heif", ".heic", ".cr2", ".nef",
        ".arw", ".dng"
    }

    def __init__(self, path):
        self.path = path

    def is_image_classification_dataset(self):
        """
        Detect if the provided path is an image classification dataset.
        """
        if not os.path.exists(self.path):
            return False

        subdirs = [d for d in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, d))]
        if not subdirs:
            return False

        classification_structure = False

        for subdir in subdirs:
            subdir_path = os.path.join(self.path, subdir)

            if self._is_class_subdirectory(subdir_path):
                classification_structure = True
            elif self._is_train_test_val_structure(subdir_path):
                classification_structure = True

        return classification_structure

    def _is_class_subdirectory(self, path):
        """
        Check if a directory contains only image files and no other file types.
        """
        for root, _, files in os.walk(path):
            for file in files:
                if not self._is_valid_image_file(file):
                    return False
        return True

    def _is_train_test_val_structure(self, path):
        """
        Check if the directory contains subdirectories like train, test, or val
        and those subdirectories contain class subdirectories with valid image files.
        """
        train_test_val = ["train", "test", "val"]
        for ttv in train_test_val:
            ttv_path = os.path.join(path, ttv)
            if os.path.exists(ttv_path) and os.path.isdir(ttv_path):
                subdirs = [d for d in os.listdir(ttv_path) if os.path.isdir(os.path.join(ttv_path, d))]
                if not subdirs:
                    return False
                if any(not self._is_class_subdirectory(os.path.join(ttv_path, subdir)) for subdir in subdirs):
                    return False
        return True

    def _is_valid_image_file(self, filename):
        """
        Check if a file is a valid image based on its extension.
        """
        _, ext = os.path.splitext(filename)
        return ext.lower() in self.VALID_IMAGE_EXTENSIONS

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


# Example usage:
path = r"M:\Codes-Scripts\ALL_Classification\Data\ALL-IDB1_70Train_30Test"
detector = DatasetTypeDetector(path)

if detector.is_image_classification_dataset():
    print(f"{path} is a valid image classification dataset.")
    if detector.contains_metadata_file():
        print("It also contains metadata files.")
else:
    print(f"{path} is not a valid image classification dataset.")
    
print(f"Folder structure for '{path}':")
print_folder_structure(path)