import { create } from 'zustand';
import { Project, Province, State, StrategicRegion, AIArea, Adjacency } from '../types';
import { parseDefinitionCSV, parseAdjacenciesCSV, createProvinceMaps } from '../parsers/csvParser';
import { parseParadoxScript, ASTNode } from '../parsers/paradox/parser';

interface ProjectState {
  // Project info
  project: Project | null;
  isLoading: boolean;
  error: string | null;

  // Provinces
  provinces: Province[];
  provinceById: Map<number, Province>;
  provinceByColor: Map<string, Province>;

  // States
  states: State[];
  stateById: Map<number, State>;

  // Strategic Regions
  strategicRegions: StrategicRegion[];
  strategicRegionById: Map<number, StrategicRegion>;

  // AI Areas
  aiAreas: AIArea[];

  // Adjacencies
  adjacencies: Adjacency[];

  // Actions
  openProject: (rootPath: string) => Promise<void>;
  closeProject: () => void;
  reloadProject: () => Promise<void>;
}

export const useProjectStore = create<ProjectState>((set, get) => ({
  project: null,
  isLoading: false,
  error: null,

  provinces: [],
  provinceById: new Map(),
  provinceByColor: new Map(),

  states: [],
  stateById: new Map(),

  strategicRegions: [],
  strategicRegionById: new Map(),

  aiAreas: [],

  adjacencies: [],

  openProject: async (rootPath: string) => {
    set({ isLoading: true, error: null });

    try {
      const api = window.electronAPI;
      
      // Detect project structure
      const mapPath = `${rootPath}/map`;
      const commonPath = `${rootPath}/common`;
      const historyPath = `${rootPath}/history`;

      // Check required directories exist
      const mapExists = await api.exists(mapPath);
      if (!mapExists) {
        throw new Error('map/ directory not found');
      }

      // Load definition.csv
      const definitionResult = await api.readTextFile(`${mapPath}/definition.csv`);
      if (!definitionResult.success) {
        throw new Error('Failed to load definition.csv');
      }
      const provinces = parseDefinitionCSV(definitionResult.data!);
      const { byId: provinceById, byColor: provinceByColor } = createProvinceMaps(provinces);

      // Load adjacencies.csv
      let adjacencies: Adjacency[] = [];
      const adjResult = await api.readTextFile(`${mapPath}/adjacencies.csv`);
      if (adjResult.success) {
        adjacencies = parseAdjacenciesCSV(adjResult.data!);
      }

      // Load states from history/states/
      const states: State[] = [];
      const stateById = new Map<number, State>();
      const statesDir = `${historyPath}/states`;
      
      if (await api.exists(statesDir)) {
        const stateFiles = await api.readDir(statesDir);
        if (stateFiles.success) {
          for (const file of stateFiles.data!) {
            if (file.isFile && file.name.endsWith('.txt')) {
              const filePath = `${statesDir}/${file.name}`;
              const content = await api.readTextFile(filePath);
              if (content.success) {
                try {
                  const ast = parseParadoxScript(content.data!);
                  const state = parseStateFromAST(ast, filePath);
                  if (state) {
                    states.push(state);
                    stateById.set(state.id, state);
                    
                    // Link provinces to state
                    for (const provId of state.provinces) {
                      const prov = provinceById.get(provId);
                      if (prov) {
                        prov.stateId = state.id;
                      }
                    }
                  }
                } catch (e) {
                  console.warn(`Failed to parse state file ${file.name}:`, e);
                }
              }
            }
          }
        }
      }

      // Load strategic regions
      const strategicRegions: StrategicRegion[] = [];
      const strategicRegionById = new Map<number, StrategicRegion>();
      const regionsDir = `${mapPath}/strategicregions`;
      
      if (await api.exists(regionsDir)) {
        const regionFiles = await api.readDir(regionsDir);
        if (regionFiles.success) {
          for (const file of regionFiles.data!) {
            if (file.isFile && file.name.endsWith('.txt')) {
              const filePath = `${regionsDir}/${file.name}`;
              const content = await api.readTextFile(filePath);
              if (content.success) {
                try {
                  const ast = parseParadoxScript(content.data!);
                  const region = parseStrategicRegionFromAST(ast, filePath);
                  if (region) {
                    strategicRegions.push(region);
                    strategicRegionById.set(region.id, region);
                    
                    // Link provinces to strategic region
                    for (const provId of region.provinces) {
                      const prov = provinceById.get(provId);
                      if (prov) {
                        prov.strategicRegionId = region.id;
                      }
                    }
                  }
                } catch (e) {
                  console.warn(`Failed to parse strategic region ${file.name}:`, e);
                }
              }
            }
          }
        }
      }

      // Load AI areas
      const aiAreas: AIArea[] = [];
      const aiAreasPath = `${commonPath}/ai_areas`;
      
      if (await api.exists(aiAreasPath)) {
        const aiFiles = await api.readDir(aiAreasPath);
        if (aiFiles.success) {
          for (const file of aiFiles.data!) {
            if (file.isFile && file.name.endsWith('.txt')) {
              const content = await api.readTextFile(`${aiAreasPath}/${file.name}`);
              if (content.success) {
                try {
                  const ast = parseParadoxScript(content.data!);
                  const areas = parseAIAreasFromAST(ast);
                  aiAreas.push(...areas);
                } catch (e) {
                  console.warn(`Failed to parse AI areas ${file.name}:`, e);
                }
              }
            }
          }
        }
      }

      // Update state
      set({
        project: {
          rootPath,
          mapPath,
          commonPath,
          historyPath,
          loaded: true,
        },
        provinces,
        provinceById,
        provinceByColor,
        states,
        stateById,
        strategicRegions,
        strategicRegionById,
        aiAreas,
        adjacencies,
        isLoading: false,
        error: null,
      });
    } catch (error) {
      set({
        isLoading: false,
        error: error instanceof Error ? error.message : String(error),
      });
    }
  },

  closeProject: () => {
    set({
      project: null,
      provinces: [],
      provinceById: new Map(),
      provinceByColor: new Map(),
      states: [],
      stateById: new Map(),
      strategicRegions: [],
      strategicRegionById: new Map(),
      aiAreas: [],
      adjacencies: [],
      error: null,
    });
  },

  reloadProject: async () => {
    const { project } = get();
    if (project) {
      await get().openProject(project.rootPath);
    }
  },
}));

