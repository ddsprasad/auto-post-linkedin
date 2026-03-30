"""
Auto LinkedIn Post Generator
----------------------------
Generates and publishes daily LinkedIn posts on Gen AI, Databricks, and SQL Server.

Usage:
    python main.py                   # Generate and post (default)
    python main.py --dry-run         # Generate but don't post (preview only)
    python main.py --force           # Post even if already posted today
    python main.py --topic gen_ai    # Override topic (gen_ai|databricks|sql_server)
    python main.py --type tip_of_day # Override post type
"""

import argparse
import io
import os
import sys
from datetime import datetime, timezone

# Force UTF-8 output on Windows so emojis in posts print correctly
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from dotenv import load_dotenv

from src.db import init_db, get_post_count, get_recent_subtopics, record_post, was_posted_today
from src.content_generator import get_topic_for_today, get_post_type, generate_post, generate_image_content
from src.image_generator import render_infographic
from src.linkedin_poster import post_to_linkedin, validate_credentials
from src.topics import TOPICS, POST_TYPES

load_dotenv()


def parse_args():
    parser = argparse.ArgumentParser(description="Auto LinkedIn Post Generator")
    parser.add_argument("--dry-run", action="store_true", help="Generate post but don't publish")
    parser.add_argument("--force", action="store_true", help="Post even if already posted today")
    parser.add_argument("--topic", choices=list(TOPICS.keys()), help="Override topic")
    parser.add_argument("--type", dest="post_type", choices=list(POST_TYPES.keys()), help="Override post type")
    parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation prompt (for automation)")
    return parser.parse_args()


def run(args):
    print(f"\n{'='*60}")
    print(f"  LinkedIn Auto Post  |  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"{'='*60}\n")

    # Initialize DB
    init_db()

    # Determine topic first (needed for per-topic duplicate guard)
    day_of_week = datetime.now(timezone.utc).weekday()
    if args.topic:
        from src.topics import TOPICS as T
        topic = {"key": args.topic, **T[args.topic]}
    else:
        topic = get_topic_for_today(day_of_week)

    # Guard: skip if this topic was already posted today
    if not args.force and not args.dry_run and was_posted_today(topic["key"]):
        print(f"Already posted {topic['name']} today. Use --force to override.")
        sys.exit(0)

    # Per-topic post count (Gen AI #1, #2 ... Databricks #1, #2 ... independently)
    post_count = get_post_count(topic["key"])
    if args.post_type:
        from src.topics import POST_TYPES as PT
        post_type = {"key": args.post_type, **PT[args.post_type]}
    else:
        post_type = get_post_type(post_count)

    print(f"Topic      : {topic['name']}")
    print(f"Post type  : {post_type['name']}")
    print(f"Post #     : {post_count + 1}")

    # Avoid recently used subtopics
    recent = get_recent_subtopics(topic["key"], limit=5)

    print("\nGenerating content with Claude...")
    content, subtopic = generate_post(
        topic=topic,
        post_type=post_type,
        recent_subtopics=recent,
        post_number=post_count + 1,
    )

    print(f"Subtopic   : {subtopic}")
    print(f"\n{'-'*60}")
    print("GENERATED POST:")
    print(f"{'-'*60}")
    print(content)
    print(f"{'-'*60}\n")
    print(f"Characters : {len(content)}")

    # Generate infographic image
    print("\nGenerating infographic image...")
    image_bytes = None
    try:
        img_data = generate_image_content(content, topic, post_count + 1)
        image_bytes = render_infographic(
            topic_key=topic["key"],
            topic_name=topic["name"],
            post_number=post_count + 1,
            title=img_data["title"],
            points=img_data["points"],
        )
        print(f"Image      : {len(image_bytes) // 1024} KB infographic ready")
    except Exception as e:
        print(f"Image generation failed (will post text only): {e}")

    if args.dry_run:
        print("\n[DRY RUN] Post not published.")
        if image_bytes:
            dry_img_path = "dry_run_image.png"
            with open(dry_img_path, "wb") as f:
                f.write(image_bytes)
            print(f"[DRY RUN] Image saved to: {dry_img_path}")
        record_post(
            topic_key=topic["key"],
            post_type=post_type["key"],
            subtopic=subtopic,
            content=content,
            linkedin_id=None,
            status="dry_run",
        )
        return

    # Interactive approval — ask before publishing
    if not args.yes:
        print("\nPublish this post to LinkedIn? [y/N] ", end="", flush=True)
        answer = input().strip().lower()
        if answer != "y":
            print("Cancelled. Post not published.")
            record_post(
                topic_key=topic["key"],
                post_type=post_type["key"],
                subtopic=subtopic,
                content=content,
                linkedin_id=None,
                status="cancelled",
            )
            return

    # Validate LinkedIn credentials
    if not validate_credentials():
        print("\nError: LinkedIn credentials invalid. Check LINKEDIN_ACCESS_TOKEN.")
        sys.exit(1)

    # Post to LinkedIn
    print("Publishing to LinkedIn...")
    result = post_to_linkedin(content, image_bytes=image_bytes)

    if result["success"]:
        linkedin_id = result["post_id"]
        record_post(
            topic_key=topic["key"],
            post_type=post_type["key"],
            subtopic=subtopic,
            content=content,
            linkedin_id=linkedin_id,
        )
        print(f"Posted successfully! LinkedIn post ID: {linkedin_id}")
    else:
        print(f"Failed to post: {result['error']}")
        record_post(
            topic_key=topic["key"],
            post_type=post_type["key"],
            subtopic=subtopic,
            content=content,
            linkedin_id=None,
            status="failed",
        )
        sys.exit(1)


if __name__ == "__main__":
    args = parse_args()
    run(args)
