"""
LinkedIn API integration for posting content.
Uses the LinkedIn REST API v2 with OAuth Bearer token.
"""

import os
import requests


LINKEDIN_API_BASE = "https://api.linkedin.com/rest"
LINKEDIN_API_VERSION = "202504"


def _get_headers() -> dict:
    token = os.environ["LINKEDIN_ACCESS_TOKEN"]
    return {
        "Authorization": f"Bearer {token}",
        "LinkedIn-Version": LINKEDIN_API_VERSION,
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
    }


def get_person_urn() -> str:
    """
    Fetch the authenticated user's person URN.
    Returns urn:li:person:{id}
    """
    urn = os.environ.get("LINKEDIN_PERSON_URN")
    if urn:
        return urn

    token = os.environ["LINKEDIN_ACCESS_TOKEN"]

    # Try /v2/me (requires r_liteprofile scope)
    resp = requests.get(
        "https://api.linkedin.com/v2/me",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    if resp.ok:
        person_id = resp.json().get("id")
        if person_id:
            return f"urn:li:person:{person_id}"

    # Try /rest/userinfo (requires openid scope)
    resp2 = requests.get(
        f"{LINKEDIN_API_BASE}/userinfo",
        headers={
            "Authorization": f"Bearer {token}",
            "LinkedIn-Version": LINKEDIN_API_VERSION,
        },
        timeout=10,
    )
    if resp2.ok:
        sub = resp2.json().get("sub")
        if sub:
            return f"urn:li:person:{sub}"

    raise ValueError(
        f"Cannot auto-fetch LinkedIn Person URN.\n"
        f"  /v2/me response:      {resp.status_code} {resp.text[:100]}\n"
        f"  /rest/userinfo resp:  {resp2.status_code} {resp2.text[:100]}\n\n"
        f"Fix: Set LINKEDIN_PERSON_URN in your .env file.\n"
        f"To find your URN: LinkedIn Developer Portal -> OAuth 2.0 tools -> \n"
        f"  regenerate token with 'r_liteprofile' scope added to your app,\n"
        f"  then run: python -c \"from src.linkedin_poster import get_person_urn; print(get_person_urn())\""
    )


def upload_image_to_linkedin(image_bytes: bytes) -> str | None:
    """
    Upload a PNG image to LinkedIn.
    Tries new REST images API first, falls back to legacy assets API.
    Returns image/asset URN string, or None on failure.
    """
    person_urn = get_person_urn()
    token = os.environ["LINKEDIN_ACCESS_TOKEN"]

    # --- New REST images API ---
    init_resp = requests.post(
        f"{LINKEDIN_API_BASE}/images?action=initializeUpload",
        headers=_get_headers(),
        json={"initializeUploadRequest": {"owner": person_urn}},
        timeout=15,
    )
    if init_resp.ok:
        val = init_resp.json().get("value", {})
        upload_url = val.get("uploadUrl")
        image_urn = val.get("image")
        if upload_url and image_urn:
            put = requests.put(
                upload_url,
                data=image_bytes,
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/octet-stream"},
                timeout=30,
            )
            if put.ok:
                return image_urn

    # --- Legacy assets API ---
    reg_resp = requests.post(
        "https://api.linkedin.com/v2/assets?action=registerUpload",
        headers={
            "Authorization": f"Bearer {token}",
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json",
        },
        json={
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "owner": person_urn,
                "serviceRelationships": [
                    {"relationshipType": "OWNER", "identifier": "urn:li:userGeneratedContent"}
                ],
            }
        },
        timeout=15,
    )
    if reg_resp.ok:
        val = reg_resp.json().get("value", {})
        upload_url = (
            val.get("uploadMechanism", {})
            .get("com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest", {})
            .get("uploadUrl")
        )
        asset_urn = val.get("asset")
        if upload_url and asset_urn:
            put = requests.put(
                upload_url,
                data=image_bytes,
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/octet-stream"},
                timeout=30,
            )
            if put.ok:
                return asset_urn

    print("Image upload failed — posting text only.")
    return None


def post_to_linkedin(content: str, image_bytes: bytes | None = None) -> dict:
    """
    Post text content (with optional image) to LinkedIn.
    Tries /rest/posts first, falls back to /v2/ugcPosts.

    Args:
        content: The text body of the LinkedIn post

    Returns:
        dict with 'success' bool and 'post_id' or 'error'
    """
    person_urn = get_person_urn()
    token = os.environ["LINKEDIN_ACCESS_TOKEN"]

    # LinkedIn has a 3000 char limit on commentary
    if len(content) > 3000:
        content = content[:2997] + "..."

    # Upload image if provided
    image_urn = None
    if image_bytes:
        image_urn = upload_image_to_linkedin(image_bytes)

    # --- Attempt 1: newer /rest/posts API ---
    payload = {
        "author": person_urn,
        "commentary": content,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }
    if image_urn and image_urn.startswith("urn:li:image:"):
        payload["content"] = {"media": {"id": image_urn}}

    resp = requests.post(
        f"{LINKEDIN_API_BASE}/posts",
        headers=_get_headers(),
        json=payload,
        timeout=15,
    )

    if resp.status_code in (200, 201):
        post_id = resp.headers.get("x-restli-id") or resp.headers.get("X-RestLi-Id", "unknown")
        return {"success": True, "post_id": post_id}

    # --- Attempt 2: fallback to legacy /v2/ugcPosts ---
    ugc_media_category = "NONE"
    ugc_media = []
    if image_urn and image_urn.startswith("urn:li:asset:"):
        ugc_media_category = "IMAGE"
        ugc_media = [{"status": "READY", "media": image_urn}]

    ugc_payload = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content},
                "shareMediaCategory": ugc_media_category,
                **({"media": ugc_media} if ugc_media else {}),
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }

    resp2 = requests.post(
        "https://api.linkedin.com/v2/ugcPosts",
        headers={
            "Authorization": f"Bearer {token}",
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json",
        },
        json=ugc_payload,
        timeout=15,
    )

    if resp2.status_code in (200, 201):
        post_id = resp2.json().get("id", "unknown")
        return {"success": True, "post_id": post_id}

    return {
        "success": False,
        "error": (
            f"/rest/posts: HTTP {resp.status_code}: {resp.text[:150]}\n"
            f"/v2/ugcPosts: HTTP {resp2.status_code}: {resp2.text[:150]}"
        ),
    }


def validate_credentials() -> bool:
    """Check that LinkedIn credentials are valid before posting."""
    try:
        get_person_urn()
        return True
    except Exception as e:
        print(f"LinkedIn credential validation failed: {e}")
        return False
