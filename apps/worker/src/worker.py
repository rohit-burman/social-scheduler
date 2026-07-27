from __future__ import annotations

import random
import time
from datetime import UTC, datetime

from pymongo import MongoClient

from src.settings import settings


def main() -> None:
    print("Worker started: waiting for jobs")
    
    client = MongoClient(settings.mongodb_url, tz_aware=True)
    db = client[settings.mongodb_db_name]
    
    while True:
        try:
            # Check for scheduled posts
            now = datetime.now(UTC)
            posts = list(db["posts"].find({
                "status": "scheduled",
                "scheduled_at": {"$lte": now}
            }))
            
            for post in posts:
                post_id = str(post["_id"])
                
                # Process the post
                result = process_post(db["posts"], post)
                
                if result["success"]:
                    print(f"Successfully published post {post_id}")
                else:
                    print(f"Failed to publish post {post_id}: {result.get('error', 'Unknown error')}")
                    
        except Exception as e:
            print(f"Worker error: {e}")
        
        time.sleep(5)


def process_post(posts, post: dict) -> dict:
    """Process a single post with retry logic."""
    current_attempt = post.get("attempt", 0)
    max_attempts = post.get("max_attempts", 5)
    
    if current_attempt >= max_attempts:
        # Move to dead letter queue
        posts.update_one(
            {"_id": post["_id"]},
            {"$set": {"status": "failed", "last_error": "Max retries exceeded"}}
        )
        return {"success": False, "error": "Max retries exceeded"}
    
    # Simulate provider call (random success/failure)
    time.sleep(random.uniform(0.5, 1.5))
    
    success = random.random() > 0.3  # 70% success rate for demo
    
    if success:
        posts.update_one(
            {"_id": post["_id"]},
            {"$set": {
                "status": "published",
                "last_error": None,
                "published_at": datetime.now(UTC)
            }}
        )
        return {"success": True}
    else:
        # Calculate backoff delay
        base_delay = 30  # seconds
        delay = base_delay * (2 ** current_attempt)
        
        # Schedule retry
        next_retry = datetime.now(UTC).timestamp() + delay
        
        posts.update_one(
            {"_id": post["_id"]},
            {"$set": {
                "status": "scheduled",
                "scheduled_at": datetime.fromtimestamp(next_retry, UTC),
                "attempt": current_attempt + 1
            }}
        )
        
        return {"success": False, "error": "Provider simulation failed", "retry_in": delay}


if __name__ == "__main__":
    main()