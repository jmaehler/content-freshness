import pytest
from unittest.mock import patch, MagicMock
import json
from auditor import audit_content

# Sample valid response content
SAMPLE_JSON_RESPONSE = """
{
  "status": "Green",
  "decay_score": 10,
  "flagged_phrases": [],
  "reasoning": "Content appears fresh.",
  "update_suggestion": "None"
}
"""

def test_audit_content_no_api_key():
    # Patch os.getenv to return None for ANTHROPIC_API_KEY
    # We also need to reload or re-import the module, or simpler: patch the global 'client' variable in auditor
    # However, 'client' is initialized at module level. Easier to patch 'auditor.client' directly.
    
    with patch('auditor.client', None):
        result = audit_content("Test text")
        assert result["status"] == "Red"
        assert "Anthropic API Key not found" in result["reasoning"]

def test_audit_content_success():
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text=SAMPLE_JSON_RESPONSE)]
    
    with patch('auditor.client') as mock_client:
        mock_client.messages.create.return_value = mock_message
        
        result = audit_content("Test text")
        assert result["status"] == "Green"
        assert result["decay_score"] == 10

def test_audit_content_markdown_parsing():
    # Claude might wrap response in ```json ... ```
    wrapped_response = f"```json\n{SAMPLE_JSON_RESPONSE}\n```"
    
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text=wrapped_response)]
    
    with patch('auditor.client') as mock_client:
        mock_client.messages.create.return_value = mock_message
        
        result = audit_content("Test text")
        assert result["status"] == "Green"

def test_audit_content_api_error():
    with patch('auditor.client') as mock_client:
        mock_client.messages.create.side_effect = Exception("API Error")
        
        result = audit_content("Test text")
        assert result["status"] == "Red"
        assert "Error during analysis" in result["reasoning"]
