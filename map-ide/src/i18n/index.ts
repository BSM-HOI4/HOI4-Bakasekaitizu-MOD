/**
 * Internationalization (i18n) system for HoI4 Map IDE
 * Supports Japanese and English
 */

export type Language = 'ja' | 'en';

export interface I18nStrings {
  // App
  appTitle: string;
  loadingProject: string;
  loadingMap: string;
  openProjectFolder: string;
  
  // Welcome Screen
  welcomeTitle: string;
  welcomeSubtitle: string;
  getStarted: string;
  welcomeDescription: string;
  openModFolder: string;
  testMode: string;
  keyboardShortcut: string;
  
  // Features
  provinceEditing: string;
  provinceEditingDesc: string;
  stateManagement: string;
  stateManagementDesc: string;
  strategicRegions: string;
  strategicRegionsDesc: string;
  aiAreas: string;
  aiAreasDesc: string;
  
  // Tools
  tools: string;
  select: string;
  brush: string;
  pencil: string;
  eraser: string;
  fill: string;
  eyedropper: string;
  line: string;
  rectangle: string;
  
  // Layers
  layers: string;
  provinces: string;
  states: string;
  terrain: string;
  showGrid: string;
  showBorders: string;
  activeLayer: string;
  
  // Panels
  properties: string;
  search: string;
  validation: string;
  colors: string;
  
  // Properties Panel
  noSelection: string;
  provinceId: string;
  provinceColor: string;
  provinceType: string;
  coastal: string;
  terrain_field: string;
  continent: string;
  belongsToState: string;
  stateId: string;
  stateName: string;
  stateProvinces: string;
  manpower: string;
  owner: string;
  regionId: string;
  regionName: string;
  regionProvinces: string;
  weather: string;
  navalTerrain: string;
  
  // Search
  searchPlaceholder: string;
  searchResults: string;
  noResults: string;
  
  // Validation
  validationTitle: string;
  noIssues: string;
  errors: string;
  warnings: string;
  
  // Actions
  save: string;
  saving: string;
  saved: string;
  unsaved: string;
  error: string;
  undo: string;
  redo: string;
  autoSave: string;
  
  // Settings
  settings: string;
  language: string;
  
  // Status
  zoomLevel: string;
  renderer: string;
  webgl: string;
  canvas: string;
  
  // Brush settings
  brushSize: string;
  brushShape: string;
  circle: string;
  square: string;
  selectedColor: string;
  noColorSelected: string;
}

const ja: I18nStrings = {
  // App
  appTitle: 'HoI4 Map IDE',
  loadingProject: 'プロジェクトを読み込み中...',
  loadingMap: 'マップを読み込み中...',
  openProjectFolder: 'プロジェクトフォルダを開く',
  
  // Welcome Screen
  welcomeTitle: 'HoI4 Map IDE',
  welcomeSubtitle: 'Hearts of Iron 4 マップ統合開発環境',
  getStarted: 'はじめに',
  welcomeDescription: 'HoI4のmodフォルダを開いて編集を開始します。フォルダには map/、common/、history/ ディレクトリが含まれている必要があります。',
  openModFolder: 'Modフォルダを開く',
  testMode: 'テストモード（デモ）',
  keyboardShortcut: 'キーボードショートカット',
  
  // Features
  provinceEditing: 'プロヴィンス編集',
  provinceEditingDesc: 'ブラシ、塗りつぶし、選択ツールでprovinces.bmpを直接編集',
  stateManagement: 'ステート管理',
  stateManagementDesc: 'ステートの管理、プロヴィンスの割り当て、プロパティの編集',
  strategicRegions: '戦略地域',
  strategicRegionsDesc: '天候設定付きの戦略地域の表示・編集',
  aiAreas: 'AIエリア',
  aiAreasDesc: '戦略地域グループ化のためのAIエリア設定',
  
  // Tools
  tools: 'ツール',
  select: '選択',
  brush: 'ブラシ',
  pencil: 'ペンシル',
  eraser: '消しゴム',
  fill: '塗りつぶし',
  eyedropper: 'スポイト',
  line: '直線',
  rectangle: '矩形',
  
  // Layers
  layers: 'レイヤー',
  provinces: 'プロヴィンス',
  states: 'ステート',
  terrain: '地形',
  showGrid: 'グリッドを表示',
  showBorders: '境界を表示',
  activeLayer: 'アクティブレイヤー',
  
  // Panels
  properties: 'プロパティ',
  search: '検索',
  validation: '検証',
  colors: '色',
  
  // Properties Panel
  noSelection: '選択なし',
  provinceId: 'プロヴィンスID',
  provinceColor: '色',
  provinceType: 'タイプ',
  coastal: '沿岸',
  terrain_field: '地形',
  continent: '大陸',
  belongsToState: '所属ステート',
  stateId: 'ステートID',
  stateName: 'ステート名',
  stateProvinces: 'プロヴィンス数',
  manpower: '人的資源',
  owner: '所有国',
  regionId: '地域ID',
  regionName: '地域名',
  regionProvinces: 'プロヴィンス数',
  weather: '天候',
  navalTerrain: '海上地形',
  
  // Search
  searchPlaceholder: 'ID、名前、色で検索...',
  searchResults: '検索結果',
  noResults: '結果なし',
  
  // Validation
  validationTitle: '検証',
  noIssues: '問題なし',
  errors: 'エラー',
  warnings: '警告',
  
  // Actions
  save: '保存',
  saving: '保存中...',
  saved: '保存済み',
  unsaved: '未保存',
  error: 'エラー',
  undo: '元に戻す',
  redo: 'やり直し',
  autoSave: '自動保存',
  
  // Settings
  settings: '設定',
  language: '言語',
  
  // Status
  zoomLevel: 'ズーム',
  renderer: 'レンダラー',
  webgl: 'WebGL',
  canvas: 'Canvas',
  
  // Brush settings
  brushSize: 'ブラシサイズ',
  brushShape: 'ブラシ形状',
  circle: '円形',
  square: '四角形',
  selectedColor: '選択中の色',
  noColorSelected: '色が選択されていません',
};

