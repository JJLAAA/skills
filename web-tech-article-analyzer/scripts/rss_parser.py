#!/usr/bin/env python3
"""
RSS/Atom Feed Parser for Blog Series Analysis

This script detects and parses RSS/Atom feeds from blog homepages,
extracting article links, titles, dates, and other metadata for batch processing.
"""

import sys
import xml.etree.ElementTree as ET
from urllib.parse import urljoin, urlparse
from datetime import datetime
import re
from typing import List, Dict, Optional, Tuple


def find_feed_links(html_content: str, base_url: str) -> List[Dict[str, str]]:
    """
    Find RSS/Atom feed links in HTML <head> section.

    Args:
        html_content: HTML content of the page
        base_url: Base URL for resolving relative links

    Returns:
        List of dicts with 'type' and 'href' keys
    """
    feeds = []

    # Pattern 1: <link rel="alternate" type="application/rss+xml" href="...">
    rss_pattern = r'<link\s+[^>]*rel=["\']alternate["\'][^>]*type=["\']application/rss\+xml["\'][^>]*href=["\']([^"\']+)["\']'
    for match in re.finditer(rss_pattern, html_content, re.IGNORECASE):
        href = match.group(1)
        feeds.append({'type': 'rss', 'href': urljoin(base_url, href)})

    # Pattern 2: <link rel="alternate" type="application/atom+xml" href="...">
    atom_pattern = r'<link\s+[^>]*rel=["\']alternate["\'][^>]*type=["\']application/atom\+xml["\'][^>]*href=["\']([^"\']+)["\']'
    for match in re.finditer(atom_pattern, html_content, re.IGNORECASE):
        href = match.group(1)
        feeds.append({'type': 'atom', 'href': urljoin(base_url, href)})

    # Pattern 3: Common feed paths (try these if no feeds found in head)
    if not feeds:
        common_paths = ['/feed', '/rss', '/atom.xml', '/feed.xml', '/rss.xml']
        for path in common_paths:
            feeds.append({'type': 'rss', 'href': urljoin(base_url, path)})

    return feeds


def is_blog_homepage(html_content: str, url: str) -> Tuple[bool, float]:
    """
    Detect if the current page is a blog homepage.

    Args:
        html_content: HTML content of the page
        url: URL of the page

    Returns:
        Tuple of (is_blog, confidence_score)
    """
    indicators = {
        'positive': 0,
        'negative': 0
    }

    # Positive indicators
    if re.search(r'<link\s+[^>]*type=["\']application/(rss|atom)\+xml["\']', html_content, re.IGNORECASE):
        indicators['positive'] += 3

    if re.search(r'(blog|weblog|journal|diary)', url, re.IGNORECASE):
        indicators['positive'] += 1

    # Check for common blog patterns
    if re.search(r'(post|article|entry)\s*(list|archive|index)', html_content, re.IGNORECASE):
        indicators['positive'] += 1

    # Multiple article links on homepage (typical blog)
    article_links = len(re.findall(r'<a\s+[^>]*href=["\'][^"\']*/(20\d{2}/\d{2}/|post|article|entry)', html_content, re.IGNORECASE))
    if article_links >= 5:
        indicators['positive'] += 2

    # Check for pagination or archive links
    if re.search(r'(page|older|newer|previous|next)\s*(post|entry|page)', html_content, re.IGNORECASE):
        indicators['positive'] += 1

    # Negative indicators (single article page)
    if re.search(r'(article|single|post)\s+(content|body|detail)', html_content, re.IGNORECASE):
        indicators['negative'] += 2

    # Calculate confidence
    total_score = indicators['positive'] - indicators['negative']
    confidence = min(max(total_score / 5.0, 0), 1)  # Normalize to 0-1

    is_blog = confidence >= 0.4
    return is_blog, confidence


