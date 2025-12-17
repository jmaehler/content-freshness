import pytest
from unittest.mock import patch, MagicMock
from scraper import scrape_url

def test_scrape_url_success():
    mock_html = """
    <html>
        <body>
            <script>console.log('ignore');</script>
            <nav>Menu</nav>
            <h1>Title</h1>
            <p>   Content paragraph.  </p>
            <footer>Copyright</footer>
        </body>
    </html>
    """
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.text = mock_html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Expected output: Title\nContent paragraph.
        # (Based on current logic: filters nav/footer/script, strips whitespace)
        result = scrape_url("http://example.com")
        
        assert "Title" in result
        assert "Content paragraph." in result
        assert "Menu" not in result
        assert "console.log" not in result

def test_scrape_url_error():
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception("Connection refused")
        
        result = scrape_url("http://bad-url.com")
        assert "Error fetching URL" in result
        assert "Connection refused" in result
