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

    "tiktok": """Transform the following content into a TikTok video script.

Rules:
- Total length: 150-300 words (60-90 second video)
- Start with a powerful hook in the first line (the first 3 seconds decide if viewers stay)
- Use a conversational, energetic, direct-to-camera tone
- Structure: Hook → Setup → Key Points (2-3 max) → Punchline/CTA
- Write in short, spoken sentences — not written prose
- Include [PAUSE] markers where dramatic pauses would go
- End with a strong CTA ("Follow for more", "Save this", "Comment your take")
- Add 3-5 hashtags on a final line

Content to repurpose:
{content}""",

    "newsletter": """Transform the following content into an email newsletter section.

Rules:
- Total length: 400-600 words
- Start with a compelling subject line on its own line, prefixed with "Subject: "
- Follow with a brief personal greeting/intro (1-2 sentences, warm and direct)
- Break the content into 2-3 scannable sections with bold section headers
- Use short paragraphs (2-3 sentences max)
- Include a "Key Takeaway" or "TL;DR" callout near the end (one sentence)
- End with a single clear call to action (reply, click, share)
- Tone: knowledgeable friend writing you an email, not a corporation

Content to repurpose:
{content}""",

    "facebook": """Transform the following content into a Facebook post.

Rules:
- Total length: 500-800 characters
- Start with a hook that makes people stop scrolling
- Use storytelling — personal angle or relatable framing
- Short paragraphs (1-2 sentences) with line breaks between them
- Include a question or call to action at the end to drive comments
- Use 1-3 emojis naturally (not forced)
- End with 1-3 hashtags max (Facebook penalizes hashtag stuffing)
- Warm, conversational tone — like talking to friends

Content to repurpose:
{content}""",

    "reddit": """Transform the following content into a Reddit post.

Rules:
- Start with a compelling title on its own line, prefixed with "Title: "
- Follow with the post body (300-600 words)
- Write in first person, conversational tone
- No hashtags, no emojis — Reddit hates both
- Be genuine and add value — Reddit rewards authenticity
- Structure with clear paragraphs and use bullet points or numbered lists where helpful
- End with a discussion prompt or question to invite comments
- Include a "TL;DR" at the very end (1-2 sentences)
- Tone: knowledgeable community member sharing insights, not a marketer

Content to repurpose:
{content}""",

    "threads": """Transform the following content into a Threads post series.

Rules:
- Create 3-7 posts in a thread
- Each post should be under 500 characters
- Number each post (1/, 2/, etc.)
- First post must be a strong hook — casual and scroll-stopping
- More conversational and casual than Twitter — think talking to a friend
- Use line breaks for readability within each post
- Emojis are welcome but don't overdo it (1-2 per post max)
- Last post should be a takeaway or CTA
- No hashtags (Threads de-prioritizes them)

Content to repurpose:
{content}""",

    "pinterest": """Transform the following content into a Pinterest pin description.

Rules:
- Total length: 200-500 characters
- Start with an attention-grabbing first sentence (this shows in preview)
- Include 3-5 relevant keywords naturally woven into the description (Pinterest is a search engine)
- Use a clear call to action ("Click to read more", "Save for later", "Try this today")
- Add 2-5 relevant hashtags at the end
- Tone: helpful, inspirational, actionable
- Write as if describing the value someone will get by clicking through

Content to repurpose:
{content}""",

    "youtube": """Transform the following content into a YouTube video description.

Rules:
- Start with a compelling 2-3 sentence summary (first 2 lines show before "Show more")
- Add a blank line, then a detailed description (150-300 words) expanding on the content
- Include a "Timestamps" section with 5-8 timestamps in the format "0:00 - Topic"
- Add a "Key Takeaways" section with 3-5 bullet points
- End with a CTA section: "Like, subscribe, and hit the bell" + relevant links placeholder
- Include 5-10 relevant tags/hashtags on the final line
- Tone: energetic and informative

Content to repurpose:
{content}""",

    "bluesky": """Transform the following content into a Bluesky thread.

Rules:
- Create 3-8 posts
- Each post MUST be 300 characters or fewer (hard limit)
- Number each post (1/, 2/, etc.)
- First post must be a compelling hook
- Write in a smart, conversational tone — Bluesky skews tech-savvy and witty
- No hashtags (Bluesky doesn't use them for discovery)
- Use line breaks within posts for readability
- Last post should be a takeaway, CTA, or witty closer
- More intellectual/dry humor welcome compared to other platforms

Content to repurpose:
{content}""",

    "reels": """Transform the following content into an Instagram/Facebook Reels script.

Rules:
- Total length: 100-200 words (30-60 second video)
- Start with a powerful hook in the FIRST line — must grab attention in 1-2 seconds
- Use quick, punchy sentences — faster paced than TikTok
- Structure: Hook → Quick Setup → 2-3 Rapid Points → Punchline/CTA
- Include [CUT] markers for visual transitions between scenes
- Include [TEXT ON SCREEN: "..."] markers for text overlays
- Write for vertical video, direct-to-camera style
- End with a CTA ("Follow for more", "Save this", "Share with a friend")
- Add 5-10 hashtags on a final line (Reels still benefit from hashtags)
- Tone: fast, energetic, visual

Content to repurpose:
{content}""",
}


def get_prompt(platform: str, content: str) -> str:
    """Return the formatted user prompt for a given platform."""
    template = PLATFORM_PROMPTS.get(platform)
    if not template:
        raise ValueError(f"Unknown platform: {platform}")
    return template.format(content=content)
