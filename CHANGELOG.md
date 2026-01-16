# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-08-14

### Added
- **Lines function**: New functionality for drawing lines on basketball courts
  - Support for basic lines, comet lines (increasing width), and transparent lines (increasing opacity)
  - Colormap integration for lines
  - Coordinate transformation support for all court orientations
  - Basketball-specific applications (pass visualization, player movement tracking)
  - Comprehensive error handling and validation
  - Performance optimized using matplotlib's LineCollection
- **Documentation**: Complete usage guide and examples in README.md
- **Testing**: 12 comprehensive test cases covering all functionality
- **Examples**: New example scripts demonstrating Lines usage

### Technical Details
- New module: `mplbasketball.lines`
- New function: `Lines()` with extensive parameter support
- Integration with existing coordinate transformation system
- Compatible with all court types (NBA, WNBA, NCAA, FIBA)

## [1.0.0] - Initial Release - 2024-09-07

### Added
- Court class for 2D basketball court visualization
- Court3D class for 3D basketball court visualization
- Support for multiple court types (NBA, WNBA, NCAA, FIBA)
- Coordinate transformation utilities
- Integration with matplotlib functions
- Comprehensive documentation and examples
