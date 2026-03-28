"""
Migration script to add subscribers_list field to existing channels
Run this ONCE to update your database schema

Usage:
    python migrate_channels.py
"""

from config.database import db

def migrate_channels():
    """Add subscribers_list field to all existing channels"""
    
    try:
        database = db.get_db()
        channels_collection = database.channels
        
        print("Starting channel migration...")
        print("-" * 50)
        
        # Update all channels that don't have subscribers_list field
        result = channels_collection.update_many(
            {'subscribers_list': {'$exists': False}},
            {
                '$set': {
                    'subscribers_list': []
                }
            }
        )
        
        print(f"✅ Migration completed!")
        print(f"   - Updated {result.modified_count} channels")
        
        # Verify migration
        total_channels = channels_collection.count_documents({})
        channels_with_list = channels_collection.count_documents({'subscribers_list': {'$exists': True}})
        
        print(f"\nDatabase Status:")
        print(f"   - Total channels: {total_channels}")
        print(f"   - Channels with subscribers_list: {channels_with_list}")
        
        if total_channels == channels_with_list:
            print("\n✅ All channels migrated successfully!")
        else:
            print(f"\n⚠️  Warning: {total_channels - channels_with_list} channels still need migration")
            
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        print("Please check your database connection and try again.")

if __name__ == "__main__":
    print("\n" + "="*50)
    print("Channel Database Migration Tool")
    print("="*50 + "\n")
    
    response = input("This will update all existing channels. Continue? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        migrate_channels()
    else:
        print("Migration cancelled.")
    
    print("\nMigration script completed!\n")