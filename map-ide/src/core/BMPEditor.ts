import { RGB, PixelChange, EditAction, BoundingBox } from '../types';
import { parseBMP, writeBMP, getPixel, setPixel } from './BMPParser';
import { rgbToKey, rgbEqual } from '../utils/colorUtils';

/**
 * BMP Editor - handles all BMP editing operations
 */
export class BMPEditor {
  private originalData: Uint8Array;
  private currentData: Uint8Array;
  private _width: number;
  private _height: number;
  
  // Color to pixel positions index for fast lookup
  private colorIndex: Map<string, Set<number>>;
  
  // Edit history
  private undoStack: EditAction[] = [];
  private redoStack: EditAction[] = [];
  private maxHistorySize = 100;
  
  // Dirty flag
  private _isDirty = false;

  constructor(bmpBuffer: ArrayBuffer) {
    const bmpData = parseBMP(bmpBuffer);
    this._width = bmpData.width;
    this._height = bmpData.height;
    this.originalData = bmpData.pixels;
    this.currentData = new Uint8Array(this.originalData);
    this.colorIndex = this.buildColorIndex();
  }

  get width(): number {
    return this._width;
  }

  get height(): number {
    return this._height;
  }

  get isDirty(): boolean {
    return this._isDirty;
  }

  get pixels(): Uint8Array {
    return this.currentData;
  }

  /**
   * Build index from color to pixel positions
   */
  private buildColorIndex(): Map<string, Set<number>> {
    const index = new Map<string, Set<number>>();
    
    for (let y = 0; y < this._height; y++) {
      for (let x = 0; x < this._width; x++) {
        const color = this.getPixel(x, y);
        const key = rgbToKey(color);
        
        if (!index.has(key)) {
          index.set(key, new Set());
        }
        index.get(key)!.add(y * this._width + x);
      }
    }
    
    return index;
  }

  /**
   * Update color index for changed pixels
   */
  private updateColorIndex(x: number, y: number, oldColor: RGB, newColor: RGB): void {
    const pos = y * this._width + x;
    const oldKey = rgbToKey(oldColor);
    const newKey = rgbToKey(newColor);

    if (oldKey === newKey) return;

    // Remove from old color set
    const oldSet = this.colorIndex.get(oldKey);
    if (oldSet) {
      oldSet.delete(pos);
      if (oldSet.size === 0) {
        this.colorIndex.delete(oldKey);
      }
    }

    // Add to new color set
    if (!this.colorIndex.has(newKey)) {
      this.colorIndex.set(newKey, new Set());
    }
    this.colorIndex.get(newKey)!.add(pos);
  }

  /**
   * Get pixel at position
   */
  getPixel(x: number, y: number): RGB {
    if (x < 0 || x >= this._width || y < 0 || y >= this._height) {
      throw new Error(`Pixel position out of bounds: (${x}, ${y})`);
    }
    return getPixel(this.currentData, this._width, x, y);
  }

  /**
   * Set pixel at position (without history)
   */
  private setPixelInternal(x: number, y: number, color: RGB): void {
    if (x < 0 || x >= this._width || y < 0 || y >= this._height) return;
    
    const oldColor = this.getPixel(x, y);
    setPixel(this.currentData, this._width, x, y, color);
    this.updateColorIndex(x, y, oldColor, color);
  }

  /**
   * Set pixel with history tracking
   */
  setPixel(x: number, y: number, color: RGB): PixelChange | null {
    if (x < 0 || x >= this._width || y < 0 || y >= this._height) return null;
    
    const oldColor = this.getPixel(x, y);
    if (rgbEqual(oldColor, color)) return null;
    
    this.setPixelInternal(x, y, color);
    this._isDirty = true;
    
    return { x, y, oldColor, newColor: color };
  }

  /**
   * Apply multiple pixel changes and add to history
   */
  applyChanges(changes: PixelChange[]): void {
    if (changes.length === 0) return;

    // Apply changes
    for (const change of changes) {
      this.setPixelInternal(change.x, change.y, change.newColor);
    }

    // Add to history
    this.undoStack.push({
      type: 'pixels',
      changes,
      timestamp: Date.now(),
    });

    // Limit history size
    if (this.undoStack.length > this.maxHistorySize) {
      this.undoStack.shift();
    }

    // Clear redo stack
    this.redoStack = [];
    this._isDirty = true;
  }

  /**
   * Get all pixels with a specific color
   */
  getPixelsByColor(color: RGB): { x: number; y: number }[] {
    const key = rgbToKey(color);
    const positions = this.colorIndex.get(key);
    
    if (!positions) return [];
    
    return Array.from(positions).map(pos => ({
      x: pos % this._width,
      y: Math.floor(pos / this._width),
    }));
  }

  /**
   * Get bounding box of all pixels with a specific color
   */
  getColorBoundingBox(color: RGB): BoundingBox | null {
    const pixels = this.getPixelsByColor(color);
    if (pixels.length === 0) return null;

    let minX = this._width;
    let minY = this._height;
    let maxX = 0;
    let maxY = 0;

    for (const { x, y } of pixels) {
      minX = Math.min(minX, x);
      minY = Math.min(minY, y);
      maxX = Math.max(maxX, x);
      maxY = Math.max(maxY, y);
    }

    return { minX, minY, maxX, maxY };
  }

  /**
   * Get all unique colors in the image
   */
  getUniqueColors(): RGB[] {
    const colors: RGB[] = [];
    for (const key of this.colorIndex.keys()) {
      const [r, g, b] = key.split(',').map(Number);
      colors.push({ r, g, b });
    }
    return colors;
  }

