from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict

@dataclass
class ParsedStory:
    title: str
    business_context: str
    acceptance_criteria: List[str]
    technical_context: str
    primary_modules: List[str]
    keywords: List[str]
    implementation_notes: str
    done_when: List[str]
    raw_text: str

SECTION_PATTERNS = {
    "title": r"^#\s*(.+)$",
    "business": r"##\s*Business Context\s*(.+?)(?=\n##|\Z)",
    "acceptance": r"##\s*Acceptance Criteria\s*(.+?)(?=\n##|\Z)",
    "tech": r"##\s*Technical Context\s*(.+?)(?=\n##|\Z)",
    "primary": r"##\s*Primary Modules\s*(.+?)(?=\n##|\Z)",
    "keywords": r"##\s*File Search Keywords\s*(.+?)(?=\n##|\Z)",
    "impl": r"##\s*Implementation Notes\s*(.+?)(?=\n##|\Z)",
    "done": r"##\s*Done When\s*(.+?)(?=\n##|\Z)",
}

def _listify(block: str) -> List[str]:
    if not block:
        return []
    items = []
    for line in block.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        line = re.sub(r"^[-*]\s*", "", line)
        items.append(line)
    return items

def parse_story(md_text: str) -> ParsedStory:
    title = re.search(SECTION_PATTERNS["title"], md_text, re.M)
    business = re.search(SECTION_PATTERNS["business"], md_text, re.S)
    acceptance = re.search(SECTION_PATTERNS["acceptance"], md_text, re.S)
    tech = re.search(SECTION_PATTERNS["tech"], md_text, re.S)
    primary = re.search(SECTION_PATTERNS["primary"], md_text, re.S)
    keywords = re.search(SECTION_PATTERNS["keywords"], md_text, re.S)
    impl = re.search(SECTION_PATTERNS["impl"], md_text, re.S)
    done = re.search(SECTION_PATTERNS["done"], md_text, re.S)

    title_text = title.group(1).strip() if title else "Untitled Story"
    business_text = (business.group(1).strip() if business else "")
    acceptance_items = _listify(acceptance.group(1) if acceptance else "")
    tech_text = (tech.group(1).strip() if tech else "")
    primary_items = _listify(primary.group(1) if primary else "")
    keyword_items = _listify(keywords.group(1) if keywords else "")
    impl_text = (impl.group(1).strip() if impl else "")
    done_items = _listify(done.group(1) if done else "")

    # Expand backticked inline tokens inside keywords list
    expanded = []
    for k in keyword_items:
        expanded.extend(re.findall(r"`([^`]+)`", k) or [k])
    keyword_items = [k.strip() for k in expanded if k.strip()]

    return ParsedStory(
        title=title_text,
        business_context=business_text,
        acceptance_criteria=acceptance_items,
        technical_context=tech_text,
        primary_modules=primary_items,
        keywords=keyword_items,
        implementation_notes=impl_text,
        done_when=done_items,
        raw_text=md_text,
    )
