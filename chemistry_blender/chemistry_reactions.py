"""
Animated basic-chemistry reactions rendered with Blender.

Every reaction is shown in four phases:
  1. the reactant molecules appear and drift together,
  2. the old bonds break (they shrink away) and a flash of energy goes off,
  3. the atoms move to their new places and the new bonds grow,
  4. the product molecules drift apart.

Atoms use CPK colours (H white, C black, N blue, O red, Na purple, Cl green)
and carry their element symbol, so you can follow every atom from the
reactants to the products. Atoms are conserved: each one is a single Blender
object that moves through the whole reaction.

Usage (from Blender, or with the `bpy` module from PyPI: pip install bpy):

    blender -b -P chemistry_reactions.py -- --out frames --reaction all
    python3 chemistry_reactions.py --out frames --reaction water
    python3 chemistry_reactions.py --list

Then join the frames into a video, for example with make_video.sh.
Pass --blend to save a .blend file for each reaction instead of rendering.
"""

import argparse
import math
import os
import sys

import bpy
from mathutils import Matrix, Vector

# ---------------------------------------------------------------------------
# Elements
# ---------------------------------------------------------------------------

# Visual radius (Blender units) and CPK-style colour for each element.
ELEMENTS = {
    "H": {"radius": 0.38, "color": (0.92, 0.92, 0.92)},
    "C": {"radius": 0.62, "color": (0.10, 0.10, 0.10)},
    "N": {"radius": 0.58, "color": (0.12, 0.25, 0.95)},
    "O": {"radius": 0.56, "color": (0.90, 0.08, 0.06)},
    "Na": {"radius": 0.82, "color": (0.55, 0.30, 0.90)},
    "Cl": {"radius": 0.76, "color": (0.15, 0.80, 0.15)},
}

# ---------------------------------------------------------------------------
# Molecule templates: atoms as (element, local position) and bonds as
# (atom index, atom index, order). Order 0.5 marks an ionic bond (drawn thin).
# The view looks along +Y, so X is left/right, Z is up/down, Y is depth.
# ---------------------------------------------------------------------------


def _tetra(length):
    dirs = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    rot = Matrix.Rotation(math.radians(20), 3, "Z") @ Matrix.Rotation(math.radians(10), 3, "X")
    return [tuple(rot @ (Vector(d).normalized() * length)) for d in dirs]


_ch4_h = _tetra(1.35)
_nh3_h = [
    (1.15 * math.cos(math.radians(a)), 1.15 * math.sin(math.radians(a)), -0.45)
    for a in (-90, 30, 150)
]
_water_half = math.radians(104.5 / 2)

MOLECULES = {
    "H2": ([("H", (-0.55, 0, 0)), ("H", (0.55, 0, 0))], [(0, 1, 1)]),
    "O2": ([("O", (-0.7, 0, 0)), ("O", (0.7, 0, 0))], [(0, 1, 2)]),
    "N2": ([("N", (-0.7, 0, 0)), ("N", (0.7, 0, 0))], [(0, 1, 3)]),
    "Cl2": ([("Cl", (-0.95, 0, 0)), ("Cl", (0.95, 0, 0))], [(0, 1, 1)]),
    "H2O": (
        [
            ("O", (0, 0, 0.25)),
            ("H", (-1.1 * math.sin(_water_half), 0, 0.25 - 1.1 * math.cos(_water_half))),
            ("H", (1.1 * math.sin(_water_half), 0, 0.25 - 1.1 * math.cos(_water_half))),
        ],
        [(0, 1, 1), (0, 2, 1)],
    ),
    "CH4": (
        [("C", (0, 0, 0))] + [("H", p) for p in _ch4_h],
        [(0, i, 1) for i in range(1, 5)],
    ),
    "CO2": (
        [("O", (-1.35, 0, 0)), ("C", (0, 0, 0)), ("O", (1.35, 0, 0))],
        [(0, 1, 2), (1, 2, 2)],
    ),
    "NH3": (
        [("N", (0, 0, 0.3))] + [("H", p) for p in _nh3_h],
        [(0, i, 1) for i in range(1, 4)],
    ),
    "Na": ([("Na", (0, 0, 0))], []),
    "NaCl": ([("Na", (-0.85, 0, 0)), ("Cl", (0.85, 0, 0))], [(0, 1, 0.5)]),
    "HCl": ([("H", (-0.75, 0, 0)), ("Cl", (0.55, 0, 0))], [(0, 1, 1)]),
    "NaOH": (
        [("Na", (-1.25, 0, 0)), ("O", (0.35, 0, 0)), ("H", (1.35, 0, 0))],
        [(0, 1, 0.5), (1, 2, 1)],
    ),
}

