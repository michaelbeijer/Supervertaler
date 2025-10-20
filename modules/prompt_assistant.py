"""
AI Prompt Assistant Module

Provides AI-powered prompt modification through natural language conversation.
Part of Phase 1 implementation for v4.0.0-beta.

Features:
- Conversational prompt modification
- Visual diff generation
- Prompt versioning
- Chat history tracking
"""

import difflib
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class PromptAssistant:
    """AI-powered prompt modification and learning system"""
    
    def __init__(self, llm_client=None):
        """
        Initialize the Prompt Assistant.
        
        Args:
            llm_client: LLM client instance (OpenAI, Anthropic, or Google)
        """
        self.llm = llm_client
        self.chat_history = []
        self.modification_history = []  # Track all prompt versions
        
        # System prompt for the AI prompt engineer
        self.system_prompt = """You are an expert prompt engineer specialising in translation and localisation prompts.

Your role is to help users refine and optimise their translation prompts based on their specific needs.

When a user requests a modification to a prompt:
1. Analyze the current prompt structure and content
2. Understand the user's specific request
3. Make targeted, meaningful changes that improve the prompt
4. Explain your modifications clearly
5. Preserve the overall structure unless changes are needed

Guidelines:
- Be specific and precise in your modifications
- Maintain professional translation terminology
- Consider linguistic and cultural aspects
- Keep prompts concise but comprehensive
- Use clear, actionable language

Always respond with:
1. An explanation of what you're changing and why
2. The complete modified prompt text
3. Key improvements made

Format your response as JSON:
{
    "explanation": "Brief explanation of changes",
    "modified_prompt": "Complete new prompt text",
    "changes_summary": ["Change 1", "Change 2", ...]
}"""
    
    def set_llm_client(self, llm_client):
        """Set or update the LLM client"""
        self.llm = llm_client
    
    def suggest_modification(self, prompt_name: str, current_prompt: str, user_request: str) -> Dict:
        """
        AI suggests changes to a prompt based on user request.
        
        Args:
            prompt_name: Name of the prompt being modified
            current_prompt: Current content of the prompt
            user_request: User's natural language request for modification
        
        Returns:
            Dictionary containing:
            - explanation: Why the changes were made
            - modified_prompt: New version of the prompt
            - changes_summary: List of key changes
            - diff: Unified diff showing changes
            - success: Boolean indicating if modification succeeded
        """
        if not self.llm:
            return {
                "success": False,
                "error": "No LLM client configured"
            }
        
        try:
            # Build conversation context
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"""Please modify the following translation prompt:

PROMPT NAME: {prompt_name}

CURRENT PROMPT:
{current_prompt}

USER REQUEST: {user_request}

Provide your response in JSON format with explanation, modified_prompt, and changes_summary."""}
            ]
            
            # Get AI response
            response = self.llm.chat(messages)
            
            # Parse JSON response
            try:
                result = json.loads(response)
            except json.JSONDecodeError:
                # Try to extract JSON from markdown code blocks
                if "```json" in response:
                    json_text = response.split("```json")[1].split("```")[0].strip()
                    result = json.loads(json_text)
                elif "```" in response:
                    json_text = response.split("```")[1].split("```")[0].strip()
                    result = json.loads(json_text)
                else:
                    # Fallback: treat entire response as modified prompt
                    result = {
                        "explanation": "Modified based on your request",
                        "modified_prompt": response,
                        "changes_summary": ["Prompt updated"]
                    }
            
            # Generate diff
            diff = self.generate_diff(current_prompt, result["modified_prompt"])
            
            # Record in modification history
            self.modification_history.append({
                "timestamp": datetime.now().isoformat(),
                "prompt_name": prompt_name,
                "original": current_prompt,
                "modified": result["modified_prompt"],
                "request": user_request,
                "explanation": result.get("explanation", "")
            })
            
            # Record in chat history
            self.chat_history.append({
                "role": "user",
                "content": user_request,
                "timestamp": datetime.now().isoformat()
            })
            self.chat_history.append({
                "role": "assistant",
                "content": result.get("explanation", "Prompt modified"),
                "timestamp": datetime.now().isoformat(),
                "has_suggestion": True
            })
            
            return {
                "success": True,
                "explanation": result.get("explanation", ""),
                "modified_prompt": result["modified_prompt"],
                "changes_summary": result.get("changes_summary", []),
                "diff": diff,
                "diff_html": self.generate_diff_html(current_prompt, result["modified_prompt"])
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to generate modification: {str(e)}"
            }
    
    def generate_diff(self, original: str, modified: str) -> str:
        """
        Generate unified diff between two prompts.
        
        Args:
            original: Original prompt text
            modified: Modified prompt text
        
        Returns:
            Unified diff string
        """
        original_lines = original.splitlines(keepends=True)
        modified_lines = modified.splitlines(keepends=True)
        
        diff = difflib.unified_diff(
            original_lines,
            modified_lines,
            fromfile="Original",
            tofile="Modified",
            lineterm=""
        )
        
        return ''.join(diff)
    
    def generate_diff_html(self, original: str, modified: str) -> List[Tuple[str, str]]:
        """
        Generate line-by-line diff suitable for colored display.
        
        Args:
            original: Original prompt text
            modified: Modified prompt text
        
        Returns:
            List of tuples (change_type, line) where change_type is:
            - 'equal': unchanged line
            - 'delete': removed line
            - 'insert': added line
            - 'replace': modified line
        """
        original_lines = original.splitlines()
        modified_lines = modified.splitlines()
        
        diff = []
        matcher = difflib.SequenceMatcher(None, original_lines, modified_lines)
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                for line in original_lines[i1:i2]:
                    diff.append(('equal', line))
            elif tag == 'delete':
                for line in original_lines[i1:i2]:
                    diff.append(('delete', line))
            elif tag == 'insert':
                for line in modified_lines[j1:j2]:
                    diff.append(('insert', line))
            elif tag == 'replace':
                for line in original_lines[i1:i2]:
                    diff.append(('delete', line))
                for line in modified_lines[j1:j2]:
                    diff.append(('insert', line))
        
        return diff
    
    def get_chat_history(self) -> List[Dict]:
        """Get the chat history"""
        return self.chat_history
    
    def clear_chat_history(self):
        """Clear the chat history"""
        self.chat_history = []
    
    def get_modification_history(self) -> List[Dict]:
        """Get the modification history"""
        return self.modification_history
    
    def undo_last_modification(self) -> Optional[Dict]:
        """
        Get the previous version of the prompt for undo functionality.
        
        Returns:
            Dictionary with original prompt info, or None if no history
        """
        if not self.modification_history:
            return None
        
        last_mod = self.modification_history[-1]
        return {
            "prompt_name": last_mod["prompt_name"],
            "original_prompt": last_mod["original"],
            "timestamp": last_mod["timestamp"]
        }
    
    def export_chat_session(self, filepath: str):
        """
        Export chat history and modifications to a file.
        
        Args:
            filepath: Path to save the session data
        """
        session_data = {
            "chat_history": self.chat_history,
            "modification_history": self.modification_history,
            "exported_at": datetime.now().isoformat()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
