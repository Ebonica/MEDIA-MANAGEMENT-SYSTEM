from config.database import db
from collections import defaultdict

database = db.get_db()

print("🔍 Cleaning up duplicate entries...\n")

# Remove duplicate channels
channels = list(database.channels.find())
seen = {}

for ch in channels:
    key = f"{ch['channel_name']}_{ch['creator_id']}"
    if key in seen:
        print(f"Deleting duplicate channel: {ch['channel_name']}")
        database.channels.delete_one({'_id': ch['_id']})
    else:
        seen[key] = ch['_id']

print(f"✅ Channels cleaned. Total channels: {database.channels.count_documents({})}")

# Remove duplicate videos
videos = list(database.videos.find())
seen = {}

for v in videos:
    key = f"{v['title']}_{v['creator_id']}_{v.get('created_at', '')}"
    if key in seen:
        print(f"Deleting duplicate video: {v['title']}")
        database.videos.delete_one({'_id': v['_id']})
    else:
        seen[key] = v['_id']

print(f"✅ Videos cleaned. Total videos: {database.videos.count_documents({})}")
print("\n✅ Cleanup complete!")