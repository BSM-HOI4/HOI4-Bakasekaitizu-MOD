import { create } from 'zustand';
import { RGB, ToolType, BrushShape, LayerType, PixelChange } from '../types';
import { BMPEditor } from '../core/BMPEditor';

interface MapState {
  // BMP Editor
  bmpEditor: BMPEditor | null;
  bmpLoaded: boolean;
  bmpError: string | null;

  // View state
  zoom: number;
  panX: number;
  panY: number;
  viewportWidth: number;
  viewportHeight: number;

  // Selection
  selectedProvinceId: number | null;
  selectedStateId: number | null;
  selectedStrategicRegionId: number | null;
  hoveredProvinceId: number | null;

  // Tool state
  activeTool: ToolType;
  brushSize: number;
  brushShape: BrushShape;
  selectedColor: RGB | null;

  // Layer visibility
  layers: Record<LayerType, boolean>;
  showGrid: boolean;
  showBorders: boolean;

  // Pending changes (for batch operations)
  pendingChanges: PixelChange[];

  // Actions
  loadBMP: (buffer: ArrayBuffer) => void;
  saveBMP: () => ArrayBuffer | null;

  // View actions
  setZoom: (zoom: number) => void;
  setPan: (x: number, y: number) => void;
  setViewport: (width: number, height: number) => void;
  zoomIn: () => void;
  zoomOut: () => void;
  fitToView: () => void;

  // Selection actions
  selectProvince: (id: number | null) => void;
  selectState: (id: number | null) => void;
  selectStrategicRegion: (id: number | null) => void;
  setHoveredProvince: (id: number | null) => void;

  // Tool actions
  setActiveTool: (tool: ToolType) => void;
  setBrushSize: (size: number) => void;
  setBrushShape: (shape: BrushShape) => void;
  setSelectedColor: (color: RGB | null) => void;

  // Layer actions
  toggleLayer: (layer: LayerType) => void;
  setLayerVisibility: (layer: LayerType, visible: boolean) => void;
  toggleGrid: () => void;
  toggleBorders: () => void;

  // Edit actions
  applyBrush: (x: number, y: number) => void;
  applyFill: (x: number, y: number) => void;
  applyLine: (x1: number, y1: number, x2: number, y2: number) => void;
  applyRect: (x1: number, y1: number, x2: number, y2: number) => void;
  pickColor: (x: number, y: number) => void;
  commitChanges: () => void;
  undo: () => boolean;
  redo: () => boolean;

  // Reset
  reset: () => void;
}

const MIN_ZOOM = 0.1;
const MAX_ZOOM = 32;

