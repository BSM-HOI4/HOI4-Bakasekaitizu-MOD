/**
 * Layer Color Generation Utilities
 * Generates distinct colors for States, Strategic Regions, and AI Areas
 * Uses graph coloring approach to ensure adjacent regions have different colors
 */

import { RGB } from '../types';
import { State, StrategicRegion, AIArea, Province } from '../types';

/**
 * Predefined color palette with high contrast colors
 * These colors are designed to be easily distinguishable
 */
const COLOR_PALETTE: RGB[] = [
  { r: 230, g: 25, b: 75 },    // Red
  { r: 60, g: 180, b: 75 },    // Green
  { r: 255, g: 225, b: 25 },   // Yellow
  { r: 0, g: 130, b: 200 },    // Blue
  { r: 245, g: 130, b: 48 },   // Orange
  { r: 145, g: 30, b: 180 },   // Purple
  { r: 70, g: 240, b: 240 },   // Cyan
  { r: 240, g: 50, b: 230 },   // Magenta
  { r: 210, g: 245, b: 60 },   // Lime
  { r: 250, g: 190, b: 212 },  // Pink
  { r: 0, g: 128, b: 128 },    // Teal
  { r: 220, g: 190, b: 255 },  // Lavender
  { r: 170, g: 110, b: 40 },   // Brown
  { r: 255, g: 250, b: 200 },  // Beige
  { r: 128, g: 0, b: 0 },      // Maroon
  { r: 170, g: 255, b: 195 },  // Mint
  { r: 128, g: 128, b: 0 },    // Olive
  { r: 255, g: 215, b: 180 },  // Apricot
  { r: 0, g: 0, b: 128 },      // Navy
  { r: 128, g: 128, b: 128 },  // Grey
  { r: 255, g: 99, b: 71 },    // Tomato
  { r: 50, g: 205, b: 50 },    // Lime Green
  { r: 255, g: 165, b: 0 },    // Orange
  { r: 138, g: 43, b: 226 },   // Blue Violet
  { r: 0, g: 191, b: 255 },    // Deep Sky Blue
  { r: 255, g: 20, b: 147 },   // Deep Pink
  { r: 0, g: 250, b: 154 },    // Medium Spring Green
  { r: 218, g: 112, b: 214 },  // Orchid
  { r: 173, g: 216, b: 230 },  // Light Blue
  { r: 144, g: 238, b: 144 },  // Light Green
];

/**
 * Generate a color from HSL values
 */
function hslToRgb(h: number, s: number, l: number): RGB {
  let r: number, g: number, b: number;

  if (s === 0) {
    r = g = b = l;
  } else {
    const hue2rgb = (p: number, q: number, t: number) => {
      if (t < 0) t += 1;
      if (t > 1) t -= 1;
      if (t < 1/6) return p + (q - p) * 6 * t;
      if (t < 1/2) return q;
      if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
      return p;
    };

    const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    const p = 2 * l - q;
    r = hue2rgb(p, q, h + 1/3);
    g = hue2rgb(p, q, h);
    b = hue2rgb(p, q, h - 1/3);
  }

  return {
    r: Math.round(r * 255),
    g: Math.round(g * 255),
    b: Math.round(b * 255),
  };
}

/**
 * Generate evenly distributed colors using golden ratio
 */
function generateDistinctColors(count: number): RGB[] {
  const colors: RGB[] = [];
  const goldenRatio = 0.618033988749895;
  let hue = Math.random();
  
  for (let i = 0; i < count; i++) {
    hue = (hue + goldenRatio) % 1;
    // Use high saturation and varying lightness for visibility
    const saturation = 0.65 + Math.random() * 0.2;
    const lightness = 0.45 + Math.random() * 0.15;
    colors.push(hslToRgb(hue, saturation, lightness));
  }
  
  return colors;
}

/**
 * Build adjacency graph for states based on province neighbors
 */
