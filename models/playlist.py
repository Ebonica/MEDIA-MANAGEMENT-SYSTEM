from datetime import datetime
from config.database import db
from bson import ObjectId


class PlaylistModel:
    def __init__(self):
        self.collection = db.get_db().playlists

    def create(self, playlist_data: dict):
        """
        Create a new playlist with strong, PERMANENT duplicate prevention.

        Rule: For each (creator_id, name) there will be at most ONE playlist.
        If the same name is submitted again for the same creator,
        we just return the existing playlist ID (no new document).
        """

        # 1️⃣ Normalize playlist name
        playlist_name = playlist_data['name'].strip()
        creator_id = playlist_data['creator_id']
        playlist_data['name'] = playlist_name

        # 2️⃣ Check if a playlist with same name + creator already exists
        existing = self.collection.find_one({
            'name': playlist_name,
            'creator_id': creator_id
        })

        if existing:
            # No new insert. Just return the existing playlist ID.
            # No warning print = no scary spam in terminal.
            return str(existing['_id'])

        # 3️⃣ If not existing, create a new one
        if 'video_ids' not in playlist_data:
            playlist_data['video_ids'] = []

        playlist_data['created_at'] = datetime.now()

        result = self.collection.insert_one(playlist_data)
        print(f"✅ New playlist created: {playlist_name} - ID: {result.inserted_id}")
        return str(result.inserted_id)

    def get_by_id(self, playlist_id: str):
        """Get playlist by ID"""
        try:
            return self.collection.find_one({"_id": ObjectId(playlist_id)})
        except Exception as e:
            print(f"[PlaylistModel] get_by_id error: {e}")
            return None

    def get_by_creator(self, creator_id: str):
        """Get all playlists by creator"""
        return list(self.collection.find({"creator_id": creator_id}))

    def get_all(self):
        """Get all playlists"""
        return list(self.collection.find())

    def update(self, playlist_id: str, data: dict):
        """Update playlist"""
        try:
            if 'name' in data and isinstance(data['name'], str):
                data['name'] = data['name'].strip()
            return self.collection.update_one(
                {"_id": ObjectId(playlist_id)},
                {"$set": data}
            )
        except Exception as e:
            print(f"[PlaylistModel] update error: {e}")
            return None

    def delete(self, playlist_id: str):
        """Delete playlist"""
        try:
            return self.collection.delete_one({"_id": ObjectId(playlist_id)})
        except Exception as e:
            print(f"[PlaylistModel] delete error: {e}")
            return None

    def add_video(self, playlist_id: str, video_id: str):
        """Add video to playlist (no duplicate videos inside playlist)"""
        try:
            return self.collection.update_one(
                {"_id": ObjectId(playlist_id)},
                {"$addToSet": {"video_ids": video_id}}
            )
        except Exception as e:
            print(f"[PlaylistModel] add_video error: {e}")
            return None

    def remove_video(self, playlist_id: str, video_id: str):
        """Remove video from playlist"""
        try:
            return self.collection.update_one(
                {"_id": ObjectId(playlist_id)},
                {"$pull": {"video_ids": video_id}}
            )
        except Exception as e:
            print(f"[PlaylistModel] remove_video error: {e}")
            return None

    def reorder_videos(self, playlist_id: str, video_ids: list):
        """Reorder videos in playlist"""
        try:
            return self.collection.update_one(
                {"_id": ObjectId(playlist_id)},
                {"$set": {"video_ids": video_ids}}
            )
        except Exception as e:
            print(f"[PlaylistModel] reorder_videos error: {e}")
            return None
