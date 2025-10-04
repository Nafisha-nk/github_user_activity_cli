#!/usr/bin/env python3
"""
GitHub Activity CLI
A simple command line tool to fetch and display recent GitHub user activity.
"""

import sys
import json
import urllib.request
import urllib.error
from datetime import datetime
from typing import List, Dict, Optional


class GitHubActivityFetcher:
    """Fetches and processes GitHub user activity."""
    
    # GitHub API base URL
    BASE_URL = "https://api.github.com/users"
    
    # Event type mappings to human-readable messages
    EVENT_MESSAGES = {
        'PushEvent': "Pushed {payload[commits]} commits to {repo[name]}",
        'IssuesEvent': "{payload[action]} an issue in {repo[name]}",
        'IssueCommentEvent': "Commented on an issue in {repo[name]}",
        'WatchEvent': "Starred {repo[name]}",
        'ForkEvent': "Forked {repo[name]}",
        'CreateEvent': "Created {payload[ref_type]} in {repo[name]}",
        'DeleteEvent': "Deleted {payload[ref_type]} in {repo[name]}",
        'PullRequestEvent': "{payload[action]} a pull request in {repo[name]}",
        'ReleaseEvent': "Released {payload[release][tag_name]} in {repo[name]}",
        'PublicEvent': "Made {repo[name]} public",
        'MemberEvent': "{payload[action]} a collaborator to {repo[name]}"
    }
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'GitHub-Activity-CLI/1.0',
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def fetch_activity(self, username: str) -> List[Dict]:
        """
        Fetch recent activity for a GitHub user.
        
        Args:
            username: GitHub username
            
        Returns:
            List of activity events
            
        Raises:
            SystemExit: On API errors or invalid username
        """
        url = f"{self.BASE_URL}/{username}/events"
        
        try:
            request = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(request) as response:
                data = response.read().decode('utf-8')
                return json.loads(data)
                
        except urllib.error.HTTPError as e:
            if e.code == 404:
                self._print_error(f"User '{username}' not found")
            elif e.code == 403:
                self._print_error("API rate limit exceeded. Please try again later.")
            else:
                self._print_error(f"GitHub API error: {e.code} - {e.reason}")
        except urllib.error.URLError as e:
            self._print_error(f"Network error: {e.reason}")
        except json.JSONDecodeError as e:
            self._print_error(f"Invalid response from GitHub API: {e}")
        except Exception as e:
            self._print_error(f"Unexpected error: {e}")
    
    def format_event(self, event: Dict) -> Optional[str]:
        """
        Format a GitHub event into a human-readable string.
        
        Args:
            event: GitHub event dictionary
            
        Returns:
            Formatted event string or None if event type is not supported
        """
        event_type = event.get('type')
        
        if event_type in self.EVENT_MESSAGES:
            try:
                message_template = self.EVENT_MESSAGES[event_type]
                message = message_template.format(**event)
                
                # Add timestamp if available
                created_at = event.get('created_at')
                if created_at:
                    timestamp = self._format_timestamp(created_at)
                    message = f"{timestamp} - {message}"
                
                return message
            except KeyError:
                return f"{event_type} in {event.get('repo', {}).get('name', 'unknown')}"
        
        return None
    
    def _format_timestamp(self, timestamp_str: str) -> str:
        """Format ISO timestamp to readable format."""
        try:
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M')
        except ValueError:
            return timestamp_str
    
    def _print_error(self, message: str):
        """Print error message and exit."""
        print(f"❌ Error: {message}", file=sys.stderr)
        sys.exit(1)
    
    def display_activity(self, username: str, max_events: int = 10):
        """
        Fetch and display recent GitHub activity.
        
        Args:
            username: GitHub username
            max_events: Maximum number of events to display
        """
        print(f"🔍 Fetching recent activity for '{username}'...")
        
        events = self.fetch_activity(username)
        
        if not events:
            print(f"📭 No recent activity found for '{username}'")
            return
        
        print(f"\n📊 Recent activity for {username}:\n")
        
        displayed_count = 0
        for event in events:
            if displayed_count >= max_events:
                break
                
            formatted_event = self.format_event(event)
            if formatted_event:
                print(f"• {formatted_event}")
                displayed_count += 1
        
        if displayed_count == 0:
            print("No supported event types found in recent activity.")
        else:
            print(f"\n📈 Displaying {displayed_count} most recent events.")


def print_usage():
    """Print usage instructions."""
    print("""
GitHub Activity CLI
Usage: github-activity <username> [max_events]

Arguments:
    username    GitHub username to fetch activity for
    max_events  Maximum number of events to display (default: 10)

Examples:
    github-activity kamranahmedse
    github-activity torvalds 5
    github-activity microsoft 20
        """)


def main():
    """Main entry point for the CLI."""
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
        print_usage()
        sys.exit(0)
    
    username = sys.argv[1]
    
    # Parse optional max_events parameter
    max_events = 10
    if len(sys.argv) > 2:
        try:
            max_events = int(sys.argv[2])
            if max_events <= 0:
                raise ValueError
        except ValueError:
            print("❌ Error: max_events must be a positive integer", file=sys.stderr)
            sys.exit(1)
    
    # Validate username
    if not username.strip():
        print("❌ Error: Username cannot be empty", file=sys.stderr)
        sys.exit(1)
    
    fetcher = GitHubActivityFetcher()
    fetcher.display_activity(username, max_events)


if __name__ == "__main__":
    main()