export function buildStateAdjacency(
  states: Map<number, State>,
  _provinces: Map<number, Province>,
  provincePixelData: Uint8Array,
  mapWidth: number,
  mapHeight: number,
  provinceByColor: Map<string, Province>
): Map<number, Set<number>> {
  const adjacency = new Map<number, Set<number>>();
  
  // Initialize adjacency sets
  for (const stateId of states.keys()) {
    adjacency.set(stateId, new Set());
  }
  
  // Build province to state mapping
  const provinceToState = new Map<number, number>();
  for (const [stateId, state] of states) {
    for (const provId of state.provinces) {
      provinceToState.set(provId, stateId);
    }
  }
  
  // Scan pixels to find adjacent provinces
  const step = Math.max(1, Math.floor(mapWidth / 512)); // Sample for performance
  
  for (let y = 0; y < mapHeight - 1; y += step) {
    for (let x = 0; x < mapWidth - 1; x += step) {
      const idx = (y * mapWidth + x) * 3;
      const r1 = provincePixelData[idx];
      const g1 = provincePixelData[idx + 1];
      const b1 = provincePixelData[idx + 2];
      const key1 = `${r1},${g1},${b1}`;
      
      // Check right neighbor
      const idx2 = (y * mapWidth + x + 1) * 3;
      const r2 = provincePixelData[idx2];
      const g2 = provincePixelData[idx2 + 1];
      const b2 = provincePixelData[idx2 + 2];
      const key2 = `${r2},${g2},${b2}`;
      
      // Check bottom neighbor
      const idx3 = ((y + 1) * mapWidth + x) * 3;
      const r3 = provincePixelData[idx3];
      const g3 = provincePixelData[idx3 + 1];
      const b3 = provincePixelData[idx3 + 2];
      const key3 = `${r3},${g3},${b3}`;
      
      const prov1 = provinceByColor.get(key1);
      const prov2 = provinceByColor.get(key2);
      const prov3 = provinceByColor.get(key3);
      
      if (prov1 && prov2 && prov1.id !== prov2.id) {
        const state1 = provinceToState.get(prov1.id);
        const state2 = provinceToState.get(prov2.id);
        if (state1 !== undefined && state2 !== undefined && state1 !== state2) {
          adjacency.get(state1)?.add(state2);
          adjacency.get(state2)?.add(state1);
        }
      }
      
      if (prov1 && prov3 && prov1.id !== prov3.id) {
        const state1 = provinceToState.get(prov1.id);
        const state3 = provinceToState.get(prov3.id);
        if (state1 !== undefined && state3 !== undefined && state1 !== state3) {
          adjacency.get(state1)?.add(state3);
          adjacency.get(state3)?.add(state1);
        }
      }
    }
  }
  
  return adjacency;
}

/**
 * Graph coloring using greedy algorithm
 * Assigns colors to nodes such that no two adjacent nodes have the same color
 */
export function graphColoring<T>(
  nodes: T[],
  adjacency: Map<T, Set<T>>,
  colors: RGB[]
): Map<T, RGB> {
  const result = new Map<T, RGB>();
  const nodeColors = new Map<T, number>();
  
  // Sort nodes by degree (number of neighbors) - color high-degree nodes first
  const sortedNodes = [...nodes].sort((a, b) => {
    const degA = adjacency.get(a)?.size ?? 0;
    const degB = adjacency.get(b)?.size ?? 0;
    return degB - degA;
  });
  
  for (const node of sortedNodes) {
    const neighbors = adjacency.get(node) ?? new Set();
    const usedColors = new Set<number>();
    
    // Find colors used by neighbors
    for (const neighbor of neighbors) {
      const neighborColor = nodeColors.get(neighbor);
      if (neighborColor !== undefined) {
        usedColors.add(neighborColor);
      }
    }
    
    // Find first available color
    let colorIndex = 0;
    while (usedColors.has(colorIndex)) {
      colorIndex++;
    }
    
    // If we run out of predefined colors, generate new one
    if (colorIndex >= colors.length) {
      const newColors = generateDistinctColors(colorIndex - colors.length + 10);
      colors.push(...newColors);
    }
    
    nodeColors.set(node, colorIndex);
    result.set(node, colors[colorIndex]);
  }
  
  return result;
}

/**
 * Generate colors for states with graph coloring
 */
export function generateStateColors(
  states: Map<number, State>,
  adjacency: Map<number, Set<number>>
): Map<number, RGB> {
  const stateIds = Array.from(states.keys());
  return graphColoring(stateIds, adjacency, [...COLOR_PALETTE]);
}