# ---------------------------------------------------------------------------
# Reactions. Each molecule instance is (template, centre, atom tags). An atom
# keeps its tag from reactant to product, which is how the animation knows
# where every atom goes.
# ---------------------------------------------------------------------------

REACTIONS = {
    "water": {
        "title": "Synthesis of Water",
        "equation": "2H\u2082 + O\u2082 \u2192 2H\u2082O",
        "note": "Hydrogen burns in oxygen: exothermic, releases energy",
        "reactants": [
            ("H2", (-7.0, 0, 1.6), ["h1", "h2"]),
            ("H2", (-7.0, 0, -1.8), ["h3", "h4"]),
            ("O2", (-3.6, 0, 0), ["o1", "o2"]),
        ],
        "products": [
            ("H2O", (4.0, 0, 1.4), ["o1", "h1", "h2"]),
            ("H2O", (6.6, 0, -1.4), ["o2", "h3", "h4"]),
        ],
    },
    "methane": {
        "title": "Combustion of Methane",
        "equation": "CH\u2084 + 2O\u2082 \u2192 CO\u2082 + 2H\u2082O",
        "note": "Natural gas burning: carbon dioxide and water are released",
        "reactants": [
            ("CH4", (-6.6, 0, 0), ["c1", "h1", "h2", "h3", "h4"]),
            ("O2", (-3.4, 0, 1.9), ["o1", "o2"]),
            ("O2", (-3.4, 0, -1.9), ["o3", "o4"]),
        ],
        "products": [
            ("CO2", (5.0, 0, 2.0), ["o1", "c1", "o3"]),
            ("H2O", (3.8, 0, -1.6), ["o2", "h1", "h2"]),
            ("H2O", (6.8, 0, -1.6), ["o4", "h3", "h4"]),
        ],
    },
    "ammonia": {
        "title": "Haber Process: Ammonia",
        "equation": "N\u2082 + 3H\u2082 \u2192 2NH\u2083",
        "note": "Nitrogen's triple bond breaks; each N picks up three H atoms",
        "reactants": [
            ("N2", (-5.2, 0, 0), ["n1", "n2"]),
            ("H2", (-8.0, 0, 2.0), ["h1", "h2"]),
            ("H2", (-8.2, 0, -0.2), ["h3", "h4"]),
            ("H2", (-2.6, 0, -2.0), ["h5", "h6"]),
        ],
        "products": [
            ("NH3", (4.0, 0, 1.0), ["n1", "h1", "h2", "h3"]),
            ("NH3", (6.8, 0, -1.4), ["n2", "h4", "h5", "h6"]),
        ],
    },
    "salt": {
        "title": "Formation of Table Salt",
        "equation": "2Na + Cl\u2082 \u2192 2NaCl",
        "note": "Each Na gives an electron to Cl and they form an ionic bond",
        "reactants": [
            ("Na", (-7.4, 0, 1.7), ["na1"]),
            ("Na", (-7.4, 0, -1.7), ["na2"]),
            ("Cl2", (-3.8, 0, 0), ["cl1", "cl2"]),
        ],
        "products": [
            ("NaCl", (5.2, 0, 1.6), ["na1", "cl1"]),
            ("NaCl", (5.2, 0, -1.6), ["na2", "cl2"]),
        ],
    },
    "neutralization": {
        "title": "Acid-Base Neutralization",
        "equation": "HCl + NaOH \u2192 NaCl + H\u2082O",
        "note": "An acid and a base make a salt and water",
        "reactants": [
            ("HCl", (-7.0, 0, 1.3), ["h1", "cl1"]),
            ("NaOH", (-4.0, 0, -1.3), ["na1", "o1", "h2"]),
        ],
        "products": [
            ("NaCl", (4.6, 0, 1.6), ["na1", "cl1"]),
            ("H2O", (5.4, 0, -1.6), ["o1", "h1", "h2"]),
        ],
    },
}

# ---------------------------------------------------------------------------
# Timeline (frames at 24 fps)
# ---------------------------------------------------------------------------

