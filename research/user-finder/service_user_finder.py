#!/usr/bin/env python3
"""
Service/Product User Finder Agent

A specialized agent that searches the web, company sites, news sites, and developer blogs
to find out who is using a particular service or product.
"""

import asyncio
import json
import re
from typing import List, Dict, Any
from dataclasses import dataclass
from urllib.parse import urlparse
import argparse
import aiohttp
import time
from bs4 import BeautifulSoup


@dataclass
class UserFinding:
    """Represents a finding about a service/product user"""
    company_name: str
    source_url: str
    evidence_text: str
    confidence_level: str  # high, medium, low
    finding_type: str  # case_study, press_release, blog_post, documentation, etc.


class ServiceUserFinder:
    """Main agent class for finding service/product users"""
    
    def __init__(self):
        self.search_patterns = {
            'usage_indicators': [
                r'{service}.*(?:customer|client|user)',
                r'(?:using|uses|deployed|implementing|adopted)\s+{service}',
                r'{service}.*(?:case study|success story)',
                r'powered by {service}',
                r'built with {service}',
                r'{service}.*integration',
                r'migrated to {service}',
                r'{service}.*implementation'
            ],
            'company_patterns': [
                r'[A-Z][a-zA-Z\s&]+(?:Inc\.|LLC|Corp\.|Corporation|Ltd\.|Limited)',
                r'[A-Z][a-zA-Z\s&]{2,30}(?:\s+(?:Inc|LLC|Corp|Corporation|Ltd|Limited))?'
            ]
        }
        
        self.target_domains = {
            'news_sites': [
                'techcrunch.com', 'venturebeat.com', 'arstechnica.com', 
                'zdnet.com', 'engadget.com', 'theverge.com'
            ],
            'developer_blogs': [
                'medium.com', 'dev.to', 'hashnode.com', 'hackernoon.com',
                'stackoverflow.blog', 'github.blog'
            ],
            'business_sites': [
                'forbes.com', 'businessinsider.com', 'cnbc.com',
                'bloomberg.com', 'reuters.com'
            ]
        }
    
    async def find_users(self, service_name: str, max_results: int = 50) -> List[UserFinding]:
        """
        Main method to find users of a service/product
        
        Args:
            service_name: Name of the service/product to search for
            max_results: Maximum number of findings to return
            
        Returns:
            List of UserFinding objects
        """
        findings = []
        
        # Generate search queries
        queries = self._generate_search_queries(service_name)
        
        print(f"🔍 Searching for users of '{service_name}'...")
        print(f"Generated {len(queries)} search queries")
        
        # Use DuckDuckGo instant answer API and web scraping
        async with aiohttp.ClientSession() as session:
            for i, query in enumerate(queries[:10], 1):  # Limit to 10 queries
                print(f"Query {i}: {query}")
                try:
                    # Perform actual web search
                    search_findings = await self._search_web(session, query, service_name)
                    findings.extend(search_findings)
                    
                    # Rate limiting
                    await asyncio.sleep(1)
                    
                    if len(findings) >= max_results:
                        break
                        
                except Exception as e:
                    print(f"Error searching for '{query}': {e}")
                    continue
        
        return findings[:max_results]
    
    def _generate_search_queries(self, service_name: str) -> List[str]:
        """Generate targeted search queries for finding service users"""
        base_queries = [
            f'"{service_name}" case study',
            f'"{service_name}" customer success',
            f'"{service_name}" implementation',
            f'companies using "{service_name}"',
            f'"{service_name}" adoption',
            f'powered by "{service_name}"',
            f'built with "{service_name}"',
            f'"{service_name}" integration',
            f'migrated to "{service_name}"',
            f'deployed "{service_name}"'
        ]
        
        # Add domain-specific queries
        domain_queries = []
        for domains in self.target_domains.values():
            for domain in domains[:3]:  # Limit domains per category
                domain_queries.extend([
                    f'site:{domain} "{service_name}" customer',
                    f'site:{domain} "{service_name}" case study',
                    f'site:{domain} using "{service_name}"'
                ])
        
        return base_queries + domain_queries
    
    async def _search_web(self, session: aiohttp.ClientSession, query: str, service_name: str) -> List[UserFinding]:
        """Perform web search using DuckDuckGo and extract findings"""
        findings = []
        
        try:
            # Use DuckDuckGo instant answer API
            search_url = "https://api.duckduckgo.com/"
            params = {
                'q': query,
                'format': 'json',
                'no_html': '1',
                'skip_disambig': '1'
            }
            
            async with session.get(search_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Process instant answer results
                    if data.get('Answer'):
                        findings.extend(self._extract_findings_from_text(
                            data['Answer'], 
                            data.get('AbstractURL', ''), 
                            service_name
                        ))
                    
                    # Process related topics
                    for topic in data.get('RelatedTopics', []):
                        if isinstance(topic, dict) and 'Text' in topic:
                            findings.extend(self._extract_findings_from_text(
                                topic['Text'],
                                topic.get('FirstURL', ''),
                                service_name
                            ))
            
            # Also try HTML search for more results
            await self._search_html(session, query, service_name, findings)
            
        except Exception as e:
            print(f"Search error for '{query}': {e}")
        
        return findings
    
    async def _search_html(self, session: aiohttp.ClientSession, query: str, service_name: str, findings: List[UserFinding]):
        """Search HTML results using DuckDuckGo HTML interface"""
        try:
            search_url = "https://html.duckduckgo.com/html/"
            params = {'q': query}
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; ServiceUserFinder/1.0)'
            }
            
            async with session.get(search_url, params=params, headers=headers) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Extract search results
                    results = soup.find_all('div', class_='result')
                    for result in results[:5]:  # Limit to top 5 results
                        title_elem = result.find('a', class_='result__a')
                        snippet_elem = result.find('a', class_='result__snippet')
                        
                        if title_elem and snippet_elem:
                            url = title_elem.get('href', '')
                            title = title_elem.get_text(strip=True)
                            snippet = snippet_elem.get_text(strip=True)
                            
                            # Extract findings from title and snippet
                            text = f"{title} {snippet}"
                            findings.extend(self._extract_findings_from_text(text, url, service_name))
                            
        except Exception as e:
            print(f"HTML search error: {e}")
    
    def _extract_findings_from_text(self, text: str, url: str, service_name: str) -> List[UserFinding]:
        """Extract company findings from text using pattern matching"""
        findings = []
        
        if not text or not url:
            return findings
        
        # Look for usage indicators
        service_mentioned = False
        for pattern_template in self.search_patterns['usage_indicators']:
            pattern = pattern_template.format(service=re.escape(service_name))
            if re.search(pattern, text, re.IGNORECASE):
                service_mentioned = True
                break
        
        if not service_mentioned:
            return findings
        
        # Extract company names
        companies = set()
        for pattern in self.search_patterns['company_patterns']:
            matches = re.findall(pattern, text)
            companies.update(matches)
        
        # Create findings for each company
        for company in companies:
            if len(company.strip()) > 2:  # Filter out very short matches
                confidence = self._assess_confidence(text)
                finding_type = self._determine_finding_type(text, url)
                
                findings.append(UserFinding(
                    company_name=company.strip(),
                    source_url=url,
                    evidence_text=text[:200] + "..." if len(text) > 200 else text,
                    confidence_level=confidence,
                    finding_type=finding_type
                ))
        
        return findings
    
    def _assess_confidence(self, text: str) -> str:
        """Assess confidence level of a finding"""
        text_lower = text.lower()
        
        high_confidence_indicators = [
            'case study', 'customer', 'implementation', 'deployed', 'using',
            'migrated to', 'success story', 'powered by'
        ]
        
        medium_confidence_indicators = [
            'integration', 'adopted', 'built with', 'uses'
        ]
        
        # Check for high confidence indicators
        for indicator in high_confidence_indicators:
            if indicator in text_lower:
                return "high"
        
        # Check for medium confidence indicators
        for indicator in medium_confidence_indicators:
            if indicator in text_lower:
                return "medium"
        
        return "low"
    
    def _determine_finding_type(self, text: str, url: str) -> str:
        """Determine the type of finding based on content and URL"""
        text_lower = text.lower()
        url_lower = url.lower()
        
        if 'case study' in text_lower:
            return "case_study"
        elif 'press release' in text_lower or 'announces' in text_lower:
            return "press_release"
        elif any(domain in url_lower for domain in ['blog', 'medium.com', 'dev.to']):
            return "blog_post"
        elif 'documentation' in text_lower or 'docs' in url_lower:
            return "documentation"
        elif any(domain in url_lower for domain in ['news', 'techcrunch', 'venturebeat']):
            return "news_article"
        else:
            return "web_mention"
    
    def export_findings(self, findings: List[UserFinding], format: str = 'json') -> str:
        """Export findings in various formats"""
        if format == 'json':
            return json.dumps([
                {
                    'company': f.company_name,
                    'source': f.source_url,
                    'evidence': f.evidence_text,
                    'confidence': f.confidence_level,
                    'type': f.finding_type
                }
                for f in findings
            ], indent=2)
        
        elif format == 'csv':
            lines = ['Company,Source,Evidence,Confidence,Type']
            for f in findings:
                lines.append(f'"{f.company_name}","{f.source_url}","{f.evidence_text}","{f.confidence_level}","{f.finding_type}"')
            return '\n'.join(lines)
        
        elif format == 'markdown':
            lines = ['# Service User Findings\n']
            for f in findings:
                lines.extend([
                    f'## {f.company_name}',
                    f'**Confidence:** {f.confidence_level}',
                    f'**Type:** {f.finding_type}',
                    f'**Source:** [{f.source_url}]({f.source_url})',
                    f'**Evidence:** {f.evidence_text}',
                    ''
                ])
            return '\n'.join(lines)
        
        return str(findings)
    
    def analyze_findings(self, findings: List[UserFinding]) -> Dict[str, Any]:
        """Analyze findings to provide insights"""
        if not findings:
            return {"error": "No findings to analyze"}
        
        analysis = {
            'total_findings': len(findings),
            'confidence_breakdown': {},
            'finding_types': {},
            'top_sources': {},
            'company_count': len(set(f.company_name for f in findings))
        }
        
        # Confidence level breakdown
        for finding in findings:
            conf = finding.confidence_level
            analysis['confidence_breakdown'][conf] = analysis['confidence_breakdown'].get(conf, 0) + 1
        
        # Finding type breakdown
        for finding in findings:
            ftype = finding.finding_type
            analysis['finding_types'][ftype] = analysis['finding_types'].get(ftype, 0) + 1
        
        # Top source domains
        for finding in findings:
            domain = urlparse(finding.source_url).netloc
            analysis['top_sources'][domain] = analysis['top_sources'].get(domain, 0) + 1
        
        return analysis


async def main():
    """Command line interface for the Service User Finder"""
    parser = argparse.ArgumentParser(description='Find users of a service or product')
    parser.add_argument('service', help='Name of the service/product to search for')
    parser.add_argument('--max-results', type=int, default=50, help='Maximum number of results')
    parser.add_argument('--format', choices=['json', 'csv', 'markdown'], default='json', help='Output format')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--analyze', action='store_true', help='Include analysis of findings')
    
    args = parser.parse_args()
    
    # Create and run the finder
    finder = ServiceUserFinder()
    findings = await finder.find_users(args.service, args.max_results)
    
    # Export results
    output = finder.export_findings(findings, args.format)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Results saved to {args.output}")
    else:
        print(output)
    
    # Show analysis if requested
    if args.analyze:
        analysis = finder.analyze_findings(findings)
        print("\n" + "="*50)
        print("ANALYSIS")
        print("="*50)
        print(json.dumps(analysis, indent=2))


if __name__ == '__main__':
    asyncio.run(main())