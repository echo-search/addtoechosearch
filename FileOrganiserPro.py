import os
import shutil

# This points to the folder you opened in a-Shell (iCloud Drive/Downloads)
BASE_DIR = os.path.expanduser("~/Downloads")

EXTENSIONS = {
    "Word": ["doc", "docx", "odt", "rtf", "wpd", "pages"],
    "Music": ["mp3", "wav", "flac", "m4a", "aiff", "ogg", "wma", "aac"],
    "HTML": ["html", "htm", "xhtml", "htmx"],
    "Text": ["txt", "md", "csv", "json", "log", "xml", "yml", "yaml", "ini", "cfg", "toml"],
    "PDF": ["pdf", "epub", "mobi", "azw3"],
    "Images": ["jpg", "jpeg", "png", "gif", "bmp", "heic", "tiff", "svg", "webp", "ico", "psd", "raw"],
    "Videos": ["mp4", "mov", "mkv", "avi", "m4v", "flv", "wmv", "webm"],
    "Code": ["py", "js", "ts", "html", "css", "json", "sh", "c", "cpp", "java", "rb", "php", "go", "rs", "swift", "kt", "tsx", "jsx"],
    "Archives": ["zip", "rar", "tar", "gz", "7z", "bz2", "cab", "iso"],
    "Fonts": ["ttf", "otf", "woff", "woff2"],
    "Presentations": ["ppt", "pptx", "key", "odp"],
    "Spreadsheets": ["xls", "xlsx", "ods", "numbers"],
    "Executables": ["exe", "app", "bat", "cmd", "run", "bin", "dmg"],
}

# Create folders in Downloads if missing
for folder in EXTENSIONS.keys():
    os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "Misc"), exist_ok=True)

# Recursive organise
for root, dirs, files in os.walk(BASE_DIR, topdown=False):
    for filename in files:
        filepath = os.path.join(root, filename)
        ext = filename.split(".")[-1].lower()
        moved = False
        for folder, ext_list in EXTENSIONS.items():
            if ext in ext_list:
                shutil.move(filepath, os.path.join(BASE_DIR, folder, filename))
                moved = True
                break
        if not moved:
            shutil.move(filepath, os.path.join(BASE_DIR, "Misc", filename))

print("✅ Organising complete!")