FPS = 24
F_INTRO = 24  # reactants pop in
F_APPROACH = 96  # reactants have drifted together
F_BREAK = 120  # old bonds gone
F_FORM = 156  # atoms in place, new bonds formed
F_SEPARATE = 216  # products drifted apart
F_END = 264  # hold

CLUSTER_SPREAD = 0.72  # how tightly molecules bunch up when they collide (0..1)
CLUSTER_GAP = 0.7  # reactants meet just left of centre, products leave just right

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def smoothstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def phase(frame, start, end):
    return smoothstep((frame - start) / float(end - start))


def make_material(name, color, metallic=0.0, roughness=0.35, emission=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if emission:
        bsdf.inputs["Emission Color"].default_value = (*color, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emission
    return mat


def load_font():
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    ):
        if os.path.exists(path):
            return bpy.data.fonts.load(path)
    return None  # Blender's built-in font


def add_text(body, location, size, material, font, align="CENTER"):
    curve = bpy.data.curves.new("text", "FONT")
    curve.body = body
    curve.size = size
    curve.align_x = align
    curve.align_y = "CENTER"
    curve.extrude = 0.01
    if font:
        curve.font = font
    obj = bpy.data.objects.new("text", curve)
    obj.location = location
    obj.rotation_euler = (math.radians(90), 0, 0)  # face the camera (-Y)
    obj.data.materials.append(material)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def key_scale(obj, frame, value):
    obj.scale = (value, value, value)
    obj.keyframe_insert("scale", frame=frame)


def show_between(obj, start, end, full=1.0, fade=8):
    """Pop an object in at `start` and out at `end` (by scaling)."""
    key_scale(obj, 0, 0.0)
    key_scale(obj, max(start, 1), 0.0)
    key_scale(obj, start + fade, full)
    if end is not None:
        key_scale(obj, end - fade, full)
        key_scale(obj, end, 0.0)


# ---------------------------------------------------------------------------
# Scene setup
# ---------------------------------------------------------------------------


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    try:
        import addon_utils

        addon_utils.enable("cycles", default_set=True)
    except Exception:
        pass


def setup_render(scene, args):
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = args.samples
    scene.cycles.use_denoising = True
    scene.cycles.max_bounces = 4
    scene.render.resolution_x = args.width
    scene.render.resolution_y = args.height
    scene.render.resolution_percentage = 100
    scene.render.fps = FPS
    scene.frame_start = 1
    scene.frame_end = F_END
    scene.render.image_settings.file_format = "PNG"
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Punchy"


def setup_world_camera_lights(scene):
    world = bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links
    bg = nodes["Background"]
    # Dark blue vertical gradient.
    coord = nodes.new("ShaderNodeTexCoord")
    sep = nodes.new("ShaderNodeSeparateXYZ")
    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.35
    ramp.color_ramp.elements[0].color = (0.004, 0.006, 0.02, 1)
    ramp.color_ramp.elements[1].position = 0.65
    ramp.color_ramp.elements[1].color = (0.03, 0.06, 0.14, 1)
    links.new(coord.outputs["Window"], sep.inputs[0])
    links.new(sep.outputs["Y"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = 1.0

    cam_data = bpy.data.cameras.new("Camera")
    cam_data.lens = 38
    cam = bpy.data.objects.new("Camera", cam_data)
    cam.location = (0, -21, 0.2)
    cam.rotation_euler = (math.radians(90), 0, 0)
    scene.collection.objects.link(cam)
    scene.camera = cam

    def area(name, loc, energy, size, rot):
        data = bpy.data.lights.new(name, "AREA")
        data.energy = energy
        data.size = size
        obj = bpy.data.objects.new(name, data)
        obj.location = loc
        obj.rotation_euler = rot
        scene.collection.objects.link(obj)
        return obj

    area("Key", (-8, -14, 10), 2500, 8, (math.radians(55), 0, math.radians(-30)))
    area("Fill", (10, -12, 2), 900, 10, (math.radians(80), 0, math.radians(40)))
    area("Rim", (0, 10, 8), 1200, 10, (math.radians(-130), 0, 0))


# ---------------------------------------------------------------------------
# Building one reaction
# ---------------------------------------------------------------------------


def expand(instances):
    """Turn molecule instances into atoms {tag: (element, centre, local, molecule)} and bonds."""
    atoms, bonds = {}, {}
    for mol, (template, centre, tags) in enumerate(instances):
        t_atoms, t_bonds = MOLECULES[template]
        if len(tags) != len(t_atoms):
            raise ValueError(f"{template}: expected {len(t_atoms)} tags, got {tags}")
        for tag, (element, local) in zip(tags, t_atoms):
            atoms[tag] = (element, Vector(centre), Vector(local), mol)
        for a, b, order in t_bonds:
            key = tuple(sorted((tags[a], tags[b])))
            bonds[key] = order
    return atoms, bonds


def spin(local, angle, tilt):
    rot = Matrix.Rotation(angle, 3, "Z") @ Matrix.Rotation(tilt, 3, "X")
    return rot @ local


def centroid(atoms):
    centres = [atom[1] for atom in atoms.values()]
    return sum(centres, Vector()) / len(centres)


def reactant_pose(frame, mol):
    """Gentle rocking of a reactant molecule (same for all its atoms, so it stays rigid)."""
    return 0.5 * math.sin(frame / 26.0 + mol * 1.7), 0.35 * math.sin(frame / 19.0 + mol * 2.3)


def product_pose(frame, mol):
    t = max(0, frame - F_FORM)
    return 0.45 * math.sin(t / 30.0 + mol * 1.3), 0.3 * math.sin(t / 22.0 + mol)


def atom_positions(frame, r_atoms, p_atoms):
    """World position of every atom at `frame`."""
    out = {}
    r_mid, p_mid = centroid(r_atoms), centroid(p_atoms)
    for tag in r_atoms:
        element, rc, rl, r_mol = r_atoms[tag]
        _, pc, pl, p_mol = p_atoms[tag]

        # Reactants start spread out and drift together, rocking gently.
        r_end_centre = (rc - r_mid) * CLUSTER_SPREAD + Vector((-CLUSTER_GAP, 0, 0))
        r_centre = rc.lerp(r_end_centre, phase(frame, F_INTRO, F_APPROACH))
        r_pos = r_centre + spin(rl, *reactant_pose(min(frame, F_BREAK), r_mol))
        r_end = r_end_centre + spin(rl, *reactant_pose(F_BREAK, r_mol))

        # Products start bunched in the middle and drift apart.
        p_start_centre = (pc - p_mid) * CLUSTER_SPREAD + Vector((CLUSTER_GAP, 0, 0))
        p_centre = p_start_centre.lerp(pc, phase(frame, F_FORM, F_SEPARATE))
        p_pos = p_centre + spin(pl, *product_pose(frame, p_mol))
        p_start = p_start_centre + spin(pl, *product_pose(F_FORM, p_mol))

        if frame <= F_BREAK:
            out[tag] = (element, r_pos)
        elif frame >= F_FORM:
            out[tag] = (element, p_pos)
        else:
            # Rearrangement: atoms bound for the same product arc together.
            m = phase(frame, F_BREAK, F_FORM)
            lift = math.sin(m * math.pi) * (0.7 if p_mol % 2 else -0.7)
            out[tag] = (element, r_end.lerp(p_start, m) + Vector((0, lift * 0.6, lift)))
    return out


def build_reaction(name, spec, font, mats):
    scene = bpy.context.scene
    r_atoms, r_bonds = expand(spec["reactants"])
    p_atoms, p_bonds = expand(spec["products"])
    if sorted(r_atoms) != sorted(p_atoms):
        raise ValueError(f"{name}: atoms are not conserved")
    for tag in r_atoms:
        if r_atoms[tag][0] != p_atoms[tag][0]:
            raise ValueError(f"{name}: atom {tag} changes element")

    # Atoms ---------------------------------------------------------------
    sphere_objs, label_objs = {}, {}
    for tag, (element, *_rest) in r_atoms.items():
        radius = ELEMENTS[element]["radius"]
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, segments=48, ring_count=24)
        obj = bpy.context.active_object
        obj.name = f"atom_{tag}"
        bpy.ops.object.shade_smooth()
        obj.data.materials.append(mats[element])
        sphere_objs[tag] = obj
        label_mat = mats["label_dark"] if element in ("H", "Cl") else mats["label_light"]
        label = add_text(element, (0, 0, 0), radius * (0.95 if len(element) == 1 else 0.8), label_mat, font)
        label.name = f"label_{tag}"
        label_objs[tag] = label

    # Bonds: one cylinder per line (double bond = 2 cylinders, etc.) -------
    bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=1.0, vertices=24)
    bpy.ops.object.shade_smooth()
    cyl_mesh = bpy.context.active_object.data
    cyl_mesh.materials.append(mats["bond"])
    bpy.data.objects.remove(bpy.context.active_object)

    # Bonds kept from reactants use their pair as key; bonds that only exist
    # (or change order) in the products get the key (pair, "p").
    all_bonds = dict(r_bonds)
    for k, v in p_bonds.items():
        if all_bonds.get(k) != v:
            all_bonds[(k, "p")] = v
    bond_objs = []  # (key, atom pair, line index, line count, radius, object)
    for key, order in all_bonds.items():
        pair = key[0] if isinstance(key[0], tuple) else key
        lines = 1 if order < 1 else int(order)
        radius = 0.07 if order < 1 else (0.13 if lines == 1 else 0.085)
        for j in range(lines):
            obj = bpy.data.objects.new(f"bond_{pair[0]}_{pair[1]}_{j}", cyl_mesh)
            obj.rotation_mode = "QUATERNION"
            scene.collection.objects.link(obj)
            obj.material_slots[0].link = "OBJECT"
            obj.material_slots[0].material = mats["ionic"] if order < 1 else mats["bond"]
            bond_objs.append((key, pair, j, lines, radius, obj))

    cam_dir = Vector((0, -1, 0))  # toward the camera

    # Keyframe every frame ------------------------------------------------
    for frame in range(1, F_END + 1):
        pos = atom_positions(frame, r_atoms, p_atoms)
        appear = phase(frame, 1, F_INTRO)
        for tag, (element, p) in pos.items():
            s_obj = sphere_objs[tag]
            s_obj.location = p
            s_obj.scale = (appear,) * 3
            s_obj.keyframe_insert("location", frame=frame)
            s_obj.keyframe_insert("scale", frame=frame)
            lab = label_objs[tag]
            lab.location = p + cam_dir * (ELEMENTS[element]["radius"] + 0.02)
            lab.scale = (appear,) * 3
            lab.keyframe_insert("location", frame=frame)
            lab.keyframe_insert("scale", frame=frame)

        for key, pair, j, lines, radius, obj in bond_objs:
            base_key = pair
            if isinstance(key[0], tuple):  # product-only version of the bond
                strength = phase(frame, F_FORM - 18, F_FORM + 6)
            elif base_key in p_bonds and p_bonds[base_key] == r_bonds.get(base_key):
                strength = 1.0
            else:
                strength = 1.0 - phase(frame, F_APPROACH, F_BREAK)
            strength *= appear
            a = pos[pair[0]][1]
            b = pos[pair[1]][1]
            d = b - a
            length = max(d.length, 1e-4)
            axis = d / length
            perp = axis.cross(Vector((0, 1, 0)))
            if perp.length < 1e-3:
                perp = axis.cross(Vector((1, 0, 0)))
            perp.normalize()
            offset = (j - (lines - 1) / 2.0) * 0.24
            # Bonds shrink toward their middle as they break / grow as they form.
            obj.location = (a + b) / 2 + perp * offset
            obj.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(axis)
            r = radius * (0.25 + 0.75 * strength) if strength > 0.01 else 0.0
            obj.scale = (r, r, length * strength)
            obj.keyframe_insert("location", frame=frame)
            obj.keyframe_insert("rotation_quaternion", frame=frame)
            obj.keyframe_insert("scale", frame=frame)

    # Energy flash at the moment of reaction -------------------------------
    flash_data = bpy.data.lights.new("Flash", "POINT")
    flash_data.color = (1.0, 0.75, 0.35)
    flash_data.shadow_soft_size = 2.0
    flash = bpy.data.objects.new("Flash", flash_data)
    flash.location = (0, -2.5, 0)
    scene.collection.objects.link(flash)
    for f, e in ((1, 0), (F_APPROACH, 0), (F_BREAK + 4, 1500), (F_FORM + 10, 0)):
        flash_data.energy = e
        flash_data.keyframe_insert("energy", frame=f)

    # Glowing shock-wave ring
    bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.03, major_segments=96)
    ring = bpy.context.active_object
    ring.rotation_euler = (math.radians(90), 0, 0)
    ring.location = (0, 0.5, 0)
    ring.data.materials.append(mats["glow"])
    for f, s in ((1, 0), (F_APPROACH + 8, 0), (F_BREAK, 0.8), (F_FORM - 6, 3.0), (F_FORM - 5, 0)):
        ring.scale = (s, s, s)
        ring.keyframe_insert("scale", frame=f)

    # Text -----------------------------------------------------------------
    title = add_text(spec["title"], (0, 0, 4.75), 0.6, mats["text_dim"], font)
    show_between(title, 2, None)
    eq = add_text(spec["equation"], (0, 0, 3.8), 0.95, mats["text"], font)
    show_between(eq, 6, None)
    note = add_text(spec["note"], (0, 0, -4.95), 0.4, mats["text_dim"], font)
    show_between(note, F_SEPARATE, None)

    captions = [
        ("Reactants approach", F_INTRO, F_APPROACH + 4),
        ("Old bonds break \u2014 atoms rearrange", F_APPROACH + 4, F_FORM + 4),
        ("New bonds form: products!", F_FORM + 4, F_SEPARATE),
    ]
    for body, start, end in captions:
        cap = add_text(body, (0, 0, -4.1), 0.5, mats["caption"], font)
        show_between(cap, start, end, fade=6)

    left = add_text("Reactants", (-5.5, 0, -3.2), 0.42, mats["text_dim"], font)
    show_between(left, F_INTRO, F_APPROACH)
    right = add_text("Products", (5.5, 0, -3.2), 0.42, mats["text_dim"], font)
    show_between(right, F_SEPARATE - 20, None)


