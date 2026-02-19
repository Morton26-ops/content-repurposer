import re
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi

from config import settings


def extract_youtube_id(url: str) -> str | None:
    """Extract video ID from various YouTube URL formats."""
    parsed = urlparse(url)
    if parsed.hostname in ("youtu.be",):
        return parsed.path.lstrip("/")
    if parsed.hostname in ("www.youtube.com", "youtube.com", "m.youtube.com"):
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [None])[0]
        if parsed.path.startswith(("/embed/", "/v/")):
            return parsed.path.split("/")[2]
    return None


def extract_youtube_transcript(url: str) -> str:
    """Fetch transcript from a YouTube video URL."""
    video_id = extract_youtube_id(url)
    if not video_id:
        raise ValueError(f"Could not extract video ID from: {url}")

    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    text = " ".join(entry.text for entry in transcript)
    return text[: settings.max_content_chars]


def extract_article(url: str) -> str:
    """Scrape article text from a URL."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # Remove non-content elements
    for tag in soup.find_all(["nav", "footer", "header", "aside", "script", "style", "noscript"]):
        tag.decompose()

    # Try <article> first, fall back to <main>, then <body>
    container = soup.find("article") or soup.find("main") or soup.find("body")
    if not container:
        raise ValueError("Could not find readable content on the page.")

    paragraphs = container.find_all(["p", "h1", "h2", "h3", "h4", "li"])
    text = "\n\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

    # Fallback: if structured tags yield little, grab all visible text
    if len(text) < 50:
        text = container.get_text(separator="\n", strip=True)

    if len(text) < 50:
        raise ValueError("Extracted content is too short — the page may be JavaScript-rendered or paywalled.")

    return text[: settings.max_content_chars]


def extract_content(input_type: str, content: str) -> str:
    """Route to the correct extractor based on input type."""
    if input_type == "youtube":
        return extract_youtube_transcript(content.strip())
    elif input_type == "url":
        return extract_article(content.strip())
    elif input_type == "text":
        if not content.strip():
            raise ValueError("Please paste some text content.")
        return content.strip()[: settings.max_content_chars]
    else:
        raise ValueError(f"Unknown input type: {input_type}")