const en: I18nStrings = {
  // App
  appTitle: 'HoI4 Map IDE',
  loadingProject: 'Loading project...',
  loadingMap: 'Loading map...',
  openProjectFolder: 'Open Project Folder',
  
  // Welcome Screen
  welcomeTitle: 'HoI4 Map IDE',
  welcomeSubtitle: 'Hearts of Iron 4 Map Integrated Development Environment',
  getStarted: 'Get Started',
  welcomeDescription: 'Open a HoI4 mod folder to begin editing. The folder should contain map/, common/, and history/ directories.',
  openModFolder: 'Open Mod Folder',
  testMode: 'Test Mode (Demo)',
  keyboardShortcut: 'Keyboard shortcut',
  
  // Features
  provinceEditing: 'Province Editing',
  provinceEditingDesc: 'Edit provinces.bmp directly with brush, fill, and selection tools',
  stateManagement: 'State Management',
  stateManagementDesc: 'Manage states, assign provinces, and edit properties',
  strategicRegions: 'Strategic Regions',
  strategicRegionsDesc: 'View and edit strategic regions with weather settings',
  aiAreas: 'AI Areas',
  aiAreasDesc: 'Configure AI areas for strategic region grouping',
  
  // Tools
  tools: 'Tools',
  select: 'Select',
  brush: 'Brush',
  pencil: 'Pencil',
  eraser: 'Eraser',
  fill: 'Fill',
  eyedropper: 'Eyedropper',
  line: 'Line',
  rectangle: 'Rectangle',
  
  // Layers
  layers: 'Layers',
  provinces: 'Provinces',
  states: 'States',
  terrain: 'Terrain',
  showGrid: 'Show Grid',
  showBorders: 'Show Borders',
  activeLayer: 'Active Layer',
  
  // Panels
  properties: 'Properties',
  search: 'Search',
  validation: 'Validation',
  colors: 'Colors',
  
  // Properties Panel
  noSelection: 'No Selection',
  provinceId: 'Province ID',
  provinceColor: 'Color',
  provinceType: 'Type',
  coastal: 'Coastal',
  terrain_field: 'Terrain',
  continent: 'Continent',
  belongsToState: 'Belongs to State',
  stateId: 'State ID',
  stateName: 'State Name',
  stateProvinces: 'Provinces',
  manpower: 'Manpower',
  owner: 'Owner',
  regionId: 'Region ID',
  regionName: 'Region Name',
  regionProvinces: 'Provinces',
  weather: 'Weather',
  navalTerrain: 'Naval Terrain',
  
  // Search
  searchPlaceholder: 'Search by ID, name, or color...',
  searchResults: 'Search Results',
  noResults: 'No results',
  
  // Validation
  validationTitle: 'Validation',
  noIssues: 'No issues',
  errors: 'Errors',
  warnings: 'Warnings',
  
  // Actions
  save: 'Save',
  saving: 'Saving...',
  saved: 'Saved',
  unsaved: 'Unsaved',
  error: 'Error',
  undo: 'Undo',
  redo: 'Redo',
  autoSave: 'Auto-save',
  
  // Settings
  settings: 'Settings',
  language: 'Language',
  
  // Status
  zoomLevel: 'Zoom',
  renderer: 'Renderer',
  webgl: 'WebGL',
  canvas: 'Canvas',
  
  // Brush settings
  brushSize: 'Brush Size',
  brushShape: 'Brush Shape',
  circle: 'Circle',
  square: 'Square',
  selectedColor: 'Selected Color',
  noColorSelected: 'No color selected',
};

const translations: Record<Language, I18nStrings> = { ja, en };

export function getTranslations(lang: Language): I18nStrings {
  return translations[lang];
}

export function getAvailableLanguages(): { code: Language; name: string }[] {
  return [
    { code: 'ja', name: '日本語' },
    { code: 'en', name: 'English' },
  ];
}