def make_materials():
    mats = {el: make_material(el, d["color"]) for el, d in ELEMENTS.items()}
    mats["Na"] = make_material("Na", ELEMENTS["Na"]["color"], metallic=0.4, roughness=0.3)
    mats["bond"] = make_material("bond", (0.75, 0.75, 0.78), roughness=0.4)
    mats["ionic"] = make_material("ionic", (1.0, 0.85, 0.3), emission=2.0)
    mats["glow"] = make_material("glow", (1.0, 0.6, 0.2), emission=6.0)
    mats["text"] = make_material("text", (1, 1, 1), emission=1.2)
    mats["text_dim"] = make_material("text_dim", (0.6, 0.75, 1.0), emission=0.9)
    mats["caption"] = make_material("caption", (1.0, 0.82, 0.35), emission=1.2)
    mats["label_light"] = make_material("label_light", (1, 1, 1), emission=1.5)
    mats["label_dark"] = make_material("label_dark", (0.02, 0.02, 0.02))
    return mats


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else argv[1:]
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--reaction", default="all", help="reaction key or 'all'")
    p.add_argument("--out", default="frames", help="output folder for PNG frames")
    p.add_argument("--width", type=int, default=1280)
    p.add_argument("--height", type=int, default=720)
    p.add_argument("--samples", type=int, default=24)
    p.add_argument("--frames", default=None, help="only render these frames, e.g. 1-50 or 130")
    p.add_argument("--step", type=int, default=1, help="render every Nth frame (previews)")
    p.add_argument("--blend", action="store_true", help="save .blend files instead of rendering")
    p.add_argument("--list", action="store_true", help="list the reactions and exit")
    return p.parse_args(argv)


