import os
import tkinter as tk
from tkinter import filedialog

def process_directory(current_dir, output_dir, start_folder_num=1, dry_run: bool = False, reserved_targets: set | None = None):
    """
    Recursively processes a directory with numbered subdirectories.
    
    Args:
        current_dir: The directory to process
        output_dir: The directory where renamed files will be moved
        start_folder_num: The starting folder number for this level
        
    Returns:
        The next available folder number after processing this directory
    """
    # Snapshot PNG files that originally exist at this level to avoid re-processing
    if reserved_targets is None:
        reserved_targets = set()
    # files that are moved into output_dir during recursion.
    png_files_in_current_snapshot = sorted([
        f for f in os.listdir(current_dir)
        if os.path.isfile(os.path.join(current_dir, f)) and f.lower().endswith('.png')
    ])

    # Get all numeric subdirectories and sort them
    numeric_dirs = []
    for item in os.listdir(current_dir):
        item_path = os.path.join(current_dir, item)
        if os.path.isdir(item_path) and item.isdigit():
            numeric_dirs.append((int(item), item_path))
    
    # Sort by original number and create mapping to consecutive numbers starting from start_folder_num
    numeric_dirs.sort(key=lambda x: x[0])
    
    current_folder_num = start_folder_num
    
    # Process each numbered subdirectory
    for original_num, dir_path in numeric_dirs:
        print(f"\nProcessing folder: {dir_path} -> Mapped to folder number {current_folder_num}")
        
        # Check if this directory contains more numbered subdirectories (recursive case)
        has_numeric_subdirs = any(
            os.path.isdir(os.path.join(dir_path, item)) and item.isdigit() 
            for item in os.listdir(dir_path)
        )
        
        if has_numeric_subdirs:
            # Recursive case: process subdirectories
            current_folder_num = process_directory(
                dir_path, output_dir, current_folder_num, dry_run, reserved_targets
            )
        else:
            # Base case: process PNG files in this directory
            png_files = sorted([f for f in os.listdir(dir_path) if f.lower().endswith('.png')])
            
            file_counter = 1
            for filename in png_files:
                base_name, extension = os.path.splitext(filename)
                new_name = f"{base_name}_{current_folder_num}_{file_counter}{extension}"
                old_path = os.path.join(dir_path, filename)
                new_path = os.path.join(output_dir, new_name)
                
                # Ensure the new name doesn't already exist
                temp_counter = file_counter
                while os.path.exists(new_path) or new_path in reserved_targets:
                    temp_counter += 1
                    new_name = f"{base_name}_{current_folder_num}_{temp_counter}{extension}"
                    new_path = os.path.join(output_dir, new_name)
                if dry_run:
                    print(f"  [DRY-RUN] Would move: '{old_path}' -> '{new_path}'")
                else:
                    os.rename(old_path, new_path)
                    print(f"  Renamed and moved: '{filename}' -> '{new_name}'")
                reserved_targets.add(new_path)
                file_counter += 1
            
            current_folder_num += 1
    
    # Process PNG files at the current directory level (same level as numbered folders)
    # Only process the snapshot taken at function entry to avoid re-processing moved files.
    if png_files_in_current_snapshot:
        print(f"\nProcessing PNG files in directory: {current_dir}")
        for filename in png_files_in_current_snapshot:
            old_path = os.path.join(current_dir, filename)
            if not os.path.exists(old_path):
                # The file might have been removed/renamed externally; skip safely.
                print(f"  Skipped (not found anymore): '{filename}'")
                continue

            base_name, extension = os.path.splitext(filename)
            new_name = f"{base_name}_{current_folder_num}_1{extension}"
            new_path = os.path.join(output_dir, new_name)

            # Ensure the new name doesn't already exist (bump the folder number part)
            temp_num = current_folder_num
            while os.path.exists(new_path) or new_path in reserved_targets:
                temp_num += 1
                new_name = f"{base_name}_{temp_num}_1{extension}"
                new_path = os.path.join(output_dir, new_name)

            if dry_run:
                print(f"  [DRY-RUN] Would move: '{old_path}' -> '{new_path}'")
            else:
                os.rename(old_path, new_path)
                print(f"  Renamed and moved: '{filename}' -> '{new_name}'")
            reserved_targets.add(new_path)
            current_folder_num += 1
    
    return current_folder_num

def rename_images_in_folders(root_dir, dry_run: bool = False):
    """
    Main function to process all numbered subdirectories and PNG files.
    Handles recursive nested structures and renumbers folders to be consecutive starting from 1.
    """
    try:
        print(f"Starting to process directory: {root_dir}\n")
        if dry_run:
            print("Running in DRY-RUN mode. No files will be changed.\n")
        process_directory(
            root_dir,
            root_dir,
            start_folder_num=1,
            dry_run=dry_run,
            reserved_targets=set(),
        )
        print("\n" + "="*60)
        if dry_run:
            print("DRY-RUN completed. No changes were made.")
        else:
            print("File renaming and moving process completed successfully!")
        print("="*60)

    except FileNotFoundError:
        print(f"Error: The directory '{root_dir}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()

def select_folder_and_rename():
    """
    Opens a dialog for the user to select a folder, then runs the renaming process.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    folder_selected = filedialog.askdirectory(title="Select the root folder containing numbered subfolders")
    
    if folder_selected:
        # Ask user whether to run dry-run
        try:
            answer = input("Run as dry-run (no changes)? [y/N]: ").strip().lower()
            dry_run = answer in ("y", "yes")
        except Exception:
            dry_run = False

        rename_images_in_folders(folder_selected, dry_run=dry_run)
    else:
        print("No folder selected. Exiting.")

if __name__ == '__main__':
    select_folder_and_rename()
