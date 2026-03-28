from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

def test_mongodb():
    print("🔍 Testing MongoDB Connection...\n")
    
    try:
        # Test connection
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        
        # Verify connection
        client.admin.command('ping')
        
        print("✅ MongoDB is running and accessible!")
        print(f"   Server: {client.address}")
        
        # List databases
        dbs = client.list_database_names()
        print(f"\n📁 Databases found: {len(dbs)}")
        for db in dbs:
            print(f"   - {db}")
        
        # Check our database
        db = client['youtube_media_db']
        collections = db.list_collection_names()
        print(f"\n📦 Collections in youtube_media_db: {len(collections)}")
        for coll in collections:
            count = db[coll].count_documents({})
            print(f"   - {coll}: {count} documents")
        
        client.close()
        return True
        
    except ServerSelectionTimeoutError:
        print("❌ ERROR: Cannot connect to MongoDB!")
        print("   MongoDB is not running or not accessible.")
        print("\n🔧 SOLUTIONS:")
        print("   1. Install MongoDB: https://www.mongodb.com/try/download/community")
        print("   2. Start MongoDB service:")
        print("      Windows: Check Services → MongoDB")
        print("      Mac: brew services start mongodb-community")
        print("      Linux: sudo systemctl start mongod")
        return False
        
    except ConnectionFailure as e:
        print(f"❌ ERROR: Connection failed: {e}")
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    test_mongodb()