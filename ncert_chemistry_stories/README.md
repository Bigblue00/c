# NCERT Chemistry Stories

Narrated 3D animations of the chemical equations in the NCERT syllabus, made
with Blender. Each equation is told as a short story: you meet the molecules,
watch them collide, see old bonds break, atoms move and (where it matters)
electrons jump, and watch the new molecules form. Every episode ends with a
**Key Idea** card.

Atoms keep their identity from start to finish, so a student can follow any
single atom from the reactants to the products and see that nothing is created
or destroyed.

## Videos

| File | Contents |
|------|----------|
| `videos/class_10_chemistry_stories.mp4` | Class 10 Science, chemistry chapters 1 to 4 (15 stories) |
| `videos/class_11_chemistry_stories.mp4` | Class 11 Chemistry (10 stories) |
| `videos/class_12_chemistry_stories.mp4` | Class 12 Chemistry (9 stories) |

## Episodes

**Class 10 Science**

| Chapter | Story | Equation |
|---|---|---|
| 1 Chemical Reactions and Equations | The Lime That Got Hot | CaO + H₂O → Ca(OH)₂ |
| | Breaking Water with Electricity | 2H₂O → 2H₂ + O₂ |
| | The Iron Nail's Takeover | Fe + CuSO₄ → FeSO₄ + Cu |
| | Swapping Partners | Na₂SO₄ + BaCl₂ → BaSO₄ + 2NaCl |
| | Hydrogen Steals an Oxygen | CuO + H₂ → Cu + H₂O |
| 2 Acids, Bases and Salts | When Acid Meets Base | HCl + NaOH → NaCl + H₂O |
| | The Fizz of Hydrogen | Zn + 2HCl → ZnCl₂ + H₂ |
| | Why Cakes Rise | 2NaHCO₃ → Na₂CO₃ + H₂O + CO₂ |
| 3 Metals and Non-metals | The Electron Gift | 2Na + Cl₂ → 2NaCl |
| | Fire That Welds Railways | Fe₂O₃ + 2Al → 2Fe + Al₂O₃ |
| | The Dazzling Ribbon | 2Mg + O₂ → 2MgO |
| 4 Carbon and its Compounds | The Blue Flame in Your Kitchen | CH₄ + 2O₂ → CO₂ + 2H₂O |
| | The Sweet Smell of Esters | CH₃COOH + C₂H₅OH → CH₃COOC₂H₅ + H₂O |
| | Turning Oil into Ghee | CH₂=CH₂ + H₂ → CH₃–CH₃ |
| | Chlorine Takes a Seat | CH₄ + Cl₂ → CH₃Cl + HCl |

**Class 11 Chemistry**

| Chapter | Story | Equation |
|---|---|---|
| 1 Some Basic Concepts | The One Who Was Left Out (limiting reagent) | 2H₂ + O₂ → 2H₂O, one H₂ left over |
| 4 Chemical Bonding | Sharing Is Caring | H· + H· → H–H |
| | A One-Sided Gift (coordinate bond) | NH₃ + BF₃ → H₃N→BF₃ |
| 5 Thermodynamics | Where Does the Heat Come From? | C + O₂ → CO₂, ΔH = −393.5 kJ/mol |
| 6 Equilibrium | The Two-Way Street (Haber) | N₂ + 3H₂ ⇌ 2NH₃ |
| | Hydrogen Meets Iodine | H₂ + I₂ ⇌ 2HI |
| 7 Redox Reactions | The Electron Handover | Zn + Cu²⁺ → Zn²⁺ + Cu |
| 8 Organic Chemistry: Basic Principles | An Unequal Breakup (carbocation) | (CH₃)₃C–Br → (CH₃)₃C⁺ + Br⁻ |
| 9 Hydrocarbons | Where Does the Bromine Go? (Markovnikov) | CH₃CH=CH₂ + HBr → CH₃CHBrCH₃ |
| | Benzene Keeps Its Ring (nitration) | C₆H₆ + HNO₃ → C₆H₅NO₂ + H₂O |

**Class 12 Chemistry**

| Chapter | Story | Equation |
|---|---|---|
| 2 Electrochemistry | Electricity Splits Salt Water | 2NaCl + 2H₂O → 2NaOH + H₂ + Cl₂ |
| 3 Chemical Kinetics | How Fast Does It Fall Apart? | 2N₂O₅ → 4NO₂ + O₂ |
| 4 d- and f-Block Elements | The Purple Crystal's Secret | 2KMnO₄ → K₂MnO₄ + MnO₂ + O₂ |
| 5 Coordination Compounds | Four Guards for Copper | Cu²⁺ + 4NH₃ → [Cu(NH₃)₄]²⁺ |
| 6 Haloalkanes and Haloarenes | The Backside Attack (S<sub>N</sub>2) | OH⁻ + CH₃Br → CH₃OH + Br⁻ |
| 7 Alcohols, Phenols and Ethers | Taking Water Out | C₂H₅OH → CH₂=CH₂ + H₂O |
| 8 Aldehydes, Ketones and Carboxylic Acids | Losing a Carbon (decarboxylation) | CH₃COONa + NaOH → CH₄ + Na₂CO₃ |
| 9 Amines | Amines Are Bases | CH₃NH₂ + HCl → CH₃NH₃⁺Cl⁻ |
| 10 Biomolecules | Building a Protein (peptide bond) | Glycine + Glycine → Glycylglycine + H₂O |

Some chapters have no chemical equations to animate, so they have no episode:
Class 11 Ch 2 Structure of Atom and Ch 3 Classification of Elements, and Class 12
Ch 1 Solutions.

The narration is original text written for this project. It follows the NCERT
syllabus but is not copied from the textbooks.

**How to read the pictures:** H white, C black, N blue, O red, Na purple, Cl green,
S yellow, and the metals are shiny. Grey sticks are covalent bonds, with double and
triple bonds drawn as 2 or 3 sticks. Thin gold sticks are ionic attractions and blue
sticks are coordinate (dative) bonds. Glowing yellow dots are electrons being
transferred.

## How it works

| File | What it does |
|------|--------------|
| `episodes.py` | The stories: the equation as SMILES, the narration for each part, and which electrons move |
| `narrate.py` | Speaks the narration with the offline Kokoro voice |
| `prepare.py` | Builds 3D molecules with RDKit, checks the equation balances, works out which atom goes where (Hungarian matching that keeps H on its parent atom), times everything to the speech and mixes the audio. Writes `plans/*.json` |
| `render_story.py` | Blender script that renders a plan. Still frames are reused instead of rendered again |
| `build.sh` | Runs everything and makes one MP4 per class |

```bash
pip install rdkit scipy numpy soundfile kokoro-onnx bpy   # or use the blender binary
# Voice model: kokoro-v1.0.int8.onnx and voices-v1.0.bin from
# https://github.com/thewh1teagle/kokoro-onnx/releases
python3 narrate.py --model kokoro-v1.0.int8.onnx --voices voices-v1.0.bin
./build.sh                         # all episodes (several hours on a CPU)
./build.sh c10_ch3_salt            # one episode
WIDTH=1920 HEIGHT=1080 SAMPLES=32 FPS=24 ./build.sh   # full HD on a GPU machine
```

### Adding a story

Add a dict to `EPISODES` in `episodes.py`. Write the reactants and products as
SMILES with counts, and the story lines for each part. Use atom-map numbers
(`[C:2]`) when it matters which atom ends up where. `prepare.py` will refuse an
equation that does not balance.
