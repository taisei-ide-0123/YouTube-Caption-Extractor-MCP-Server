# YouTube-Caption-Extractor-MCP-Server

This project provides a FastMCP server for extracting YouTube video captions along with video metadata such as the title and channel name.
Designed for integration with Claude for Desktop and other MCP-compatible clients.

## Features

- Extracts captions using prioritized languages (English > Japanese > Auto-generated).
- Returns plain text captions for easy integration with language models.
- Retrieves video metadata: title and channel name.
- **Automatically summarizes video content using MCP Client like Claude.**
- Supports standard, shortened, and embedded YouTube URLs.
- Graceful error handling when captions are unavailable.

## Installation

1. Clone the repository:

```bash
git clone git@github.com:taisei-ide-0123/YouTube-Caption-Extractor-MCP-Server.git
cd YouTube-Caption-Extractor-MCP-Server
```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Integration with Claude for Desktop

1. Open the Claude configuration file:

```bash
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

2. Add the following configuration:

```json
{
  "mcpServers": {
    "youtube_caption_extractor": {
      "command": "python3",
      "args": [
        "/ABSOLUTE/PATH/TO/YouTube-Caption-Extractor-MCP-Server/server.py"
      ]
    }
  }
}
```

3. Restart Claude for Desktop.

---

## Example Usage

### YouTube Link

Simply paste a YouTube link on Claude Desktop or compatible MCP clients.

```
https://www.youtube.com/watch?v=CXhYDOvgpuU
```

You can also summarize the video with your native language like this.

```
日本語で要約してください。
https://www.youtube.com/watch?v=CXhYDOvgpuU
```

### MCP Client Request

```json
{
  "youtube_url": "https://youtu.be/CXhYDOvgpuU?si=UOQMshq-XNYaO_Kw"
}
```

### MCP Server Response

```json
{
  "status": "success",
  "title": "Lessons on AI agents from Claude Plays Pokemon",
  "channel": "Anthropic",
  "language_code": "en",
  "language_name": "English",
  "is_generated": false,
  "available_languages": [
    {
      "code": "en",
      "name": "English",
      "is_generated": false
    },
    {
      "code": "en",
      "name": "English (auto-generated)",
      "is_generated": true
    }
  ],
  "captions": "- AI agents take independent actions and learn from feedback.\n- Claude plays Pokemon ..."
}
```

### Claude's Response

```
I'll help you with that YouTube video. Let me extract the captions to understand what it's about.

Based on the captions, this is a discussion about "Lessons on AI agents from Claude Plays Pokemon" featuring David from Anthropic's Applied AI team and Alex who leads Claude Relations at Anthropic. Let me summarize the key points:

The video discusses an experiment where Claude (Anthropic's AI model) was set up to play the game Pokemon Red autonomously as a way to test and demonstrate AI agents. Here are the main insights:

1. Purpose of the experiment:
   - Testing how Claude performs when taking many actions without human intervention
   - Evaluating how AI agents can develop strategies, learn from feedback, and adapt
   - Creating a visible demonstration of what "AI agents" actually means in practice

2. How it works:
   - Claude receives screenshots of the game and can press Game Boy buttons (A, B, up, down, left, right)
   - The AI has to figure out gameplay through trial and error
   - They implemented memory management so Claude could remember what it had done previously

3. Claude's evolution playing Pokemon:
   - Earlier models (Claude 3.5 Sonnet) struggled with basic navigation
   - Newer models (Claude 3.7 Sonnet) showed dramatic improvement in planning and persistence
   - The experiment became a good benchmark for measuring model improvement

4. Key agent capabilities demonstrated:
   - Planning and strategy development
   - Trying different approaches when stuck
   - Learning from feedback and incorporating new information
   - Adapting to unexpected situations

5. Challenges and limitations:
   - Visual understanding (Claude struggles to interpret the game screen accurately)
   - Navigation and spatial awareness
   - Time perception (Claude doesn't get "tired" of repeating the same action thousands of times)
   - Self-awareness of its own limitations

The video highlights how this experiment has helped people understand AI agents beyond just chatbots - showing an AI that can take independent actions, observe results, and adjust strategies. The project became unexpectedly popular with thousands of viewers on Twitch cheering Claude on as it progressed through the game.

Would you like me to elaborate on any particular aspect of this video?
```

### Error Response Example

```json
{
  "status": "error",
  "message": "Captions are not available or have been disabled for this video."
}
```

---

## Dependencies

- fastmcp
- youtube_transcript_api
- yt_dlp

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
