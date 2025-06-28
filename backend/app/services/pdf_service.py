import markdown
from weasyprint import HTML, CSS
from io import BytesIO
from typing import Dict, Any, Optional
import logging
import re
import PyPDF2
import pdfplumber
import io

logger = logging.getLogger(__name__)

class PDFService:
    
    def __init__(self):
        """Initialize PDF service with default styles"""
        self.default_css = self._get_default_css()
        self.max_file_size = 5 * 1024 * 1024  # 5MB

    
    def generate_pdf(self, markdown_content: str, settings: Optional[Dict[str, Any]] = None) -> bytes:
        """
        Generate PDF from markdown content with custom styling.
        
        Args:
            markdown_content: The CV content in markdown format
            settings: Styling settings (font, margins, theme, etc.)
            
        Returns:
            bytes: PDF file content
        """
        try:
            # Process special formatting markers (this now handles markdown conversion too)
            html_content = self._process_special_formatting(markdown_content)
            
            # Wrap in complete HTML document
            final_html = self._wrap_html(html_content)
            
            # Generate CSS based on settings
            css_styles = self._generate_css(settings or {})
            
            # Create PDF
            html = HTML(string=final_html)
            css = CSS(string=css_styles)
            
            # Generate PDF to bytes
            pdf_buffer = BytesIO()
            html.write_pdf(pdf_buffer, stylesheets=[css])
            
            return pdf_buffer.getvalue()
            
        except Exception as e:
            logger.error(f"PDF generation failed: {str(e)}")
            raise Exception(f"Failed to generate PDF: {str(e)}")
        
    def extract_text_from_pdf(self, pdf_bytes: bytes) -> Dict[str, Any]:
        """Extract text from PDF using multiple methods"""
        try:
            # Check file size
            if len(pdf_bytes) > self.max_file_size:
                return {
                    "success": False,
                    "error": "PDF file too large (max 5MB)",
                    "text": ""
                }
            
            # Method 1: pdfplumber (better for complex layouts)
            text = self._extract_with_pdfplumber(pdf_bytes)
            
            if not text.strip():
                # Method 2: PyPDF2 (fallback)
                text = self._extract_with_pypdf2(pdf_bytes)
            
            return {
                "success": True,
                "text": text,
                "method": "pdfplumber" if text else "pypdf2"
            }
        except Exception as e:
            logger.error(f"PDF text extraction failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "text": ""
            }
    
    def _extract_with_pdfplumber(self, pdf_bytes: bytes) -> str:
        """Extract using pdfplumber for better layout preservation"""
        text_content = []
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
        return "\n\n".join(text_content)
    
    def _extract_with_pypdf2(self, pdf_bytes: bytes) -> str:
        """Fallback extraction method"""
        text_content = []
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        for page in pdf_reader.pages:
            text_content.append(page.extract_text())
        return "\n\n".join(text_content)
    
    def _process_special_formatting(self, content: str) -> str:
        """Process special formatting markers after markdown conversion"""
        if not content:
            return ""
        
        # First convert markdown to HTML normally
        md = markdown.Markdown(extensions=['markdown.extensions.extra'])
        html_content = md.convert(content)
        
        # Then process our special markers in the HTML
        lines = html_content.split('\n')
        processed_lines = []
        
        for line in lines:
            # Check for CENTER marker
            if '[CENTER]' in line:
                clean_line = line.replace('[CENTER]', '').strip()
                # If it's already wrapped in HTML tags, add class
                if clean_line.strip().startswith('<'):
                    # Add center class to existing HTML element
                    clean_line = re.sub(r'<(\w+)([^>]*)>', r'<\1 class="center-text"\2>', clean_line, count=1)
                    processed_lines.append(clean_line)
                else:
                    processed_lines.append(f'<div class="center-text">{clean_line}</div>')
            # Check for DATE-RIGHT marker  
            elif '[DATE:' in line:
                # Extract date from [DATE: content]
                date_match = re.search(r'\[DATE:\s*([^\]]+)\]', line)
                if date_match:
                    date_content = date_match.group(1).strip()
                    clean_line = re.sub(r'\s*\[DATE:[^\]]+\]', '', line).strip()
                    
                    # Check if it's a header element
                    if clean_line.startswith('<h'):
                        # For headers, add the date as a span inside the header
                        header_match = re.match(r'(<h\d[^>]*>)(.*?)(</h\d>)', clean_line)
                        if header_match:
                            opening_tag = header_match.group(1)
                            header_content = header_match.group(2)
                            closing_tag = header_match.group(3)
                            processed_lines.append(f'{opening_tag}{header_content}<span class="header-date">{date_content}</span>{closing_tag}')
                        else:
                            processed_lines.append(clean_line)
                    else:
                        # For non-headers, use the flex layout
                        processed_lines.append(f'<div class="date-line"><span class="content">{clean_line}</span><span class="date">{date_content}</span></div>')
                else:
                    processed_lines.append(line)
            else:
                processed_lines.append(line)
        
        return '\n'.join(processed_lines)
    
    def _wrap_html(self, html_body: str) -> str:
        """Wrap processed HTML in complete document"""
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>CV</title>
        </head>
        <body>
            {html_body}
        </body>
        </html>
        """
    
    def _generate_css(self, settings: Dict[str, Any]) -> str:
        """Generate CSS styles based on user settings"""
        # Default settings
        defaults = {
            "font": "Arial",
            "fontSize": 11,
            "margins": {"top": 20, "bottom": 20, "left": 15, "right": 15},
            "theme": "professional",
            "lineHeight": 1.4
        }
        
        # Merge with user settings
        config = {**defaults, **settings}
        margins = config.get("margins", defaults["margins"])
        
        # Font family mapping
        font_families = {
            "Arial": "Arial, sans-serif",
            "Helvetica": "Helvetica, Arial, sans-serif",
            "Times New Roman": "'Times New Roman', Times, serif",
            "Georgia": "Georgia, serif",
            "Verdana": "Verdana, sans-serif"
        }
        
        # Theme-based colors
        themes = {
            "professional": {
                "primary": "#2c3e50",
                "secondary": "#34495e",
                "accent": "#3498db",
                "text": "#2c3e50",
                "background": "#ffffff"
            },
            "modern": {
                "primary": "#1a1a1a",
                "secondary": "#4a4a4a",
                "accent": "#007acc",
                "text": "#333333",
                "background": "#ffffff"
            },
            "minimal": {
                "primary": "#000000",
                "secondary": "#666666",
                "accent": "#888888",
                "text": "#333333",
                "background": "#ffffff"
            },
            "creative": {
                "primary": "#8e44ad",
                "secondary": "#9b59b6",
                "accent": "#e74c3c",
                "text": "#2c3e50",
                "background": "#ffffff"
            }
        }
        
        theme_colors = themes.get(config.get("theme", "professional"), themes["professional"])
        font_family = font_families.get(config.get("font", "Arial"), font_families["Arial"])
        
        css = f"""
        @page {{
            size: A4;
            margin: {margins.get('top', 20)}mm {margins.get('right', 15)}mm {margins.get('bottom', 20)}mm {margins.get('left', 15)}mm;
        }}
        
        body {{
            font-family: {font_family};
            font-size: {config.get('fontSize', 11)}pt;
            line-height: {config.get('lineHeight', 1.4)};
            color: {theme_colors['text']};
            background-color: {theme_colors['background']};
            margin: 0;
            padding: 0;
        }}
        
        h1 {{
            color: {theme_colors['primary']};
            font-size: {config.get('fontSize', 11) + 6}pt;
            font-weight: bold;
            margin: 0 0 8pt 0;
            padding: 0;
            border-bottom: 2pt solid {theme_colors['accent']};
            padding-bottom: 4pt;
        }}
        
        h2 {{
            color: {theme_colors['primary']};
            font-size: {config.get('fontSize', 11) + 3}pt;
            font-weight: bold;
            margin: 16pt 0 6pt 0;
            padding: 0;
            border-bottom: 1pt solid {theme_colors['secondary']};
            padding-bottom: 2pt;
        }}
        
        h3 {{
            color: {theme_colors['secondary']};
            font-size: {config.get('fontSize', 11) + 1}pt;
            font-weight: bold;
            margin: 12pt 0 4pt 0;
            padding: 0;
        }}
        
        p {{
            margin: 6pt 0;
            text-align: justify;
        }}
        
        ul, ol {{
            margin: 6pt 0 6pt 20pt;
            padding: 0;
        }}
        
        li {{
            margin: 3pt 0;
        }}
        
        strong {{
            color: {theme_colors['primary']};
            font-weight: bold;
        }}
        
        em {{
            font-style: italic;
            color: {theme_colors['secondary']};
        }}
        
        a {{
            color: {theme_colors['accent']};
            text-decoration: none;
        }}
        
        hr {{
            border: none;
            border-top: 1pt solid {theme_colors['secondary']};
            margin: 16pt 0;
        }}
        
        /* Special formatting classes */
        .center-text {{
            text-align: center !important;
            margin: 6pt 0;
        }}
        
        .date-line {{
            position: relative;
            margin: 6pt 0;
            min-height: 1.2em;
        }}
        
        .date-line .content {{
            display: block;
            padding-right: 120pt; /* Reserve space for date */
        }}
        
        .date-line .date {{
            position: absolute;
            right: 0;
            top: 0;
            font-style: italic;
            color: {theme_colors['secondary']};
            font-size: {config.get('fontSize', 11) - 1}pt;
            white-space: nowrap;
            width: 110pt; /* Fixed width for dates */
            text-align: right;
        }}
        
        /* Header with dates - keep on same line */
        .header-date {{
            float: right;
            font-style: italic;
            color: {theme_colors['secondary']};
            font-size: {config.get('fontSize', 11) - 1}pt;
            font-weight: normal;
            line-height: 1.2;
        }}
        
        /* Ensure headers with dates don't break */
        h1, h2, h3 {{
            position: relative;
            overflow: hidden;
        }}
        
        h1 .header-date {{
            position: absolute;
            right: 0;
            top: 0;
            font-size: {config.get('fontSize', 11) + 2}pt;
        }}
        
        h2 .header-date {{
            position: absolute;
            right: 0;
            top: 0;
            font-size: {config.get('fontSize', 11)}pt;
        }}
        
        h3 .header-date {{
            position: absolute;
            right: 0;
            top: 0;
            font-size: {config.get('fontSize', 11) - 1}pt;
        }}
        
        /* Clear floats */
        .date-line:after {{
            content: "";
            display: table;
            clear: both;
        }}
        """
        
        return css
    
    def _get_default_css(self) -> str:
        """Get basic default CSS for fallback"""
        return """
        @page {
            size: A4;
            margin: 20mm 15mm;
        }
        
        body {
            font-family: Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.4;
            color: #333;
        }
        
        h1, h2, h3 {
            color: #2c3e50;
        }
        """

pdf_service = PDFService()