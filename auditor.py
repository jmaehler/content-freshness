import os
import json
import anthropic
from prompts import get_system_prompt
from dotenv import load_dotenv

load_dotenv()

# Check for API key
api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key) if api_key else None

def audit_content(text: str) -> dict:
    if not client:
        return {
            "status": "Red",
            "decay_score": 0,
            "flagged_phrases": [],
            "reasoning": "Anthropic API Key not found. Please add ANTHROPIC_API_KEY to your .env file.",
            "update_suggestion": "Configure API Key."
        }
        
    try:
        prompt = get_system_prompt()
        
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4096,
            system=prompt,
            messages=[
                {"role": "user", "content": f"Content to Analyze:\n\n{text}"}
            ]
        )
        
        # Claude returns the JSON inside the content block, sometimes with markdown
        content = response.content[0].text
        
        # Clean up if markdown code blocks are present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].strip()
            
        return json.loads(content)
        
    except Exception as e:
        return {
            "status": "Red",
            "decay_score": 0,
            "flagged_phrases": [],
            "reasoning": f"Error during analysis: {str(e)}",
            "update_suggestion": "Check connection and try again."
        }
