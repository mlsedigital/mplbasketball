"""Tests for the lines functionality in mplbasketball."""

import numpy as np
import pytest
from matplotlib.collections import LineCollection

from mplbasketball import Court, Lines


class TestLines:
    """Test class for lines functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.court = Court(court_type="nba", origin="center")
        self.fig, self.ax = self.court.draw(orientation="h")

    def test_basic_lines(self):
        """Test basic line drawing."""
        xstart, ystart = [0, 10], [0, 10]
        xend, yend = [20, 30], [20, 30]
        
        line_collection = Lines(xstart, ystart, xend, yend, 
                               color="red", ax=self.ax)
        
        assert isinstance(line_collection, LineCollection)
        assert len(line_collection.get_paths()) == 2

    def test_comet_lines(self):
        """Test comet line drawing."""
        line_collection = Lines(0, 0, 20, 20, comet=True, 
                               color="blue", linewidth=5, ax=self.ax)
        
        assert isinstance(line_collection, LineCollection)
        # Comet lines should have multiple segments
        assert len(line_collection.get_paths()) > 1

    def test_transparent_lines(self):
        """Test transparent line drawing."""
        line_collection = Lines(0, 0, 20, 20, transparent=True, 
                               color="green", alpha_start=0.1, alpha_end=1.0, 
                               ax=self.ax)
        
        assert isinstance(line_collection, LineCollection)
        # Transparent lines should have multiple segments
        assert len(line_collection.get_paths()) > 1

    def test_colormap_lines(self):
        """Test lines with colormap."""
        line_collection = Lines([0, 10], [0, 10], [20, 30], [20, 30], 
                               cmap="viridis", ax=self.ax)
        
        assert isinstance(line_collection, LineCollection)
        assert line_collection.get_cmap() is not None

    def test_coordinate_transformation(self):
        """Test coordinate transformation in lines."""
        # Test transformation from half-court left to full court
        line_collection = Lines([-10, -15], [5, -5], [10, 15], [-5, 5], 
                               fr="hl", to="h", color="purple", ax=self.ax)
        
        assert isinstance(line_collection, LineCollection)

    def test_invalid_parameters(self):
        """Test error handling for invalid parameters."""
        # Test invalid comet parameter
        with pytest.raises(TypeError):
            Lines(0, 0, 20, 20, comet="invalid", ax=self.ax)
        
        # Test invalid transparent parameter
        with pytest.raises(TypeError):
            Lines(0, 0, 20, 20, transparent="invalid", ax=self.ax)
        
        # Test invalid alpha values
        with pytest.raises(TypeError):
            Lines(0, 0, 20, 20, transparent=True, alpha_start=-1, ax=self.ax)
        
        with pytest.raises(TypeError):
            Lines(0, 0, 20, 20, transparent=True, alpha_end=2, ax=self.ax)

    def test_array_size_validation(self):
        """Test validation of array sizes."""
        # Test mismatched array sizes
        with pytest.raises(ValueError):
            Lines([0, 10], [0], [20, 30], [20, 30], ax=self.ax)
        
        with pytest.raises(ValueError):
            Lines([0, 10], [0, 10], [20], [20, 30], ax=self.ax)

    def test_multiple_colors_with_comet(self):
        """Test that multiple colors with comet raises error."""
        with pytest.raises(NotImplementedError):
            Lines([0, 10], [0, 10], [20, 30], [20, 30], 
                  color=["red", "blue"], comet=True, ax=self.ax)

    def test_multiple_linewidths_with_comet(self):
        """Test that multiple linewidths with comet raises error."""
        with pytest.raises(NotImplementedError):
            Lines([0, 10], [0, 10], [20, 30], [20, 30], 
                  linewidth=[2, 3], comet=True, ax=self.ax)

    def test_color_and_cmap_conflict(self):
        """Test that color and cmap cannot be used together."""
        with pytest.raises(ValueError):
            Lines(0, 0, 20, 20, color="red", cmap="viridis", ax=self.ax)

    def test_linewidth_aliases(self):
        """Test that both 'linewidth' and 'lw' work."""
        line_collection1 = Lines(0, 0, 20, 20, linewidth=3, ax=self.ax)
        line_collection2 = Lines(0, 0, 20, 20, lw=3, ax=self.ax)
        
        assert isinstance(line_collection1, LineCollection)
        assert isinstance(line_collection2, LineCollection)

    def test_scalar_inputs(self):
        """Test that scalar inputs work correctly."""
        line_collection = Lines(0, 0, 20, 20, color="red", ax=self.ax)
        assert isinstance(line_collection, LineCollection)
        assert len(line_collection.get_paths()) == 1


if __name__ == "__main__":
    pytest.main([__file__])
