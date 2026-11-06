"""
Turn each episode into a plan (JSON) that the Blender script can render.

For every episode this:
  * builds 3D coordinates for every molecule from its SMILES (RDKit),
  * checks that the equation balances,
  * decides which reactant atom becomes which product atom,
  * times the story from the narration audio (or estimates it without audio),
  * mixes the narration lines into one WAV track for the episode.

Run with ordinary Python (needs rdkit, numpy, scipy; soundfile for audio):
    python3 prepare.py                 # all episodes
    python3 prepare.py c10_ch3_salt    # one episode
"""

import json
import math
import os
import sys

import numpy as np
from rdkit import Chem, RDLogger
from rdkit.Chem import AllChem
from scipy.optimize import linear_sum_assignment

from elements import ELEMENTS, radius
from episodes import EPISODES, PHASES

RDLogger.DisableLog("rdApp.*")

HERE = os.path.dirname(os.path.abspath(__file__))
COORD_SCALE = 1.3  # angstrom -> scene units (spreads atoms so the sticks show)
GAP_LINE = 0.45  # silence after each narration line (s)
LEAD_IN = 2.2  # seconds of title card before the first line
TAIL = 1.6
MIN_PHASE = {"approach": 3.0, "react": 4.5, "products": 3.0}
SUPERSCRIPT = str.maketrans("0123456789+-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻")


# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------


def orient(coords):
    """Centre coordinates and rotate them so the longest extent is along X,
    the next along Z (up) and the thinnest along Y (depth)."""
    c = coords - coords.mean(axis=0)
    if len(c) < 2:
        return c
    _, _, vt = np.linalg.svd(c, full_matrices=False)
    axes = np.zeros((3, 3))
    axes[: vt.shape[0]] = vt
    if np.linalg.matrix_rank(axes) < 3:
        axes[2] = np.cross(axes[0], axes[1]) if np.linalg.norm(np.cross(axes[0], axes[1])) > 1e-6 else [0, 0, 1]
    if np.linalg.det(axes) < 0:
        axes[2] *= -1
    local = c @ axes.T  # columns: principal 1, 2, 3
    return np.stack([local[:, 0], local[:, 2], local[:, 1]], axis=1)  # X, Y(depth), Z(up)


def embed_fragment(frag, flat=False):
    n = frag.GetNumAtoms()
    if n == 1:
        return np.zeros((1, 3))
    try:
        if flat:
            raise RuntimeError("flat layout requested")
        params = AllChem.ETKDGv3()
        params.randomSeed = 11
        if AllChem.EmbedMolecule(frag, params) == 0:
            try:
                AllChem.MMFFOptimizeMolecule(frag)
            except Exception:
                pass
            coords = frag.GetConformer().GetPositions()
            if np.isfinite(coords).all():
                return orient(coords)
    except Exception:
        pass
    AllChem.Compute2DCoords(frag)
    coords = frag.GetConformer().GetPositions()
    coords[:, 2] = 0
    return orient(coords)


def bond_order(bond):
    if bond.GetBondType() == Chem.BondType.DATIVE:
        return "dative"
    return {1.0: 1, 2.0: 2, 3.0: 3}.get(bond.GetBondTypeAsDouble(), 1)