def main():
    args = parse_args()
    if args.list:
        for key, spec in REACTIONS.items():
            print(f"{key:15s} {spec['equation']}")
        return
    names = list(REACTIONS) if args.reaction == "all" else args.reaction.split(",")
    out_root = os.path.abspath(args.out)
    for name in names:
        spec = REACTIONS[name]
        reset_scene()
        scene = bpy.context.scene
        setup_render(scene, args)
        setup_world_camera_lights(scene)
        build_reaction(name, spec, load_font(), make_materials())
        folder = os.path.join(out_root, name)
        os.makedirs(folder, exist_ok=True)
        if args.blend:
            path = os.path.join(folder, f"{name}.blend")
            bpy.ops.wm.save_as_mainfile(filepath=path)
            print("saved", path)
            continue
        if args.frames:
            lo, _, hi = args.frames.partition("-")
            frames = range(int(lo), int(hi or lo) + 1)
        else:
            frames = range(scene.frame_start, scene.frame_end + 1)
        for f in list(frames)[:: args.step]:
            scene.frame_set(f)
            scene.render.filepath = os.path.join(folder, f"{f:04d}.png")
            bpy.ops.render.render(write_still=True)
            print(f"{name}: frame {f}/{scene.frame_end}", flush=True)


if __name__ == "__main__":
    main()
