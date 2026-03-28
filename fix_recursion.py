import os
import re

def fix_file(filepath):
    """Remove problematic st.rerun() calls"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Pattern 1: st.rerun() after button click outside form
        # This is the most common cause of recursion
        pattern1 = r'(if st\.button\([^)]+\):.*?)(\s+st\.rerun\(\))'
        content = re.sub(pattern1, r'\1\n        st.success("✓ Done! Refresh page to see changes.")', content, flags=re.DOTALL)
        
        # Pattern 2: st.rerun() in if statements that check session state
        pattern2 = r'(if st\.session_state\.get\([^)]+\).*?)(\s+st\.rerun\(\))'
        content = re.sub(pattern2, r'\1', content, flags=re.DOTALL)
        
        # Pattern 3: Multiple st.rerun() in succession
        content = re.sub(r'st\.rerun\(\)\s+st\.rerun\(\)', 'st.rerun()', content)
        
        if content != original:
            # Backup original
            backup_path = filepath + '.backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original)
            
            # Write fixed version
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Fixed: {filepath}")
            print(f"   Backup saved: {backup_path}")
            return True
        else:
            print(f"⏭️  No changes: {filepath}")
            return False
    
    except Exception as e:
        print(f"❌ Error fixing {filepath}: {e}")
        return False

def main():
    print("🚨 EMERGENCY RECURSION FIX\n")
    print("This will:")
    print("1. Find problematic st.rerun() calls")
    print("2. Create backups of original files")
    print("3. Replace with safe alternatives\n")
    
    files_to_fix = [
        'app.py',
        'pages/2_🔐_Login.py',
        'pages/3_📝_Register.py',
        'pages/4_📺_Channel_Management.py',
        'pages/5_🎬_Video_Management.py',
        'pages/6_📋_Playlist_Management.py',
        'pages/7_💬_Comment_System.py',
        'pages/10_⚙️_Settings.py',
    ]
    
    fixed_count = 0
    for filepath in files_to_fix:
        if os.path.exists(filepath):
            if fix_file(filepath):
                fixed_count += 1
        else:
            print(f"⚠️  Not found: {filepath}")
    
    print(f"\n{'='*50}")
    print(f"✅ Fixed {fixed_count} files")
    print(f"{'='*50}\n")
    
    print("🔧 MANUAL FIXES NEEDED:\n")
    print("1. Open pages/2_🔐_Login.py")
    print("   - Remove st.rerun() after successful login EXCEPT inside form\n")
    
    print("2. Open pages/3_📝_Register.py")
    print("   - Remove all st.rerun() calls\n")
    
    print("3. Open app.py")
    print("   - In sidebar logout button, keep st.rerun() (it's safe there)\n")
    
    print("4. Test by running:")
    print("   streamlit run app.py\n")
    
    print("If recursion persists, restore from backups:")
    print("   cp filename.py.backup filename.py")

if __name__ == "__main__":
    main()