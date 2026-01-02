import { Province, ProvinceType, TerrainType, Adjacency } from '../types';

/**
 * Parse definition.csv file
 * Format: id;r;g;b;type;coastal;terrain;continent
 */
export function parseDefinitionCSV(content: string): Province[] {
  const lines = content.split('\n');
  const provinces: Province[] = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line || line.startsWith('#')) continue;

    const parts = line.split(';');
    if (parts.length < 8) continue;

    const id = parseInt(parts[0], 10);
    if (isNaN(id) || id === 0) continue; // Skip invalid or ID 0

    const r = parseInt(parts[1], 10);
    const g = parseInt(parts[2], 10);
    const b = parseInt(parts[3], 10);
    
    if (isNaN(r) || isNaN(g) || isNaN(b)) continue;

    const typeStr = parts[4].toLowerCase();
    let type: ProvinceType = 'land';
    if (typeStr === 'sea') type = 'sea';
    else if (typeStr === 'lake') type = 'lake';

    const coastal = parts[5].toLowerCase() === 'true';
    
    const terrainStr = parts[6].toLowerCase();
    const terrain = parseTerrainType(terrainStr);
    
    const continent = parseInt(parts[7], 10) || 0;

    provinces.push({
      id,
      color: { r, g, b },
      type,
      coastal,
      terrain,
      continent,
    });
  }

  return provinces;
}

/**
 * Parse terrain string to TerrainType
 */
function parseTerrainType(terrain: string): TerrainType {
  const mapping: Record<string, TerrainType> = {
    'ocean': 'ocean',
    'lakes': 'lakes',
    'forest': 'forest',
    'hills': 'hills',
    'mountain': 'mountain',
    'plains': 'plains',
    'urban': 'urban',
    'jungle': 'jungle',
    'marsh': 'marsh',
    'desert': 'desert',
  };
  return mapping[terrain] || 'unknown';
}

/**
 * Serialize provinces to definition.csv format
 */
export function serializeDefinitionCSV(provinces: Province[]): string {
  const lines: string[] = [];
  
  // Sort by ID
  const sorted = [...provinces].sort((a, b) => a.id - b.id);
  
  for (const prov of sorted) {
    const line = [
      prov.id,
      prov.color.r,
      prov.color.g,
      prov.color.b,
      prov.type,
      prov.coastal ? 'true' : 'false',
      prov.terrain,
      prov.continent,
    ].join(';');
    
    lines.push(line);
  }

  return lines.join('\n');
}

/**
 * Parse adjacencies.csv file
 * Format: From;To;Type;Through;start_x;start_y;stop_x;stop_y;adjacency_rule_name;Comment
 */
export function parseAdjacenciesCSV(content: string): Adjacency[] {
  const lines = content.split('\n');
  const adjacencies: Adjacency[] = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    
    // Skip header and empty lines
    if (!line || line.startsWith('From') || line.startsWith('#')) continue;

    // Handle BOM
    const cleanLine = line.replace(/^\uFEFF/, '');
    const parts = cleanLine.split(';');
    
    if (parts.length < 10) continue;

    const from = parseInt(parts[0], 10);
    const to = parseInt(parts[1], 10);
    
    if (isNaN(from) || isNaN(to)) continue;

    adjacencies.push({
      from,
      to,
      type: parts[2] === 'sea' ? 'sea' : '',
      through: parseInt(parts[3], 10) || 0,
      startX: parseInt(parts[4], 10) || -1,
      startY: parseInt(parts[5], 10) || -1,
      stopX: parseInt(parts[6], 10) || -1,
      stopY: parseInt(parts[7], 10) || -1,
      ruleName: parts[8] || '',
      comment: parts[9] || '',
    });
  }

  return adjacencies;
}

/**
 * Serialize adjacencies to CSV format
 */
export function serializeAdjacenciesCSV(adjacencies: Adjacency[]): string {
  const lines: string[] = [
    'From;To;Type;Through;start_x;start_y;stop_x;stop_y;adjacency_rule_name;Comment',
  ];

  for (const adj of adjacencies) {
    const line = [
      adj.from,
      adj.to,
      adj.type,
      adj.through || '',
      adj.startX,
      adj.startY,
      adj.stopX,
      adj.stopY,
      adj.ruleName,
      adj.comment,
    ].join(';');
    
    lines.push(line);
  }

  return lines.join('\n');
}

/**
 * Create province lookup maps
 */
export function createProvinceMaps(provinces: Province[]): {
  byId: Map<number, Province>;
  byColor: Map<string, Province>;
} {
  const byId = new Map<number, Province>();
  const byColor = new Map<string, Province>();

  for (const prov of provinces) {
    byId.set(prov.id, prov);
    const colorKey = `${prov.color.r},${prov.color.g},${prov.color.b}`;
    byColor.set(colorKey, prov);
  }

  return { byId, byColor };
}