// Helper functions to parse AST to domain objects

function parseStateFromAST(ast: ASTNode, filePath: string): State | null {
  const stateNode = ast.state as ASTNode | undefined;
  if (!stateNode) return null;

  const id = stateNode.id as number;
  if (!id) return null;

  const history = stateNode.history as ASTNode | undefined;
  
  return {
    id,
    name: (stateNode.name as string) || `STATE_${id}`,
    manpower: (stateNode.manpower as number) || 0,
    stateCategory: (stateNode.state_category as string) || 'wasteland',
    owner: history?.owner as string || '',
    cores: extractCores(history),
    claims: extractClaims(history),
    provinces: extractProvinces(stateNode.provinces),
    buildings: extractBuildings(history),
    victoryPoints: extractVictoryPoints(history),
    localSupplies: (stateNode.local_supplies as number) || 0,
    filePath,
  };
}

function extractProvinces(value: unknown): number[] {
  if (Array.isArray(value)) {
    return value.filter(v => typeof v === 'number') as number[];
  }
  return [];
}

function extractCores(history: ASTNode | undefined): string[] {
  if (!history) return [];
  const cores: string[] = [];
  const addCore = history.add_core_of;
  if (typeof addCore === 'string') {
    cores.push(addCore);
  } else if (Array.isArray(addCore)) {
    cores.push(...addCore.filter(c => typeof c === 'string') as string[]);
  }
  return cores;
}

function extractClaims(history: ASTNode | undefined): string[] {
  if (!history) return [];
  const claims: string[] = [];
  const addClaim = history.add_claim_by;
  if (typeof addClaim === 'string') {
    claims.push(addClaim);
  } else if (Array.isArray(addClaim)) {
    claims.push(...addClaim.filter(c => typeof c === 'string') as string[]);
  }
  return claims;
}

