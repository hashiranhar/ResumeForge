import markdown
from weasyprint import HTML, CSS
from io import BytesIO
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class PDFService:
    
    def __init__(self):
        """Initialize PDF service with default styles"""
        self.default_css = self._get_default_css()
    
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
            # Convert markdown to HTML
            html_content = self._markdown_to_html(markdown_content)
            
            # Generate CSS based on settings
            css_styles = self._generate_css(settings or {})
            
            # Create PDF
            html = HTML(string=html_content)
            css = CSS(string=css_styles)
            
            # Generate PDF to bytes
            pdf_buffer = BytesIO()
            html.write_pdf(pdf_buffer, stylesheets=[css])
            
            return pdf_buffer.getvalue()
            
        except Exception as e:
            logger.error(f"PDF generation failed: {str(e)}")
            raise Exception(f"Failed to generate PDF: {str(e)}")
    
    def _markdown_to_html(self, markdown_content: str) -> str:
        """Convert markdown content to HTML"""
        if not markdown_content or markdown_content.strip() == "":
            markdown_content = "# Your CV\n\nPlease add your CV content here."
        
        # Configure markdown with extensions
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc'
        ])
        
        html_body = md.convert(markdown_content)
        
        # Wrap in complete HTML document
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>CV</title>
        </head>
        <body>
            {html_body}
        </body>
        </html>
        """
        
        return html_content
    
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
        
        blockquote {{
            margin: 8pt 0 8pt 20pt;
            padding: 4pt 0 4pt 12pt;
            border-left: 3pt solid {theme_colors['accent']};
            font-style: italic;
            color: {theme_colors['secondary']};
        }}
        
        code {{
            background-color: #f8f9fa;
            border: 1pt solid #e9ecef;
            padding: 1pt 3pt;
            font-family: 'Courier New', monospace;
            font-size: {config.get('fontSize', 11) - 1}pt;
        }}
        
        pre {{
            background-color: #f8f9fa;
            border: 1pt solid #e9ecef;
            padding: 8pt;
            margin: 8pt 0;
            font-family: 'Courier New', monospace;
            font-size: {config.get('fontSize', 11) - 1}pt;
            overflow-x: auto;
        }}
        
        hr {{
            border: none;
            border-top: 1pt solid {theme_colors['secondary']};
            margin: 16pt 0;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 8pt 0;
        }}
        
        th, td {{
            border: 1pt solid {theme_colors['secondary']};
            padding: 4pt 8pt;
            text-align: left;
        }}
        
        th {{
            background-color: {theme_colors['primary']};
            color: white;
            font-weight: bold;
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

# Create a singleton instance
pdf_service = PDFService()