import { create } from 'zustand';
import { Project, Province, State, StrategicRegion, AIArea, Adjacency, WeatherPeriod } from '../types';
import { parseDefinitionCSV, parseAdjacenciesCSV, createProvinceMaps, serializeDefinitionCSV } from '../parsers/csvParser';
import { parseParadoxScript, ASTNode } from '../parsers/paradox/parser';
import { serializeParadoxScript } from '../parsers/paradox/serializer';
import { rgbToKey } from '../utils/colorUtils';

interface ProjectState {
  // Project info
  project: Project | null;
  isLoading: boolean;
  error: string | null;
  isDirty: boolean;

  // Provinces
  provinces: Map<number, Province>;
  provinceById: Map<number, Province>;
  provinceByColor: Map<string, Province>;

  // States
  states: Map<number, State>;
  stateById: Map<number, State>;

  // Strategic Regions
  strategicRegions: Map<number, StrategicRegion>;
  strategicRegionById: Map<number, StrategicRegion>;

  // AI Areas
  aiAreas: AIArea[];

  // Adjacencies
  adjacencies: Adjacency[];

  // Actions
  openProject: (rootPath: string) => Promise<void>;
  closeProject: () => void;
  reloadProject: () => Promise<void>;

  // Province management
  addProvince: (province: Province) => void;
  updateProvince: (province: Province) => void;
  deleteProvince: (id: number) => void;
  saveDefinitionCSV: () => Promise<boolean>;

  // State management
  updateState: (state: State) => void;
  addProvinceToState: (stateId: number, provinceId: number) => void;
  removeProvinceFromState: (stateId: number, provinceId: number) => void;
  saveState: (stateId: number) => Promise<boolean>;
  saveAllStates: () => Promise<boolean>;

  // Strategic region management
  updateStrategicRegion: (region: StrategicRegion) => void;
  addProvinceToRegion: (regionId: number, provinceId: number) => void;
  removeProvinceFromRegion: (regionId: number, provinceId: number) => void;
  saveStrategicRegion: (regionId: number) => Promise<boolean>;
  saveAllStrategicRegions: () => Promise<boolean>;

  // AI Area management
  updateAIArea: (area: AIArea) => void;
  saveAIAreas: () => Promise<boolean>;

  // Mark dirty
  markDirty: () => void;
  markClean: () => void;
}