  /**
   * Count pixels of a specific color
   */
  countPixels(color: RGB): number {
    const key = rgbToKey(color);
    return this.colorIndex.get(key)?.size ?? 0;
  }

  /**
   * Flood fill algorithm
   */
  floodFill(startX: number, startY: number, newColor: RGB): PixelChange[] {
    if (startX < 0 || startX >= this._width || startY < 0 || startY >= this._height) {
      return [];
    }

    const targetColor = this.getPixel(startX, startY);
    if (rgbEqual(targetColor, newColor)) {
      return [];
    }

    const changes: PixelChange[] = [];
    const visited = new Set<number>();
    const stack: [number, number][] = [[startX, startY]];

    while (stack.length > 0) {
      const [x, y] = stack.pop()!;
      const pos = y * this._width + x;

      if (visited.has(pos)) continue;
      if (x < 0 || x >= this._width || y < 0 || y >= this._height) continue;

      const currentColor = this.getPixel(x, y);
      if (!rgbEqual(currentColor, targetColor)) continue;

      visited.add(pos);
      changes.push({ x, y, oldColor: currentColor, newColor });

      // Add neighbors
      stack.push([x + 1, y]);
      stack.push([x - 1, y]);
      stack.push([x, y + 1]);
      stack.push([x, y - 1]);
    }

    return changes;
  }

  /**
   * Draw a line using Bresenham's algorithm
   */
  drawLine(x1: number, y1: number, x2: number, y2: number, color: RGB): PixelChange[] {
    const changes: PixelChange[] = [];
    
    const dx = Math.abs(x2 - x1);
    const dy = Math.abs(y2 - y1);
    const sx = x1 < x2 ? 1 : -1;
    const sy = y1 < y2 ? 1 : -1;
    let err = dx - dy;

    let x = x1;
    let y = y1;

    while (true) {
      if (x >= 0 && x < this._width && y >= 0 && y < this._height) {
        const oldColor = this.getPixel(x, y);
        if (!rgbEqual(oldColor, color)) {
          changes.push({ x, y, oldColor, newColor: color });
        }
      }

      if (x === x2 && y === y2) break;

      const e2 = 2 * err;
      if (e2 > -dy) {
        err -= dy;
        x += sx;
      }
      if (e2 < dx) {
        err += dx;
        y += sy;
      }
    }

    return changes;
  }

  /**
   * Draw a filled rectangle
   */
  drawFilledRect(x1: number, y1: number, x2: number, y2: number, color: RGB): PixelChange[] {
    const changes: PixelChange[] = [];
    
    const minX = Math.max(0, Math.min(x1, x2));
    const maxX = Math.min(this._width - 1, Math.max(x1, x2));
    const minY = Math.max(0, Math.min(y1, y2));
    const maxY = Math.min(this._height - 1, Math.max(y1, y2));

    for (let y = minY; y <= maxY; y++) {
      for (let x = minX; x <= maxX; x++) {
        const oldColor = this.getPixel(x, y);
        if (!rgbEqual(oldColor, color)) {
          changes.push({ x, y, oldColor, newColor: color });
        }
      }
    }

    return changes;
  }

  /**
   * Draw with brush
   */
  drawBrush(
    centerX: number,
    centerY: number,
    color: RGB,
    size: number,
    shape: 'circle' | 'square'
  ): PixelChange[] {
    const changes: PixelChange[] = [];
    const radius = Math.floor(size / 2);

    for (let dy = -radius; dy <= radius; dy++) {
      for (let dx = -radius; dx <= radius; dx++) {
        const x = centerX + dx;
        const y = centerY + dy;

        if (x < 0 || x >= this._width || y < 0 || y >= this._height) continue;

        // Check if within brush shape
        let inBrush = false;
        if (shape === 'square') {
          inBrush = true;
        } else {
          // Circle: check distance from center
          const dist = Math.sqrt(dx * dx + dy * dy);
          inBrush = dist <= radius;
        }

        if (inBrush) {
          const oldColor = this.getPixel(x, y);
          if (!rgbEqual(oldColor, color)) {
            changes.push({ x, y, oldColor, newColor: color });
          }
        }
      }
    }

    return changes;
  }

  /**
   * Undo last action
   */
  undo(): boolean {
    const action = this.undoStack.pop();
    if (!action) return false;

    // Reverse changes
    for (const change of action.changes) {
      this.setPixelInternal(change.x, change.y, change.oldColor);
    }

    // Add to redo stack
    this.redoStack.push(action);
    this._isDirty = this.undoStack.length > 0;

    return true;
  }

  /**
   * Redo last undone action
   */
  redo(): boolean {
    const action = this.redoStack.pop();
    if (!action) return false;

    // Reapply changes
    for (const change of action.changes) {
      this.setPixelInternal(change.x, change.y, change.newColor);
    }

    // Add to undo stack
    this.undoStack.push(action);
    this._isDirty = true;

    return true;
  }

  /**
   * Check if undo is available
   */
  canUndo(): boolean {
    return this.undoStack.length > 0;
  }

  /**
   * Check if redo is available
   */
  canRedo(): boolean {
    return this.redoStack.length > 0;
  }

  /**
   * Reset to original data
   */
  reset(): void {
    this.currentData = new Uint8Array(this.originalData);
    this.colorIndex = this.buildColorIndex();
    this.undoStack = [];
    this.redoStack = [];
    this._isDirty = false;
  }

  /**
   * Mark current state as saved
   */
  markSaved(): void {
    this._isDirty = false;
    this.originalData = new Uint8Array(this.currentData);
  }

  /**
   * Export as BMP buffer
   */
  exportBMP(): ArrayBuffer {
    return writeBMP(this._width, this._height, this.currentData);
  }
}
