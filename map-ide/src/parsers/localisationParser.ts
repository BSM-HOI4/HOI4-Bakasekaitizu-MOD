/**
 * HoI4 Localisation Parser
 * Parses .yml localisation files and extracts key-value pairs
 * Handles STATE_X, STRATEGICREGION_X format
 */

export interface LocalisationData {
  states: Map<number, string>;       // STATE_X -> name
  strategicRegions: Map<number, string>; // STRATEGICREGION_X -> name
  countries: Map<string, string>;    // TAG -> name
  other: Map<string, string>;        // other keys
}

/**
 * Parse a single localisation file content
 */
export function parseLocalisationFile(content: string): Map<string, string> {
  const result = new Map<string, string>();
  const lines = content.split('\n');
  
  // Skip BOM and first line (l_japanese: or l_english:)
  let startIndex = 0;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (line.startsWith('l_') && line.endsWith(':')) {
      startIndex = i + 1;
      break;
    }
  }
  
  for (let i = startIndex; i < lines.length; i++) {
    const line = lines[i];
    
    // Skip empty lines and comments
    if (!line.trim() || line.trim().startsWith('#')) continue;
    
    // Parse key:version "value" or key: "value"
    // Examples:
    // STATE_183: "南キプロス"
    // STRATEGICREGION_1:0 "イングランド南部"
    const match = line.match(/^\s*([A-Za-z0-9_]+):(?:\d+)?\s*"(.*)"\s*$/);
    if (match) {
      const [, key, value] = match;
      result.set(key, value);
    }
  }
  
  return result;
}

/**
 * Extract state names from parsed localisation data
 */
export function extractStateNames(data: Map<string, string>): Map<number, string> {
  const states = new Map<number, string>();
  
  for (const [key, value] of data) {
    const match = key.match(/^STATE_(\d+)$/);
    if (match) {
      const stateId = parseInt(match[1], 10);
      states.set(stateId, value);
    }
  }
  
  return states;
}

/**
 * Extract strategic region names from parsed localisation data
 */
export function extractStrategicRegionNames(data: Map<string, string>): Map<number, string> {
  const regions = new Map<number, string>();
  
  for (const [key, value] of data) {
    const match = key.match(/^STRATEGICREGION_(\d+)$/);
    if (match) {
      const regionId = parseInt(match[1], 10);
      regions.set(regionId, value);
    }
  }
  
  return regions;
}

/**
 * Load all localisation files from a directory
 * @param readDir Function to read directory contents
 * @param readFile Function to read file content
 * @param basePath Base localisation path (e.g., /mod/localisation/japanese)
 */
export async function loadAllLocalisations(
  readDir: (path: string) => Promise<{ success: boolean; data?: { name: string; isDirectory: boolean; isFile: boolean }[] }>,
  readFile: (path: string) => Promise<{ success: boolean; data?: string }>,
  basePath: string
): Promise<LocalisationData> {
  const result: LocalisationData = {
    states: new Map(),
    strategicRegions: new Map(),
    countries: new Map(),
    other: new Map(),
  };
  
  // Recursive function to scan directories
  async function scanDirectory(dirPath: string): Promise<void> {
    const dirResult = await readDir(dirPath);
    if (!dirResult.success || !dirResult.data) return;
    
    for (const entry of dirResult.data) {
      const fullPath = `${dirPath}/${entry.name}`;
      
      if (entry.isDirectory) {
        await scanDirectory(fullPath);
      } else if (entry.isFile && entry.name.endsWith('.yml')) {
        const fileResult = await readFile(fullPath);
        if (fileResult.success && fileResult.data) {
          const parsed = parseLocalisationFile(fileResult.data);
          
          // Extract specific data types
          const stateNames = extractStateNames(parsed);
          const regionNames = extractStrategicRegionNames(parsed);
          
          // Merge into result
          for (const [id, name] of stateNames) {
            result.states.set(id, name);
          }
          for (const [id, name] of regionNames) {
            result.strategicRegions.set(id, name);
          }
          
          // Store other keys
          for (const [key, value] of parsed) {
            if (!key.match(/^STATE_\d+$/) && !key.match(/^STRATEGICREGION_\d+$/)) {
              result.other.set(key, value);
            }
          }
        }
      }
    }
  }
  
  await scanDirectory(basePath);
  return result;
}

/**
 * Get state name from localisation data, fallback to ID
 */
export function getStateName(locData: LocalisationData | null, stateId: number): string {
  if (locData && locData.states.has(stateId)) {
    return locData.states.get(stateId)!;
  }
  return `State ${stateId}`;
}

/**
 * Get strategic region name from localisation data, fallback to ID
 */
export function getStrategicRegionName(locData: LocalisationData | null, regionId: number): string {
  if (locData && locData.strategicRegions.has(regionId)) {
    return locData.strategicRegions.get(regionId)!;
  }
  return `Strategic Region ${regionId}`;
}
