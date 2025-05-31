#!/usr/bin/env python3
"""
Script to seed the database with default CV templates.
Run this from the backend/ directory: python scripts/seed_templates.py
"""

import sys
import os
# Add the parent directory (backend) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.cv import Template

def seed_templates():
    db = SessionLocal()
    try:
        # Check if templates already exist
        existing_templates = db.query(Template).count()
        if existing_templates > 0:
            print(f"Templates already exist ({existing_templates} found). Skipping seed.")
            return

        # Template 1: Software Engineer
        software_template = Template(
            name="Software Engineer",
            description="Professional template for software developers and engineers",
            markdown_content="""# [Your Name]
**Software Engineer**

📧 [your.email@example.com] | 📱 [Your Phone] | 🌐 [LinkedIn/Portfolio]

## Professional Summary
Experienced software engineer with [X] years of expertise in full-stack development, specializing in [your technologies]. Passionate about building scalable applications and solving complex technical challenges.

## Technical Skills
- **Languages:** Python, JavaScript, TypeScript, Java
- **Frontend:** React, Vue.js, HTML5, CSS3
- **Backend:** Node.js, FastAPI, Django, Express
- **Databases:** PostgreSQL, MongoDB, Redis
- **Tools:** Docker, Git, AWS, CI/CD

## Professional Experience

### Senior Software Engineer | [Company Name]
*[Start Date] - Present*
- Developed and maintained [describe key projects/systems]
- Improved system performance by [X]% through [specific improvements]
- Led a team of [X] developers on [project description]
- Technologies used: [list technologies]

### Software Engineer | [Previous Company]
*[Start Date] - [End Date]*
- Built [describe key features/products]
- Collaborated with cross-functional teams to deliver [results]
- Implemented [specific technologies/practices]

## Education
**[Degree] in [Field]** | [University Name]
*Graduated: [Year]*

## Projects
- **[Project Name]:** [Brief description and technologies used]
- **[Project Name]:** [Brief description and technologies used]""",
            settings={
                "font": "Arial",
                "fontSize": 11,
                "margins": {"top": 20, "bottom": 20, "left": 15, "right": 15},
                "theme": "professional"
            },
            is_default="true"
        )

        # Template 2: Marketing Manager
        marketing_template = Template(
            name="Marketing Manager",
            description="Clean template for marketing professionals and managers",
            markdown_content="""# [Your Name]
**Marketing Manager**

📧 [email@example.com] | 📱 [phone] | 🔗 [LinkedIn Profile]

## Professional Summary
Results-driven marketing manager with [X]+ years of experience developing and executing comprehensive marketing strategies. Proven track record of increasing brand awareness, driving customer acquisition, and managing cross-functional teams.

## Core Competencies
- **Digital Marketing:** SEO/SEM, Social Media, Email Campaigns
- **Analytics:** Google Analytics, Facebook Ads Manager, HubSpot
- **Strategy:** Brand Management, Content Strategy, Market Research
- **Leadership:** Team Management, Project Coordination, Budget Planning

## Professional Experience

### Marketing Manager | [Company Name]
*[Start Date] - Present*
- Increased brand awareness by [X]% through integrated marketing campaigns
- Managed marketing budget of $[amount] across multiple channels
- Led team of [X] marketing specialists and coordinators
- Developed content strategy resulting in [X]% increase in engagement

### Digital Marketing Specialist | [Previous Company]
*[Start Date] - [End Date]*
- Executed social media campaigns reaching [X] customers monthly
- Improved email marketing open rates by [X]% through A/B testing
- Collaborated with sales team to generate [X] qualified leads per quarter

## Education
**[Degree] in Marketing/Business** | [University Name]
*Graduated: [Year]*

## Certifications
- Google Analytics Certified
- HubSpot Content Marketing Certification
- Facebook Blueprint Certification

## Key Achievements
- Launched successful product campaign resulting in [X]% sales increase
- Managed rebranding initiative across [X] markets
- Built marketing automation system reducing manual work by [X] hours/week""",
            settings={
                "font": "Helvetica",
                "fontSize": 11,
                "margins": {"top": 25, "bottom": 25, "left": 20, "right": 20},
                "theme": "modern"
            },
            is_default="true"
        )

        # Template 3: Simple/Minimal
        simple_template = Template(
            name="Simple & Clean",
            description="Minimal template suitable for any profession",
            markdown_content="""# [Your Name]

📧 [your.email@example.com] | 📱 [phone number]

## About
[Write a brief 2-3 sentence summary about yourself and your professional focus]

## Experience

**[Job Title] | [Company Name]**  
*[Start Date] - [End Date]*
- [Key achievement or responsibility]
- [Key achievement or responsibility]
- [Key achievement or responsibility]

**[Previous Job Title] | [Previous Company]**  
*[Start Date] - [End Date]*
- [Key achievement or responsibility]
- [Key achievement or responsibility]

## Skills
- [Skill 1]
- [Skill 2]
- [Skill 3]
- [Skill 4]

## Education
**[Degree]** | [University Name] | [Year]

## Contact
Feel free to reach out via email or phone for opportunities and collaborations.""",
            settings={
                "font": "Times New Roman",
                "fontSize": 12,
                "margins": {"top": 30, "bottom": 30, "left": 25, "right": 25},
                "theme": "minimal"
            },
            is_default="false"
        )

        # Add templates to database
        db.add(software_template)
        db.add(marketing_template)
        db.add(simple_template)
        db.commit()

        print("✅ Successfully added 3 CV templates to the database!")
        print("Templates added:")
        print("1. Software Engineer (default)")
        print("2. Marketing Manager (default)")
        print("3. Simple & Clean")

    except Exception as e:
        print(f"❌ Error seeding templates: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_templates()