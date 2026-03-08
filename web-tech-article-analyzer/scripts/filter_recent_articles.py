#!/usr/bin/env python3
"""
Filter RSS articles to past N days (default: 7).

This script provides reliable date filtering for RSS feeds, handling various
date formats commonly used in RSS/Atom feeds.
"""

import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import argparse
import sys


def parse_rss_date(date_str):
    """Parse various RSS date formats."""
    formats = [
        '%a, %d %b %Y %H:%M:%S %Z',  # RFC 2822
        '%a, %d %b %Y %H:%M:%S %z',  # Alternative timezone
        '%Y-%m-%dT%H:%M:%SZ',           # ISO 8601
        '%Y-%m-%dT%H:%M:%S%z',           # ISO 8601 with offset
        '%Y-%m-%d %H:%M:%S',             # Simple format
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def filter_articles(feed_file, days=7):
    """Filter RSS articles to past N days."""
    cutoff_date = datetime.now() - timedelta(days=days)

    with open(feed_file, 'r', encoding='utf-8') as f:
        xml_content = f.read()

    root = ET.fromstring(xml_content)
    items = root.findall('.//item')

    recent_articles = []
    skipped_count = 0

    for item in items:
        title = item.find('title')
        link = item.find('link')
        pub_date = item.find('pubDate')

        if title is None or link is None:
            skipped_count += 1
            continue

        title_text = title.text if title.text is not None else 'No Title'
        link_text = link.text if link.text is not None else 'No Link'

        if pub_date is not None and pub_date.text:
            parsed_date = parse_rss_date(pub_date.text)
            if parsed_date and parsed_date >= cutoff_date:
                recent_articles.append((parsed_date, title_text, link_text))
            else:
                skipped_count += 1
        else:
            skipped_count += 1

    recent_articles.sort(reverse=True)  # Newest first
    return recent_articles, skipped_count


def main():
    parser = argparse.ArgumentParser(
        description='Filter RSS articles to past N days'
    )
    parser.add_argument(
        'feed_file',
        help='Path to RSS feed XML file'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=7,
        help='Number of days to look back (default: 7)'
    )

    args = parser.parse_args()

    articles, skipped = filter_articles(args.feed_file, args.days)

    print(f"## 发现 {len(articles)} 篇文章 (过去 {args.days} 天)\n")

    for i, (pub_date, title, link) in enumerate(articles, 1):
        print(f"{i}. {title}")
        print(f"   URL: {link}")
        print(f"   Date: {pub_date.strftime('%Y-%m-%d')}\n")

    if skipped > 0:
        print(f"... 还有 {skipped} 篇文章被过滤 (超出时间范围)\n", file=sys.stderr)


if __name__ == '__main__':
    main()