/**
 * Build adjacency graph for strategic regions directly from pixel data
 * Used when state data is not available
 */
export function buildStrategicRegionAdjacencyDirect(
  regions: Map<number, StrategicRegion>,
  _provinces: Map<number, Province>,
  provincePixelData: Uint8Array,
  mapWidth: number,
  mapHeight: number,
  provinceByColor: Map<string, Province>
): Map<number, Set<number>> {
  const adjacency = new Map<number, Set<number>>();
  
  // Initialize adjacency sets
  for (const regionId of regions.keys()) {
    adjacency.set(regionId, new Set());
  }
  
  // Build province to region mapping
  const provinceToRegion = new Map<number, number>();
  for (const [regionId, region] of regions) {
    for (const provId of region.provinces) {
      provinceToRegion.set(provId, regionId);
    }
  }
  
  // Scan pixels to find adjacent provinces
  const step = Math.max(1, Math.floor(mapWidth / 512));
  
  for (let y = 0; y < mapHeight - 1; y += step) {
    for (let x = 0; x < mapWidth - 1; x += step) {
      const idx = (y * mapWidth + x) * 3;
      const r1 = provincePixelData[idx];
      const g1 = provincePixelData[idx + 1];
      const b1 = provincePixelData[idx + 2];
      const key1 = `${r1},${g1},${b1}`;
      
      // Check right neighbor
      const idx2 = (y * mapWidth + x + 1) * 3;
      const r2 = provincePixelData[idx2];
      const g2 = provincePixelData[idx2 + 1];
      const b2 = provincePixelData[idx2 + 2];
      const key2 = `${r2},${g2},${b2}`;
      
      // Check bottom neighbor
      const idx3 = ((y + 1) * mapWidth + x) * 3;
      const r3 = provincePixelData[idx3];
      const g3 = provincePixelData[idx3 + 1];
      const b3 = provincePixelData[idx3 + 2];
      const key3 = `${r3},${g3},${b3}`;
      
      const prov1 = provinceByColor.get(key1);
      const prov2 = provinceByColor.get(key2);
      const prov3 = provinceByColor.get(key3);
      
      if (prov1 && prov2 && prov1.id !== prov2.id) {
        const region1 = provinceToRegion.get(prov1.id);
        const region2 = provinceToRegion.get(prov2.id);
        if (region1 !== undefined && region2 !== undefined && region1 !== region2) {
          adjacency.get(region1)?.add(region2);
          adjacency.get(region2)?.add(region1);
        }
      }
      
      if (prov1 && prov3 && prov1.id !== prov3.id) {
        const region1 = provinceToRegion.get(prov1.id);
        const region3 = provinceToRegion.get(prov3.id);
        if (region1 !== undefined && region3 !== undefined && region1 !== region3) {
          adjacency.get(region1)?.add(region3);
          adjacency.get(region3)?.add(region1);
        }
      }
    }
  }
  
  return adjacency;
}

/**
 * Build adjacency graph for strategic regions
 */
export function buildStrategicRegionAdjacency(
  regions: Map<number, StrategicRegion>,
  states: Map<number, State>,
  stateAdjacency: Map<number, Set<number>>
): Map<number, Set<number>> {
  const adjacency = new Map<number, Set<number>>();
  
  // Initialize
  for (const regionId of regions.keys()) {
    adjacency.set(regionId, new Set());
  }
  
  // Build province to region mapping
  const provinceToRegion = new Map<number, number>();
  for (const [regionId, region] of regions) {
    for (const provId of region.provinces) {
      provinceToRegion.set(provId, regionId);
    }
  }
  
  // Use state adjacency to determine region adjacency
  for (const [stateId, state] of states) {
    const adjacentStates = stateAdjacency.get(stateId) ?? new Set();
    
    // Find region of this state's provinces
    const stateRegions = new Set<number>();
    for (const provId of state.provinces) {
      const regionId = provinceToRegion.get(provId);
      if (regionId !== undefined) stateRegions.add(regionId);
    }
    
    // Find regions of adjacent states
    for (const adjStateId of adjacentStates) {
      const adjState = states.get(adjStateId);
      if (!adjState) continue;
      
      for (const provId of adjState.provinces) {
        const adjRegionId = provinceToRegion.get(provId);
        if (adjRegionId !== undefined) {
          for (const regionId of stateRegions) {
            if (regionId !== adjRegionId) {
              adjacency.get(regionId)?.add(adjRegionId);
              adjacency.get(adjRegionId)?.add(regionId);
            }
          }
        }
      }
    }
  }
  
  return adjacency;
}

