// RGB Color
export interface RGB {
  r: number;
  g: number;
  b: number;
}

// HSV Color
export interface HSV {
  h: number;
  s: number;
  v: number;
}

// Color type (can be RGB or HSV)
export type Color = 
  | { type: 'rgb'; value: RGB }
  | { type: 'hsv'; value: HSV };

// Bounding box
export interface BoundingBox {
  minX: number;
  minY: number;
  maxX: number;
  maxY: number;
}

// Province type
export type ProvinceType = 'land' | 'sea' | 'lake';

// Terrain types
export type TerrainType = 
  | 'ocean'
  | 'lakes'
  | 'forest'
  | 'hills'
  | 'mountain'
  | 'plains'
  | 'urban'
  | 'jungle'
  | 'marsh'
  | 'desert'
  | 'unknown';

// Province definition from definition.csv
export interface Province {
  id: number;
  color: RGB;
  type: ProvinceType;
  coastal: boolean;
  terrain: TerrainType;
  continent: number;
  // Computed fields
  pixelCount?: number;
  boundingBox?: BoundingBox;
  // References
  stateId?: number;
  strategicRegionId?: number;
}

// State from history/states/*.txt
export interface State {
  id: number;
  name: string;
  manpower: number;
  stateCategory: string;
  owner: string;
  cores: string[];
  claims: string[];
  provinces: number[];
  buildings: Building[];
  victoryPoints: VictoryPoint[];
  localSupplies: number;
  // Source file path
  filePath?: string;
}

export interface Building {
  type: string;
  level: number;
  provinceId?: number; // For province-specific buildings like naval_base
}

export interface VictoryPoint {
  provinceId: number;
  value: number;
}

// Strategic Region from map/strategicregions/*.txt
export interface StrategicRegion {
  id: number;
  name: string;
  provinces: number[];
  weather: WeatherPeriod[];
  // Source file path
  filePath?: string;
}

export interface WeatherPeriod {
  between: [number, number];
  temperature: [number, number];
  no_phenomenon: number;
  rain_light: number;
  rain_heavy: number;
  snow: number;
  blizzard: number;
  arctic_water: number;
  mud: number;
  sandstorm: number;
  min_snow_level: number;
}

// AI Area from common/ai_areas/*.txt
export interface AIArea {
  name: string;
  strategicRegions?: number[];
  continents?: string[];
}

// Country color from common/countries/colors.txt
export interface CountryColor {
  tag: string;
  color: Color;
  colorUI: Color;
}

// Adjacency from adjacencies.csv
export interface Adjacency {
  from: number;
  to: number;
  type: 'sea' | '';
  through: number;
  startX: number;
  startY: number;
  stopX: number;
  stopY: number;
  ruleName: string;
  comment: string;
}

// Edit tool types
export type ToolType = 
  | 'select'
  | 'brush'
  | 'fill'
  | 'pencil'
  | 'eyedropper'
  | 'eraser'
  | 'rectangle'
  | 'line';

// Brush shape
export type BrushShape = 'circle' | 'square';

// Pixel change for undo/redo
export interface PixelChange {
  x: number;
  y: number;
  oldColor: RGB;
  newColor: RGB;
}

// Edit action for history
export interface EditAction {
  type: 'pixels';
  changes: PixelChange[];
  timestamp: number;
}

// Layer types
export type LayerType = 
  | 'provinces'
  | 'states'
  | 'strategicRegions'
  | 'aiAreas'
  | 'terrain';

// Project structure
export interface Project {
  rootPath: string;
  mapPath: string;
  commonPath: string;
  historyPath: string;
  loaded: boolean;
}

// Validation error/warning
export interface ValidationIssue {
  type: 'error' | 'warning';
  code: string;
  message: string;
  file?: string;
  provinceId?: number;
  stateId?: number;
}
