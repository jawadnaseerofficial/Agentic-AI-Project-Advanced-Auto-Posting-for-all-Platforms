# Agentic-AI-Project-Advanced-Auto-Posting-for-all-Platforms or Agentic-AI-Advanced-AutoPublisher

Automated, high-quality content and image publishing across multiple platforms using agentic AI.

This project leverages Google's Agent Development Kit (ADK) along with APIs like Unsplash to autonomously generate professional articles, create visually appealing image posts, and publish them directly to social media platforms such as Mastodon.

Features

Real-time Trend Analysis: Automatically fetches the latest technology and industry topics.

Professional Content Generation: Generates concise, human-like articles (~50 words) optimized for engagement.

Visual Content Creation: Produces image posts with title and content over blurred, semi-transparent overlays on contextually relevant images fetched via the Unsplash API.

Multi-Platform Distribution: Seamlessly posts to platforms like Mastodon.

Agentic AI Workflow: Fully autonomous content research, writing, design, and publishing pipeline.

Use Cases

Tech & business news articles

Social media marketing campaigns

Company updates & announcements

Blog summaries, newsletters, and content repurposing

Any domain requiring timely, visually rich, high-impact content

Installation

Clone this repository:

git clone https://github.com/jawadnaseerofficial/Agentic-AI-Project-Advanced-Auto-Posting-for-all-Platforms.git
cd Agentic-AI-Project-Advanced-Auto-Posting-for-all-Platforms


Create a virtual environment and activate it:

python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


Set your API keys in the script:

GOOGLE_API_KEY for Google ADK

UNSPLASH_ACCESS_KEY for Unsplash API

Mastodon CLIENT_KEY, CLIENT_SECRET, and ACCESS_TOKEN

Usage

Run the agent to automatically generate and post content:

python agent.py


The system will:

Fetch trending topics from Google.

Generate professional, human-like articles.

Fetch a relevant image from Unsplash.

Overlay the title and article text over a blurred, semi-transparent background.

Post the image with content to Mastodon.

Customization

Fonts & Styles: Update arialbd.ttf and arial.ttf for customized text appearance.

Overlay & Colors: Adjust gradient and overlay settings in agent.py for different visual effects.

Target Platforms: Extend posting to other social media APIs as needed.

Contributing

Contributions are welcome! Feel free to submit pull requests for:

New features

Bug fixes

Visual enhancements

Multi-platform integrations

License

This project is open-source and available under the MIT License.