def build_species(smiles):
    """Atoms (element, local xyz, map number, label, parent), bonds for one formula unit."""
    mol = Chem.MolFromSmiles(smiles, sanitize=False)
    if mol is None:
        raise ValueError(f"bad SMILES {smiles}")
    try:
        Chem.SanitizeMol(mol)
    except Exception:
        mol.UpdatePropertyCache(strict=False)
    Chem.Kekulize(mol, clearAromaticFlags=True)
    mol = Chem.AddHs(mol)
    mol.UpdatePropertyCache(strict=False)

    frag_ids = Chem.GetMolFrags(mol, asMols=False, sanitizeFrags=False)
    coords = np.zeros((mol.GetNumAtoms(), 3))
    frag_info = []
    for ids in frag_ids:
        # Build the fragment as its own molecule.
        em = Chem.RWMol()
        index = {}
        for i in ids:
            a = mol.GetAtomWithIdx(i)
            na = Chem.Atom(a.GetAtomicNum())
            na.SetFormalCharge(a.GetFormalCharge())
            na.SetNoImplicit(True)
            na.SetNumExplicitHs(0)
            na.SetNumRadicalElectrons(a.GetNumRadicalElectrons())
            index[i] = em.AddAtom(na)
        for b in mol.GetBonds():
            i, j = b.GetBeginAtomIdx(), b.GetEndAtomIdx()
            if i in index and j in index:
                em.AddBond(index[i], index[j], b.GetBondType())
        frag = em.GetMol()
        frag.UpdatePropertyCache(strict=False)
        try:
            Chem.SanitizeMol(frag, Chem.SanitizeFlags.SANITIZE_NONE)
        except Exception:
            pass
        # Square-planar complexes such as [Cu(NH3)4]2+ are drawn flat.
        flat = any(b.GetBondType() == Chem.BondType.DATIVE for b in frag.GetBonds()) and any(
            a.GetSymbol() in ("Cu", "Ni", "Pt", "Pd") for a in frag.GetAtoms()
        )
        local = embed_fragment(frag, flat) * COORD_SCALE
        for i, row in zip(ids, local):
            coords[i] = row
        charge = sum(mol.GetAtomWithIdx(i).GetFormalCharge() for i in ids)
        frag_info.append((list(ids), charge))

    # Lay multi-fragment (ionic) units out in a row, alternating charges.
    if len(frag_info) > 1:
        pos = [f for f in frag_info if f[1] > 0]
        neg = [f for f in frag_info if f[1] <= 0]
        many, few = (pos, neg) if len(pos) >= len(neg) else (neg, pos)
        order = []
        while many or few:
            if many:
                order.append(many.pop(0))
            if few:
                order.append(few.pop(0))
        x = 0.0
        placed = []
        for ids, _ in order:
            xs = [coords[i][0] - radius(el_of(mol, i)) for i in ids]
            xe = [coords[i][0] + radius(el_of(mol, i)) for i in ids]
            lo, hi = min(xs), max(xe)
            shift = x - lo
            for i in ids:
                coords[i][0] += shift
            x += (hi - lo) + 0.3
            placed.append(ids)
        coords -= coords.mean(axis=0)
        ionic_pairs = []
        for a_ids, b_ids in zip(placed, placed[1:]):
            # Link the charged atoms of neighbouring ions (closest pair first).
            def charged(ids):
                c = [i for i in ids if mol.GetAtomWithIdx(i).GetFormalCharge()]
                return c or [i for i in ids if mol.GetAtomWithIdx(i).GetAtomicNum() > 1]

            best = min(
                ((i, j) for i in charged(a_ids) for j in charged(b_ids)),
                key=lambda p: np.linalg.norm(coords[p[0]] - coords[p[1]]),
                default=None,
            )
            if best:
                ionic_pairs.append(best)
    else:
        ionic_pairs = []

    atoms = []
    for a in mol.GetAtoms():
        el = a.GetSymbol()
        if el not in ELEMENTS:
            raise ValueError(f"no display data for element {el}")
        label = el
        q = a.GetFormalCharge()
        frag_charge = next(c for ids, c in frag_info if a.GetIdx() in ids)
        if q and frag_charge:
            label = el + (str(abs(q)) if abs(q) > 1 else "").translate(SUPERSCRIPT) + ("+" if q > 0 else "-").translate(SUPERSCRIPT)
        parent = None
        if el == "H" and a.GetDegree():
            parent = a.GetNeighbors()[0].GetIdx()
        atoms.append(
            {"el": el, "local": coords[a.GetIdx()].tolist(), "map": a.GetAtomMapNum() or None, "label": label, "parent": parent}
        )
    bonds = [[b.GetBeginAtomIdx(), b.GetEndAtomIdx(), bond_order(b)] for b in mol.GetBonds()]
    bonds += [[i, j, "ionic"] for i, j in ionic_pairs]
    return atoms, bonds


def el_of(mol, i):
    return mol.GetAtomWithIdx(i).GetSymbol()


def extent(atoms):
    xs = [a["local"][0] for a in atoms]
    zs = [a["local"][2] for a in atoms]
    rs = [radius(a["el"]) for a in atoms]
    w = max(x + r for x, r in zip(xs, rs)) - min(x - r for x, r in zip(xs, rs))
    h = max(z + r for z, r in zip(zs, rs)) - min(z - r for z, r in zip(zs, rs))
    return w, h


