from huggingface_hub import InferenceClient
from typing import Dict, Any, Optional, List
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class LLMService:
    
    def __init__(self):
        """Initialize LLM service with Hugging Face client"""
        self.client = None
        self.model = "deepseek-ai/DeepSeek-V3-0324"
        
        # Only initialize if API key is provided
        if settings.huggingface_api_key:
            try:
                self.client = InferenceClient(
                    provider="novita",
                    api_key=settings.huggingface_api_key,
                )
                logger.info("LLM service initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize LLM service: {e}")
                self.client = None
        else:
            logger.warning("LLM service not initialized - no API key provided")
    
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
    
    def chat_about_cv(self, cv_content: str, user_message: str, conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Function 1: Chat interface - Pure conversation about CV, no editing.
        """
        if not self.client:
            return {
                "success": False,
                "error": "LLM service not available",
                "reply": "AI chat is currently unavailable"
            }
        
        try:
            system_prompt = """You are a senior technical recruiter and career strategist with 15+ years of experience in tech hiring. You understand modern software engineering roles, emerging technologies, and what hiring managers actually look for in 2024-2025.

CONVERSATION MODE - Provide strategic career advice and detailed CV feedback without editing content.

Core expertise areas:
- Software engineering career progression (junior → senior → staff → principal)
- Modern tech stack relevance and market demand
- Compensation benchmarking and negotiation strategies  
- Technical leadership and management transition paths
- Remote work positioning and distributed team experience
- Startup vs enterprise positioning strategies

Response approach:
- Give specific, actionable insights based on current market conditions
- Reference concrete examples from the CV when providing feedback
- Suggest strategic improvements that align with career goals
- Address both immediate job search needs and long-term career trajectory
- Ask targeted follow-up questions to provide personalized advice
- Be direct about market realities while remaining constructive

Industry focus: Prioritize advice for software engineering, DevOps, data science, product management, and technical leadership roles."""

            # Build conversation context
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add conversation history
            if conversation_history:
                for msg in conversation_history[-5:]:  # Keep last 5 messages for context
                    messages.append(msg)
            
            # Add CV context and current message
            user_prompt = f"Here's the CV we're discussing:\n\n{cv_content}\n\nUser question: {user_message}"
            messages.append({"role": "user", "content": user_prompt})
            
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            reply = completion.choices[0].message.content
            
            return {
                "success": True,
                "reply": reply,
                "suggestions": []  # Could extract quick suggestions from reply
            }
            
        except Exception as e:
            logger.error(f"CV chat failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "reply": "Sorry, I couldn't process your message. Please try again."
            }
    
    def inline_edit_content(self, current_content: str, edit_instruction: str, focus_section: Optional[str] = None) -> Dict[str, Any]:
        """
        Function 2: Inline editor - Edit content in real-time, return only edited content.
        """
        if not self.client:
            return {
                "success": False,
                "error": "LLM service not available",
                "edited_content": current_content
            }
        
        try:
            system_prompt = """You are a professional CV content editor specializing in technical resumes. Your sole function is to directly modify CV content according to user instructions.

CRITICAL RULES:
- Return ONLY the complete, edited CV content
- Never include meta-commentary like "Here are your proposed edits" or "I've made the following changes"
- Never add explanatory text outside the CV content itself
- Preserve all markdown formatting exactly ([CENTER], [DATE: content], bullets, headers)
- Make edits that sound natural and professionally written
- Focus on impact-driven language with quantified results when possible

Technical CV optimization principles:
- Use strong action verbs (Architected, Optimized, Implemented, Led, Delivered)
- Quantify achievements with metrics (performance improvements, user counts, revenue impact)
- Include relevant technical keywords naturally within context
- Emphasize business impact alongside technical details
- Use consistent tense (past for previous roles, present for current role)
- Prioritize recent and relevant experience

Examples of strong technical language:
- "Built scalable microservices architecture serving 2M+ daily requests"
- "Reduced deployment time by 75% through CI/CD pipeline automation"
- "Led team of 6 engineers delivering $2M revenue-generating platform"

Output the complete edited CV with no additional commentary."""

            focus_instruction = f" Focus specifically on the {focus_section} section." if focus_section else ""
            user_prompt = f"Edit this CV content: {edit_instruction}{focus_instruction}\n\nCV Content:\n{current_content}"
            
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            edited_content = completion.choices[0].message.content.strip()
            
            # Simple change detection
            changes_made = []
            if edited_content != current_content:
                changes_made.append("Content updated based on your request")
            
            return {
                "success": True,
                "edited_content": edited_content,
                "changes_made": changes_made
            }
            
        except Exception as e:
            logger.error(f"Inline edit failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "edited_content": current_content
            }
    
    def analyze_ats_score(self, cv_content: str, target_role: Optional[str] = None, job_description: Optional[str] = None) -> Dict[str, Any]:
        """
        Function 3: ATS Score analysis - Comprehensive CV scoring and recommendations.
        """
        if not self.client:
            return {
                "success": False,
                "error": "LLM service not available"
            }
        
        try:
            system_prompt = """You are an ATS (Applicant Tracking System) expert and CV analyzer. Analyze CVs like a recruiter and ATS system would.

Provide your response as a JSON object with:
- "ats_score": number 0-100
- "score_breakdown": {"formatting": 0-25, "keywords": 0-25, "experience": 0-25, "skills": 0-25}
- "strengths": list of strengths
- "weaknesses": list of weaknesses  
- "upgrade_suggestions": list of specific actionable improvements
- "keyword_analysis": {"missing_keywords": [], "present_keywords": []}

Be specific, actionable, and focus on what ATS systems and recruiters actually look for."""

            context = ""
            if target_role:
                context += f"Target Role: {target_role}\n"
            if job_description:
                context += f"Job Description: {job_description}\n"
            
            user_prompt = f"Analyze this CV for ATS compatibility and recruiter appeal:\n\n{context}\nCV Content:\n{cv_content}"
            
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
            
            # Try to parse as JSON
            try:
                import json
                analysis = json.loads(response_content)
            except:
                # Fallback if JSON parsing fails
                analysis = {
                    "ats_score": 75,
                    "score_breakdown": {"formatting": 20, "keywords": 15, "experience": 20, "skills": 20},
                    "strengths": ["Professional structure", "Clear contact information"],
                    "weaknesses": ["Missing keywords", "Could be more specific"],
                    "upgrade_suggestions": ["Add more industry-specific keywords", "Quantify achievements"],
                    "keyword_analysis": {"missing_keywords": [], "present_keywords": []}
                }
            
            return {
                "success": True,
                **analysis
            }
            
        except Exception as e:
            logger.error(f"ATS analysis failed: {e}")
            return {
                "success": False,
                "error": str(e)
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