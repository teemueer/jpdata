import svgwrite

# Create an SVG drawing
dwg = svgwrite.Drawing("app/static/芬.svg", profile="tiny", size=("200px", "200px"))

# Add a white background
dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="white"))

# Add the character 芬 with the specified color #002F6C
dwg.add(
    dwg.text(
        "芬",
        insert=("50%", "50%"),
        fill="#002F6C",
        font_size="150px",
        font_family="ms gothic",
        text_anchor="middle",
    )
)

# Save the SVG file
dwg.save()
