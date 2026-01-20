import difflib

def load_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []

def show_changes(draft_lines, revised_lines):
    differ = difflib.unified_diff(
        draft_lines, revised_lines,
        fromfile="AI Draft",
        tofile="Revised Version",
        lineterm=''
    )
    
    print("Modification Summary (diff):")
    for line in differ:
        print(line.rstrip())

if __name__ == "__main__":
    draft = input("Enter AI draft filename: ").strip()
    revised = input("Enter revised filename: ").strip()
    
    draft_lines = load_file(draft)
    revised_lines = load_file(revised)
    
    if draft_lines and revised_lines:
        show_changes(draft_lines, revised_lines)
    else:
        print("Could not load files.")
