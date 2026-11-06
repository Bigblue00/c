# Basic Chemistry Reactions in Blender

`chemistry_reactions.py` builds and renders 3D animations of five basic
chemical reactions with Blender. Atoms are drawn as balls in the usual CPK
colours, bonds as sticks, and every atom is labelled with its element symbol.

| Key              | Reaction                         | Equation                    |
|------------------|----------------------------------|-----------------------------|
| `water`          | Synthesis of water               | 2H₂ + O₂ → 2H₂O             |
| `methane`        | Combustion of methane            | CH₄ + 2O₂ → CO₂ + 2H₂O      |
| `ammonia`        | Haber process                    | N₂ + 3H₂ → 2NH₃             |
| `salt`           | Formation of table salt          | 2Na + Cl₂ → 2NaCl           |
| `neutralization` | Acid–base neutralization         | HCl + NaOH → NaCl + H₂O     |

Each clip is 11 seconds (264 frames at 24 fps):

1. **Reactants approach.** The molecules appear on the left and drift together.
2. **Old bonds break.** The reactant bonds shrink away and a flash and shock ring
   mark the energy of the collision.
3. **Atoms rearrange.** Each atom moves to its place in a product molecule. The
   same atom objects are used from start to finish, so atoms are conserved and
   you can follow any one of them. Bonds that stay intact (like the O–H in
   NaOH → H₂O) never break.
4. **New bonds form.** The product molecules drift apart to the right, and a
   short note explains the reaction.

Colours: H white, C black, N blue, O red, Na purple, Cl green. Ionic bonds
(Na–Cl, Na–O) are drawn as thin glowing gold sticks.

`chemistry_reactions.mp4` is the rendered video of all five reactions (about 55 s).

## Rendering it yourself

You need Blender 4.2 or newer (or the `bpy` module: `pip install bpy`) and ffmpeg.

```bash
# Everything, then join into chemistry_reactions.mp4
./make_video.sh

# Quick low-resolution preview
./make_video.sh --width 640 --height 360 --samples 6

# One reaction only, as PNG frames
blender -b -P chemistry_reactions.py -- --reaction salt --out frames

# Save .blend files to open and tweak in Blender instead of rendering
blender -b -P chemistry_reactions.py -- --blend --out scenes

# List the reactions
python3 chemistry_reactions.py --list
```

Options: `--reaction` (a key, a comma-separated list, or `all`), `--out`,
`--width`, `--height`, `--samples` (Cycles samples, default 24),
`--frames 100-140` to render a range, `--step N` for every Nth frame.

## Adding a reaction

1. Add any new molecule shapes to `MOLECULES`: a list of `(element, (x, y, z))`
   atoms and `(atom_index, atom_index, bond_order)` bonds.
2. Add an entry to `REACTIONS`. Each reactant and product is
   `(molecule, centre, tags)`. Give each atom a tag and use the same tag for
   that atom in the products; this is how the animation knows where each atom goes.
   The script checks that the atoms balance.
3. Add the key to `REACTIONS` in `make_video.sh`.
