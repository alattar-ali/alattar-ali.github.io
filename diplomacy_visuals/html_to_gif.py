from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image


html_files = [
    "frame1.html",
    "frame2.html",
    "frame3.html",
    "frame4.html",
    "frame5.html", 
]

# Screenshot settings
viewport_width = 1200
viewport_height = 800

duration_ms = 1000  
output_gif = "output.gif"

frames = []

with sync_playwright() as p:
    browser = p.chromium.launch()

    page = browser.new_page(
        viewport={
            "width": viewport_width,
            "height": viewport_height
        }
    )

    for i, html_file in enumerate(html_files):
        html_path = Path(html_file).resolve()

        page.goto(html_path.as_uri())
        page.wait_for_timeout(300)

        screenshot_path = f"frame_{i:03}.png"

        page.screenshot(
            path=screenshot_path,
            full_page=False
        )

        frame = Image.open(screenshot_path).convert("RGB")
        frames.append(frame)

    browser.close()

frames[0].save(
    output_gif,
    save_all=True,
    append_images=frames[1:],
    duration=duration_ms,
    loop=0
)

print(f"Created {output_gif}")