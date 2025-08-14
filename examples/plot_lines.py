"""
Example demonstrating the lines functionality in mplbasketball.

This example shows how to use the Lines function to draw various types of lines
on basketball courts, including basic lines, comet lines, transparent lines,
and lines with colormaps. This version simulates a high-intensity basketball game
with many passes and movements.
"""

import matplotlib.pyplot as plt
import numpy as np

from mplbasketball import Court, Lines


def generate_pass_data(n_passes=200):
    """Generate realistic basketball pass data."""
    passes = []
    
    # Define court boundaries (NBA court in feet)
    court_width = 94
    court_height = 50
    
    for _ in range(n_passes):
        # Only assist passes
        # Short to medium passes
        x1 = np.random.uniform(-40, 40)
        y1 = np.random.uniform(-20, 20)
        x2 = x1 + np.random.uniform(-15, 15)
        y2 = y1 + np.random.uniform(-15, 15)
        
        # Ensure coordinates are within court bounds
        x1 = np.clip(x1, -47, 47)
        y1 = np.clip(y1, -25, 25)
        x2 = np.clip(x2, -47, 47)
        y2 = np.clip(y2, -25, 25)
        
        passes.append((x1, y1, x2, y2, 'completed'))
    
    return passes


def main():
    # Create a court
    court = Court(court_type="nba", origin="center")
    fig, ax = court.draw(orientation="h", showaxis=False)
    
    # Generate pass data
    print("Generating pass data...")
    passes = generate_pass_data(n_passes=300)
    
    # Define styles for completed passes
    completed_style = {
        'color': 'gold',
        'linewidth': 2,
        'comet': True,
        'transparent': False
    }
    
    # Draw passes
    print("Drawing passes...")
    for x_start, y_start, x_end, y_end, pass_type in passes:
        style = completed_style.copy()
        
        # Add some randomness to make it look more realistic
        x_start += np.random.normal(0, 1)
        y_start += np.random.normal(0, 1)
        x_end += np.random.normal(0, 1)
        y_end += np.random.normal(0, 1)
        
        # Draw the pass
        Lines(x_start, y_start, x_end, y_end, ax=ax, **style)
    

    
    # Add title and adjust layout
    plt.title("Basketball Game Simulation - Completed Passes\nUsing mplbasketball Lines Function", 
              fontsize=14, fontweight='bold', color='white')
    
    # Add legend
    legend_elements = [
        plt.Line2D([0], [0], color='gold', linewidth=3, label='Completed Passes')
    ]
    
    ax.legend(handles=legend_elements, loc='upper right', 
             bbox_to_anchor=(1.15, 1), fontsize=10)
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
