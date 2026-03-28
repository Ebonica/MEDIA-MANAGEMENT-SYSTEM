# Save as fix_indentation.py
import os

files = [
    'pages/4_📺_Channel_Management.py',
    'pages/5_🎬_Video_Management.py',
    'pages/6_📋_Playlist_Management.py',
]

for filepath in files:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace tabs with 4 spaces
        content = content.replace('\t', '    ')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Fixed: {filepath}")

print("\n✅ All files fixed! Run: streamlit run app.py")