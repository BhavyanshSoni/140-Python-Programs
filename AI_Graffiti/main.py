import random
import time
from rich.console import Console
from rich.text import Text
import numpy as np
from rich.live import Live
from rich.panel import Panel

# Initialize Rich console
console = Console()

# ASCII characters for different density levels
ASCII_CHARS = ' .:-=+*#%@'

def type_print(text, delay=0.03):
    """Print text with cyberpunk typing effect"""
    for char in text:
        console.print(char, end='', style='bold green')
        time.sleep(delay)
    print()

def generate_neural_pattern(width, height):
    """Generate a neural network-like pattern"""
    pattern = np.random.rand(height, width)
    # Apply convolution-like effect
    for _ in range(3):
        pattern = np.convolve(pattern.flatten(), [0.2, 0.5, 0.2], mode='same').reshape(height, width)
    return pattern

def apply_glitch_effect(art):
    """Apply random glitch effects to ASCII art"""
    lines = art.split('\n')
    glitched_lines = []
    
    for line in lines:
        if random.random() < 0.1:  # 10% chance of glitch per line
            # Random glitch effects
            effects = [
                lambda x: x[::-1],  # Reverse
                lambda x: ''.join(random.choice(ASCII_CHARS) if random.random() < 0.3 else c for c in x),
                lambda x: x.replace(' ', random.choice(ASCII_CHARS)),
            ]
            line = random.choice(effects)(line)
        glitched_lines.append(line)
    
    return '\n'.join(glitched_lines)

def generate_ai_art(text, width=40, height=15):
    """Generate AI-inspired ASCII art"""
    # Generate base pattern
    pattern = generate_neural_pattern(width, height)
    
    # Convert to ASCII
    art = ''
    for row in pattern:
        for val in row:
            art += ASCII_CHARS[int(val * len(ASCII_CHARS))]
        art += '\n'
    
    # Add text overlay
    if text:
        lines = art.split('\n')
        text_pos = height // 2
        text_line = text.center(width)
        lines[text_pos] = text_line
        art = '\n'.join(lines)
    
    return art

def animate_art(text):
    """Create an animated ASCII art display"""
    with Live(refresh_per_second=4) as live:
        while True:
            try:
                art = generate_ai_art(text)
                glitched_art = apply_glitch_effect(art)
                
                # Create styled panel
                styled_text = Text(glitched_art)
                panel = Panel(
                    styled_text,
                    title="[bold green]AI Graffiti[/]",
                    border_style="green",
                    subtitle="[bold red]Neural Network Visualization[/]"
                )
                
                live.update(panel)
                time.sleep(0.25)
            except KeyboardInterrupt:
                break

def main():
    """Main program with cool AI-themed interface"""
    console.clear()
    type_print("🤖 Welcome to AI_Graffiti", delay=0.05)
    type_print("    Neural Network Art Generator", delay=0.03)
    print()
    
    while True:
        try:
            type_print("Enter text to convert (or press Enter for pattern):", delay=0.02)
            text = input("> ").strip()
            print("\nGenerating neural art...\n")
            animate_art(text)
        except KeyboardInterrupt:
            print("\n")
            type_print("🧠 Neural network powering down...", delay=0.05)
            break

if __name__ == "__main__":
    main() 