import re
import comfy
from typing import Any, Tuple, Dict

class TextProcessorNode:
    """
    Text Processing Node mit folgenden Funktionen:
    - Entfernt leere Zeilen
    - Regex-Suchen/Ersetzen
    - Zeilenzugriff per Index
    """
    
    CATEGORY = "Custom Nodes/Text Processing"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("FULL_TEXT", "LINE_BY_INDEX")
    
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "dynamicPrompts": False
                }),
                "remove_empty_lines": ("BOOLEAN", {
                    "default": True
                }),
                "search_pattern": ("STRING", {
                    "default": "",
                    "placeholder": "Regex pattern"
                }),
                "replace_with": ("STRING", {
                    "default": "",
                    "placeholder": "Replacement"
                }),
                "line_index": ("INT", {
                    "default": 0,
                    "min": 0,
                    "step": 1
                })
            }
        }

    def process(self, text: str, remove_empty_lines: bool, 
                search_pattern: str, replace_with: str, 
                line_index: int) -> Tuple[str, str]:
        """
        Hauptverarbeitungsfunktion mit Fehlerbehandlung
        """
        processed = text
        
        # Leerzeilen entfernen
        if remove_empty_lines:
            processed = self._remove_empty_lines(processed)
        
        # Regex-Ersetzung
        if search_pattern and replace_with:
            processed = self._regex_replace(
                processed, 
                search_pattern, 
                replace_with
            )
        
        # Zeilenzugriff
        full_text, selected_line = self._get_line_by_index(
            processed, 
            line_index
        )
        
        return (full_text, selected_line)

    def _remove_empty_lines(self, text: str) -> str:
        """Hilfsfunktion zum Entfernen leerer Zeilen"""
        return "\n".join(
            [line for line in text.splitlines() if line.strip()]
        )

    def _regex_replace(self, text: str, pattern: str, replacement: str) -> str:
        """Sicherer Regex-Ersatz mit Fehlerbehandlung"""
        try:
            return re.sub(pattern, replacement, text)
        except re.error as e:
            return f"Regex Error: {str(e)}"

    def _get_line_by_index(self, text: str, index: int) -> Tuple[str, str]:
        """Zeilenindex-Validierung"""
        lines = text.splitlines()
        try:
            return (text, lines[index])
        except IndexError:
            return (text, f"Error: Line {index} not found")


