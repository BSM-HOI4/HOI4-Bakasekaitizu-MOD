---
name: hoi4-image-asset-creator
description: Create, source, convert, or wire up Hearts of Iron IV mod image assets when implementing features that need gfx/interface textures, icons, TGA/DDS files, sprite sheets, scripted GUI graphics, decision images, focus icons, leader portraits, flags, or other bitmap assets. Use when a task references missing image assets, placeholder art, .gfx texturefile entries, gfx/interface paths, or asks whether Codex should generate usable image assets instead of leaving TODOs.
---

# HOI4 Image Asset Creator

Use this skill when HOI4 mod work needs image files, not just code references to images. The default behavior is to produce usable project-bound assets when feasible and ask only when the missing input is artistic direction, external-source choice, or permission to use AI-generated imagery.

## Decision Rules

1. Inspect the consuming files first: `.gfx`, `.gui`, scripted GUI, decisions, focuses, ideas, events, localisation tooltips, and nearby `gfx/` folders.
2. Prefer existing repo assets when they already match the needed style, size, frame layout, or UI role. Reuse, tint, crop, composite, or sprite-sheet them before inventing new art.
3. If the asset is deterministic or data-driven, create it directly with local tooling. Do not ask whether to create it.
4. If the asset is aesthetic, historical, or representational and the user did not specify the subject/style/source, ask one concise question before generating or sourcing it.
5. If the user asked to implement a feature end to end, do not leave missing textures, blank placeholders, or TODO asset paths when a reasonable generated asset can be made.
6. Never overwrite an existing asset unless explicitly requested. Create a versioned or feature-specific filename and update references.

## Generation Strategy

Choose the lowest-risk method that produces a real in-game asset:

- **Existing texture adaptation:** Use for HOI4-style buttons, panels, bars, frames, markers, overlays, and icons that should match vanilla or local UI.
- **Pillow/code generation:** Use for simple colored assets, masks, seat dots, party color bars, backplates, generated sprite sheets, and frame strips.
- **Image generation skill:** Use `$imagegen` for new bitmap art such as portraits, event images, focus art concepts, illustrated decision images, or custom scene/icon artwork that cannot be assembled reliably from local assets.
- **External reference/source lookup:** Use only when the task requires a historically specific source image or current/public-domain status; verify license/source before placing it in the mod.

For the Tsareich2 parliament pattern, prefer Python/Pillow generation from party color data: seat icons, color bars, government markers, and backplates are generated assets, not reasons to stop and ask. The completed design notes in `.plan/done/parliament_system_v2.md` establish that color-defined parliament UI graphics should be generated from configuration and then referenced from `.gfx`.

## HOI4 Asset Workflow

1. Find all texture consumers:
   - Search for `texturefile`, `spriteType`, `quadTextureSprite`, `GFX_`, `.dds`, `.tga`, and feature-specific prefixes.
   - Compare declared paths with files under `gfx/`.
2. Determine the required technical shape:
   - file path and extension
   - dimensions
   - alpha channel requirements
   - frame count and frame order
   - whether the `.gfx` entry uses `noOfFrames`
   - naming prefix convention, especially country tags like `GER_`
3. Create missing assets:
   - Use Pillow for deterministic UI elements.
   - Use local source textures for overlays and frames when available.
   - Use `$imagegen` only for genuinely new raster artwork.
4. Save assets into the mod tree, usually under `gfx/interface/<feature>/`, `gfx/leaders/<TAG>/`, `gfx/flags/`, or the nearest existing feature folder.
5. Update `.gfx`/`.gui` references to match the generated filenames and frame counts.
6. Validate:
   - Open generated files with Pillow or an available image tool.
   - Confirm dimensions, mode/alpha, frame strip width, and non-empty pixels.
   - Grep references to ensure every generated asset is consumed or intentionally staged.

## Format Guidance

- Match the repo's existing format for the same asset family. Tsareich2 parliament currently uses `.tga` assets under `gfx/interface/parliament/`.
- Use `.dds` when nearby assets or existing `.gfx` entries require it and local tooling can write it correctly.
- Use `.tga` as a practical fallback for generated UI textures with alpha when DDS writing is unavailable.
- Keep transparent background for icons, markers, seats, and overlays unless the surrounding UI expects an opaque panel.
- For sprite sheets, keep each frame the same size and document the frame order in code or configuration when it is not obvious.

## Asking Policy

Ask before creating or importing assets only when one of these is true:

- The user must choose between multiple visual directions.
- The asset would use AI-generated representational art and the user has not already authorized that kind of asset.
- The asset needs a specific historical person, emblem, photograph, or copyrighted-looking source.
- The mod's intended art style cannot be inferred from nearby assets.

Do not ask when the asset is a mechanical UI texture, color swatch, generated sprite sheet, simple marker, backplate, mask, or converted existing asset.

## Reporting

When finished, report:

- generated or adapted asset paths
- changed consuming files
- generation method used
- validation performed
- any remaining assets that still need user art direction
