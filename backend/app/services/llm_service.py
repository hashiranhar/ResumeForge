from huggingface_hub import InferenceClient
from typing import Dict, Any, Optional
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class LLMService:
    
    def __init__(self):
        """Initialize LLM service with Hugging Face client"""
        try:
            self.client = InferenceClient(
                provider="novita",
                api_key=settings.huggingface_api_key,
            )
            self.model = "deepseek-ai/DeepSeek-V3-0324"
            logger.info("LLM service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize LLM service: {e}")
            self.client = None
    
    def edit_cv_content(self, current_content: str, user_instruction: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Edit CV content based on user instructions.
        
        Args:
            current_content: The current markdown content of the CV
            user_instruction: What the user wants to change/improve
            context: Additional context (CV name, user preferences, etc.)
            
        Returns:
            Dict with success status, edited content, and explanation
        """
        if not self.client:
            return {
                "success": False,
                "error": "LLM service not available",
                "edited_content": current_content,
                "explanation": "AI editing is currently unavailable"
            }
        
        try:
            # Create the system prompt for CV editing
            system_prompt = self._create_system_prompt()
            
            # Create the user prompt with context
            user_prompt = self._create_user_prompt(current_content, user_instruction, context)
            
            # Call the LLM
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            # Parse the response
            response_content = completion.choices[0].message.content
            parsed_response = self._parse_llm_response(response_content)
            
            return {
                "success": True,
                "edited_content": parsed_response["content"],
                "explanation": parsed_response["explanation"],
                "suggestions": parsed_response.get("suggestions", [])
            }
            
        except Exception as e:
            logger.error(f"LLM editing failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "edited_content": current_content,
                "explanation": "Failed to process your request. Please try again."
            }
    
    def suggest_improvements(self, cv_content: str) -> Dict[str, Any]:
        """
        Suggest general improvements for a CV.
        
        Args:
            cv_content: The current markdown content of the CV
            
        Returns:
            Dict with suggestions and analysis
        """
        if not self.client:
            return {
                "success": False,
                "error": "LLM service not available",
                "suggestions": []
            }
        
        try:
            system_prompt = """You are a professional CV advisor. Analyze the given CV and provide specific, actionable suggestions for improvement. Focus on:
            1. Content quality and relevance
            2. Professional presentation
            3. Missing sections or information
            4. Better phrasing or terminology
            5. Structure and organization
            
            Provide your response as a JSON object with:
            - "overall_score": number 1-10
            - "strengths": list of positive aspects
            - "improvements": list of specific suggestions
            - "missing_sections": list of sections that could be added
            """
            
            user_prompt = f"Please analyze this CV and provide improvement suggestions:\n\n{cv_content}"
            
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            response_content = completion.choices[0].message.content
            
            # Try to parse as JSON, fallback to text if needed
            try:
                import json
                suggestions = json.loads(response_content)
            except:
                suggestions = {
                    "overall_score": 7,
                    "analysis": response_content,
                    "improvements": ["See analysis for detailed suggestions"]
                }
            
            return {
                "success": True,
                "suggestions": suggestions
            }
            
        except Exception as e:
            logger.error(f"CV analysis failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "suggestions": []
            }
    
    def _create_system_prompt(self) -> str:
        """Create the system prompt for CV editing"""
        return """You are an expert CV editor and career advisor. Your job is to help users improve their CV content while maintaining their voice and keeping the information accurate.

IMPORTANT GUIDELINES:
1. Always preserve the original markdown formatting and structure
2. Keep the ResumeForge formatting markers: [CENTER] and [DATE: content]
3. Only edit the content that the user specifically asks about
4. Make improvements sound natural and professional
5. Don't add false information - only enhance what's already there
6. Maintain the same sections and overall structure unless asked to change it

Response format:
EDITED_CONTENT:
[The improved CV content in markdown format]

EXPLANATION:
[Brief explanation of what you changed and why]"""
    
    def _create_user_prompt(self, current_content: str, instruction: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Create the user prompt with CV content and instruction"""
        context_info = ""
        if context:
            if context.get("cv_name"):
                context_info += f"CV Name: {context['cv_name']}\n"
            if context.get("target_role"):
                context_info += f"Target Role: {context['target_role']}\n"
        
        prompt = f"""Please help me improve my CV based on this instruction: "{instruction}"

{context_info}
Current CV Content:
{current_content}

Please edit the content according to my instruction while following your guidelines."""
        
        return prompt
    
    def _parse_llm_response(self, response: str) -> Dict[str, str]:
        """Parse the LLM response to extract content and explanation"""
        try:
            # Look for the structured response format
            if "EDITED_CONTENT:" in response and "EXPLANATION:" in response:
                parts = response.split("EXPLANATION:")
                content_part = parts[0].replace("EDITED_CONTENT:", "").strip()
                explanation_part = parts[1].strip()
                
                return {
                    "content": content_part,
                    "explanation": explanation_part
                }
            else:
                # Fallback: treat entire response as content
                return {
                    "content": response.strip(),
                    "explanation": "Content has been improved based on your request."
                }
        except Exception as e:
            logger.error(f"Failed to parse LLM response: {e}")
            return {
                "content": response.strip(),
                "explanation": "Content has been processed."
            }

# Create a singleton instance
llm_service = LLMService()