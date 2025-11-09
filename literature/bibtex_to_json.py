#!/usr/bin/env python3
"""
Convert BibTeX references to JSON format for easier parsing and analysis.

This script reads references.bib and outputs a structured JSON file
with all citation information, suitable for citation network analysis
and programmatic reference management.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode


def parse_author_names(author_str: str) -> List[Dict[str, str]]:
    """
    Parse author string into structured format.
    
    Args:
        author_str: BibTeX author string (e.g., "Last1, First1 and Last2, First2")
        
    Returns:
        List of author dictionaries with 'family' and 'given' names
    """
    authors = []
    
    # Split by 'and'
    author_parts = author_str.split(' and ')
    
    for author in author_parts:
        author = author.strip()
        
        # Handle "Last, First" format
        if ',' in author:
            parts = author.split(',', 1)
            family = parts[0].strip()
            given = parts[1].strip() if len(parts) > 1 else ""
        # Handle "First Last" format
        else:
            parts = author.split()
            family = parts[-1] if parts else ""
            given = ' '.join(parts[:-1]) if len(parts) > 1 else ""
        
        authors.append({
            'family': family,
            'given': given,
            'literal': author
        })
    
    return authors


def extract_doi(entry: Dict) -> Optional[str]:
    """Extract DOI from entry, handling various formats."""
    doi = entry.get('doi', '')
    
    # Remove URL prefix if present
    doi = re.sub(r'^https?://doi.org/', '', doi)
    doi = re.sub(r'^https?://dx\.doi\.org/', '', doi)
    
    return doi if doi else None


def convert_bibtex_to_json(
    bibtex_file: Path,
    output_file: Path,
    pretty_print: bool = True
) -> Dict:
    """
    Convert BibTeX file to JSON format.
    
    Args:
        bibtex_file: Path to input .bib file
        output_file: Path to output .json file
        pretty_print: If True, format JSON with indentation
        
    Returns:
        Dictionary with all references
    """
    # Read BibTeX file
    with open(bibtex_file, 'r', encoding='utf-8') as f:
        bibtex_str = f.read()
    
    # Parse BibTeX
    parser = BibTexParser(common_strings=True)
    parser.customization = convert_to_unicode
    bib_database = bibtexparser.loads(bibtex_str, parser=parser)
    
    # Convert to JSON structure
    references = []
    
    for entry in bib_database.entries:
        ref = {
            'id': entry.get('ID', ''),
            'type': entry.get('ENTRYTYPE', ''),
            'title': entry.get('title', ''),
            'author': parse_author_names(entry.get('author', '')),
            'year': entry.get('year', ''),
            'doi': extract_doi(entry),
            'url': entry.get('url', ''),
            'journal': entry.get('journal', ''),
            'booktitle': entry.get('booktitle', ''),
            'volume': entry.get('volume', ''),
            'number': entry.get('number', ''),
            'pages': entry.get('pages', ''),
            'publisher': entry.get('publisher', ''),
            'abstract': entry.get('abstract', ''),
            'keywords': entry.get('keywords', '').split(',') if entry.get('keywords') else [],
        }
        
        # Add any additional fields
        for key, value in entry.items():
            if key not in ['ID', 'ENTRYTYPE', 'title', 'author', 'year', 'doi',
                          'url', 'journal', 'booktitle', 'volume', 'number',
                          'pages', 'publisher', 'abstract', 'keywords']:
                ref[key.lower()] = value
        
        references.append(ref)
    
    # Create output structure
    output = {
        'metadata': {
            'total_references': len(references),
            'source_file': str(bibtex_file),
            'generated_by': 'bibtex_to_json.py',
        },
        'references': references
    }
    
    # Write JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        if pretty_print:
            json.dump(output, f, indent=2, ensure_ascii=False)
        else:
            json.dump(output, f, ensure_ascii=False)
    
    return output


def filter_by_keywords(
    references: List[Dict],
    keywords: List[str],
    case_sensitive: bool = False
) -> List[Dict]:
    """
    Filter references by keywords.
    
    Args:
        references: List of reference dictionaries
        keywords: Keywords to search for (searches in title, abstract, keywords)
        case_sensitive: If True, perform case-sensitive matching
        
    Returns:
        Filtered list of references
    """
    filtered = []
    
    for ref in references:
        # Combine searchable fields
        searchable = ' '.join([
            ref.get('title', ''),
            ref.get('abstract', ''),
            ' '.join(ref.get('keywords', []))
        ])
        
        if not case_sensitive:
            searchable = searchable.lower()
            keywords = [k.lower() for k in keywords]
        
        # Check if any keyword matches
        if any(kw in searchable for kw in keywords):
            filtered.append(ref)
    
    return filtered


def generate_citation_stats(references: List[Dict]) -> Dict:
    """Generate statistics about the reference collection."""
    stats = {
        'total_references': len(references),
        'by_type': {},
        'by_year': {},
        'journals': {},
        'total_authors': 0,
    }
    
    all_authors = set()
    
    for ref in references:
        # Count by type
        ref_type = ref.get('type', 'unknown')
        stats['by_type'][ref_type] = stats['by_type'].get(ref_type, 0) + 1
        
        # Count by year
        year = ref.get('year', 'unknown')
        stats['by_year'][year] = stats['by_year'].get(year, 0) + 1
        
        # Count journals
        journal = ref.get('journal', '')
        if journal:
            stats['journals'][journal] = stats['journals'].get(journal, 0) + 1
        
        # Count unique authors
        for author in ref.get('author', []):
            all_authors.add(author.get('literal', ''))
    
    stats['total_authors'] = len(all_authors)
    
    return stats


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Convert BibTeX references to JSON format'
    )
    parser.add_argument(
        '--input', '-i',
        type=Path,
        default='references.bib',
        help='Input BibTeX file (default: references.bib)'
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        default='references.json',
        help='Output JSON file (default: references.json)'
    )
    parser.add_argument(
        '--compact',
        action='store_true',
        help='Output compact JSON (no indentation)'
    )
    parser.add_argument(
        '--filter-keywords',
        nargs='+',
        help='Filter references by keywords'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Print statistics about references'
    )
    
    args = parser.parse_args()
    
    # Convert BibTeX to JSON
    print(f"Reading {args.input}...")
    output = convert_bibtex_to_json(
        args.input,
        args.output,
        pretty_print=not args.compact
    )
    
    references = output['references']
    
    # Apply filters if requested
    if args.filter_keywords:
        print(f"\nFiltering by keywords: {args.filter_keywords}")
        references = filter_by_keywords(references, args.filter_keywords)
        print(f"Found {len(references)} matching references")
    
    # Print stats if requested
    if args.stats:
        stats = generate_citation_stats(references)
        print("\n=== Citation Statistics ===")
        print(f"Total references: {stats['total_references']}")
        print(f"Total unique authors: {stats['total_authors']}")
        print(f"\nBy type:")
        for ref_type, count in sorted(stats['by_type'].items()):
            print(f"  {ref_type}: {count}")
        print(f"\nTop 5 years:")
        for year, count in sorted(stats['by_year'].items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {year}: {count}")
        print(f"\nTop 5 journals:")
        for journal, count in sorted(stats['journals'].items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {journal}: {count}")
    
    print(f"\nOutput written to {args.output}")
    print(f"Total references: {len(output['references'])}")
