"""
QUICK FIX FOR NAVIGATION ERRORS
Run this script in your project root directory to fix all st.switch_page() issues
"""

import os
import re

def fix_navigation_in_file(filepath):
    """Fix st.switch_page() calls in a file"""
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Store original content
        original = content
        
        # Replace all st.switch_page() with appropriate alternatives
        replacements = [
            # Login/Register navigation
            (r'st\.switch_page\("pages/2_🔐_Login\.py"\)', 
             'st.info("Please use the sidebar to navigate to Login page")'),
            
            (r'st\.switch_page\("pages/3_📝_Register\.py"\)', 
             'st.info("Please use the sidebar to navigate to Register page")'),
            
            # App/Home navigation
            (r'st\.switch_page\("app\.py"\)', 
             'st.rerun()'),
            
            # Channel Management
            (r'st\.switch_page\("pages/4_📺_Channel_Management\.py"\)', 
             'st.info("Navigate to Channel Management using the sidebar")'),
            
            # Video Management
            (r'st\.switch_page\("pages/5_🎬_Video_Management\.py"\)', 
             'st.info("Navigate to Video Management using the sidebar")'),
            
            # Playlist Management
            (r'st\.switch_page\("pages/6_📋_Playlist_Management\.py"\)', 
             'st.info("Navigate to Playlist Management using the sidebar")'),
            
            # Comment System
            (r'st\.switch_page\("pages/7_💬_Comment_System\.py"\)', 
             'st.info("Navigate to Comment System using the sidebar")'),
            
            # Analytics
            (r'st\.switch_page\("pages/8_📊_Analytics_Reports\.py"\)', 
             'st.info("Navigate to Analytics & Reports using the sidebar")'),
            
            # Search
            (r'st\.switch_page\("pages/9_🔍_Search_Filter\.py"\)', 
             'st.info("Navigate to Search & Filter using the sidebar")'),
            
            # Settings
            (r'st\.switch_page\("pages/10_⚙️_Settings\.py"\)', 
             'st.info("Navigate to Settings using the sidebar")'),
        ]
        
        # Apply replacements
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        # If content changed, write it back
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed: {filepath}")
            return True
        else:
            print(f"⏭️  No changes needed: {filepath}")
            return False
            
    except Exception as e:
        print(f"❌ Error fixing {filepath}: {e}")
        return False

def main():
    """Main function to fix all files"""
    print("🔧 Starting navigation fix...\n")
    
    files_to_fix = [
        'app.py',
        'pages/1_🏠_Home.py',
        'pages/2_🔐_Login.py',
        'pages/3_📝_Register.py',
        'pages/4_📺_Channel_Management.py',
        'pages/5_🎬_Video_Management.py',
        'pages/6_📋_Playlist_Management.py',
        'pages/7_💬_Comment_System.py',
        'pages/8_📊_Analytics_Reports.py',
        'pages/9_🔍_Search_Filter.py',
        'pages/10_⚙️_Settings.py',
    ]
    
    fixed_count = 0
    for filepath in files_to_fix:
        if os.path.exists(filepath):
            if fix_navigation_in_file(filepath):
                fixed_count += 1
        else:
            print(f"⚠️  File not found: {filepath}")
    
    print(f"\n✅ Fixed {fixed_count} files!")
    print("\n🚀 You can now run: streamlit run app.py")

if __name__ == "__main__":
    main()