#!/usr/bin/env python3
"""
HOI4 Modifier Searcher - Search for available modifiers by category or keyword
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Optional


class ModifierDatabase:
    """Database of HOI4 modifiers organized by category"""

    def __init__(self):
        self.modifiers = self._load_modifiers()
        self.categories = self._build_category_index()

    def _load_modifiers(self) -> Dict[str, Dict]:
        """Load modifier definitions"""
        return {
            # Political & Stability
            "stability_factor": {
                "category": "political",
                "description": "Stability modifier",
                "example": "0.10",
                "tags": ["stability", "political", "internal"]
            },
            "war_support_factor": {
                "category": "political",
                "description": "War support modifier",
                "example": "0.10",
                "tags": ["war_support", "political", "internal"]
            },
            "political_power_gain": {
                "category": "political",
                "description": "Daily political power gain",
                "example": "0.15",
                "tags": ["political_power", "pp", "political"]
            },
            "political_power_factor": {
                "category": "political",
                "description": "Political power gain multiplier",
                "example": "0.10",
                "tags": ["political_power", "pp", "political"]
            },
            "drift_defence_factor": {
                "category": "political",
                "description": "Ideology drift defense",
                "example": "0.30",
                "tags": ["ideology", "drift", "political"]
            },
            "democratic_drift": {
                "category": "political",
                "description": "Daily democratic ideology drift",
                "example": "0.05",
                "tags": ["ideology", "drift", "democratic"]
            },
            "communism_drift": {
                "category": "political",
                "description": "Daily communist ideology drift",
                "example": "0.05",
                "tags": ["ideology", "drift", "communist"]
            },
            "fascism_drift": {
                "category": "political",
                "description": "Daily fascist ideology drift",
                "example": "0.05",
                "tags": ["ideology", "drift", "fascist"]
            },
            "neutrality_drift": {
                "category": "political",
                "description": "Daily neutrality ideology drift",
                "example": "0.05",
                "tags": ["ideology", "drift", "neutral"]
            },

            # Economy & Production
            "consumer_goods_factor": {
                "category": "economy",
                "description": "Consumer goods factories percentage",
                "example": "0.05",
                "tags": ["consumer_goods", "economy", "factories"]
            },
            "production_speed_buildings_factor": {
                "category": "economy",
                "description": "All construction speed",
                "example": "0.10",
                "tags": ["construction", "production", "buildings"]
            },
            "production_speed_industrial_complex_factor": {
                "category": "economy",
                "description": "Civilian factory construction speed",
                "example": "0.10",
                "tags": ["construction", "civ", "factory"]
            },
            "production_speed_arms_factory_factor": {
                "category": "economy",
                "description": "Military factory construction speed",
                "example": "0.10",
                "tags": ["construction", "mil", "factory"]
            },
            "production_speed_dockyard_factor": {
                "category": "economy",
                "description": "Dockyard construction speed",
                "example": "0.10",
                "tags": ["construction", "naval", "dockyard"]
            },
            "production_factory_max_efficiency_factor": {
                "category": "economy",
                "description": "Maximum factory efficiency",
                "example": "0.10",
                "tags": ["efficiency", "factory", "production"]
            },
            "production_factory_efficiency_gain_factor": {
                "category": "economy",
                "description": "Factory efficiency gain speed",
                "example": "0.10",
                "tags": ["efficiency", "factory", "production"]
            },
            "industrial_capacity_factory": {
                "category": "economy",
                "description": "Factory output bonus",
                "example": "0.10",
                "tags": ["output", "factory", "production"]
            },
            "industrial_capacity_dockyard": {
                "category": "economy",
                "description": "Dockyard output bonus",
                "example": "0.10",
                "tags": ["output", "naval", "dockyard"]
            },
            "line_change_production_efficiency_factor": {
                "category": "economy",
                "description": "Production line change efficiency retention",
                "example": "0.10",
                "tags": ["efficiency", "production", "change"]
            },

            # Military - General
            "army_morale_factor": {
                "category": "military",
                "description": "Army morale",
                "example": "0.10",
                "tags": ["morale", "army", "combat"]
            },
            "army_org_factor": {
                "category": "military",
                "description": "Army organization",
                "example": "0.10",
                "tags": ["organization", "org", "army"]
            },
            "conscription_factor": {
                "category": "military",
                "description": "Conscription modifier",
                "example": "0.10",
                "tags": ["conscription", "manpower", "recruitment"]
            },
            "training_time_factor": {
                "category": "military",
                "description": "Training time modifier (negative = faster)",
                "example": "-0.10",
                "tags": ["training", "army", "time"]
            },
            "experience_gain_factor": {
                "category": "military",
                "description": "Experience gain multiplier",
                "example": "0.05",
                "tags": ["experience", "xp", "training"]
            },
            "land_reinforce_rate": {
                "category": "military",
                "description": "Reinforcement rate",
                "example": "0.05",
                "tags": ["reinforcement", "army", "recovery"]
            },
            "army_attack_factor": {
                "category": "military",
                "description": "Army attack modifier",
                "example": "0.10",
                "tags": ["attack", "army", "combat"]
            },
            "army_defence_factor": {
                "category": "military",
                "description": "Army defense modifier",
                "example": "0.10",
                "tags": ["defense", "army", "combat"]
            },
            "max_planning": {
                "category": "military",
                "description": "Maximum planning bonus percentage",
                "example": "0.10",
                "tags": ["planning", "army", "combat"]
            },
            "planning_speed": {
                "category": "military",
                "description": "Planning speed multiplier",
                "example": "0.10",
                "tags": ["planning", "army", "speed"]
            },

            # Air Force
            "air_ace_generation_chance_factor": {
                "category": "air",
                "description": "Air ace generation chance",
                "example": "0.10",
                "tags": ["ace", "air", "pilots"]
            },
            "air_attack_factor": {
                "category": "air",
                "description": "Air attack modifier",
                "example": "0.10",
                "tags": ["attack", "air", "combat"]
            },
            "air_defence_factor": {
                "category": "air",
                "description": "Air defense modifier",
                "example": "0.10",
                "tags": ["defense", "air", "combat"]
            },
            "air_agility_factor": {
                "category": "air",
                "description": "Air agility modifier",
                "example": "0.10",
                "tags": ["agility", "air", "stats"]
            },
            "air_range_factor": {
                "category": "air",
                "description": "Air range modifier",
                "example": "0.10",
                "tags": ["range", "air", "stats"]
            },

            # Navy
            "navy_max_range_factor": {
                "category": "navy",
                "description": "Naval range modifier",
                "example": "0.10",
                "tags": ["range", "naval", "stats"]
            },
            "navy_org_factor": {
                "category": "navy",
                "description": "Naval organization",
                "example": "0.10",
                "tags": ["organization", "org", "naval"]
            },
            "convoy_escort_efficiency": {
                "category": "navy",
                "description": "Convoy escort efficiency",
                "example": "0.10",
                "tags": ["convoy", "escort", "naval"]
            },
            "convoy_raiding_efficiency_factor": {
                "category": "navy",
                "description": "Convoy raiding efficiency",
                "example": "0.10",
                "tags": ["convoy", "raiding", "naval"]
            },
            "naval_coordination_factor": {
                "category": "navy",
                "description": "Naval coordination",
                "example": "0.10",
                "tags": ["coordination", "naval", "stats"]
            },
            "naval_speed_factor": {
                "category": "navy",
                "description": "Naval speed modifier",
                "example": "0.10",
                "tags": ["speed", "naval", "stats"]
            },

            # Intelligence
            "operative_slot": {
                "category": "intelligence",
                "description": "Number of operative slots",
                "example": "1",
                "tags": ["operative", "spy", "intelligence"]
            },
            "crypto_strength": {
                "category": "intelligence",
                "description": "Encryption strength",
                "example": "1",
                "tags": ["crypto", "encryption", "intelligence"]
            },
            "decryption_factor": {
                "category": "intelligence",
                "description": "Decryption speed",
                "example": "0.10",
                "tags": ["decryption", "intelligence", "crypto"]
            },

            # Resources
            "local_resources_factor": {
                "category": "resources",
                "description": "Resource extraction efficiency",
                "example": "0.15",
                "tags": ["resources", "extraction", "economy"]
            },
            "trade_laws_cost_factor": {
                "category": "resources",
                "description": "Trade law change cost",
                "example": "-0.50",
                "tags": ["trade", "cost", "economy"]
            },

            # Other
            "attrition": {
                "category": "other",
                "description": "Land attrition modifier",
                "example": "-0.10",
                "tags": ["attrition", "army", "supply"]
            },
            "supply_consumption_factor": {
                "category": "other",
                "description": "Supply consumption modifier",
                "example": "-0.10",
                "tags": ["supply", "consumption", "logistics"]
            },
            "ai_focus_aggressive_factor": {
                "category": "other",
                "description": "AI aggression modifier",
                "example": "0.25",
                "tags": ["ai", "aggression", "behavior"]
            },
        }

    def _build_category_index(self) -> Dict[str, List[str]]:
        """Build index of modifiers by category"""
        index = {}
        for mod_name, mod_data in self.modifiers.items():
            category = mod_data["category"]
            if category not in index:
                index[category] = []
            index[category].append(mod_name)
        return index

    def search_by_keyword(self, keyword: str) -> List[tuple]:
        """Search modifiers by keyword in name, tags, or description"""
        keyword_lower = keyword.lower()
        results = []

        for mod_name, mod_data in self.modifiers.items():
            # Search in name
            if keyword_lower in mod_name.lower():
                results.append((mod_name, mod_data, "name"))
                continue

            # Search in tags
            if any(keyword_lower in tag.lower() for tag in mod_data["tags"]):
                results.append((mod_name, mod_data, "tag"))
                continue

            # Search in description
            if keyword_lower in mod_data["description"].lower():
                results.append((mod_name, mod_data, "description"))

        return results

    def get_by_category(self, category: str) -> List[tuple]:
        """Get all modifiers in a category"""
        category_lower = category.lower()
        results = []

        for mod_name in self.categories.get(category_lower, []):
            results.append((mod_name, self.modifiers[mod_name]))

        return results

    def list_categories(self) -> List[str]:
        """List all available categories"""
        return sorted(self.categories.keys())


def format_modifier(mod_name: str, mod_data: Dict, match_type: Optional[str] = None) -> str:
    """Format a modifier for display"""
    result = []
    result.append(f"📌 {mod_name}")
    result.append(f"   Category: {mod_data['category']}")
    result.append(f"   Description: {mod_data['description']}")
    result.append(f"   Example: {mod_name} = {mod_data['example']}")
    if match_type:
        result.append(f"   Match: {match_type}")
    return "\n".join(result)


def main():
    parser = argparse.ArgumentParser(
        description="Search HOI4 modifiers by keyword or category",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search by keyword
  %(prog)s --search stability

  # Search by category
  %(prog)s --category political

  # List all categories
  %(prog)s --list-categories

  # Show all modifiers
  %(prog)s --all
        """
    )

    parser.add_argument('--search', '-s', type=str,
                        help='Search modifiers by keyword')
    parser.add_argument('--category', '-c', type=str,
                        help='Show all modifiers in a category')
    parser.add_argument('--list-categories', '-l', action='store_true',
                        help='List all available categories')
    parser.add_argument('--all', '-a', action='store_true',
                        help='Show all modifiers')
    parser.add_argument('--limit', type=int, default=50,
                        help='Maximum number of results (default: 50)')

    args = parser.parse_args()

    db = ModifierDatabase()

    # List categories
    if args.list_categories:
        print("📂 Available Categories:\n")
        for category in db.list_categories():
            count = len(db.categories[category])
            print(f"  • {category} ({count} modifiers)")
        return

    # Show all modifiers
    if args.all:
        print("📋 All Modifiers:\n")
        for category in db.list_categories():
            print(f"\n{'=' * 70}")
            print(f"Category: {category.upper()}")
            print('=' * 70)
            results = db.get_by_category(category)
            for mod_name, mod_data in results:
                print(format_modifier(mod_name, mod_data))
                print()
        return

    # Search by keyword
    if args.search:
        results = db.search_by_keyword(args.search)
        if not results:
            print(f"❌ No modifiers found for keyword: {args.search}")
            return

        print(f"🔎 Found {len(results)} modifier(s) matching '{args.search}':\n")
        print('=' * 70)
        for mod_name, mod_data, match_type in results[:args.limit]:
            print(format_modifier(mod_name, mod_data, match_type))
            print()

        if len(results) > args.limit:
            print(f"... and {len(results) - args.limit} more (use --limit to show more)")
        return

    # Show category
    if args.category:
        results = db.get_by_category(args.category)
        if not results:
            print(f"❌ Category not found: {args.category}")
            print(f"\nAvailable categories: {', '.join(db.list_categories())}")
            return

        print(f"📂 Modifiers in category '{args.category}':\n")
        print('=' * 70)
        for mod_name, mod_data in results:
            print(format_modifier(mod_name, mod_data))
            print()
        return

    # No arguments - show help
    parser.print_help()


if __name__ == "__main__":
    main()
