"""
Content generator using Claude Agent SDK (uses your Claude Code Max subscription).
No separate ANTHROPIC_API_KEY required.
"""

import anyio
import json
import random
import re
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage
from .topics import TOPICS, POST_TYPES, POST_TYPE_ROTATION, WEEKLY_SCHEDULE


def get_topic_for_today(day_of_week: int) -> dict:
    """Return the topic config for a given day (0=Monday, 6=Sunday)."""
    topic_key = WEEKLY_SCHEDULE.get(day_of_week, "gen_ai")
    return {"key": topic_key, **TOPICS[topic_key]}


def get_post_type(post_count: int) -> dict:
    """Rotate through post types based on total post count."""
    idx = post_count % len(POST_TYPE_ROTATION)
    post_type_key = POST_TYPE_ROTATION[idx]
    return {"key": post_type_key, **POST_TYPES[post_type_key]}


async def _call_agent(prompt: str, system_prompt: str) -> str:
    """Run the Agent SDK query and return the result text."""
    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            allowed_tools=[],  # pure text generation — no file/web tools needed
            system_prompt=system_prompt,
        ),
    ):
        if isinstance(message, ResultMessage):
            return message.result
    return ""


def generate_post(
    topic: dict,
    post_type: dict,
    recent_subtopics: list[str] | None = None,
    post_number: int = 1,
) -> tuple[str, str]:
    """
    Generate a LinkedIn post using Claude Agent SDK (Claude Code Max subscription).

    Args:
        topic: Topic config from TOPICS dict
        post_type: Post type config from POST_TYPES dict
        recent_subtopics: List of recently used subtopics to avoid repeating
        post_number: Sequential post number for series tracking

    Returns:
        Tuple of (post_content, subtopic_used)
    """
    # Pick a subtopic, avoiding recently used ones
    available = topic["subtopics"]
    if recent_subtopics:
        available = [s for s in available if s not in recent_subtopics] or topic["subtopics"]
    subtopic = random.choice(available)

    system_prompt = (
        f"You are an expert in {topic['name']} with 10+ years of hands-on experience. "
        "You write highly engaging LinkedIn posts that get strong engagement from technical professionals. "
        "Your posts are practical, insightful, and always include real-world examples. "
        "You avoid fluff and get straight to the point. "
        "IMPORTANT: Never use markdown formatting (no **, no ##). Use plain text only. Do NOT use emojis anywhere in the post."
    )

    user_prompt = (
        f"Write a LinkedIn post about: {subtopic}\n\n"
        f"Post type: {post_type['name']}\n"
        f"Instructions: {post_type['prompt_instruction']}\n\n"
        f"Topic hashtags to include: {topic['hashtags']}\n\n"
        f"This is post #{post_number} in the series. Make it feel like part of an ongoing series "
        f"that professionals look forward to.\n\n"
        f"REQUIRED: The very first line must be exactly this format (no emojis, no extra symbols):\n"
        f"Post #{post_number} {topic['name']} - [short descriptive title for this post]\n\n"
        "Then leave a blank line and write the post body.\n"
        "Write only the post content. No introductions or meta-commentary.\n\n"
        "CRITICAL: The ENTIRE post (including title, body, and hashtags) must be under 2800 characters total. "
        "LinkedIn cuts off posts over 3000 characters. Keep it concise and complete."
    )

    post_content = anyio.run(_call_agent, user_prompt, system_prompt)
    return post_content.strip(), subtopic


def generate_image_content(post_text: str, topic: dict, post_number: int) -> dict:
    """
    Extract structured content for the infographic image from a post.
    Returns dict with 'title' (str) and 'points' (list of 5 strings).
    """
    prompt = (
        f"Extract key insights from this LinkedIn post for a visual infographic card.\n\n"
        f"POST:\n{post_text[:1400]}\n\n"
        f"Return ONLY a raw JSON object — no markdown, no code fences, no extra text:\n"
        f'{{ "title": "punchy title max 44 chars", "points": ["insight 1 max 58 chars", "insight 2", "insight 3", "insight 4", "insight 5"] }}'
    )

    result = anyio.run(
        _call_agent,
        prompt,
        "You extract key insights for infographic visuals. Return ONLY valid raw JSON. No markdown. No explanations.",
    )

    # Parse JSON robustly
    for pattern in [r'\{.*?"title".*?"points".*?\}', r'\{.*\}']:
        match = re.search(pattern, result, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group())
                if "title" in data and "points" in data:
                    return data
            except json.JSONDecodeError:
                pass

    # Fallback if parsing fails
    return {
        "title": f"{topic['name']} — Key Insights",
        "points": [
            "Practical insight from today's post",
            "Common mistake to avoid",
            "Pro tip for better results",
            "What separates beginners from experts",
            "Action you can take right now",
        ],
    }
