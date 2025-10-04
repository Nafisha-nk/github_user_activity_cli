# GitHub User Activity CLI

A simple command line tool to fetch and display recent GitHub user activity.

## Features

- Fetch recent activity for any GitHub user
- Display activities in human-readable format
- Support for various event types (pushes, issues, stars, forks, etc.)
- Error handling for invalid usernames and API issues
- Configurable number of events to display

## Installation

1. Clone or download the script
2. Make it executable:
   ```bash
   chmod +x github_activity.py

# Basic usage
python github_activity.py <username>

# Display specific number of events
python github_activity.py <username> <max_events>

# Examples
python github_activity.py kamranahmedse
python github_activity.py torvalds 5
python github_activity.py microsoft 20

# Help
python github_activity.py --help

## Supported Event Types

- PushEvent: Code pushes and commits

- IssuesEvent: Issue creation and modifications

- WatchEvent: Repository starring

- ForkEvent: Repository forking

- CreateEvent: Branch/tag creation

- And more...

## Error Handling

- Invalid usernames

- API rate limits

- Network connectivity issues

- Invalid responses


## How to Use

1. **Save the code** as `github_activity.py`
2. **Make it executable** (optional):
   ```bash
   chmod +x github_activity.py


## Rn the tool
python github_activity.py kamranahmedse

## Example Output
🔍 Fetching recent activity for 'kamranahmedse'...

📊 Recent activity for kamranahmedse:

• 2024-01-15 14:30 - Pushed 3 commits to kamranahmedse/developer-roadmap
• 2024-01-15 12:15 - Opened an issue in kamranahmedse/developer-roadmap
• 2024-01-14 16:45 - Starred facebook/react
• 2024-01-14 11:20 - Created branch in kamranahmedse/project
• 2024-01-13 09:30 - Pushed 1 commit to kamranahmedse/notes

📈 Displaying 5 most recent events.

## Key Features

  - No External Dependencies: Uses only Python standard library

  - Comprehensive Error Handling: Handles various API errors gracefully

  - User-Friendly Output: Clean, readable format with emojis

  - Multiple Event Types: Supports various GitHub activity types

  - Configurable: Optional limit on number of events to display

Advanced Features You Can Add

  - Caching responses to avoid rate limits

  - Filtering by event type

  - JSON output option

  - Colorized terminal output

  - More detailed commit/issue information

  - Support for private repositories with authentication

https://roadmap.sh/projects/github-user-activity
