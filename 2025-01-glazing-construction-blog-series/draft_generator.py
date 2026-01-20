# Simple script to simulate AI draft generation from prompts
# Outputs raw draft text to console or file

PROMPTS = {
    "article1": "Write a blog post about modern glazing techniques for energy-efficient buildings. Keep it simple.",
    "article2": "Write a blog post about decorative glazing in interior design. Include examples."
}

def generate_draft(article_key):
    # Simulated AI output - in real use, this would call an API
    drafts = {
        "article1": """# Modern Glazing Techniques for Energy-Efficient Buildings

Glazing is super important in modern construction. It means the glass parts of buildings. Today we have many new techniques that make buildings use less energy.

Double glazing is when there are two panes of glass with air or gas between them. This helps keep heat inside in winter and outside in summer. Triple glazing is even better but more expensive.

Low-E coatings are special layers on glass that reflect heat. They let light in but block infrared. This is good for energy saving.

Smart glass can change from clear to tinted when electricity is applied. It's cool for privacy and sun control.

Vacuum insulated glass is new technology with vacuum between panes. It's very thin but has excellent insulation.

These techniques help buildings meet energy standards and reduce carbon footprint. Architects like them because they look nice too.

In conclusion, glazing technology is advancing fast and helping make greener buildings.""",

        "article2": """# Decorative Glazing in Interior Design

Decorative glazing is using fancy glass in interiors. It can make spaces look beautiful.

Fritted glass has patterns baked into it. It's good for privacy and design.

Stained glass is old but still used in modern ways. Colored glass makes nice light effects.

Etched glass has designs cut into surface. It can be frosted for privacy.

Laminated glass with fabrics or films inside can have colors and textures.

These options help designers create unique looks while also providing function like sound control or safety.

Decorative glazing is popular in hotels, offices, and homes."""
    }
    
    if article_key in drafts:
        print(f"Generated draft for {article_key}:\n")
        print(drafts[article_key])
        # Optional: save to file
        with open(f"{article_key}_ai_draft.md", "w", encoding="utf-8") as f:
            f.write(drafts[article_key])
        print(f"\nDraft saved to {article_key}_ai_draft.md")
    else:
        print("Prompt not found.")

if __name__ == "__main__":
    print("AI Draft Generator for Glazing Blog Series")
    choice = input("Enter article key (article1 or article2): ").strip()
    generate_draft(choice)