def parse_rss_feed(xml_content: str, feed_url: str) -> List[Dict[str, str]]:
    """
    Parse RSS/Atom feed XML and extract article entries.

    Args:
        xml_content: RSS/Atom XML content
        feed_url: URL of the feed (for resolving relative links)

    Returns:
        List of article dicts with 'title', 'url', 'date', 'description' keys
    """
    articles = []

    try:
        root = ET.fromstring(xml_content)

        # Determine feed type and namespace
        is_rss = root.tag == 'rss' or 'rss' in root.tag.lower()
        is_atom = root.tag == '{http://www.w3.org/2005/Atom}feed' or root.tag == 'feed'

        entries = []

        if is_rss:
            # RSS format
            channel = root.find('.//channel')
            if channel is not None:
                entries = channel.findall('.//item')
        elif is_atom:
            # Atom format
            entries = root.findall('.//{http://www.w3.org/2005/Atom}entry')
        else:
            # Try to find items regardless of namespace
            entries = root.findall('.//item') + root.findall('.//{*}entry')

        for entry in entries:
            article = {}

            # Title
            title_elem = entry.find('.//title') or entry.find('.//{*}title')
            article['title'] = title_elem.text if title_elem is not None else 'Untitled'

            # URL/Link
            link_elem = entry.find('.//link') or entry.find('.//{*}link')
            if link_elem is not None:
                if link_elem.get('href'):
                    article['url'] = link_elem.get('href')
                else:
                    article['url'] = link_elem.text
            else:
                # Try guid as fallback
                guid_elem = entry.find('.//guid') or entry.find('.//{*}guid')
                article['url'] = guid_elem.text if guid_elem is not None else ''

            # Resolve relative URLs
            if article['url']:
                article['url'] = urljoin(feed_url, article['url'])

            # Date
            date_elem = (entry.find('.//pubDate') or entry.find('.//{*}pubDate') or
                        entry.find('.//published') or entry.find('.//{*}published') or
                        entry.find('.//updated') or entry.find('.//{*}updated'))
            article['date'] = date_elem.text if date_elem is not None else ''

            # Description/Summary
            desc_elem = (entry.find('.//description') or entry.find('.//{*}description') or
                        entry.find('.//summary') or entry.find('.//{*}summary') or
                        entry.find('.//content') or entry.find('.//{*}content'))
            article['description'] = desc_elem.text if desc_elem is not None else ''

            # Strip HTML tags from description
            if article['description']:
                article['description'] = re.sub(r'<[^>]+>', '', article['description'])
                article['description'] = ' '.join(article['description'].split())[:200]

            articles.append(article)

    except ET.ParseError as e:
        print(f"ERROR: Failed to parse XML: {e}", file=sys.stderr)
        return []

    return articles


def parse_article_date(date_str: str) -> Optional[float]:
    """
    Parse article date string into Unix timestamp.

    Handles both RSS 2.0 and Atom date formats:
    - RSS 2.0: "Fri, 13 Feb 2026 00:00:00 GMT" (pubDate)
    - Atom: "2026-02-14T04:54:41+00:00" (published)

    Args:
        date_str: Date string from RSS/Atom feed

    Returns:
        Unix timestamp (float) or None if parsing fails
    """
    if not date_str:
        return None

    # Normalize timezone abbreviations to UTC
    normalized = date_str.replace('GMT', '+0000').replace('UTC', '+0000').replace('Z', '+0000')

    # Comprehensive list of date formats for RSS/Atom feeds
    # RSS 2.0 formats (RFC 2822 / RFC 822)
    rss_formats = [
        '%a, %d %b %Y %H:%M:%S %z',      # Fri, 13 Feb 2026 00:00:00 +0000
        '%a, %d %b %Y %H:%M:%S %Z',       # Fri, 13 Feb 2026 00:00:00 GMT (after normalization to +0000)
        '%a, %d %b %y %H:%M:%S %z',      # Fri, 13 Feb 26 00:00:00 +0000
        '%a, %d %b %Y %H:%M:%S',         # Fri, 13 Feb 2026 00:00:00 (no timezone)
        '%d %b %Y %H:%M:%S %z',          # 13 Feb 2026 00:00:00 +0000
        '%d %b %Y',                       # 13 Feb 2026
    ]

    # Atom formats (ISO 8601 / RFC 3339)
    atom_formats = [
        '%Y-%m-%dT%H:%M:%S%z',           # 2026-02-14T04:54:41+00:00
        '%Y-%m-%dT%H:%M:%SZ',            # 2026-02-14T04:54:41+0000
        '%Y-%m-%dT%H:%M:%S',             # 2026-02-14T04:54:41 (no timezone)
        '%Y-%m-%dT%H:%M:%S.%f%z',        # 2026-02-14T04:54:41.123+00:00
        '%Y-%m-%dT%H:%M:%S.%fZ',         # 2026-02-14T04:54:41.123+0000
        '%Y-%m-%d',                       # 2026-02-14
    ]

    # Try RSS formats first (more common for blogs)
    for fmt in rss_formats + atom_formats:
        try:
            dt = datetime.strptime(normalized, fmt)
            return dt.timestamp()
        except ValueError:
            continue

    # Try parsing without weekday name (may be in different languages)
    try:
        # Remove weekday name from beginning (e.g., "Fri, " -> "")
        cleaned = re.sub(r'^[A-Za-z]+,\s*', '', normalized)
        for fmt in rss_formats + atom_formats:
            try:
                dt = datetime.strptime(cleaned, fmt)
                return dt.timestamp()
            except ValueError:
                continue
    except Exception:
        pass

    return None


