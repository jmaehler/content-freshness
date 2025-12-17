# Content Freshness & Decay Auditor

A premium web application that analyzes content for "Information Decay". It determines if a piece of content is still accurate, relevant, and "fresh" based on the current date.

## Features
- **Decay Scoring**: accurate 0-100 score of how obsolete the content is.
- **Visual Highlighter**: Color-coded highlighting of specific outdated phrases.
- **URL Fetcher**: Direct analysis of blog posts via URL.
- **Premium UI**: Dark mode, glassmorphism design.

## Setup
1. **Create and Activate Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Requirements**:
   ```bash
   pip install flask requests beautifulsoup4 anthropic python-dotenv
   ```

3. **Set your API Key**:
   Create a `.env` file and add:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

4. **Run the app**:
   ```bash
   python app.py
   ```