def layout(side_species, sign):
    """Place molecule instances into rows on one side (sign -1 left, +1 right)."""
    instances = []
    for smiles, count in side_species:
        atoms, bonds = build_species(smiles)
        for k in range(count):
            instances.append({"smiles": smiles, "k": k, "atoms": atoms, "bonds": bonds, "size": extent(atoms)})
    n = len(instances)
    total_w = sum(i["size"][0] for i in instances) + 0.8 * (n - 1)
    rows = max(1, min(n, math.ceil(total_w / 7.5)))
    per_row = math.ceil(n / rows)
    grid = [instances[r * per_row : (r + 1) * per_row] for r in range(rows)]
    row_h = [max(i["size"][1] for i in row) for row in grid if row]
    total_h = sum(row_h) + 0.9 * (len(row_h) - 1)
    z = total_h / 2
    width = 0
    for row, h in zip(grid, row_h):
        w = sum(i["size"][0] for i in row) + 0.9 * (len(row) - 1)
        width = max(width, w)
        x = -w / 2
        for inst in row:
            inst["centre"] = [x + inst["size"][0] / 2, 0.0, z - h / 2]
            x += inst["size"][0] + 0.9
        z -= h + 0.9
    shift = sign * (width / 2 + 1.4)
    for inst in instances:
        inst["centre"][0] += shift
    return instances, width, total_h


# ---------------------------------------------------------------------------
# Atom mapping
# ---------------------------------------------------------------------------


def flatten(instances, cluster_sign):
    """List of atoms with world positions in the collision cluster."""
    centres = np.array([i["centre"] for i in instances])
    mid = centres.mean(axis=0)
    out = []
    for n, inst in enumerate(instances):
        base = len(out)
        cluster_c = (np.array(inst["centre"]) - mid) * 0.7 + np.array([cluster_sign * 0.6, 0, 0])
        for idx, a in enumerate(inst["atoms"]):
            out.append(
                {
                    **a,
                    "inst": n,
                    "key": (a["map"], inst["k"]) if a["map"] else None,
                    "pos": cluster_c + np.array(a["local"]),
                    "parent": base + a["parent"] if a["parent"] is not None else None,
                    "idx_in_inst": idx,
                }
            )
    return out


def map_atoms(r_atoms, p_atoms, name):
    r_el = sorted(a["el"] for a in r_atoms)
    p_el = sorted(a["el"] for a in p_atoms)
    if r_el != p_el:
        raise ValueError(f"{name}: equation does not balance: {r_el} vs {p_el}")
    p_to_r = {}
    r_keys = {a["key"]: i for i, a in enumerate(r_atoms) if a["key"]}
    for j, a in enumerate(p_atoms):
        if a["key"] and a["key"] in r_keys and r_atoms[r_keys[a["key"]]]["el"] == a["el"]:
            p_to_r[j] = r_keys[a["key"]]

    def assign(heavy):
        used = set(p_to_r.values())
        for el in sorted(set(r_el)):
            if (el == "H") == heavy:
                continue
            rs = [i for i, a in enumerate(r_atoms) if a["el"] == el and i not in used]
            ps = [j for j, a in enumerate(p_atoms) if a["el"] == el and j not in p_to_r]
            if not ps:
                continue
            cost = np.zeros((len(ps), len(rs)))
            for x, j in enumerate(ps):
                for y, i in enumerate(rs):
                    c = np.linalg.norm(p_atoms[j]["pos"] - r_atoms[i]["pos"])
                    if el == "H":
                        pp, rp = p_atoms[j]["parent"], r_atoms[i]["parent"]
                        same = pp is not None and rp is not None and p_to_r.get(pp) == rp
                        c += 0 if same else 6.0
                    cost[x, y] = c
            rows, cols = linear_sum_assignment(cost)
            for x, y in zip(rows, cols):
                p_to_r[ps[x]] = rs[y]

    assign(heavy=True)
    assign(heavy=False)
    return p_to_r


# ---------------------------------------------------------------------------
# Timeline and audio
# ---------------------------------------------------------------------------