def filter_articles_by_date(articles: List[Dict], days: int = 7) -> List[Dict]:
    """
    Filter articles by date range (default: last 7 days).

    Args:
        articles: List of article dicts
        days: Number of recent days to include (0 = no filtering)

    Returns:
        Filtered list of articles within the specified time range
    """
    if not days:
        return articles

    cutoff_date = datetime.now().timestamp() - (days * 86400)
    filtered = []
    skipped_count = 0

    for article in articles:
        if not article.get('date'):
            # Skip articles without date information
            skipped_count += 1
            continue

        article_timestamp = parse_article_date(article['date'])

        if article_timestamp is None:
            # If date parsing fails, skip this article
            skipped_count += 1
            continue

        if article_timestamp >= cutoff_date:
            filtered.append(article)

    # Log skipped articles count to stderr for debugging
    if skipped_count > 0:
        print(f"NOTE: Skipped {skipped_count} articles with invalid/missing dates", file=sys.stderr)

    return filtered


def format_article_list(articles: List[Dict], max_count: int = 20) -> str:
    """
    Format article list for display.

    Args:
        articles: List of article dicts
        max_count: Maximum number of articles to display

    Returns:
        Formatted string
    """
    output = []
    output.append(f"## 发现 {len(articles)} 篇文章\n")

    for i, article in enumerate(articles[:max_count], 1):
        date_str = f" ({article['date']})" if article['date'] else ''
        desc_str = f"\n   {article['description']}" if article['description'] else ''
        output.append(f"{i}. {article['title']}{date_str}")
        output.append(f"   URL: {article['url']}{desc_str}")
        output.append("")

    if len(articles) > max_count:
        output.append(f"\n... 还有 {len(articles) - max_count} 篇文章未显示")

    return "\n".join(output)


def main():
    """CLI interface for the RSS parser."""

    if len(sys.argv) < 2:
        print("Usage: rss_parser.py <command> [args]", file=sys.stderr)
        print("", file=sys.stderr)
        print("Commands:", file=sys.stderr)
        print("  detect <html_file> <base_url>    - Detect if page is blog homepage", file=sys.stderr)
        print("  find-feeds <html_file> <base_url> - Find RSS/Atom feed links", file=sys.stderr)
        print("  parse <xml_file> <feed_url>      - Parse RSS/Atom feed", file=sys.stderr)
        print("  recent <xml_file> <feed_url> [days] - Get recent articles (default 7 days)", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    if command == 'detect':
        if len(sys.argv) < 4:
            print("Usage: rss_parser.py detect <html_file> <base_url>", file=sys.stderr)
            sys.exit(1)

        with open(sys.argv[2], 'r', encoding='utf-8') as f:
            html = f.read()

        is_blog, confidence = is_blog_homepage(html, sys.argv[3])
        print(f"IS_BLOG: {is_blog}")
        print(f"CONFIDENCE: {confidence:.2f}")

    elif command == 'find-feeds':
        if len(sys.argv) < 4:
            print("Usage: rss_parser.py find-feeds <html_file> <base_url>", file=sys.stderr)
            sys.exit(1)

        with open(sys.argv[2], 'r', encoding='utf-8') as f:
            html = f.read()

        feeds = find_feed_links(html, sys.argv[3])
        print(f"FOUND: {len(feeds)}")
        for feed in feeds:
            print(f"FEED: {feed['type']} -> {feed['href']}")

    elif command == 'parse':
        if len(sys.argv) < 4:
            print("Usage: rss_parser.py parse <xml_file> <feed_url>", file=sys.stderr)
            sys.exit(1)

        with open(sys.argv[2], 'r', encoding='utf-8') as f:
            xml = f.read()

        articles = parse_rss_feed(xml, sys.argv[3])
        print(format_article_list(articles))

    elif command == 'recent':
        days = int(sys.argv[4]) if len(sys.argv) > 4 else 7

        with open(sys.argv[2], 'r', encoding='utf-8') as f:
            xml = f.read()

        articles = parse_rss_feed(xml, sys.argv[3])
        recent = filter_articles_by_date(articles, days)
        print(format_article_list(recent))

    else:
        print(f"ERROR: Unknown command '{command}'", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
