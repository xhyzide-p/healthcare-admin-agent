"""
Script to create a project thumbnail image
Creates a 560x280 PNG image for the project card
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    # Create image
    width, height = 560, 280
    img = Image.new('RGB', (width, height), color='#1a237e')
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fallback to default
    try:
        title_font = ImageFont.truetype("arial.ttf", 28)
        subtitle_font = ImageFont.truetype("arial.ttf", 16)
        agent_font = ImageFont.truetype("arial.ttf", 12)
        small_font = ImageFont.truetype("arial.ttf", 11)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        agent_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Title
    title = "Healthcare Administrative Assistant"
    subtitle = "Multi-Agent AI System"
    
    # Get text dimensions for centering
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = bbox[2] - bbox[0]
    draw.text(((width - title_width) // 2, 20), title, fill='#ffffff', font=title_font)
    
    bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = bbox[2] - bbox[0]
    draw.text(((width - subtitle_width) // 2, 55), subtitle, fill='#b0bec5', font=subtitle_font)
    
    # Orchestrator box
    orchestrator_x = 200
    orchestrator_y = 90
    orchestrator_w = 160
    orchestrator_h = 50
    draw.rectangle([orchestrator_x, orchestrator_y, orchestrator_x + orchestrator_w, orchestrator_y + orchestrator_h], 
                   fill='#3949ab', outline='#ffffff', width=2)
    
    bbox = draw.textbbox((0, 0), "Orchestrator Agent", font=agent_font)
    text_width = bbox[2] - bbox[0]
    draw.text((orchestrator_x + (orchestrator_w - text_width) // 2, orchestrator_y + 15), 
              "Orchestrator Agent", fill='#ffffff', font=agent_font)
    
    # Agent boxes
    agent_y = 160
    agent_h = 40
    agent_w = 100
    
    agents = [
        ("Intake", 80),
        ("Scheduling", 200),
        ("Verification", 320)
    ]
    
    for agent_name, agent_x in agents:
        # Box
        draw.rectangle([agent_x, agent_y, agent_x + agent_w, agent_y + agent_h], 
                      fill='#5c6bc0', outline='#ffffff', width=1)
        
        # Text
        bbox = draw.textbbox((0, 0), agent_name, font=small_font)
        text_width = bbox[2] - bbox[0]
        draw.text((agent_x + (agent_w - text_width) // 2, agent_y + 8), 
                 agent_name, fill='#ffffff', font=small_font)
        draw.text((agent_x + (agent_w - text_width) // 2, agent_y + 21), 
                 "Agent", fill='#ffffff', font=small_font)
        
        # Arrow from orchestrator
        arrow_x = orchestrator_x + orchestrator_w // 2 + (agent_x + agent_w // 2 - orchestrator_x - orchestrator_w // 2) // 2
        draw.line([arrow_x, orchestrator_y + orchestrator_h, arrow_x, agent_y], 
                 fill='#ffffff', width=2)
        # Arrowhead
        draw.polygon([(arrow_x - 5, agent_y - 5), (arrow_x + 5, agent_y - 5), (arrow_x, agent_y)], 
                    fill='#ffffff')
    
    # Followup Agent
    followup_x = 200
    followup_y = 220
    followup_w = 160
    followup_h = 40
    draw.rectangle([followup_x, followup_y, followup_x + followup_w, followup_y + followup_h], 
                   fill='#7986cb', outline='#ffffff', width=1)
    
    bbox = draw.textbbox((0, 0), "Followup Agent", font=agent_font)
    text_width = bbox[2] - bbox[0]
    draw.text((followup_x + (followup_w - text_width) // 2, followup_y + 12), 
              "Followup Agent", fill='#ffffff', font=agent_font)
    
    # Arrow to followup
    center_x = orchestrator_x + orchestrator_w // 2
    draw.line([center_x, agent_y + agent_h, center_x, followup_y], 
             fill='#ffffff', width=2)
    draw.polygon([(center_x - 5, followup_y - 5), (center_x + 5, followup_y - 5), (center_x, followup_y)], 
                fill='#ffffff')
    
    # Footer text
    footer = "Automates Healthcare Administration • 95% Faster • HIPAA Compliant"
    bbox = draw.textbbox((0, 0), footer, font=small_font)
    footer_width = bbox[2] - bbox[0]
    draw.text(((width - footer_width) // 2, 255), footer, fill='#b0bec5', font=small_font)
    
    # Save
    img.save('project_thumbnail.png')
    print("✓ Created project_thumbnail.png (560x280)")
    print("  File saved successfully!")
    
except ImportError:
    print("PIL/Pillow not installed. Installing...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    print("Please run this script again after installation.")
except Exception as e:
    print(f"Error creating image: {e}")
    print("\nAlternative: Use the SVG file (project_thumbnail.svg) and convert it to PNG")
    print("You can use online tools like: https://cloudconvert.com/svg-to-png")


