"""
The story episodes, one or more per NCERT chapter that has chemical equations.

Each episode is one reaction told as a short story in five parts:
  intro     - meet the characters (the reactant molecules)
  approach  - they move toward each other
  react     - old bonds break, atoms rearrange (and electrons move)
  products  - new molecules are born
  takeaway  - the key idea a student should remember

Molecules are written as SMILES. Atom-map numbers such as [C:2] pin an atom
to the same atom in the products (use them where it matters which atom goes
where, e.g. esterification); unmapped atoms are matched automatically by the
shortest path. `electrons` lists electron transfers as (from element, to element).

The narration is original text written for this project, following the
NCERT syllabus (Class 10 Science, Class 11 and Class 12 Chemistry).
"""

EPISODES = [
    # ------------------------------------------------------------------ Class 10
    {
        "id": "c10_ch1_quicklime",
        "class": 10,
        "chapter": "Ch 1 · Chemical Reactions and Equations",
        "title": "The Lime That Got Hot",
        "equation": "CaO + H₂O → Ca(OH)₂",
        "condition": "combination reaction · heat is released",
        "reactants": [("[Ca+2].[O-2]", 1), ("O", 1)],
        "products": [("[OH-].[Ca+2].[OH-]", 1)],
        "story": {
            "intro": [
                "Meet quicklime, calcium oxide. A calcium ion and an oxide ion, holding on tightly.",
                "Nearby floats a single water molecule, minding its own business.",
            ],
            "approach": ["When water is poured on quicklime, the two rush toward each other."],
            "react": [
                "Water splits apart. Its hydrogen jumps onto the oxide ion.",
                "Now there are two hydroxide ions, and the beaker becomes hot to touch.",
            ],
            "products": ["Calcium hydroxide is born. We call it slaked lime, used to whitewash walls."],
            "takeaway": ["Two substances combining to form one new substance is a combination reaction."],
        },
    },
    {
        "id": "c10_ch1_electrolysis",
        "class": 10,
        "chapter": "Ch 1 · Chemical Reactions and Equations",
        "title": "Breaking Water with Electricity",
        "equation": "2H₂O → 2H₂ + O₂",
        "condition": "decomposition reaction · electric current",
        "reactants": [("O", 2)],
        "products": [("[H][H]", 2), ("O=O", 1)],
        "story": {
            "intro": [
                "Two water molecules sit in a beaker. Each one has an oxygen atom holding two hydrogens.",
                "Water is very stable. It will not fall apart on its own.",
            ],
            "approach": ["But then we switch on an electric current."],
            "react": [
                "The energy from electricity breaks every oxygen hydrogen bond.",
                "The hydrogens pair up with each other, and the two oxygens join hands.",
            ],
            "products": [
                "Out bubble two molecules of hydrogen gas and one molecule of oxygen gas.",
                "That is why we collect twice as much hydrogen as oxygen.",
            ],
            "takeaway": ["When one substance breaks into simpler substances, it is a decomposition reaction."],
        },
    },
    {
        "id": "c10_ch1_iron_copper",
        "class": 10,
        "chapter": "Ch 1 · Chemical Reactions and Equations",
        "title": "The Iron Nail's Takeover",
        "equation": "Fe + CuSO₄ → FeSO₄ + Cu",
        "condition": "displacement reaction · blue solution turns green",
        "reactants": [("[Fe:7]", 1), ("[Cu+2:1].[O-:3][S:2](=[O:4])(=[O:5])[O-:6]", 1)],
        "products": [("[Fe+2:7].[O-:3][S:2](=[O:4])(=[O:5])[O-:6]", 1), ("[Cu:1]", 1)],
        "electrons": [("Fe", "Cu"), ("Fe", "Cu")],
        "story": {
            "intro": [
                "An iron nail is dipped into blue copper sulphate solution.",
                "Copper is paired with the sulphate ion. Iron is all alone.",
            ],
            "approach": ["Iron is more reactive than copper, and it wants the sulphate for itself."],
            "react": [
                "Iron gives away two electrons to the copper ion.",
                "Copper becomes a plain metal atom, and iron takes its place beside sulphate.",
            ],
            "products": [
                "Now we have green iron sulphate, and a brown coat of copper on the nail.",
            ],
            "takeaway": ["A more reactive metal pushes a less reactive metal out of its compound. This is displacement."],
        },
    },
    {
        "id": "c10_ch1_double_displacement",
        "class": 10,
        "chapter": "Ch 1 · Chemical Reactions and Equations",
        "title": "Swapping Partners",
        "equation": "Na₂SO₄ + BaCl₂ → BaSO₄↓ + 2NaCl",
        "condition": "double displacement · white precipitate",
        "reactants": [
            ("[Na+].[Na+].[O-:3][S:2](=[O:4])(=[O:5])[O-:6]", 1),
            ("[Cl-].[Ba+2:1].[Cl-]", 1),
        ],
        "products": [("[Ba+2:1].[O-:3][S:2](=[O:4])(=[O:5])[O-:6]", 1), ("[Na+].[Cl-]", 2)],
        "story": {
            "intro": [
                "Two couples meet at a dance. Sodium sulphate on one side, barium chloride on the other.",
            ],
            "approach": ["Their solutions are mixed, and the ions start to mingle."],
            "react": [
                "Barium and sulphate find each other irresistible.",
                "The partners swap. Sodium goes off with chloride.",
            ],
            "products": [
                "Barium sulphate does not dissolve. It falls out as a white solid, called a precipitate.",
                "Sodium chloride stays dissolved in the water.",
            ],
            "takeaway": ["When two compounds exchange their ions, it is a double displacement reaction."],
        },
    },
    {
        "id": "c10_ch1_redox",
        "class": 10,
        "chapter": "Ch 1 · Chemical Reactions and Equations",
        "title": "Hydrogen Steals an Oxygen",
        "equation": "CuO + H₂ → Cu + H₂O",
        "condition": "redox reaction · heat",
        "reactants": [("[Cu:1]=[O:2]", 1), ("[H][H]", 1)],
        "products": [("[Cu:1]", 1), ("[OH2:2]", 1)],
        "story": {
            "intro": [
                "Black copper oxide is heated in a tube.",
                "Hydrogen gas is passed over it.",
            ],
            "approach": ["Hydrogen has its eye on copper's oxygen."],
            "react": [
                "Hydrogen pulls the oxygen away from copper.",
                "Copper loses oxygen, so it is reduced. Hydrogen gains oxygen, so it is oxidised.",
            ],
            "products": ["Shiny brown copper is left behind, and water vapour forms."],
            "takeaway": ["Oxidation and reduction always happen together. Together they are called redox."],
        },
    },
    {
        "id": "c10_ch2_neutralization",
        "class": 10,
        "chapter": "Ch 2 · Acids, Bases and Salts",
        "title": "When Acid Meets Base",
        "equation": "HCl + NaOH → NaCl + H₂O",
        "condition": "neutralization",
        "reactants": [("[H:1][Cl:2]", 1), ("[Na+:3].[OH-:4]", 1)],
        "products": [("[Na+:3].[Cl-:2]", 1), ("[OH-:4][H:1]", 1)],
        "story": {
            "intro": [
                "Hydrochloric acid carries a hydrogen it is ready to give away.",
                "Sodium hydroxide is a base. Its hydroxide ion is ready to accept a hydrogen.",
            ],
            "approach": ["The acid and the base are poured together."],
            "react": [
                "The hydrogen leaves chlorine and joins the hydroxide ion.",
                "Sodium and chloride are left to pair up.",
            ],
            "products": ["The result is common salt and water. The acid and base cancel each other out."],
            "takeaway": ["Acid plus base gives salt plus water. This is neutralization."],
        },
    },
    {
        "id": "c10_ch2_zinc_acid",
        "class": 10,
        "chapter": "Ch 2 · Acids, Bases and Salts",
        "title": "The Fizz of Hydrogen",
        "equation": "Zn + 2HCl → ZnCl₂ + H₂↑",
        "condition": "metal + acid",
        "reactants": [("[Zn]", 1), ("[H]Cl", 2)],
        "products": [("[Cl-].[Zn+2].[Cl-]", 1), ("[H][H]", 1)],
        "electrons": [("Zn", "H"), ("Zn", "H")],
        "story": {
            "intro": [
                "A granule of zinc drops into dilute hydrochloric acid.",
                "Two acid molecules surround it.",
            ],
            "approach": ["Zinc moves in to meet them."],
            "react": [
                "Zinc gives one electron to each hydrogen.",
                "The two hydrogens pair up, and zinc grabs the two chlorides.",
            ],
            "products": ["Zinc chloride forms, and bubbles of hydrogen gas rise up."],
            "takeaway": ["Metals react with acids to give a salt and hydrogen gas. A burning splinter pops in hydrogen."],
        },
    },
    {
        "id": "c10_ch2_baking_soda",
        "class": 10,
        "chapter": "Ch 2 · Acids, Bases and Salts",
        "title": "Why Cakes Rise",
        "equation": "2NaHCO₃ → Na₂CO₃ + H₂O + CO₂",
        "condition": "heat",
        "reactants": [("[Na+].[O-]C(=O)O", 2)],
        "products": [("[Na+].[O-]C(=O)[O-].[Na+]", 1), ("O", 1), ("O=C=O", 1)],
        "story": {
            "intro": ["Two baking soda units, sodium hydrogen carbonate, are mixed into cake batter."],
            "approach": ["The oven gets hot, and the particles start jostling."],
            "react": [
                "Heat breaks them apart. A hydrogen and an oxygen leave to make water.",
                "One carbon and two oxygens escape as carbon dioxide.",
            ],
            "products": [
                "Sodium carbonate stays behind, and carbon dioxide gas makes tiny bubbles.",
                "Those bubbles make the cake soft and spongy.",
            ],
            "takeaway": ["On heating, baking soda releases carbon dioxide. That gas is what makes bread and cakes rise."],
        },
    },
    {
        "id": "c10_ch3_salt",
        "class": 10,
        "chapter": "Ch 3 · Metals and Non-metals",
        "title": "The Electron Gift",
        "equation": "2Na + Cl₂ → 2NaCl",
        "condition": "ionic bond formation",
        "reactants": [("[Na]", 2), ("ClCl", 1)],
        "products": [("[Na+].[Cl-]", 2)],
        "electrons": [("Na", "Cl"), ("Na", "Cl")],
        "story": {
            "intro": [
                "Sodium is a soft metal with one lonely electron in its outer shell.",
                "Chlorine is a poisonous green gas that needs just one more electron.",
            ],
            "approach": ["They are perfect for each other."],
            "react": [
                "The chlorine molecule breaks into two atoms.",
                "Each sodium gives its outer electron to a chlorine atom.",
            ],
            "products": [
                "Sodium becomes a positive ion, chlorine a negative ion, and opposite charges attract.",
                "Together they make harmless table salt.",
            ],
            "takeaway": ["Bonds formed by transfer of electrons are ionic bonds. Metals give electrons, non-metals take them."],
        },
    },
    {
        "id": "c10_ch3_thermite",
        "class": 10,
        "chapter": "Ch 3 · Metals and Non-metals",
        "title": "Fire That Welds Railways",
        "equation": "Fe₂O₃ + 2Al → 2Fe + Al₂O₃",
        "condition": "thermite reaction · very high heat",
        "reactants": [("[O-2].[Fe+3].[O-2].[Fe+3].[O-2]", 1), ("[Al]", 2)],
        "products": [("[Fe]", 2), ("[O-2].[Al+3].[O-2].[Al+3].[O-2]", 1)],
        "electrons": [("Al", "Fe"), ("Al", "Fe")],
        "story": {
            "intro": [
                "Iron oxide, which is rust, sits next to two aluminium atoms.",
                "Aluminium is much more reactive than iron.",
            ],
            "approach": ["The mixture is ignited."],
            "react": [
                "Aluminium snatches all three oxygens from iron.",
                "So much heat is released that the iron melts.",
            ],
            "products": ["Molten iron flows out, and aluminium oxide is left behind."],
            "takeaway": ["The thermite reaction is used to join broken railway tracks. Reactive metals can reduce metal oxides."],
        },
    },
    {
        "id": "c10_ch3_magnesium",
        "class": 10,
        "chapter": "Ch 3 · Metals and Non-metals",
        "title": "The Dazzling Ribbon",
        "equation": "2Mg + O₂ → 2MgO",
        "condition": "burns with a dazzling white flame",
        "reactants": [("[Mg]", 2), ("O=O", 1)],
        "products": [("[Mg+2].[O-2]", 2)],
        "electrons": [("Mg", "O"), ("Mg", "O"), ("Mg", "O"), ("Mg", "O")],
        "story": {
            "intro": ["A magnesium ribbon is held in a flame. Two magnesium atoms meet an oxygen molecule."],
            "approach": ["The ribbon catches fire."],
            "react": [
                "The oxygen molecule splits in two.",
                "Each magnesium gives two electrons to an oxygen atom.",
            ],
            "products": ["A brilliant white light, and a white powder of magnesium oxide is left."],
            "takeaway": ["Metals combine with oxygen to form metal oxides, which are basic in nature."],
        },
    },
    {
        "id": "c10_ch4_methane",
        "class": 10,
        "chapter": "Ch 4 · Carbon and its Compounds",
        "title": "The Blue Flame in Your Kitchen",
        "equation": "CH₄ + 2O₂ → CO₂ + 2H₂O",
        "condition": "combustion · heat and light",
        "reactants": [("C", 1), ("O=O", 2)],
        "products": [("O=C=O", 1), ("O", 2)],
        "story": {
            "intro": [
                "Methane is the main gas in natural gas. One carbon holding four hydrogens.",
                "Two oxygen molecules float in the air around it.",
            ],
            "approach": ["A spark lights the gas."],
            "react": [
                "Every bond breaks apart.",
                "Carbon takes two oxygens, and the hydrogens pair up with the other two oxygens.",
            ],
            "products": ["Carbon dioxide and water vapour fly off, and a lot of heat is released."],
            "takeaway": ["Burning carbon compounds in oxygen gives carbon dioxide, water, heat and light. This is combustion."],
        },
    },
    {
        "id": "c10_ch4_ester",
        "class": 10,
        "chapter": "Ch 4 · Carbon and its Compounds",
        "title": "The Sweet Smell of Esters",
        "equation": "CH₃COOH + C₂H₅OH → CH₃COOC₂H₅ + H₂O",
        "condition": "esterification · acid catalyst",
        "reactants": [
            ("[CH3:1][C:2](=[O:3])[OH:4]", 1),
            ("[CH3:5][CH2:6][OH:7]", 1),
        ],
        "products": [("[CH3:1][C:2](=[O:3])[O:7][CH2:6][CH3:5]", 1), ("[OH2:4]", 1)],
        "story": {
            "intro": [
                "Ethanoic acid gives vinegar its sour taste.",
                "Ethanol is an alcohol.",
            ],
            "approach": ["Warm them with a little acid as a helper."],
            "react": [
                "The acid lets go of its OH group. The alcohol lets go of its hydrogen.",
                "These leftover pieces join to make a water molecule, and the two big parts link up.",
            ],
            "products": ["The new molecule is an ester. It smells sweet and fruity."],
            "takeaway": ["Acid plus alcohol gives ester plus water. Esters are used in perfumes and flavours."],
        },
    },
    {
        "id": "c10_ch4_hydrogenation",
        "class": 10,
        "chapter": "Ch 4 · Carbon and its Compounds",
        "title": "Turning Oil into Ghee",
        "equation": "CH₂=CH₂ + H₂ → CH₃–CH₃",
        "condition": "addition reaction · nickel catalyst",
        "reactants": [("[CH2:1]=[CH2:2]", 1), ("[H][H]", 1)],
        "products": [("[CH3:1][CH3:2]", 1)],
        "story": {
            "intro": [
                "Ethene has a double bond between its two carbons. It is unsaturated.",
                "A hydrogen molecule comes along.",
            ],
            "approach": ["With nickel as a catalyst, they meet."],
            "react": [
                "One part of the double bond opens up.",
                "Each carbon grabs one hydrogen atom.",
            ],
            "products": ["Now we have ethane, with only single bonds. It is saturated."],
            "takeaway": ["Adding hydrogen across a double bond is an addition reaction. It turns vegetable oils into vanaspati ghee."],
        },
    },
    {
        "id": "c10_ch4_substitution",
        "class": 10,
        "chapter": "Ch 4 · Carbon and its Compounds",
        "title": "Chlorine Takes a Seat",
        "equation": "CH₄ + Cl₂ → CH₃Cl + HCl",
        "condition": "substitution reaction · sunlight",
        "reactants": [("[CH4:1]", 1), ("[Cl:2][Cl:3]", 1)],
        "products": [("[CH3:1][Cl:2]", 1), ("[H][Cl:3]", 1)],
        "story": {
            "intro": [
                "Methane is saturated, so it is quite unreactive.",
                "But chlorine is around, and the sun is shining.",
            ],
            "approach": ["Sunlight gives them the energy to react."],
            "react": [
                "The chlorine molecule splits.",
                "One chlorine takes the place of a hydrogen on carbon. The other leaves with that hydrogen.",
            ],
            "products": ["We get chloromethane and hydrogen chloride."],
            "takeaway": ["Replacing one atom by another is a substitution reaction. Saturated hydrocarbons do this."],
        },
    },
    # ------------------------------------------------------------------ Class 11
    {
        "id": "c11_ch1_limiting",
        "class": 11,
        "chapter": "Ch 1 · Some Basic Concepts of Chemistry",
        "title": "The One Who Was Left Out",
        "equation": "2H₂ + O₂ → 2H₂O  (1 H₂ left over)",
        "condition": "limiting reagent · conservation of mass",
        "reactants": [("[H:1][H:2]", 3), ("O=O", 1)],
        "products": [("O", 2), ("[H:1][H:2]", 1)],
        "story": {
            "intro": [
                "Three hydrogen molecules and one oxygen molecule are in a flask.",
                "The equation says two hydrogens are needed for every one oxygen.",
            ],
            "approach": ["A spark sets them off."],
            "react": [
                "Two hydrogen molecules react with the oxygen.",
                "Count the atoms. Nothing is created and nothing is destroyed. They only rearrange.",
            ],
            "products": [
                "Two water molecules form. The third hydrogen molecule has no oxygen left to react with.",
            ],
            "takeaway": ["Oxygen ran out first, so oxygen is the limiting reagent. Hydrogen is in excess."],
        },
    },
    {
        "id": "c11_ch4_covalent",
        "class": 11,
        "chapter": "Ch 4 · Chemical Bonding and Molecular Structure",
        "title": "Sharing Is Caring",
        "equation": "H· + H· → H–H",
        "condition": "covalent bond · 436 kJ/mol released",
        "reactants": [("[H]", 2)],
        "products": [("[H][H]", 1)],
        "story": {
            "intro": [
                "Two hydrogen atoms, each with a single electron.",
                "Alone, each one is unstable.",
            ],
            "approach": ["As they come closer, each nucleus starts attracting the other atom's electron."],
            "react": [
                "Their orbitals overlap.",
                "The two electrons are now shared by both atoms.",
            ],
            "products": ["A hydrogen molecule is formed, with a shared pair of electrons between them."],
            "takeaway": ["A covalent bond is a pair of electrons shared between two atoms. Energy is released when it forms."],
        },
    },
    {
        "id": "c11_ch4_coordinate",
        "class": 11,
        "chapter": "Ch 4 · Chemical Bonding and Molecular Structure",
        "title": "A One-Sided Gift",
        "equation": "NH₃ + BF₃ → H₃N→BF₃",
        "condition": "coordinate bond",
        "reactants": [("[NH3:1]", 1), ("F[B:2](F)F", 1)],
        "products": [("[NH3:1]->[B:2](F)(F)F", 1)],
        "story": {
            "intro": [
                "Ammonia has a lone pair of electrons it is not using.",
                "Boron trifluoride has only six electrons around boron. It needs two more.",
            ],
            "approach": ["Ammonia approaches with its lone pair pointing at boron."],
            "react": ["Nitrogen donates both electrons of its lone pair to boron."],
            "products": ["A new bond forms, but both its electrons came from nitrogen."],
            "takeaway": ["When both shared electrons come from one atom, it is a coordinate bond."],
        },
    },
    {
        "id": "c11_ch5_enthalpy",
        "class": 11,
        "chapter": "Ch 5 · Thermodynamics",
        "title": "Where Does the Heat Come From?",
        "equation": "C + O₂ → CO₂   ΔH = −393.5 kJ/mol",
        "condition": "enthalpy of combustion",
        "reactants": [("[C]", 1), ("O=O", 1)],
        "products": [("O=C=O", 1)],
        "story": {
            "intro": [
                "A carbon atom from a piece of coal meets an oxygen molecule.",
                "Every chemical bond stores energy.",
            ],
            "approach": ["They need a little push to begin. This is the activation energy."],
            "react": [
                "Breaking the oxygen-oxygen bond costs energy.",
                "But forming two strong carbon-oxygen double bonds releases much more.",
            ],
            "products": ["Carbon dioxide forms, and the extra energy escapes as heat."],
            "takeaway": ["Delta H is negative, so the reaction is exothermic. 393.5 kilojoules are released per mole."],
        },
    },
    {
        "id": "c11_ch6_haber",
        "class": 11,
        "chapter": "Ch 6 · Equilibrium",
        "title": "The Two-Way Street",
        "equation": "N₂ + 3H₂ ⇌ 2NH₃",
        "condition": "Haber process · iron catalyst · high pressure",
        "reactants": [("N#N", 1), ("[H][H]", 3)],
        "products": [("N", 2)],
        "story": {
            "intro": [
                "Nitrogen holds itself together with a very strong triple bond.",
                "Three hydrogen molecules are waiting.",
            ],
            "approach": ["High pressure squeezes them together on an iron catalyst."],
            "react": [
                "The triple bond finally breaks.",
                "Each nitrogen collects three hydrogen atoms.",
            ],
            "products": [
                "Two ammonia molecules form. But some ammonia breaks back into nitrogen and hydrogen.",
                "When the forward and backward rates are equal, we reach equilibrium.",
            ],
            "takeaway": ["Fewer gas molecules are on the product side, so higher pressure shifts equilibrium toward ammonia. This is Le Chatelier's principle."],
        },
    },
    {
        "id": "c11_ch6_hi",
        "class": 11,
        "chapter": "Ch 6 · Equilibrium",
        "title": "Hydrogen Meets Iodine",
        "equation": "H₂ + I₂ ⇌ 2HI",
        "condition": "reversible reaction · Kc",
        "reactants": [("[H][H]", 1), ("II", 1)],
        "products": [("[H]I", 2)],
        "story": {
            "intro": ["A hydrogen molecule and a violet iodine molecule are sealed in a hot flask."],
            "approach": ["They collide."],
            "react": [
                "Both molecules break apart.",
                "Each hydrogen pairs with an iodine.",
            ],
            "products": ["Two molecules of hydrogen iodide form. Some of them break back into hydrogen and iodine."],
            "takeaway": ["At equilibrium, Kc equals HI concentration squared, divided by hydrogen times iodine concentrations."],
        },
    },
    {
        "id": "c11_ch7_redox",
        "class": 11,
        "chapter": "Ch 7 · Redox Reactions",
        "title": "The Electron Handover",
        "equation": "Zn + Cu²⁺ → Zn²⁺ + Cu",
        "condition": "oxidation: Zn loses 2e⁻ · reduction: Cu²⁺ gains 2e⁻",
        "reactants": [("[Zn:1]", 1), ("[Cu+2:2]", 1)],
        "products": [("[Zn+2:1]", 1), ("[Cu:2]", 1)],
        "electrons": [("Zn", "Cu"), ("Zn", "Cu")],
        "story": {
            "intro": [
                "A zinc atom stands next to a copper ion in solution.",
                "Zinc gives away electrons more easily than copper does.",
            ],
            "approach": ["They come close enough to trade."],
            "react": [
                "Zinc hands over two electrons. Zinc is oxidised.",
                "The copper ion accepts them. Copper is reduced.",
            ],
            "products": ["Zinc becomes a zinc ion, and copper becomes a neutral metal atom."],
            "takeaway": ["Oxidation is loss of electrons. Reduction is gain of electrons. Remember: OIL RIG."],
        },
    },
    {
        "id": "c11_ch8_heterolysis",
        "class": 11,
        "chapter": "Ch 8 · Organic Chemistry: Basic Principles",
        "title": "An Unequal Breakup",
        "equation": "(CH₃)₃C–Br → (CH₃)₃C⁺ + Br⁻",
        "condition": "heterolytic cleavage · carbocation",
        "reactants": [("C[C:1](C)(C)[Br:2]", 1)],
        "products": [("C[C+:1](C)C", 1), ("[Br-:2]", 1)],
        "story": {
            "intro": ["Tertiary butyl bromide. A carbon with three methyl groups and one bromine."],
            "approach": ["In a polar solvent, the carbon-bromine bond starts to stretch."],
            "react": ["Bromine is more electronegative. When the bond breaks, bromine takes both electrons."],
            "products": [
                "Bromine leaves as a negative bromide ion.",
                "The carbon becomes positive. This is a carbocation, and its three methyl groups help stabilise it.",
            ],
            "takeaway": ["When a bond breaks and one atom keeps both electrons, it is heterolytic cleavage."],
        },
    },
    {
        "id": "c11_ch9_markovnikov",
        "class": 11,
        "chapter": "Ch 9 · Hydrocarbons",
        "title": "Where Does the Bromine Go?",
        "equation": "CH₃CH=CH₂ + HBr → CH₃CHBrCH₃",
        "condition": "Markovnikov's rule",
        "reactants": [("[CH3:1][CH:2]=[CH2:3]", 1), ("[H:4][Br:5]", 1)],
        "products": [("[CH3:1][CH:2]([Br:5])[CH2:3][H:4]", 1)],
        "story": {
            "intro": [
                "Propene has a double bond at one end.",
                "Hydrogen bromide wants to add across that double bond.",
            ],
            "approach": ["But which carbon gets the hydrogen, and which gets the bromine?"],
            "react": [
                "The hydrogen goes to the end carbon, which already has more hydrogens.",
                "The bromine goes to the middle carbon.",
            ],
            "products": ["The product is 2-bromopropane."],
            "takeaway": ["Markovnikov's rule: the negative part adds to the carbon with fewer hydrogens."],
        },
    },
    {
        "id": "c11_ch9_nitration",
        "class": 11,
        "chapter": "Ch 9 · Hydrocarbons",
        "title": "Benzene Keeps Its Ring",
        "equation": "C₆H₆ + HNO₃ → C₆H₅NO₂ + H₂O",
        "condition": "nitration · conc. H₂SO₄",
        "reactants": [
            ("[cH:1]1[cH:2][cH:3][cH:4][cH:5][cH:6]1", 1),
            ("[OH:10][N+:11](=[O:12])[O-:13]", 1),
        ],
        "products": [
            ("[c:1]1([N+:11](=[O:12])[O-:13])[cH:2][cH:3][cH:4][cH:5][cH:6]1", 1),
            ("[OH2:10]", 1),
        ],
        "story": {
            "intro": [
                "Benzene is a ring of six carbons with a very stable cloud of electrons.",
                "Nitric acid carries a nitro group.",
            ],
            "approach": ["Concentrated sulphuric acid helps make the nitro group ready to attack."],
            "react": [
                "The nitro group attaches to the ring, and one hydrogen is pushed out.",
                "That hydrogen joins the OH from nitric acid to form water.",
            ],
            "products": ["Nitrobenzene forms, and the benzene ring stays whole."],
            "takeaway": ["Benzene prefers substitution over addition, because that keeps its stable aromatic ring."],
        },
    },
    # ------------------------------------------------------------------ Class 12
    {
        "id": "c12_ch2_brine",
        "class": 12,
        "chapter": "Ch 2 · Electrochemistry",
        "title": "Electricity Splits Salt Water",
        "equation": "2NaCl + 2H₂O → 2NaOH + H₂ + Cl₂",
        "condition": "electrolysis of brine · chlor-alkali process",
        "reactants": [("[Na+].[Cl-]", 2), ("O", 2)],
        "products": [("[Na+].[OH-]", 2), ("[H][H]", 1), ("ClCl", 1)],
        "story": {
            "intro": [
                "Brine is salt dissolved in water. Here are two sodium chloride units and two water molecules.",
            ],
            "approach": ["An electric current flows through the solution."],
            "react": [
                "At the anode, chloride ions lose electrons and pair up as chlorine gas.",
                "At the cathode, water gains electrons and releases hydrogen gas.",
            ],
            "products": ["Sodium hydroxide stays in the solution."],
            "takeaway": ["One process gives three useful products: sodium hydroxide, chlorine and hydrogen."],
        },
    },
    {
        "id": "c12_ch3_n2o5",
        "class": 12,
        "chapter": "Ch 3 · Chemical Kinetics",
        "title": "How Fast Does It Fall Apart?",
        "equation": "2N₂O₅ → 4NO₂ + O₂",
        "condition": "first order reaction · rate = k[N₂O₅]",
        "reactants": [("[O-][N+](=O)O[N+](=O)[O-]", 2)],
        "products": [("O=N[O]", 4), ("O=O", 1)],
        "story": {
            "intro": [
                "Two molecules of dinitrogen pentoxide.",
                "They are unstable and slowly decompose.",
            ],
            "approach": ["The question is not if, but how fast."],
            "react": [
                "The central oxygen bridges break.",
                "Four nitrogen dioxide molecules form, and two oxygen atoms pair up.",
            ],
            "products": ["Brown nitrogen dioxide gas and oxygen are released."],
            "takeaway": ["The rate depends only on the concentration of N2O5 raised to the power one. It is a first order reaction."],
        },
    },
    {
        "id": "c12_ch4_permanganate",
        "class": 12,
        "chapter": "Ch 4 · The d- and f-Block Elements",
        "title": "The Purple Crystal's Secret",
        "equation": "2KMnO₄ → K₂MnO₄ + MnO₂ + O₂",
        "condition": "heating at 513 K",
        "reactants": [("[K+].[O-][Mn](=O)(=O)=O", 2)],
        "products": [("[K+].[O-][Mn](=O)(=O)[O-].[K+]", 1), ("O=[Mn]=O", 1), ("O=O", 1)],
        "story": {
            "intro": [
                "Potassium permanganate forms beautiful purple crystals.",
                "Manganese here is in the plus seven oxidation state.",
            ],
            "approach": ["The crystals are heated strongly."],
            "react": [
                "Two permanganate units break apart and share out their oxygens.",
                "Two oxygen atoms escape together.",
            ],
            "products": ["We get green potassium manganate, black manganese dioxide, and oxygen gas."],
            "takeaway": ["Transition metals like manganese show many oxidation states. Here plus seven becomes plus six and plus four."],
        },
    },
    {
        "id": "c12_ch5_complex",
        "class": 12,
        "chapter": "Ch 5 · Coordination Compounds",
        "title": "Four Guards for Copper",
        "equation": "Cu²⁺ + 4NH₃ → [Cu(NH₃)₄]²⁺",
        "condition": "ligands · coordination number 4 · deep blue",
        "reactants": [("[Cu+2]", 1), ("N", 4)],
        "products": [("N->[Cu+2](<-N)(<-N)<-N", 1)],
        "story": {
            "intro": [
                "A copper ion floats in pale blue solution.",
                "Four ammonia molecules arrive, each carrying a lone pair.",
            ],
            "approach": ["They surround the copper ion."],
            "react": ["Each ammonia donates its lone pair to copper, forming a coordinate bond."],
            "products": [
                "The tetraammine copper two complex forms, with ammonia at the four corners of a square.",
                "The solution turns a deep, beautiful blue.",
            ],
            "takeaway": ["Ammonia here is a ligand, and copper has a coordination number of four."],
        },
    },
    {
        "id": "c12_ch6_sn2",
        "class": 12,
        "chapter": "Ch 6 · Haloalkanes and Haloarenes",
        "title": "The Backside Attack",
        "equation": "OH⁻ + CH₃Br → CH₃OH + Br⁻",
        "condition": "Sₙ2 reaction · inversion of configuration",
        "reactants": [("[OH-:1]", 1), ("[CH3:2][Br:3]", 1)],
        "products": [("[CH3:2][OH:1]", 1), ("[Br-:3]", 1)],
        "story": {
            "intro": [
                "Bromomethane has a carbon attached to a bromine.",
                "A hydroxide ion is looking for a carbon to attack.",
            ],
            "approach": ["It attacks from the side opposite to bromine. The backside."],
            "react": [
                "As the new carbon-oxygen bond forms, the carbon-bromine bond breaks at the same time.",
                "The molecule flips inside out, like an umbrella in the wind.",
            ],
            "products": ["Methanol forms and a bromide ion leaves."],
            "takeaway": ["S N 2 happens in one step, with two molecules involved, and the configuration inverts."],
        },
    },
    {
        "id": "c12_ch7_dehydration",
        "class": 12,
        "chapter": "Ch 7 · Alcohols, Phenols and Ethers",
        "title": "Taking Water Out",
        "equation": "C₂H₅OH → CH₂=CH₂ + H₂O",
        "condition": "conc. H₂SO₄ · 443 K",
        "reactants": [("[CH3:1][CH2:2][OH:3]", 1)],
        "products": [("[CH2:1]=[CH2:2]", 1), ("[OH2:3]", 1)],
        "story": {
            "intro": ["An ethanol molecule is heated with concentrated sulphuric acid."],
            "approach": ["The acid helps the OH group get ready to leave."],
            "react": [
                "The OH group leaves along with a hydrogen from the next carbon.",
                "The two carbons, each with a free hand, form a double bond.",
            ],
            "products": ["Ethene gas and a water molecule are formed."],
            "takeaway": ["Removing water from an alcohol gives an alkene. This is dehydration."],
        },
    },
    {
        "id": "c12_ch8_decarboxylation",
        "class": 12,
        "chapter": "Ch 8 · Aldehydes, Ketones and Carboxylic Acids",
        "title": "Losing a Carbon",
        "equation": "CH₃COONa + NaOH → CH₄ + Na₂CO₃",
        "condition": "decarboxylation · soda lime · heat",
        "reactants": [
            ("[CH3:1][C:2](=[O:3])[O-:4].[Na+:5]", 1),
            ("[Na+:6].[OH-:7]", 1),
        ],
        "products": [("[CH4:1]", 1), ("[Na+:5].[O-:4][C:2](=[O:3])[O-:7].[Na+:6]", 1)],
        "story": {
            "intro": [
                "Sodium ethanoate is the salt of a carboxylic acid.",
                "It is heated with soda lime, which supplies sodium hydroxide.",
            ],
            "approach": ["The two meet in the hot mixture."],
            "react": [
                "The carboxyl group is cut away from the methyl group.",
                "The methyl group picks up a hydrogen from the hydroxide.",
            ],
            "products": ["Methane gas escapes, and sodium carbonate is left behind."],
            "takeaway": ["Removing carbon dioxide from a carboxylic acid salt is decarboxylation. The chain gets one carbon shorter."],
        },
    },
    {
        "id": "c12_ch9_amine",
        "class": 12,
        "chapter": "Ch 9 · Amines",
        "title": "Amines Are Bases",
        "equation": "CH₃NH₂ + HCl → CH₃NH₃⁺Cl⁻",
        "condition": "basic character of amines",
        "reactants": [("C[NH2:1]", 1), ("[H:2][Cl:3]", 1)],
        "products": [("C[NH2+:1][H:2].[Cl-:3]", 1)],
        "story": {
            "intro": [
                "Methylamine has a nitrogen with a lone pair of electrons.",
                "Hydrochloric acid has a hydrogen to give away.",
            ],
            "approach": ["The lone pair reaches out for the hydrogen."],
            "react": ["Nitrogen uses its lone pair to bond with the hydrogen. Chlorine leaves as chloride."],
            "products": ["Methylammonium chloride forms, a salt."],
            "takeaway": ["The lone pair on nitrogen makes amines basic. They react with acids to form salts."],
        },
    },
    {
        "id": "c12_ch10_peptide",
        "class": 12,
        "chapter": "Ch 10 · Biomolecules",
        "title": "Building a Protein",
        "equation": "Glycine + Glycine → Glycylglycine + H₂O",
        "condition": "peptide bond · –CO–NH–",
        "reactants": [
            ("[NH2:1][CH2:2][C:3](=[O:4])[OH:5]", 1),
            ("[NH2:6][CH2:7][C:8](=[O:9])[OH:10]", 1),
        ],
        "products": [
            ("[NH2:1][CH2:2][C:3](=[O:4])[NH:6][CH2:7][C:8](=[O:9])[OH:10]", 1),
            ("[OH2:5]", 1),
        ],
        "story": {
            "intro": [
                "Glycine is the simplest amino acid, a building block of proteins.",
                "Each one has an amino group on one end and an acid group on the other.",
            ],
            "approach": ["Two glycines line up, head to tail."],
            "react": [
                "The acid end of the first loses its OH. The amino end of the second loses a hydrogen.",
                "Out comes a water molecule, and a carbon-nitrogen bond links them.",
            ],
            "products": ["This new link is a peptide bond. The molecule is a dipeptide."],
            "takeaway": ["Join hundreds of amino acids with peptide bonds, and you get a protein."],
        },
    },
]

PHASES = ["intro", "approach", "react", "products", "takeaway"]


def by_id():
    return {e["id"]: e for e in EPISODES}
