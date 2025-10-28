NDefines.NGraphics.MINIMUM_PROVINCE_SIZE_IN_PIXELS = 0
NDefines.NBuildings.MAX_SHARED_SLOTS = 56	
NDefines.NBuildings.MAX_BUILDING_LEVELS = 56			-- Max levels a building can have.
NDefines.RADAR_RANGE_BASE = 10				-- Radar range base, first level radar will be this + min, best radar will be this + max
NDefines.RADAR_RANGE_MIN = 10				-- Radar range (from state center to province center) in measure of map pixels. Exluding techs.
NDefines.RADAR_RANGE_MAX = 1000				-- Range is interpolated between building levels 1-15.