export const useProjectStore = create<ProjectState>((set, get) => ({
  project: null,
  isLoading: false,
  error: null,
  isDirty: false,

  provinces: new Map(),
  provinceById: new Map(),
  provinceByColor: new Map(),

  states: new Map(),
  stateById: new Map(),

  strategicRegions: new Map(),
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
      const provincesArray = parseDefinitionCSV(definitionResult.data!);
      const { byId: provinceById, byColor: provinceByColor } = createProvinceMaps(provincesArray);
      const provinces = provinceById;

      // Load adjacencies.csv
      let adjacencies: Adjacency[] = [];
      const adjResult = await api.readTextFile(`${mapPath}/adjacencies.csv`);
      if (adjResult.success) {
        adjacencies = parseAdjacenciesCSV(adjResult.data!);
      }

      // Load states from history/states/
      const states = new Map<number, State>();
      const stateById = states;
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
                    states.set(state.id, state);
                    
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
      const strategicRegions = new Map<number, StrategicRegion>();
      const strategicRegionById = strategicRegions;
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
                    strategicRegions.set(region.id, region);
                    
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
              const filePath = `${aiAreasPath}/${file.name}`;
              const content = await api.readTextFile(filePath);
              if (content.success) {
                try {
                  const ast = parseParadoxScript(content.data!);
                  const areas = parseAIAreasFromAST(ast, filePath);
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
        isDirty: false,
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
      provinces: new Map(),
      provinceById: new Map(),
      provinceByColor: new Map(),
      states: new Map(),
      stateById: new Map(),
      strategicRegions: new Map(),
      strategicRegionById: new Map(),
      aiAreas: [],
      adjacencies: [],
      isDirty: false,
      error: null,
    });
  },

  reloadProject: async () => {
    const { project } = get();
    if (project) {
      await get().openProject(project.rootPath);
    }
  },

  // Province management
  addProvince: (province: Province) => {
    set((state) => {
      const newProvinces = new Map(state.provinces);
      const newProvinceByColor = new Map(state.provinceByColor);
      
      newProvinces.set(province.id, province);
      newProvinceByColor.set(rgbToKey(province.color), province);
      
      return {
        provinces: newProvinces,
        provinceById: newProvinces,
        provinceByColor: newProvinceByColor,
        isDirty: true,
      };
    });
  },

  updateProvince: (province: Province) => {
    set((state) => {
      const oldProvince = state.provinces.get(province.id);
      const newProvinces = new Map(state.provinces);
      const newProvinceByColor = new Map(state.provinceByColor);
      
      // Remove old color mapping if color changed
      if (oldProvince) {
        const oldColorKey = rgbToKey(oldProvince.color);
        const newColorKey = rgbToKey(province.color);
        if (oldColorKey !== newColorKey) {
          newProvinceByColor.delete(oldColorKey);
        }
      }
      
      newProvinces.set(province.id, province);
      newProvinceByColor.set(rgbToKey(province.color), province);
      
      return {
        provinces: newProvinces,
        provinceById: newProvinces,
        provinceByColor: newProvinceByColor,
        isDirty: true,
      };
    });
  },

  deleteProvince: (id: number) => {
    set((state) => {
      const province = state.provinces.get(id);
      if (!province) return state;
      
      const newProvinces = new Map(state.provinces);
      const newProvinceByColor = new Map(state.provinceByColor);
      
      newProvinces.delete(id);
      newProvinceByColor.delete(rgbToKey(province.color));
      
      return {
        provinces: newProvinces,
        provinceById: newProvinces,
        provinceByColor: newProvinceByColor,
        isDirty: true,
      };
    });
  },

  saveDefinitionCSV: async () => {
    const { project, provinces } = get();
    if (!project) return false;
    
    try {
      const provincesArray = Array.from(provinces.values());
      const content = serializeDefinitionCSV(provincesArray);
      const filePath = `${project.mapPath}/definition.csv`;
      
      const result = await window.electronAPI.writeTextFile(filePath, content);
      return result.success;
    } catch (error) {
      console.error('Failed to save definition.csv:', error);
      return false;
    }
  },

  // State management
  updateState: (state: State) => {
    set((s) => {
      const newStates = new Map(s.states);
      newStates.set(state.id, state);
      
      // Update province references
      const newProvinces = new Map(s.provinces);
      for (const prov of newProvinces.values()) {
        if (prov.stateId === state.id && !state.provinces.includes(prov.id)) {
          prov.stateId = undefined;
        }
      }
      for (const provId of state.provinces) {
        const prov = newProvinces.get(provId);
        if (prov) {
          prov.stateId = state.id;
        }
      }
      
      return {
        states: newStates,
        stateById: newStates,
        provinces: newProvinces,
        provinceById: newProvinces,
        isDirty: true,
      };
    });
  },

  addProvinceToState: (stateId: number, provinceId: number) => {
    set((s) => {
      const state = s.states.get(stateId);
      if (!state || state.provinces.includes(provinceId)) return s;
      
      const newStates = new Map(s.states);
      const newState = { ...state, provinces: [...state.provinces, provinceId] };
      newStates.set(stateId, newState);
      
      const newProvinces = new Map(s.provinces);
      const prov = newProvinces.get(provinceId);
      if (prov) {
        // Remove from old state if any
        if (prov.stateId && prov.stateId !== stateId) {
          const oldState = newStates.get(prov.stateId);
          if (oldState) {
            oldState.provinces = oldState.provinces.filter(p => p !== provinceId);
          }
        }
        prov.stateId = stateId;
      }
      
      return {
        states: newStates,
        stateById: newStates,
        provinces: newProvinces,
        provinceById: newProvinces,
        isDirty: true,
      };
    });
  },

  removeProvinceFromState: (stateId: number, provinceId: number) => {
    set((s) => {
      const state = s.states.get(stateId);
      if (!state) return s;
      
      const newStates = new Map(s.states);
      const newState = { 
        ...state, 
        provinces: state.provinces.filter(p => p !== provinceId) 
      };
      newStates.set(stateId, newState);
      
      const newProvinces = new Map(s.provinces);
      const prov = newProvinces.get(provinceId);
      if (prov && prov.stateId === stateId) {
        prov.stateId = undefined;
      }
      
      return {
        states: newStates,
        stateById: newStates,
        provinces: newProvinces,
        provinceById: newProvinces,
        isDirty: true,
      };
    });
  },

  saveState: async (stateId: number) => {
    const { states } = get();
    const state = states.get(stateId);
    if (!state || !state.filePath) return false;
    
    try {
      const ast = stateToAST(state);
      const content = serializeParadoxScript(ast);
      const result = await window.electronAPI.writeTextFile(state.filePath, content);
      return result.success;
    } catch (error) {
      console.error(`Failed to save state ${stateId}:`, error);
      return false;
    }
  },

  saveAllStates: async () => {
    const { states } = get();
    let success = true;
    
    for (const state of states.values()) {
      if (state.filePath) {
        const result = await get().saveState(state.id);
        if (!result) success = false;
      }
    }
    
    return success;
  },

  // Strategic region management
  updateStrategicRegion: (region: StrategicRegion) => {
    set((s) => {
      const newRegions = new Map(s.strategicRegions);
      newRegions.set(region.id, region);
      
      // Update province references
      const newProvinces = new Map(s.provinces);
      for (const prov of newProvinces.values()) {
        if (prov.strategicRegionId === region.id && !region.provinces.includes(prov.id)) {
          prov.strategicRegionId = undefined;
        }
      }
      for (const provId of region.provinces) {
        const prov = newProvinces.get(provId);
        if (prov) {
          prov.strategicRegionId = region.id;
        }
      }
      
      return {
        strategicRegions: newRegions,
        strategicRegionById: newRegions,
        provinces: newProvinces,
        provinceById: newProvinces,
        isDirty: true,
      };
    });
  },

  addProvinceToRegion: (regionId: number, provinceId: number) => {
    set((s) => {
      const region = s.strategicRegions.get(regionId);
      if (!region || region.provinces.includes(provinceId)) return s;
      
      const newRegions = new Map(s.strategicRegions);
      const newRegion = { ...region, provinces: [...region.provinces, provinceId] };
      newRegions.set(regionId, newRegion);
      
      const newProvinces = new Map(s.provinces);
      const prov = newProvinces.get(provinceId);
      if (prov) {
        // Remove from old region if any
        if (prov.strategicRegionId && prov.strategicRegionId !== regionId) {
          const oldRegion = newRegions.get(prov.strategicRegionId);
          if (oldRegion) {
            oldRegion.provinces = oldRegion.provinces.filter(p => p !== provinceId);
          }
        }
        prov.strategicRegionId = regionId;
      }
      
      return {
        strategicRegions: newRegions,
        strategicRegionById: newRegions,
        provinces: newProvinces,
        provinceById: newProvinces,
        isDirty: true,
      };
    });
  },

  removeProvinceFromRegion: (regionId: number, provinceId: number) => {
    set((s) => {
      const region = s.strategicRegions.get(regionId);
      if (!region) return s;
      
      const newRegions = new Map(s.strategicRegions);
      const newRegion = { 
        ...region, 
        provinces: region.provinces.filter(p => p !== provinceId) 
      };
      newRegions.set(regionId, newRegion);
      
      const newProvinces = new Map(s.provinces);
      const prov = newProvinces.get(provinceId);
      if (prov && prov.strategicRegionId === regionId) {
        prov.strategicRegionId = undefined;
      }
      
      return {
        strategicRegions: newRegions,
        strategicRegionById: newRegions,
        provinces: newProvinces,
        provinceById: newProvinces,
        isDirty: true,
      };
    });
  },

  saveStrategicRegion: async (regionId: number) => {
    const { strategicRegions } = get();
    const region = strategicRegions.get(regionId);
    if (!region || !region.filePath) return false;
    
    try {
      const ast = strategicRegionToAST(region);
      const content = serializeParadoxScript(ast);
      const result = await window.electronAPI.writeTextFile(region.filePath, content);
      return result.success;
    } catch (error) {
      console.error(`Failed to save strategic region ${regionId}:`, error);
      return false;
    }
  },

  saveAllStrategicRegions: async () => {
    const { strategicRegions } = get();
    let success = true;
    
    for (const region of strategicRegions.values()) {
      if (region.filePath) {
        const result = await get().saveStrategicRegion(region.id);
        if (!result) success = false;
      }
    }
    
    return success;
  },

  // AI Area management
  updateAIArea: (area: AIArea) => {
    set((s) => {
      const newAreas = s.aiAreas.map(a => 
        a.name === area.name ? area : a
      );
      return { aiAreas: newAreas, isDirty: true };
    });
  },

  saveAIAreas: async () => {
    const { project, aiAreas } = get();
    if (!project) return false;
    
    try {
      // Group areas by file path
      const areasByFile = new Map<string, AIArea[]>();
      for (const area of aiAreas) {
        const filePath = area.filePath || `${project.commonPath}/ai_areas/default.txt`;
        if (!areasByFile.has(filePath)) {
          areasByFile.set(filePath, []);
        }
        areasByFile.get(filePath)!.push(area);
      }
      
      // Save each file
      for (const [filePath, areas] of areasByFile) {
        const ast = aiAreasToAST(areas);
        const content = serializeParadoxScript(ast);
        const result = await window.electronAPI.writeTextFile(filePath, content);
        if (!result.success) return false;
      }
      
      return true;
    } catch (error) {
      console.error('Failed to save AI areas:', error);
      return false;
    }
  },

  markDirty: () => set({ isDirty: true }),
  markClean: () => set({ isDirty: false }),
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
  
  if (Array.isArray(vpData) && vpData.length === 2 && typeof vpData[0] === 'number') {
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

function parseAIAreasFromAST(ast: ASTNode, filePath: string): AIArea[] {
  const areas: AIArea[] = [];
  const areasNode = ast.areas as ASTNode | undefined;
  
  if (!areasNode) return areas;
  
  for (const [name, value] of Object.entries(areasNode)) {
    if (typeof value !== 'object' || Array.isArray(value)) continue;
    
    const areaNode = value as ASTNode;
    const area: AIArea = { name, filePath };
    
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

// Convert domain objects back to AST for serialization

function stateToAST(state: State): ASTNode {
  const historyNode: ASTNode = {};
  
  if (state.owner) {
    historyNode.owner = state.owner;
  }
  
  for (const core of state.cores) {
    if (!historyNode.add_core_of) {
      historyNode.add_core_of = core;
    } else if (typeof historyNode.add_core_of === 'string') {
      historyNode.add_core_of = [historyNode.add_core_of, core];
    } else {
      (historyNode.add_core_of as string[]).push(core);
    }
  }
  
  if (state.victoryPoints.length > 0) {
    if (state.victoryPoints.length === 1) {
      historyNode.victory_points = [state.victoryPoints[0].provinceId, state.victoryPoints[0].value];
    } else {
      historyNode.victory_points = state.victoryPoints.map(vp => [vp.provinceId, vp.value]);
    }
  }
  
  if (state.buildings.length > 0) {
    const buildingsNode: ASTNode = {};
    for (const building of state.buildings) {
      if (building.provinceId) {
        if (!buildingsNode[building.provinceId]) {
          buildingsNode[building.provinceId] = {};
        }
        (buildingsNode[building.provinceId] as ASTNode)[building.type] = building.level;
      } else {
        buildingsNode[building.type] = building.level;
      }
    }
    historyNode.buildings = buildingsNode;
  }
  
  const stateNode: ASTNode = {
    id: state.id,
    name: state.name,
    manpower: state.manpower,
    state_category: state.stateCategory,
    provinces: state.provinces,
  };
  
  if (state.localSupplies) {
    stateNode.local_supplies = state.localSupplies;
  }
  
  if (Object.keys(historyNode).length > 0) {
    stateNode.history = historyNode;
  }
  
  return { state: stateNode };
}

function strategicRegionToAST(region: StrategicRegion): ASTNode {
  const regionNode: ASTNode = {
    id: region.id,
    name: region.name,
    provinces: region.provinces,
  };
  
  if (region.weather.length > 0) {
    const weatherNode: ASTNode = {
      period: region.weather.map((p: WeatherPeriod) => ({
        between: p.between,
        temperature: p.temperature,
        no_phenomenon: p.no_phenomenon,
        rain_light: p.rain_light,
        rain_heavy: p.rain_heavy,
        snow: p.snow,
        blizzard: p.blizzard,
        arctic_water: p.arctic_water,
        mud: p.mud,
        sandstorm: p.sandstorm,
        min_snow_level: p.min_snow_level,
      })),
    };
    regionNode.weather = weatherNode;
  }
  
  return { strategic_region: regionNode };
}

function aiAreasToAST(areas: AIArea[]): ASTNode {
  const areasNode: ASTNode = {};
  
  for (const area of areas) {
    const areaNode: ASTNode = {};
    
    if (area.strategicRegions && area.strategicRegions.length > 0) {
      areaNode.strategic_regions = area.strategicRegions;
    }
    
    if (area.continents && area.continents.length > 0) {
      areaNode.continents = area.continents;
    }
    
    areasNode[area.name] = areaNode;
  }
  
  return { areas: areasNode };
}
