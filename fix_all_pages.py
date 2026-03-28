import os
import re

def remove_dangerous_reruns(filepath):
    """Remove st.rerun() outside forms"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    in_form = False
    form_depth = 0
    
    for i, line in enumerate(lines):
        # Track if we're inside a form
        if 'with st.form' in line or 'st.form(' in line:
            in_form = True
            form_depth += 1
        
        # Check for form end (dedent)
        if in_form and line.strip() and not line[0].isspace():
            form_depth = 0
            in_form = False
        
        # Remove st.rerun() outside forms (except after logout)
        if 'st.rerun()' in line and not in_form:
            # Keep rerun after logout
            if i > 0 and 'logout' in lines[i-1].lower():
                new_lines.append(line)
            else:
                # Comment it out
                indent = len(line) - len(line.lstrip())
                new_lines.append(' ' * indent + '# st.rerun() - Removed to prevent hanging\n')
                new_lines.append(' ' * indent + 'st.success("✓ Action completed! Refresh page to see changes.")\n')
        else:
            new_lines.append(line)
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"✅ Fixed: {filepath}")

# Fix all page files
page_files = [
    'pages/4_📺_Channel_Management.py',
    'pages/5_🎬_Video_Management.py',
    'pages/6_📋_Playlist_Management.py',
    'pages/7_💬_Comment_System.py',
    'pages/10_⚙️_Settings.py',
]

for filepath in page_files:
    if os.path.exists(filepath):
        remove_dangerous_reruns(filepath)

print("\n✅ All pages fixed!")
print("\nNow restart your app:")