/**
 * Generate colors for strategic regions
 */
export function generateStrategicRegionColors(
  regions: Map<number, StrategicRegion>,
  adjacency: Map<number, Set<number>>
): Map<number, RGB> {
  const regionIds = Array.from(regions.keys());
  return graphColoring(regionIds, adjacency, [...COLOR_PALETTE]);
}

/**
 * Build adjacency graph for AI areas
 */
export function buildAIAreaAdjacency(
  aiAreas: AIArea[],
  regionAdjacency: Map<number, Set<number>>
): Map<string, Set<string>> {
  const adjacency = new Map<string, Set<string>>();
  
  // Initialize
  for (const area of aiAreas) {
    adjacency.set(area.name, new Set());
  }
  
  // Build region to area mapping
  const regionToArea = new Map<number, string>();
  for (const area of aiAreas) {
    if (area.strategicRegions) {
      for (const regionId of area.strategicRegions) {
        regionToArea.set(regionId, area.name);
      }
    }
  }
  
  // Use region adjacency to determine area adjacency
  for (const [regionId, adjacentRegions] of regionAdjacency) {
    const areaName = regionToArea.get(regionId);
    if (!areaName) continue;
    
    for (const adjRegionId of adjacentRegions) {
      const adjAreaName = regionToArea.get(adjRegionId);
      if (adjAreaName && adjAreaName !== areaName) {
        adjacency.get(areaName)?.add(adjAreaName);
        adjacency.get(adjAreaName)?.add(areaName);
      }
    }
  }
  
  return adjacency;
}

/**
 * Generate colors for AI areas
 */
export function generateAIAreaColors(
  aiAreas: AIArea[],
  adjacency: Map<string, Set<string>>
): Map<string, RGB> {
  const areaNames = aiAreas.map(a => a.name);
  return graphColoring(areaNames, adjacency, [...COLOR_PALETTE]);
}

/**
 * Create overlay texture for a layer
 * Returns RGBA data with layer colors applied to provinces
 */
export function createLayerOverlay(
  width: number,
  height: number,
  provincePixelData: Uint8Array,
  provinceByColor: Map<string, Province>,
  provinceToEntity: Map<number, number | string>,
  entityColors: Map<number | string, RGB>,
  opacity: number = 0.7
): Uint8Array {
  const rgba = new Uint8Array(width * height * 4);
  const alpha = Math.round(opacity * 255);
  
  let coloredPixels = 0;
  let unmappedProvinces = 0;
  let noEntityMapping = 0;
  
  for (let i = 0; i < width * height; i++) {
    const r = provincePixelData[i * 3];
    const g = provincePixelData[i * 3 + 1];
    const b = provincePixelData[i * 3 + 2];
    const key = `${r},${g},${b}`;
    
    const province = provinceByColor.get(key);
    if (province) {
      const entityId = provinceToEntity.get(province.id);
      if (entityId !== undefined) {
        const color = entityColors.get(entityId);
        if (color) {
          rgba[i * 4] = color.r;
          rgba[i * 4 + 1] = color.g;
          rgba[i * 4 + 2] = color.b;
          rgba[i * 4 + 3] = alpha;
          coloredPixels++;
          continue;
        }
      } else {
        noEntityMapping++;
      }
    } else {
      unmappedProvinces++;
    }
    
    // Transparent if no mapping
    rgba[i * 4 + 3] = 0;
  }
  
  console.log('[createLayerOverlay] Stats:', {
    totalPixels: width * height,
    coloredPixels,
    unmappedProvinces,
    noEntityMapping,
    provinceByColorSize: provinceByColor.size,
    provinceToEntitySize: provinceToEntity.size,
    entityColorsSize: entityColors.size,
  });
  
  return rgba;
}
