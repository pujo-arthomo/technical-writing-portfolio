import os
import datetime

# Configuration - Change these if needed
FOLDER_PATH = "reports"          # Folder to scan for CSV files
DEFAULT_PREFIX = "2025_projectA" # Default prefix if user doesn't provide one
LOG_FILE = "rename_log.txt"      # Log file for feedback

def log_message(message):
    """Write message to log file and print to console"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    print(full_message)
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(full_message + "\n")

def get_user_prefix():
    """Ask user for custom prefix (optional)"""
    print(f"Default prefix: {DEFAULT_PREFIX}")
    custom = input("Enter custom prefix (or press Enter for default): ").strip()
    return custom if custom else DEFAULT_PREFIX

def preview_changes(folder_path, prefix):
    """Show preview of planned renames"""
    print("\nPreview of changes:")
    csv_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.csv')]
    if not csv_files:
        print("No CSV files found in folder.")
        return False
    
    for filename in csv_files:
        new_filename = f"{prefix}_{filename}"
        print(f"  {filename} → {new_filename}")
    return True

def rename_files(folder_path, prefix):
    """Perform the actual renaming with basic duplicate check"""
    renamed_count = 0
    skipped_count = 0
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.csv'):
            old_path = os.path.join(folder_path, filename)
            new_filename = f"{prefix}_{filename}"
            new_path = os.path.join(folder_path, new_filename)
            
            if os.path.exists(new_path):
                log_message(f"Skipped (would overwrite): {filename} → {new_filename}")
                skipped_count += 1
                continue
                
            try:
                os.rename(old_path, new_path)
                log_message(f"Renamed: {filename} → {new_filename}")
                renamed_count += 1
            except Exception as e:
                log_message(f"Error renaming {filename}: {str(e)}")
    
    log_message(f"\nSummary: {renamed_count} files renamed, {skipped_count} skipped.")

if __name__ == "__main__":
    print("Enhanced CSV File Renamer Tool")
    print(f"Scanning folder: {FOLDER_PATH}\n")
    
    if not os.path.exists(FOLDER_PATH):
        print(f"Error: Folder '{FOLDER_PATH}' not found.")
        input("Press Enter to exit...")
        exit()
    
    # Clear previous log
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    
    prefix = get_user_prefix()
    
    if preview_changes(FOLDER_PATH, prefix):
        confirm = input("\nProceed with renaming? (y/n): ").strip().lower()
        if confirm == 'y':
            rename_files(FOLDER_PATH, prefix)
        else:
            print("Renaming cancelled.")
    else:
        print("Nothing to do.")
    
    print(f"\nLog saved to {LOG_FILE}")
    input("Press Enter to exit...")
