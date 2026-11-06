"""
Render one story episode (a plan made by prepare.py) with Blender.

    blender -b -P render_story.py -- plans/c10_ch3_salt.json --out frames
    python3 render_story.py plans/c10_ch3_salt.json --out frames   # with `pip install bpy`

Only needs Blender's own Python: all chemistry is precomputed in the plan.
Frames whose picture would not change (nothing moving) are copied rather
than rendered again.
"""

import argparse
import json
import math
import os
import shutil
import sys

import bpy
from mathutils import Matrix, Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from elements import METALS, color, dark_label, radius  # noqa: E402

HUD_DIST = 10.0  # distance of the on-screen text in front of the camera
HUD_HALF_W = HUD_DIST * 18 / 38
HUD_HALF_H = HUD_HALF_W * 9 / 16


def smooth(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def ramp(t, a, b):
    return smooth((t - a) / (b - a)) if b > a else float(t >= b)


# ---------------------------------------------------------------------------
# Materials, text
# ---------------------------------------------------------------------------


def material(name, rgb, metallic=0.0, rough=0.35, emit=0.0, alpha=1.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (*rgb, 1)
    p.inputs["Metallic"].default_value = metallic
    p.inputs["Roughness"].default_value = rough
    if emit:
        p.inputs["Emission Color"].default_value = (*rgb, 1)
        p.inputs["Emission Strength"].default_value = emit
    if alpha < 1:
        p.inputs["Alpha"].default_value = alpha
    return m


def font():
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "C:/Windows/Fonts/seguisb.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ):
        if os.path.exists(path):
            return bpy.data.fonts.load(path)
    return None


def hud_only(obj):
    """On-screen elements must not cast shadows or light the molecules."""
    for attr in ("visible_shadow", "visible_diffuse", "visible_glossy", "visible_transmission", "visible_volume_scatter"):
        if hasattr(obj, attr):
            setattr(obj, attr, False)


def text(body, size, mat, fnt, parent=None, loc=(0, 0, 0), align="CENTER"):
    cu = bpy.data.curves.new("txt", "FONT")
    cu.body = body
    cu.size = size
    cu.align_x = align
    cu.align_y = "CENTER"
    cu.space_line = 1.05
    if fnt:
        cu.font = fnt
    ob = bpy.data.objects.new("txt", cu)
    ob.data.materials.append(mat)
    bpy.context.scene.collection.objects.link(ob)
    if parent:
        ob.parent = parent
        ob.location = loc
        hud_only(ob)
    else:
        ob.location = loc
        ob.rotation_euler = (math.radians(90), 0, 0)
    return ob


def wrap(s, width=62):
    words, lines, cur = s.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Scene
# ---------------------------------------------------------------------------


class Story:
    def __init__(self, plan, args):
        self.plan = plan
        self.args = args
        bpy.ops.wm.read_factory_settings(use_empty=True)
        try:
            import addon_utils

            addon_utils.enable("cycles", default_set=True)
        except Exception:
            pass
        self.scene = bpy.context.scene
        self.font = font()
        self.setup_render()
        self.setup_world()
        self.setup_camera()
        self.mats = self.make_materials()
        self.build_atoms()
        self.build_bonds()
        self.build_effects()
        self.build_hud()

    # -- setup -------------------------------------------------------------
    def setup_render(self):
        s, a = self.scene, self.args
        s.render.engine = "CYCLES"
        s.cycles.device = "CPU"
        s.cycles.samples = a.samples
        s.cycles.use_denoising = True
        s.cycles.max_bounces = 3
        s.render.use_persistent_data = True
        s.render.resolution_x, s.render.resolution_y = a.width, a.height
        s.render.fps = a.fps
        s.render.image_settings.file_format = "PNG"
        s.view_settings.view_transform = "AgX"
        s.view_settings.look = "AgX - Punchy"

    def setup_world(self):
        w = bpy.data.worlds.new("World")
        self.scene.world = w
        w.use_nodes = True
        nt = w.node_tree
        coord = nt.nodes.new("ShaderNodeTexCoord")
        sep = nt.nodes.new("ShaderNodeSeparateXYZ")
        rmp = nt.nodes.new("ShaderNodeValToRGB")
        rmp.color_ramp.elements[0].position = 0.3
        rmp.color_ramp.elements[0].color = (0.004, 0.006, 0.02, 1)
        rmp.color_ramp.elements[1].position = 0.75
        rmp.color_ramp.elements[1].color = (0.03, 0.06, 0.14, 1)
        nt.links.new(coord.outputs["Window"], sep.inputs[0])
        nt.links.new(sep.outputs["Y"], rmp.inputs["Fac"])
        nt.links.new(rmp.outputs["Color"], nt.nodes["Background"].inputs["Color"])

    def setup_camera(self):
        sx, sz = self.plan["span"]
        sx = max(sx, 6.0)
        # Fit molecules between the title area and the subtitles.
        d = max(14.0, sx / (0.4737 * 0.95), (sz + 0.8) / (0.58 * 0.2664))
        self.cam_dist = d
        cd = bpy.data.cameras.new("Camera")
        cd.lens = 38
        cam = bpy.data.objects.new("Camera", cd)
        cam.location = (0, -d, 0)
        cam.rotation_euler = (math.radians(90), 0, 0)
        self.scene.collection.objects.link(cam)
        self.scene.camera = cam
        self.cam = cam

        k = d / 21.0
        for name, loc, energy, size, rot in (
            ("Key", (-8, -14, 10), 2500, 8, (55, 0, -30)),
            ("Fill", (10, -12, 2), 900, 10, (80, 0, 40)),
            ("Rim", (0, 10, 8), 1200, 10, (-130, 0, 0)),
        ):
            ld = bpy.data.lights.new(name, "AREA")
            ld.energy = energy * k * k
            ld.size = size * k
            lo = bpy.data.objects.new(name, ld)
            lo.location = Vector(loc) * k
            lo.rotation_euler = [math.radians(v) for v in rot]
            self.scene.collection.objects.link(lo)

    def make_materials(self):
        m = {}
        for el in {a["el"] for a in self.plan["atoms"]}:
            metal = el in METALS
            m[el] = material(el, color(el), metallic=0.5 if metal else 0.0, rough=0.3)
        m["bond"] = material("bond", (0.75, 0.75, 0.78), rough=0.4)
        m["ionic"] = material("ionic", (1.0, 0.82, 0.3), emit=2.0)
        m["dative"] = material("dative", (0.35, 0.75, 1.0), emit=1.5)
        m["glow"] = material("glow", (1.0, 0.6, 0.2), emit=6.0)
        m["electron"] = material("electron", (1.0, 0.95, 0.3), emit=12.0)
        m["white"] = material("white", (1, 1, 1), emit=1.3)
        m["dim"] = material("dim", (0.6, 0.75, 1.0), emit=0.9)
        m["gold"] = material("gold", (1.0, 0.8, 0.3), emit=1.3)
        m["label_light"] = material("label_light", (1, 1, 1), emit=1.5)
        m["label_dark"] = material("label_dark", (0.02, 0.02, 0.02))
        m["panel"] = material("panel", (0.0, 0.0, 0.0), alpha=0.55)
        return m

    # -- molecules ---------------------------------------------------------
    def build_atoms(self):
        self.atom_objs, self.labels = [], []
        meshes = {}
        for a in self.plan["atoms"]:
            el = a["el"]
            if el not in meshes:
                bpy.ops.mesh.primitive_uv_sphere_add(radius=radius(el), segments=40, ring_count=20)
                tmp = bpy.context.active_object
                bpy.ops.object.shade_smooth()
                meshes[el] = tmp.data
                meshes[el].materials.append(self.mats[el])
                bpy.data.objects.remove(tmp)
            ob = bpy.data.objects.new(el, meshes[el])
            self.scene.collection.objects.link(ob)
            self.atom_objs.append(ob)
            lm = self.mats["label_dark"] if dark_label(el) else self.mats["label_light"]
            pair = []
            for body in (a["r_label"], a["p_label"]):
                size = radius(el) * (0.9 if len(body) == 1 else 0.68 if len(body) == 2 else 0.55)
                pair.append(text(body, size, lm, self.font))
            self.labels.append(pair)

    def build_bonds(self):
        bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=1.0, vertices=20)
        tmp = bpy.context.active_object
        bpy.ops.object.shade_smooth()
        mesh = tmp.data
        mesh.materials.append(self.mats["bond"])
        bpy.data.objects.remove(tmp)

        r = {(a, b): o for a, b, o in self.plan["r_bonds"]}
        p = {(a, b): o for a, b, o in self.plan["p_bonds"]}
        self.bonds = []  # (pair, kind, lines, radius, [objects])
        for pair, order in r.items():
            kind = "keep" if p.get(pair) == order else "break"
            self.bonds.append(self.make_bond(mesh, pair, order, kind))
        for pair, order in p.items():
            if r.get(pair) != order:
                self.bonds.append(self.make_bond(mesh, pair, order, "form"))

    def make_bond(self, mesh, pair, order, kind):
        if order in ("ionic", "dative"):
            lines, rad, mat = 1, (0.07 if order == "ionic" else 0.11), self.mats[order]
        else:
            lines, rad, mat = int(order), (0.13 if order == 1 else 0.085), self.mats["bond"]
        objs = []
        for _ in range(lines):
            ob = bpy.data.objects.new("bond", mesh)
            ob.rotation_mode = "QUATERNION"
            self.scene.collection.objects.link(ob)
            ob.material_slots[0].link = "OBJECT"
            ob.material_slots[0].material = mat
            objs.append(ob)
        return (tuple(pair), kind, lines, rad, objs)

    def build_effects(self):
        fd = bpy.data.lights.new("Flash", "POINT")
        fd.color = (1.0, 0.75, 0.35)
        fd.shadow_soft_size = 2.0
        self.flash = bpy.data.objects.new("Flash", fd)
        self.flash.location = (0, -3, 0)
        self.scene.collection.objects.link(self.flash)

        bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.03, major_segments=96)
        self.ring = bpy.context.active_object
        self.ring.rotation_euler = (math.radians(90), 0, 0)
        self.ring.location = (0, 0.6, 0)
        self.ring.data.materials.append(self.mats["glow"])

        self.electrons = []
        for _ in self.plan["electrons"]:
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.22, segments=16, ring_count=8)
            e = bpy.context.active_object
            e.data.materials.append(self.mats["electron"])
            self.electrons.append(e)

    def build_hud(self):
        p, m, f, cam = self.plan, self.mats, self.font, self.cam
        z = -HUD_DIST
        top = HUD_HALF_H
        self.hud_chapter = text(f"Class {p['class']}  \u00b7  {p['chapter']}", 0.15, m["dim"], f, cam, (0, top - 0.22, z))
        self.hud_eq = text(p["equation"], 0.3, m["white"], f, cam, (0, top - 0.6, z))
        self.hud_cond = text(p["condition"], 0.16, m["gold"], f, cam, (0, top - 0.93, z))
        self.hud_title = text(p["title"], 0.42, m["white"], f, cam, (0, 0.15, z))
        self.hud_title_sub = text("A story from NCERT Chemistry", 0.16, m["dim"], f, cam, (0, -0.35, z))
        self.hud_key = text("KEY IDEA", 0.16, m["gold"], f, cam, (0, -HUD_HALF_H + 0.98, z))
        self.subs = []
        for ln in p["lines"]:
            ob = text(wrap(ln["text"], 56), 0.2, m["white"], f, cam, (0, -HUD_HALF_H + 0.5, z))
            self.subs.append((ln, ob))
        bpy.ops.mesh.primitive_plane_add(size=1)
        panel = bpy.context.active_object
        panel.parent = cam
        panel.location = (0, -HUD_HALF_H + 0.5, z - 0.02)
        panel.scale = (HUD_HALF_W * 2, 0.72, 1)
        panel.data.materials.append(m["panel"])
        hud_only(panel)
        self.panel = panel

    # -- animation ---------------------------------------------------------
    def motion_envelope(self, t):
        """1 while things are moving (approach, reaction, products drifting
        apart), 0 while the narrator talks over a still scene. Still frames
        are copied instead of rendered, which saves most of the render time."""
        ph = self.plan["phases"]
        a0 = ph["approach"][0]
        p0, p1 = ph["products"]
        p_end = p0 + min(4.0, p1 - p0 + 2)
        return ramp(t, a0 - 0.6, a0 + 0.6) * (1 - ramp(t, p_end, p_end + 1.0))

    def pose(self, t, mol, side):
        """Gentle rocking (rotation about Z and X) of one molecule."""
        a = self.args.rock * self.motion_envelope(t)
        ph = mol * 1.7 + (0 if side == "r" else 4.0)
        return (0.45 * a * math.sin(t / 2.2 + ph), 0.3 * a * math.sin(t / 1.6 + ph * 1.3))

    @staticmethod
    def rot(local, angles):
        return (Matrix.Rotation(angles[0], 3, "Z") @ Matrix.Rotation(angles[1], 3, "X")) @ Vector(local)

    def positions(self, t):
        p = self.plan
        ph = p["phases"]
        A0, A1 = ph["approach"]
        R0, R1 = ph["react"]
        P0, P1 = ph["products"]
        rc = [Vector(c) for c in p["r_centres"]]
        pc = [Vector(c) for c in p["p_centres"]]
        r_mid = sum(rc, Vector()) / len(rc)
        p_mid = sum(pc, Vector()) / len(pc)
        r_end = [(c - r_mid) * 0.7 + Vector((-0.6, 0, 0)) for c in rc]
        p_start = [(c - p_mid) * 0.7 + Vector((0.6, 0, 0)) for c in pc]

        u = (t - R0) / max(R1 - R0, 1e-3)
        move = smooth((u - 0.25) / 0.55)
        drift_in = ramp(t, A0, A1)
        drift_out = ramp(t, P0, P0 + min(4.0, P1 - P0 + 2))
        out = []
        for a in p["atoms"]:
            ri, pi = a["r_inst"], a["p_inst"]
            tr = min(t, R0 + 0.25 * (R1 - R0))
            r_pos = rc[ri].lerp(r_end[ri], drift_in) + self.rot(a["r_local"], self.pose(tr, ri, "r"))
            tp = max(t, R0 + 0.8 * (R1 - R0))
            p_pos = p_start[pi].lerp(pc[pi], drift_out) + self.rot(a["p_local"], self.pose(tp, pi, "p"))
            if move <= 0:
                out.append(r_pos)
            elif move >= 1:
                out.append(p_pos)
            else:
                lift = math.sin(move * math.pi) * (0.6 if pi % 2 else -0.6)
                out.append(r_pos.lerp(p_pos, move) + Vector((0, lift * 0.5, lift)))
        return out, u, move

    def apply(self, t):
        p = self.plan
        ph = p["phases"]
        pos, u, move = self.positions(t)
        appear = ramp(t, 1.7, 2.5)
        cam_dir = Vector((0, -1, 0))

        for a, ob, (lab_r, lab_p), x in zip(p["atoms"], self.atom_objs, self.labels, pos):
            ob.location = x
            ob.scale = (appear,) * 3
            front = x + cam_dir * (radius(a["el"]) + 0.02)
            show_p = move > 0.5
            for lab, on in ((lab_r, not show_p), (lab_p, show_p)):
                lab.location = front
                lab.scale = (appear if on else 0,) * 3

        brk = 1 - smooth(u / 0.35)
        form = smooth((u - 0.6) / 0.35)
        for pair, kind, lines, rad, objs in self.bonds:
            s = {"keep": 1.0, "break": brk, "form": form}[kind] * appear
            a, b = pos[pair[0]], pos[pair[1]]
            d = b - a
            length = max(d.length, 1e-4)
            axis = d / length
            perp = axis.cross(Vector((0, 1, 0)))
            if perp.length < 1e-3:
                perp = axis.cross(Vector((1, 0, 0)))
            perp.normalize()
            for j, ob in enumerate(objs):
                off = (j - (lines - 1) / 2) * 0.24
                ob.location = (a + b) / 2 + perp * off
                ob.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(axis)
                r = rad * (0.3 + 0.7 * s) if s > 0.01 else 0.0
                ob.scale = (r, r, length * s)

        # Flash and shock ring at the moment the old bonds give way.
        self.flash.data.energy = 1500 * (self.cam_dist / 21) ** 2 * max(0.0, 1 - abs(u - 0.3) / 0.2)
        ring = (2.8 * smooth((u - 0.2) / 0.4)) if 0.2 < u < 0.6 else 0.0
        self.ring.scale = (ring,) * 3

        # Electrons travel from donor to acceptor.
        for e, (frm, to) in zip(self.electrons, p["electrons"]):
            k = (u - 0.05) / 0.4
            if 0 < k < 1:
                w = smooth(k)
                e.location = pos[frm].lerp(pos[to], w) + Vector((0, -1.0, math.sin(w * math.pi) * 1.2))
                e.scale = (1,) * 3
            else:
                e.scale = (0,) * 3

        # On-screen text.
        title = ramp(t, 0.1, 0.5) * (1 - ramp(t, 1.8, 2.2))
        self.hud_title.scale = (title,) * 3
        self.hud_title_sub.scale = (title,) * 3
        info = ramp(t, 1.9, 2.4)
        for ob in (self.hud_chapter, self.hud_eq, self.hud_cond):
            ob.scale = (info,) * 3
        any_sub = False
        for ln, ob in self.subs:
            on = ln["start"] - 0.1 <= t <= ln["start"] + ln["dur"] + 0.35
            ob.scale = (1 if on else 0,) * 3
            any_sub |= on
        self.panel.scale = (HUD_HALF_W * 2 if any_sub else 0, 0.8 if any_sub else 0, 1)
        key = ph["takeaway"][0] - 0.1 <= t
        self.hud_key.scale = (1 if key else 0,) * 3

    def signature(self):
        sig = []
        for ob in self.scene.objects:
            if ob.type in ("MESH", "FONT"):
                sig.append(tuple(round(v, 4) for v in (*ob.location, *ob.scale, *ob.rotation_quaternion)))
        sig.append(round(self.flash.data.energy, 2))
        return tuple(sig)

    def render(self, out_dir, frames):
        os.makedirs(out_dir, exist_ok=True)
        fps = self.args.fps
        last_sig, last_file = None, None
        rendered = 0
        for f in frames:
            t = (f - 1) / fps
            self.apply(t)
            path = os.path.join(out_dir, f"{f:05d}.png")
            sig = self.signature()
            if sig == last_sig and last_file:
                shutil.copyfile(last_file, path)
            else:
                self.scene.render.filepath = path
                bpy.ops.render.render(write_still=True)
                rendered += 1
            last_sig, last_file = sig, path
            print(f"{self.plan['id']}: frame {f}/{frames[-1]} (rendered {rendered})", flush=True)


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else sys.argv[1:]
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--out", default="frames")
    ap.add_argument("--width", type=int, default=960)
    ap.add_argument("--height", type=int, default=540)
    ap.add_argument("--samples", type=int, default=8)
    ap.add_argument("--fps", type=int, default=12, help="render rate; the video is played at 24 fps")
    ap.add_argument("--rock", type=float, default=1.0, help="molecule wobble (0 = still)")
    ap.add_argument("--frames", default=None, help="e.g. 1-100 or 250")
    ap.add_argument("--at", default=None, help="comma-separated times in seconds to render (previews)")
    args = ap.parse_args(argv)
    with open(args.plan) as fh:
        plan = json.load(fh)
    story = Story(plan, args)
    out = os.path.join(args.out, plan["id"])
    total = int(math.ceil(plan["duration"] * args.fps))
    if args.at:
        frames = [int(float(x) * args.fps) + 1 for x in args.at.split(",")]
    elif args.frames:
        lo, _, hi = args.frames.partition("-")
        frames = list(range(int(lo), int(hi or lo) + 1))
    else:
        frames = list(range(1, total + 1))
    story.render(out, frames)


if __name__ == "__main__":
    main()
