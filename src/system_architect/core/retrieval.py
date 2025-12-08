from typing import List, Dict, Any, Optional
from datetime import datetime
import re


class ConversationMemory:
    """
    Smart conversation memory without embeddings.
    Uses structured storage, keyword matching, and recency for context retrieval.
    """
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.entries: List[Dict[str, Any]] = []
        self.max_entries = 100  # Keep last 100 entries
        
    def add(self, text: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Add text to conversation memory with metadata.
        
        Args:
            text: The content to store
            metadata: Optional metadata (id, type, keywords, etc.)
        """
        metadata = metadata or {}
        
        # Extract keywords from text
        keywords = self._extract_keywords(text)
        
        entry = {
            "id": metadata.get("id", f"entry_{len(self.entries)}"),
            "text": text,
            "type": metadata.get("type", "general"),
            "keywords": keywords,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata
        }
        
        self.entries.append(entry)
        
        # Keep only recent entries to avoid memory bloat
        if len(self.entries) > self.max_entries:
            self.entries = self.entries[-self.max_entries:]
    
    def query(self, prompt: str, n: int = 5) -> List[str]:
        """
        Retrieve relevant context using keyword matching and recency.
        
        Args:
            prompt: User query
            n: Number of results to return
            
        Returns:
            List of relevant text entries
        """
        if not self.entries:
            return []
        
        # Extract keywords from query
        query_keywords = self._extract_keywords(prompt)
        
        # Score each entry
        scored_entries = []
        for entry in self.entries:
            score = self._calculate_relevance_score(
                entry,
                query_keywords,
                prompt.lower()
            )
            scored_entries.append((score, entry))
        
        # Sort by score (descending) and get top n
        scored_entries.sort(key=lambda x: x[0], reverse=True)
        top_entries = scored_entries[:n]
        
        # Return text from top entries
        return [entry["text"] for score, entry in top_entries if score > 0]
    
    def get_by_type(self, entry_type: str) -> List[str]:
        """Get all entries of a specific type."""
        return [
            entry["text"]
            for entry in self.entries
            if entry["type"] == entry_type
        ]
    
    def get_recent(self, n: int = 5) -> List[str]:
        """Get the n most recent entries."""
        recent = self.entries[-n:] if len(self.entries) >= n else self.entries
        return [entry["text"] for entry in reversed(recent)]
    
    def clear(self):
        """Clear all memory entries."""
        self.entries = []
    
    def _extract_keywords(self, text: str) -> set:
        """
        Extract meaningful keywords from text.
        Simple approach: lowercase words, filter common words.
        """
        # Common stop words to ignore
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this',
            'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
        
        # Extract words (alphanumeric sequences)
        words = re.findall(r'\b[a-z0-9]+\b', text.lower())
        
        # Filter stop words and short words
        keywords = {
            word for word in words
            if word not in stop_words and len(word) > 2
        }
        
        return keywords
    
    def _calculate_relevance_score(
        self,
        entry: Dict[str, Any],
        query_keywords: set,
        query_text: str
    ) -> float:
        """
        Calculate relevance score for an entry.
        
        Scoring factors:
        1. Keyword overlap (most important)
        2. Type priority (requirements, architecture > general)
        3. Recency (newer entries get slight boost)
        4. Exact phrase matching
        """
        score = 0.0
        
        # 1. Keyword overlap (0-10 points)
        entry_keywords = entry["keywords"]
        if query_keywords and entry_keywords:
            overlap = len(query_keywords & entry_keywords)
            keyword_score = min(overlap * 2, 10)  # Cap at 10
            score += keyword_score
        
        # 2. Type priority (0-5 points)
        type_priority = {
            "requirements": 5,
            "architecture": 5,
            "explanation": 4,
            "recommendations": 3,
            "qa": 2,
            "general": 1
        }
        score += type_priority.get(entry["type"], 1)
        
        # 3. Recency bonus (0-2 points)
        # More recent entries get a small boost
        entry_index = self.entries.index(entry)
        recency_score = (entry_index / len(self.entries)) * 2
        score += recency_score
        
        # 4. Exact phrase matching (bonus 5 points)
        entry_text_lower = entry["text"].lower()
        # Check for significant phrases (3+ words)
        query_phrases = re.findall(r'\b\w+\s+\w+\s+\w+\b', query_text)
        for phrase in query_phrases:
            if phrase in entry_text_lower:
                score += 5
                break
        
        return score


# Alias for backward compatibility
class Retrieval(ConversationMemory):
    """Alias for ConversationMemory to maintain backward compatibility."""
    pass
