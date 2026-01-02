# HoI4 Map IDE

Hearts of Iron 4 Map Integrated Development Environment - A cross-platform visual editor for HoI4 mod map files.

## Features

### Province Map Editing (provinces.bmp)
- **Visual Editing**: Direct pixel-level editing of provinces.bmp
- **Drawing Tools**: 
  - Brush (variable size, circle/square shape)
  - Pencil (1px precision)
  - Fill (flood fill)
  - Eraser
  - Line
  - Rectangle
  - Eyedropper (color picker)
- **Province Management**:
  - Create new provinces with auto-generated colors
  - Merge/Split provinces
  - Edit province properties (type, terrain, coastal)
- **Undo/Redo**: Full history support for all edits

### Data Management
- **definition.csv**: View and edit province definitions
- **States** (history/states/*.txt): View state assignments and properties
- **Strategic Regions** (map/strategicregions/*.txt): View region boundaries and weather settings
- **AI Areas** (common/ai_areas/*.txt): View AI area configurations

### Visualization
- **Layer System**:
  - Province borders
  - State boundaries
  - Strategic region boundaries
  - AI area boundaries
  - Terrain overlay
  - Pixel grid (at high zoom)
- **Zoom & Pan**: Smooth navigation with mouse wheel and drag

## Supported File Formats

| Directory | Files | Description |
|-----------|-------|-------------|
| `map/` | `provinces.bmp` | Province color map (24-bit BMP, editable) |
| `map/` | `definition.csv` | Province definitions |
| `map/` | `adjacencies.csv` | Straits and canals |
| `map/strategicregions/` | `*.txt` | Strategic region definitions |
| `common/ai_areas/` | `*.txt` | AI area definitions |
| `common/countries/` | `colors.txt` | Country colors |
| `history/states/` | `*.txt` | State definitions |

## Installation

### Requirements
- Node.js 18+
- npm or yarn

### Development Setup

```bash
# Clone the repository
cd map-ide

# Install dependencies
npm install

# Start development server
npm run dev
```

### Building

```bash
# Build for production (Vite only)
npm run build

# Build Electron app for distribution
npm run build:electron
```

## Usage

1. Launch the application
2. Click "Open Mod Folder" or press `Ctrl/Cmd + O`
3. Select your HoI4 mod folder (should contain `map/`, `common/`, `history/` directories)
4. The provinces.bmp will be loaded automatically

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl/Cmd + O` | Open project |
| `Ctrl/Cmd + S` | Save changes |
| `Ctrl/Cmd + Z` | Undo |
| `Ctrl/Cmd + Shift + Z` | Redo |
| `+` / `=` | Zoom in |
| `-` | Zoom out |
| `V` | Select tool |
| `B` | Brush tool |
| `G` | Fill tool |
| `P` | Pencil tool |
| `I` | Eyedropper tool |
| `E` | Eraser tool |
| `L` | Line tool |
| `R` | Rectangle tool |

### Mouse Controls

- **Left Click**: Use current tool
- **Middle Button / Alt + Left**: Pan view
- **Scroll Wheel**: Zoom in/out

## Project Structure

```
map-ide/
├── electron/           # Electron main process
│   ├── main.ts        # Main process entry
│   └── preload.ts     # Preload script
├── src/
│   ├── components/    # React components
│   │   ├── layout/    # Header, Sidebar, StatusBar
│   │   ├── map/       # MapCanvas
│   │   └── panels/    # PropertyPanel, ColorPalette
│   ├── core/          # Core editing engine
│   │   ├── BMPParser.ts   # BMP read/write
│   │   └── BMPEditor.ts   # Editing operations
│   ├── parsers/       # File parsers
│   │   ├── csvParser.ts       # CSV parsing
│   │   └── paradox/           # Paradox script parsing
│   ├── stores/        # Zustand state stores
│   │   ├── projectStore.ts    # Project data
│   │   └── mapStore.ts        # Map view state
│   └── types/         # TypeScript types
└── package.json
```

## Technology Stack

- **Framework**: Electron
- **UI**: React 18 + TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Build Tool**: Vite

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.
