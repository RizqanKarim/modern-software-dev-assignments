import re
from typing import Dict, List, Optional


def extract_action_items(text: str) -> Dict[str, List[str]]:
    """
    Extract action items from text with enhanced pattern recognition.

    Supports:
    - Plain text patterns (TODO:, ACTION:, !)
    - Markdown checkboxes (- [ ] and - [x])
    - Markdown lists with action keywords
    - Tags extraction (#tag)

    Returns:
        Dict with 'action_items' and 'tags' keys
    """
    try:
        if not isinstance(text, str):
            raise ValueError("Input must be a string")

        action_items: List[str] = []
        tags: List[str] = []

        # Extract tags first
        tag_pattern = r'#(\w+)'
        tags = re.findall(tag_pattern, text)

        # Split into lines and process each line
        lines = text.splitlines()

        for line in lines:
            line = line.strip()
            if not line:
                continue

            normalized = line.lower()

            # Remove Markdown formatting for cleaner extraction
            clean_line = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)  # Bold
            clean_line = re.sub(r'\*([^*]+)\*', r'\1', clean_line)  # Italic
            clean_line = re.sub(r'`([^`]+)`', r'\1', clean_line)  # Code

            # Check for various action item patterns
            is_action_item = False

            # 1. Markdown checkboxes (unchecked)
            if re.match(r'^\s*-\s*\[\s*\]\s+', line):
                # Extract text after checkbox
                checkbox_match = re.match(r'^\s*-\s*\[\s*\]\s+(.+)', line)
                if checkbox_match:
                    action_items.append(checkbox_match.group(1).strip())
                    is_action_item = True

            # 2. Markdown checkboxes (checked) - still extract as they might be relevant
            elif re.match(r'^\s*-\s*\[x\]\s+', line):
                checkbox_match = re.match(r'^\s*-\s*\[x\]\s+(.+)', line)
                if checkbox_match:
                    action_items.append(f"[DONE] {checkbox_match.group(1).strip()}")
                    is_action_item = True

            # 3. Traditional TODO/ACTION prefixes (with or without dash)
            elif normalized.startswith("todo:") or normalized.startswith("action:") or \
                 normalized.startswith("- todo:") or normalized.startswith("- action:"):
                # Clean up the line by removing leading dash if present
                clean_item = re.sub(r'^\s*-\s*', '', line)
                action_items.append(clean_item.strip())
                is_action_item = True

            # 4. Lines ending with exclamation (urgent items) - handle bullet points
            elif line.endswith("!") or (line.strip().startswith("- ") and line.strip("- ").endswith("!")):
                # Clean up bullet point prefix if present
                clean_item = re.sub(r'^\s*-\s*', '', line)
                action_items.append(clean_item.strip())
                is_action_item = True

            # 5. Lines with action verbs at the beginning (but not in headers)
            elif re.match(r'^\s*(buy|call|email|send|write|review|check|fix|update|create|implement|test)', normalized) and \
                 not re.match(r'^\s*#', line) and \
                 not any(word in normalized for word in ['completed', 'done', 'finished', 'cancelled']):
                action_items.append(line)
                is_action_item = True

            # 6. Markdown headers with action keywords (only specific action keywords, not general "task")
            elif re.match(r'^\s*#{1,6}\s+', line) and any(keyword in normalized for keyword in ['todo', 'action', 'next', 'pending', 'upcoming']):
                # Remove header markers for cleaner output
                header_content = re.sub(r'^\s*#{1,6}\s+', '', line)
                action_items.append(f"Header: {header_content}")
                is_action_item = True

            # 7. Numbered lists with action keywords
            elif re.match(r'^\s*\d+\.\s+', line) and any(keyword in normalized for keyword in ['todo', 'action', 'task']):
                action_items.append(line)
                is_action_item = True

            # 8. Action verbs at start of line (but avoid false positives in headers or general text)
            elif re.match(r'^\s*(buy|call|email|send|write|review|check|fix|update|create|implement|test)\s', normalized) and \
                 not re.match(r'^\s*#', line) and \
                 not any(word in normalized for word in ['completed', 'done', 'finished', 'cancelled']):
                action_items.append(line)
                is_action_item = True

        # Remove duplicates while preserving order
        seen = set()
        unique_action_items = []
        for item in action_items:
            if item not in seen:
                unique_action_items.append(item)
                seen.add(item)

        return {
            "action_items": unique_action_items,
            "tags": list(set(tags))  # Remove duplicate tags
        }

    except Exception as e:
        # Return error information instead of raising exception
        return {
            "action_items": [],
            "tags": [],
            "error": f"Extraction failed: {str(e)}"
        }