export const useMapStore = create<MapState>((set, get) => ({
  bmpEditor: null,
  bmpLoaded: false,
  bmpError: null,

  zoom: 1,
  panX: 0,
  panY: 0,
  viewportWidth: 800,
  viewportHeight: 600,

  selectedProvinceId: null,
  selectedStateId: null,
  selectedStrategicRegionId: null,
  hoveredProvinceId: null,

  activeTool: 'select',
  brushSize: 5,
  brushShape: 'circle',
  selectedColor: null,

  layers: {
    provinces: true,
    states: false,
    strategicRegions: false,
    aiAreas: false,
    terrain: false,
  },
  showGrid: false,
  showBorders: true,

  pendingChanges: [],

  loadBMP: (buffer: ArrayBuffer) => {
    try {
      const editor = new BMPEditor(buffer);
      set({
        bmpEditor: editor,
        bmpLoaded: true,
        bmpError: null,
      });
    } catch (error) {
      set({
        bmpEditor: null,
        bmpLoaded: false,
        bmpError: error instanceof Error ? error.message : String(error),
      });
    }
  },

  saveBMP: () => {
    const { bmpEditor } = get();
    if (!bmpEditor) return null;
    return bmpEditor.exportBMP();
  },

  setZoom: (zoom: number) => {
    set({ zoom: Math.max(MIN_ZOOM, Math.min(MAX_ZOOM, zoom)) });
  },

  setPan: (x: number, y: number) => {
    set({ panX: x, panY: y });
  },

  setViewport: (width: number, height: number) => {
    set({ viewportWidth: width, viewportHeight: height });
  },

  zoomIn: () => {
    const { zoom } = get();
    set({ zoom: Math.min(MAX_ZOOM, zoom * 1.5) });
  },

  zoomOut: () => {
    const { zoom } = get();
    set({ zoom: Math.max(MIN_ZOOM, zoom / 1.5) });
  },

  fitToView: () => {
    const { bmpEditor, viewportWidth, viewportHeight } = get();
    if (!bmpEditor) return;

    const scaleX = viewportWidth / bmpEditor.width;
    const scaleY = viewportHeight / bmpEditor.height;
    const scale = Math.min(scaleX, scaleY) * 0.9;

    set({
      zoom: scale,
      panX: (viewportWidth - bmpEditor.width * scale) / 2,
      panY: (viewportHeight - bmpEditor.height * scale) / 2,
    });
  },

  selectProvince: (id: number | null) => {
    set({ selectedProvinceId: id });
  },

  selectState: (id: number | null) => {
    set({ selectedStateId: id });
  },

  selectStrategicRegion: (id: number | null) => {
    set({ selectedStrategicRegionId: id });
  },

  setHoveredProvince: (id: number | null) => {
    set({ hoveredProvinceId: id });
  },

  setActiveTool: (tool: ToolType) => {
    set({ activeTool: tool });
  },

  setBrushSize: (size: number) => {
    set({ brushSize: Math.max(1, Math.min(50, size)) });
  },

  setBrushShape: (shape: BrushShape) => {
    set({ brushShape: shape });
  },

  setSelectedColor: (color: RGB | null) => {
    set({ selectedColor: color });
  },

  toggleLayer: (layer: LayerType) => {
    set((state) => ({
      layers: {
        ...state.layers,
        [layer]: !state.layers[layer],
      },
    }));
  },

  setLayerVisibility: (layer: LayerType, visible: boolean) => {
    set((state) => ({
      layers: {
        ...state.layers,
        [layer]: visible,
      },
    }));
  },

  toggleGrid: () => {
    set((state) => ({ showGrid: !state.showGrid }));
  },

  toggleBorders: () => {
    set((state) => ({ showBorders: !state.showBorders }));
  },

  applyBrush: (x: number, y: number) => {
    const { bmpEditor, selectedColor, brushSize, brushShape } = get();
    if (!bmpEditor || !selectedColor) return;

    const changes = bmpEditor.drawBrush(
      Math.floor(x),
      Math.floor(y),
      selectedColor,
      brushSize,
      brushShape
    );

    if (changes.length > 0) {
      set((state) => ({
        pendingChanges: [...state.pendingChanges, ...changes],
      }));
    }
  },

  applyFill: (x: number, y: number) => {
    const { bmpEditor, selectedColor } = get();
    if (!bmpEditor || !selectedColor) return;

    const changes = bmpEditor.floodFill(
      Math.floor(x),
      Math.floor(y),
      selectedColor
    );

    if (changes.length > 0) {
      bmpEditor.applyChanges(changes);
    }
  },

  applyLine: (x1: number, y1: number, x2: number, y2: number) => {
    const { bmpEditor, selectedColor } = get();
    if (!bmpEditor || !selectedColor) return;

    const changes = bmpEditor.drawLine(
      Math.floor(x1),
      Math.floor(y1),
      Math.floor(x2),
      Math.floor(y2),
      selectedColor
    );

    if (changes.length > 0) {
      bmpEditor.applyChanges(changes);
    }
  },

  applyRect: (x1: number, y1: number, x2: number, y2: number) => {
    const { bmpEditor, selectedColor } = get();
    if (!bmpEditor || !selectedColor) return;

    const changes = bmpEditor.drawFilledRect(
      Math.floor(x1),
      Math.floor(y1),
      Math.floor(x2),
      Math.floor(y2),
      selectedColor
    );

    if (changes.length > 0) {
      bmpEditor.applyChanges(changes);
    }
  },

  pickColor: (x: number, y: number) => {
    const { bmpEditor } = get();
    if (!bmpEditor) return;

    try {
      const color = bmpEditor.getPixel(Math.floor(x), Math.floor(y));
      set({ selectedColor: color });
    } catch {
      // Ignore out of bounds
    }
  },

  commitChanges: () => {
    const { bmpEditor, pendingChanges } = get();
    if (!bmpEditor || pendingChanges.length === 0) return;

    bmpEditor.applyChanges(pendingChanges);
    set({ pendingChanges: [] });
  },

  undo: () => {
    const { bmpEditor } = get();
    if (!bmpEditor) return false;
    return bmpEditor.undo();
  },

  redo: () => {
    const { bmpEditor } = get();
    if (!bmpEditor) return false;
    return bmpEditor.redo();
  },

  reset: () => {
    set({
      bmpEditor: null,
      bmpLoaded: false,
      bmpError: null,
      zoom: 1,
      panX: 0,
      panY: 0,
      selectedProvinceId: null,
      selectedStateId: null,
      selectedStrategicRegionId: null,
      hoveredProvinceId: null,
      activeTool: 'select',
      selectedColor: null,
      pendingChanges: [],
    });
  },
}));