def load_durations(ep_id):
    path = os.path.join(HERE, "audio", ep_id, "durations.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None


def timeline(ep):
    durations = load_durations(ep["id"])
    lines, phases = [], {}
    t = LEAD_IN
    n = 0
    for phase in PHASES:
        start = t
        for text in ep["story"][phase]:
            d = durations[n] if durations else max(2.0, len(text.split()) / 2.6)
            lines.append({"text": text, "start": t, "dur": d, "phase": phase, "n": n})
            t += d + GAP_LINE
            n += 1
        t = max(t, start + MIN_PHASE.get(phase, 0))
        phases[phase] = [start, t]
    return lines, phases, t + TAIL, durations is not None


def mix_audio(ep_id, lines, total):
    import soundfile as sf

    folder = os.path.join(HERE, "audio", ep_id)
    first, sr = sf.read(os.path.join(folder, "00.wav"))
    track = np.zeros(int(total * sr) + sr)
    for ln in lines:
        data, _ = sf.read(os.path.join(folder, f"{ln['n']:02d}.wav"))
        s = int(ln["start"] * sr)
        track[s : s + len(data)] += data
    out = os.path.join(folder, "episode.wav")
    sf.write(out, track[: int(total * sr)], sr)
    return out


# ---------------------------------------------------------------------------


def prepare(ep):
    r_inst, r_w, r_h = layout(ep["reactants"], -1)
    p_inst, p_w, p_h = layout(ep["products"], +1)
    r_atoms = flatten(r_inst, -1)
    p_atoms = flatten(p_inst, +1)
    p_to_r = map_atoms(r_atoms, p_atoms, ep["id"])
    r_to_p = {r: p for p, r in p_to_r.items()}

    atoms = []
    for i, a in enumerate(r_atoms):
        p = p_atoms[r_to_p[i]]
        atoms.append(
            {
                "el": a["el"],
                "r_label": a["label"],
                "p_label": p["label"],
                "r_inst": a["inst"],
                "r_local": a["local"],
                "p_inst": p["inst"],
                "p_local": p["local"],
            }
        )

    def side_bonds(instances, flat, to_tag):
        bonds, base = [], 0
        for inst in instances:
            for i, j, order in inst["bonds"]:
                a, b = to_tag(base + i), to_tag(base + j)
                bonds.append([min(a, b), max(a, b), order])
            base += len(inst["atoms"])
        return bonds

    r_bonds = side_bonds(r_inst, r_atoms, lambda i: i)
    p_bonds = side_bonds(p_inst, p_atoms, lambda j: p_to_r[j])

    electrons = []
    used_from, used_to = {}, {}
    for frm, to in ep.get("electrons", []):
        froms = [i for i, a in enumerate(atoms) if a["el"] == frm]
        tos = [i for i, a in enumerate(atoms) if a["el"] == to]
        fi = used_from.get(frm, 0)
        ti = used_to.get(to, 0)
        electrons.append([froms[fi % len(froms)], tos[ti % len(tos)]])
        used_from[frm] = fi + 1
        used_to[to] = ti + 1

    lines, phases, total, has_audio = timeline(ep)
    audio = mix_audio(ep["id"], lines, total) if has_audio else None

    span_x = max(abs(i["centre"][0]) + i["size"][0] / 2 for i in r_inst + p_inst)
    span_z = max(r_h, p_h) / 2
    plan = {
        "id": ep["id"],
        "class": ep["class"],
        "chapter": ep["chapter"],
        "title": ep["title"],
        "equation": ep["equation"],
        "condition": ep.get("condition", ""),
        "atoms": atoms,
        "r_centres": [i["centre"] for i in r_inst],
        "p_centres": [i["centre"] for i in p_inst],
        "r_bonds": r_bonds,
        "p_bonds": p_bonds,
        "electrons": electrons,
        "lines": lines,
        "phases": phases,
        "duration": total,
        "audio": audio,
        "span": [span_x + 0.6, span_z + 0.4],
    }
    os.makedirs(os.path.join(HERE, "plans"), exist_ok=True)
    with open(os.path.join(HERE, "plans", ep["id"] + ".json"), "w") as f:
        json.dump(plan, f, indent=1)
    return plan


def main():
    wanted = set(sys.argv[1:])
    for ep in EPISODES:
        if wanted and ep["id"] not in wanted:
            continue
        plan = prepare(ep)
        print(f"{ep['id']:32s} {len(plan['atoms']):3d} atoms  {plan['duration']:5.1f} s  audio={'yes' if plan['audio'] else 'no'}")


if __name__ == "__main__":
    main()