function extractBuildings(history: ASTNode | undefined): { type: string; level: number; provinceId?: number }[] {
  if (!history?.buildings) return [];
  const buildings: { type: string; level: number; provinceId?: number }[] = [];
  const buildingsNode = history.buildings as ASTNode;
  
  for (const [key, value] of Object.entries(buildingsNode)) {
    if (typeof value === 'number') {
      buildings.push({ type: key, level: value });
    } else if (typeof value === 'object' && !Array.isArray(value)) {
      // Province-specific building
      const provinceId = parseInt(key, 10);
      if (!isNaN(provinceId)) {
        for (const [bType, bLevel] of Object.entries(value as ASTNode)) {
          if (typeof bLevel === 'number') {
            buildings.push({ type: bType, level: bLevel, provinceId });
          }
        }
      }
    }
  }
  
  return buildings;
}

function extractVictoryPoints(history: ASTNode | undefined): { provinceId: number; value: number }[] {
  if (!history?.victory_points) return [];
  const vps: { provinceId: number; value: number }[] = [];
  const vpData = history.victory_points;
  
  if (Array.isArray(vpData) && vpData.length === 2) {
    vps.push({ provinceId: vpData[0] as number, value: vpData[1] as number });
  } else if (Array.isArray(vpData)) {
    // Multiple victory points
    for (const vp of vpData) {
      if (Array.isArray(vp) && vp.length === 2) {
        vps.push({ provinceId: vp[0] as number, value: vp[1] as number });
      }
    }
  }
  
  return vps;
}

function parseStrategicRegionFromAST(ast: ASTNode, filePath: string): StrategicRegion | null {
  const regionNode = ast.strategic_region as ASTNode | undefined;
  if (!regionNode) return null;

  const id = regionNode.id as number;
  if (!id) return null;

  return {
    id,
    name: (regionNode.name as string) || `STRATEGICREGION_${id}`,
    provinces: extractProvinces(regionNode.provinces),
    weather: extractWeather(regionNode.weather as ASTNode | undefined),
    filePath,
  };
}

function extractWeather(weatherNode: ASTNode | undefined): StrategicRegion['weather'] {
  if (!weatherNode) return [];
  
  const periods: StrategicRegion['weather'] = [];
  const periodData = weatherNode.period;
  
  if (!periodData) return periods;
  
  const periodArray = Array.isArray(periodData) ? periodData : [periodData];
  
  for (const p of periodArray) {
    if (typeof p !== 'object' || Array.isArray(p)) continue;
    const period = p as ASTNode;
    
    const between = period.between as number[] | undefined;
    const temp = period.temperature as number[] | undefined;
    
    periods.push({
      between: between ? [between[0], between[1]] : [0, 30],
      temperature: temp ? [temp[0], temp[1]] : [0, 20],
      no_phenomenon: (period.no_phenomenon as number) || 0,
      rain_light: (period.rain_light as number) || 0,
      rain_heavy: (period.rain_heavy as number) || 0,
      snow: (period.snow as number) || 0,
      blizzard: (period.blizzard as number) || 0,
      arctic_water: (period.arctic_water as number) || 0,
      mud: (period.mud as number) || 0,
      sandstorm: (period.sandstorm as number) || 0,
      min_snow_level: (period.min_snow_level as number) || 0,
    });
  }
  
  return periods;
}

function parseAIAreasFromAST(ast: ASTNode): AIArea[] {
  const areas: AIArea[] = [];
  const areasNode = ast.areas as ASTNode | undefined;
  
  if (!areasNode) return areas;
  
  for (const [name, value] of Object.entries(areasNode)) {
    if (typeof value !== 'object' || Array.isArray(value)) continue;
    
    const areaNode = value as ASTNode;
    const area: AIArea = { name };
    
    if (areaNode.strategic_regions) {
      area.strategicRegions = extractProvinces(areaNode.strategic_regions);
    }
    
    if (areaNode.continents) {
      const continents = areaNode.continents;
      if (Array.isArray(continents)) {
        area.continents = continents.filter(c => typeof c === 'string') as string[];
      } else if (typeof continents === 'string') {
        area.continents = [continents];
      }
    }
    
    areas.push(area);
  }
  
  return areas;
}
