SYSTEM_PROMPT = """You are an expert content repurposer. Your job is to transform long-form content \
into engaging, platform-specific short-form content. Preserve the original message, key insights, \
and tone while adapting the format for maximum engagement on the target platform. \
Do NOT add information that isn't in the original content. Output ONLY the final content — \
no preamble, no commentary, no explanations."""

PLATFORM_PROMPTS = {
    "twitter": """Transform the following content into a Twitter/X thread.

Rules:
- Create 3 to 10 tweets
- Each tweet MUST be 280 characters or fewer (this is a hard limit)
- Number each tweet (1/, 2/, etc.)
- First tweet must be a compelling hook that stops the scroll
- Last tweet should be a summary or call to action
- Use line breaks within tweets for readability
- No hashtags except optionally 1-2 on the final tweet

Content to repurpose:
{content}""",

    "linkedin": """Transform the following content into a single LinkedIn post.

Rules:
- Total length: 1000-1300 characters
- Start with a bold hook line (the first line people see before "...see more")
- Use short paragraphs (1-2 sentences each)
- Add line breaks between paragraphs for readability
- Include a clear takeaway or call to action
- End with 3-5 relevant hashtags on a separate line
- Professional but conversational tone

Content to repurpose:
{content}""",

    "instagram": """Transform the following content into an Instagram caption.

Rules:
- Main caption body: under 300 characters, punchy and engaging
- Include a clear call to action (e.g., "Save this", "Share with someone who needs this")
- After the main caption, add a blank line then a hashtag block
- Hashtag block: 15-25 relevant hashtags, mix of broad and niche
- Use emojis sparingly (1-3 max in the caption body)

Content to repurpose:
{content}""",
}


def get_prompt(platform: str, content: str) -> str:
    """Return the formatted user prompt for a given platform."""
    template = PLATFORM_PROMPTS.get(platform)
    if not template:
        raise ValueError(f"Unknown platform: {platform}")
    return template.format(content=content)
