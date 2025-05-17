from fastmcp import FastMCP
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from yt_dlp import YoutubeDL
import re
from typing import Dict, Any, Optional, List

mcp = FastMCP("YouTube Caption Extractor")

LANGUAGE_PRIORITY = ["en", "ja"]

def _extract_video_id(url: str) -> str:
    """
    Extracts the YouTube Video ID from a given URL.
    """
    patterns = [
        r"v=([0-9A-Za-z_-]{11})(?:[&?$#])?",
        r"youtu\.be/([0-9A-Za-z_-]{11})(?:[&?$#/])?",
        r"embed/([0-9A-Za-z_-]{11})(?:[?$#])?"
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    raise ValueError("Invalid YouTube URL.")

def _get_video_metadata(video_id: str) -> Dict[str, str]:
    with YoutubeDL({'quiet': True}) as ydl:
        url = f"https://www.youtube.com/watch?v={video_id}"
        info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title", "Unknown Title"),
            "channel": info.get("uploader", "Unknown Channel")
        }

def _select_transcript(
    transcripts: List[Any], language_preference: Optional[str]
) -> Optional[Any]:
    """
    Selects the best transcript based on language preference and defined priority.
    """
    if language_preference:
        for transcript in transcripts:
            if transcript.language_code.startswith(language_preference):
                return transcript

    for lang_prefix in LANGUAGE_PRIORITY:
        for transcript in transcripts:
            if transcript.language_code.startswith(lang_prefix):
                return transcript

    for transcript in transcripts:
        if transcript.is_generated:
            return transcript

    return transcripts[0] if transcripts else None

def _combine_captions(captions: List[Dict[str, Any]]) -> str:
    """
    Combines a list of caption entries into a plain text block.
    """
    return "\n".join(getattr(item, "text", "") for item in captions)

def _list_available_languages(transcripts: List[Any]) -> List[Dict[str, Any]]:
    """
    Returns a summary of available languages from the transcript list.
    """
    return [
        {"code": t.language_code, "name": t.language, "is_generated": t.is_generated}
        for t in transcripts
    ]

def _error_response(message: str) -> Dict[str, str]:
    """
    Generates a standardized error response.
    """
    return {"status": "error", "message": message}

@mcp.tool(
    name="extract_youtube_captions",
    description="Extract captions from a YouTube video. Provide the video URL."
)
def get_captions(
    youtube_url: str, language_preference: Optional[str] = None
) -> Dict[str, Any]:
    """
    Extracts captions from a YouTube video.
    Prioritizes languages: English > Japanese > Auto-generated.

    Args:
        youtube_url (str): The YouTube video URL.
        language_preference (Optional[str]): Preferred language code (e.g., 'en', 'ja').

    Returns:
        dict: Extraction result with status, language details, and plain text captions.
    """
    try:
        video_id = _extract_video_id(youtube_url)
        transcripts = list(YouTubeTranscriptApi.list_transcripts(video_id))

        selected_transcript = _select_transcript(transcripts, language_preference)
        if not selected_transcript:
            return _error_response("No available captions found.")

        captions_text = _combine_captions(selected_transcript.fetch())
        metadata = _get_video_metadata(video_id)

        return {
            "status": "success",
            "title": metadata["title"],
            "channel": metadata["channel"],
            "language_code": selected_transcript.language_code,
            "language_name": selected_transcript.language,
            "is_generated": selected_transcript.is_generated,
            "available_languages": _list_available_languages(transcripts),
            "captions": captions_text
        }

    except (NoTranscriptFound, TranscriptsDisabled, VideoUnavailable):
        return _error_response("Captions are not available or have been disabled for this video.")
    except ValueError as ve:
        return _error_response(str(ve))
    except Exception as ex:
        return _error_response(f"Unexpected error: {str(ex)}")

if __name__ == "__main__":
    mcp.run()
