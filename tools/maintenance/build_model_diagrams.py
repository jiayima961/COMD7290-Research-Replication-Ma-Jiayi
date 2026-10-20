"""Build editable Mermaid and SVG model diagrams from one node registry."""
from pathlib import Path
import csv
import html
import json
import re
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
FIGS = DOCS / "figures"
FIGS.mkdir(exist_ok=True)
MATRIX = list(csv.DictReader((DOCS / "hypothesis_matrix.csv").open(encoding="utf-8-sig")))
NODES = []


def node(identifier, label, figure, models, equation, scripts, source, unit, raw=None):
    ids = [r["row_id"] for r in MATRIX if r["analysis_id"] in models]
    if any(m in models for m in ["M2", "M3"]):
        ids += ["C3", "P2"]
    if "M1" in models:
        ids += ["C1", "C2", "P1", "S1"]
    NODES.append(dict(node_id=identifier, figure_id=figure, label=label,
                      construct_or_parameter=label.replace("\n", " "),
                      measurement_or_distribution=unit, equation_or_syntax=equation,
                      analysis_id=" | ".join(models), matrix_row_ids=" | ".join(dict.fromkeys(ids)),
                      planned_script_path=" | ".join(scripts), source_locator=source,
                      implementation_status="Executed model, documentation reconstructed on 2026-10-20",
                      data_variables=raw or "Computational parameter or specification note"))


def registry():
    src = "sources/author_code/MedCon_Civility_an.do, both recode blocks and Analysis 4. docs/execution_specification.md."
    prep = ["analysis/prepare_replication.py"]
    node("POL", "Political system\nraw 1 consensus / 2 majoritarian / 3 mixed\nanalysis 1 consensus / 2 mixed / 3 majoritarian", "Figure 1", ["M1", "M2", "M3"],
         "polsys.map({1:1,2:3,3:2}); reference=consensus", prep, src, "Observed nominal country classification attached to item", "polsys")
    node("SEC", "Division over secularism\nraw 1 contested / 2 stable\nanalysis 1 stable / 2 contested", "Figure 1", ["M1", "M2", "M3"],
         "socdiv.map({1:2,2:1}); reference=stable", prep, src, "Observed binary nominal country classification attached to item", "socdiv")
    node("MED", "Media category\nraw 1 blog / 2 newspaper / 3 website\nanalysis 1 blog / 2 website / 3 newspaper", "Figure 1", ["M1", "M2", "M3"],
         "mediatype.map({1:1,2:3,3:2}); reference=blog", prep, src, "Observed nominal item classification", "mediatype")
    node("X", "Five 0/1 indicators, in this order\nX = [I(polsys=2), I(polsys=3), I(socdiv=2), I(mediatype=2), I(mediatype=3)]\nOrder: mixed, majoritarian, contested, website, newspaper\nCodes above are analytical codes. Bases are consensus, stable secularism and blogs.",
         "Figures 1 and 2", ["M1", "M2", "M3"], "analysis.prepare_replication.design() and ordinal_reproduction.design(), five fixed slopes, no centering", prep + ["analysis/ordinal_reproduction.py"], src,
         "Derived indicator vector, not five new measured constructs", "polsys | socdiv | mediatype")
    for mid, out, name in [("M2", "actrefoutbin", "Outrage"), ("M3", "actrefrecbin", "Recognition")]:
        n = mid[-1]
        scripts = ["analysis/run_binary_models.py", "analysis/nested_logit.py"]
        node(mid + "U", f"u{n}_j ~ Normal(0, sigma{n}_item^2)\nItem-specific random intercept\nGroup key: text_id", "Figure 1", [mid],
             f"u_j~N(0,sigma_item^2), fitted separately for {out}", scripts, src,
             "Gaussian random effect at news-item level, j", "text_id")
        node(mid + "V", f"v{n}_aj ~ Normal(0, sigma{n}_actor^2)\nOriginating actor/statement random intercept\nact_id = text_id + '_' + akteur_id", "Figure 1", [mid],
             "act_id=text_id+'_'+akteur_id; v_aj~N(0,sigma_actor^2)", prep + scripts, src,
             "Gaussian random effect nested in item, a within j", "text_id | akteur_id | act_id")
        node(mid + "ETA", f"eta{n}_raj = beta{n}_0 + X_j beta{n}\n                         + u{n}_j + v{n}_aj\nFive fixed slopes plus a fixed intercept", "Figure 1", [mid],
             f"logit[P({out}=1|u_j,v_aj)]=beta0+X_j beta+u_j+v_aj", scripts, src,
             "Conditional linear predictor at directed-reference level", out)
        node(mid + "Y", f"{name}: {out}\nY{n}_raj ~ Bernoulli(p{n}_raj)\nlogit(p{n}_raj) = eta{n}_raj\n0 absent / 1 explicit presence", "Figure 1", [mid],
             f"Separate Bernoulli logit likelihood for {out}", scripts, src,
             "Observed binary reference outcome", out)
    node("CONFIG", "Separate fits with distinct beta and variance parameters. No estimated cross-outcome covariance.\nWithin each model, item and actor random effects are independent and independent of X.\nFrequentist marginal ML, recursive mean/variance adaptive GH, 7 nodes per random intercept.\nObserved-information covariance and normal 95% Wald intervals. No priors, weights or imputation.\nNo centering, interactions, indirect paths or random slopes. Country is not a random level.\nNo missing required outcome, grouping or predictor values in the author-prepared analysis sample.\nInput: data/original/MedCon_Civility_actref.dta, with the source recodes shown above.",
         "Figure 1", ["M2", "M3"], "melogit Y i.polsys i.socdiv i.mediatype || text_id: || act_id:, intpoints(7)",
         ["analysis/nested_logit.py", "analysis/run_binary_models.py"], src,
         "Estimation and dependence restrictions, not observed variables")
    node("M1ETA", "eta_i = X_i beta1\nFive fixed slopes\nNo separate free intercept or random effects", "Figure 2", ["M1"],
         "eta_i=X_i beta, five fixed slopes", ["analysis/ordinal_reproduction.py"],
         "Author Analysis 2 ologit tone i.polsys i.socdiv i.mediatype", "Computational item-level predictor", "polsys | socdiv | mediatype")
    node("M1C", "Four ordered cutpoints\nc0 < c1 < c2 < c3\nSlopes common across all four thresholds", "Figure 2", ["M1"],
         "Four ordered thresholds, no separate free intercept", ["analysis/ordinal_reproduction.py"], "Author Analysis 2 ologit and Table 3", "Ordered identification/cumulative-link parameters")
    node("M1Y", "Item tone: archive 1-5 is recoded to 0-4\nlogit Pr(tone_i > k) = eta_i - c_k, k = 0,1,2,3\nPr(tone_i = k) = F(c_k - eta_i) - F(c_(k-1) - eta_i), F = logistic CDF\nFive ordered categories, with outer cutpoints at minus/plus infinity", "Figure 2", ["M1"],
         "Proportional-odds ordinal logistic likelihood with four thresholds and five slopes", ["analysis/ordinal_reproduction.py"],
         "Codebook 1 section 1.11 and author Analysis 2", "Observed ordinal item outcome, not a continuous or binary regression", "tone")
    node("M1CONFIG", "N = 1700 news items. The reference-row copy of tone is not a separate M1 sample.\nUnweighted maximum likelihood, observed information, normal 95% Wald intervals.\nNo random effects, centering, interactions, mediation, priors or imputation.\nC1 retains the original assumption diagnostics, C2 the original alternative links, P1 the probabilities.\nUnmeasured compromise, identity boundaries and editorial gatekeeping are proposed mechanisms.\nThey are not estimated mediators in M1, M2 or M3.\nInput: data/original/MedCon_Civility_item.dta, with item likelihood independence assumed.", "Figure 2", ["M1"],
         "ologit tone i.polsys i.socdiv i.mediatype", ["analysis/ordinal_reproduction.py"],
         "Author Analysis 2 and docs/execution_specification.md", "Estimation and interpretation restrictions")


def label(n):
    return next(r["label"] for r in NODES if r["node_id"] == n)


def mermaid():
    lines = ["%% Figure 1", "%% Separate three-level models of directed-reference outrage and recognition", "%% Observational window August 2015-July 2016, no longitudinal wave/lag structure.", "flowchart TB"]
    for n in ["POL", "SEC", "MED", "X"]:
        lines.append(f'  {n}["{label(n).replace(chr(10), "<br/>")}"]')
    lines += ["  POL --> X", "  SEC --> X", "  MED --> X"]
    for mid, outcome in [("M2", "Outrage"), ("M3", "Recognition")]:
        lines += [f'  subgraph {mid}PANEL["{mid}: {outcome}, fitted separately"]',
                  f'    subgraph {mid}L3["Level 3: item j, 1183 items"]',
                  f'      {mid}U["{label(mid + "U").replace(chr(10), "<br/>")}"]',
                  f'      subgraph {mid}L2["Level 2: originating actor/statement a within j, 2453 groups"]',
                  f'        {mid}V["{label(mid + "V").replace(chr(10), "<br/>")}"]',
                  f'        subgraph {mid}L1["Level 1: directed reference r, 3770 rows"]',
                  f'          {mid}ETA["{label(mid + "ETA").replace(chr(10), "<br/>")}"]',
                  f'          {mid}Y["{label(mid + "Y").replace(chr(10), "<br/>")}"]',
                  "        end", "      end", "    end", "  end", f"  X --> {mid}ETA", f"  {mid}U --> {mid}ETA", f"  {mid}V --> {mid}ETA", f"  {mid}ETA --> {mid}Y"]
    lines += [f'  CONFIG["{label("CONFIG").replace(chr(10), "<br/>")}"]',
              "%% Note. AI-assisted original reconstruction from author syntax and verified input metadata.",
              "%% Student review remains pending. No claim of pre-AI student authorship or pre-estimation approval.",
              "%% Original software build/internal finite-node details remain incompletely pinned. See execution_specification.md."]
    (DOCS / "model_diagram.mmd").write_text("\n".join(lines) + "\n", encoding="utf-8")
    lines = ["%% Figure 2", "%% Item-level proportional-odds model of outrage tone", "flowchart TB"]
    for n in ["X", "M1ETA", "M1C", "M1Y", "M1CONFIG"]:
        lines.append(f'  {n}["{label(n).replace(chr(10), "<br/>")}"]')
    lines += ["  X --> M1ETA", "  M1ETA --> M1Y", "  M1C --> M1Y",
              "%% Note. X uses the source recodes displayed in Figure 1. AI-assisted documentation, student review pending."]
    (DOCS / "model_diagram_m1.mmd").write_text("\n".join(lines) + "\n", encoding="utf-8")


def svg(ordinal=False):
    width, height = 1450, 1170 if ordinal else 1750
    scale = 2
    raster = Image.new("RGB", (width * scale, height * scale), "white")
    painter = ImageDraw.Draw(raster)
    def font(size, bold=False, italic=False):
        fname = "arialbi.ttf" if bold and italic else "arialbd.ttf" if bold else "ariali.ttf" if italic else "arial.ttf"
        return ImageFont.truetype(str(Path("C:/Windows/Fonts") / fname), int(size * scale))
    lines = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
             '<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9" fill="#222"/></marker></defs>',
             '<rect width="100%" height="100%" fill="white"/>',
             '<g font-family="Arial, sans-serif" fill="#111">']
    placements = []

    def text(x, y, words, size=23, bold=False, italic=False):
        lines.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{"bold" if bold else "normal"}" font-style="{"italic" if italic else "normal"}">{html.escape(words)}</text>')
        painter.text((x * scale, y * scale), words, font=font(size, bold, italic), fill="#111", anchor="ls")

    def box(n, x, y, w, h, size=22):
        def wrap(size):
            result = []
            for original in label(n).splitlines():
                current = ""
                for word in original.split():
                    candidate = (current + " " + word).strip()
                    if current and font(size).getlength(candidate) / scale > w - 32:
                        result.append(current)
                        current = word
                    else:
                        current = candidate
                result.append(current)
            return result
        parts = wrap(size)
        while 28 + (len(parts) - 1) * (size + 9) + 10 > h and size > 17:
            size -= 1
            parts = wrap(size)
        assert 28 + (len(parts) - 1) * (size + 9) + 10 <= h, (n, "text too tall")
        assert all(font(size).getlength(p) / scale <= w - 32 for p in parts), (n, "text too wide")
        lines.append(f'<g id="{n}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="white" stroke="#222" stroke-width="1.7"/>')
        painter.rounded_rectangle((x * scale, y * scale, (x + w) * scale, (y + h) * scale), radius=7 * scale, fill="white", outline="#222", width=3)
        for i, part in enumerate(parts):
            text(x + 16, y + 28 + i * (size + 9), part, size)
        lines.append("</g>")
        placements.append(dict(node_id=n, x=x, y=y, width=w, height=h, font_size=size,
                               text_line_count=len(parts), text_within_box=True))

    def path(d):
        lines.append(f'<path d="{d}" fill="none" stroke="#222" stroke-width="2" marker-end="url(#arrow)"/>')
        numbers = [float(v) for v in re.findall(r"-?\d+(?:\.\d+)?", d)]
        points = list(zip(numbers[::2], numbers[1::2]))
        painter.line([(x * scale, y * scale) for x, y in points], fill="#222", width=4)
        a, b = points[-2:]
        angle = math.atan2(b[1] - a[1], b[0] - a[0])
        triangle = [b, (b[0] - 14 * math.cos(angle) + 6 * math.sin(angle), b[1] - 14 * math.sin(angle) - 6 * math.cos(angle)),
                    (b[0] - 14 * math.cos(angle) - 6 * math.sin(angle), b[1] - 14 * math.sin(angle) + 6 * math.cos(angle))]
        painter.polygon([(x * scale, y * scale) for x, y in triangle], fill="#222")

    def band(y, h, title):
        lines.append(f'<rect x="35" y="{y}" width="1380" height="{h}" fill="#f3f3f3" stroke="#aaa"/>')
        painter.rectangle((35 * scale, y * scale, 1415 * scale, (y + h) * scale), fill="#f3f3f3", outline="#aaa", width=2)
        for i, part in enumerate(title.split("\n")):
            text(52, y + 34 + i * 28, part, 20, i == 0)

    text(40, 42, "Figure 2" if ordinal else "Figure 1", 28, True)
    text(40, 83, "Item-level proportional-odds model of outrage tone" if ordinal else "Separate three-level models of directed-reference outrage and recognition", 28, italic=True)
    if ordinal:
        text(40, 124, "The five indicators use the coding and reference categories in Figure 1.", 23)
        box("X", 55, 160, 1340, 165, 21)
        box("M1ETA", 75, 430, 675, 130, 25)
        box("M1C", 805, 430, 570, 130, 25)
        path("M725 325 L725 375 L412 375 L412 428")
        path("M412 560 L412 640")
        path("M1090 560 L1090 640")
        box("M1Y", 75, 645, 1300, 170, 24)
        box("M1CONFIG", 55, 860, 1340, 235, 23)
        text(40, 1140, "Note. Original AI-assisted reconstruction from author code, not a copied published figure. Student review pending.", 19)
    else:
        text(40, 112, "Observational window: August 2015-July 2016. No repeated-wave or lag structure.", 20)
        box("POL", 40, 130, 445, 135, 21)
        box("SEC", 502, 130, 445, 135, 21)
        box("MED", 964, 130, 445, 135, 21)
        for x in [263, 725, 1187]:
            path(f"M{x} 265 L{x} 320")
        box("X", 55, 325, 1340, 165, 21)
        text(195, 548, "M2: outrage", 28, True)
        text(810, 548, "M3: recognition", 28, True)
        band(585, 175, "Level 3\nNews item j\n1183 items")
        band(780, 175, "Level 2\nActor a\nwithin item j\n2453 groups")
        band(975, 440, "Level 1\nDirected\nreference r\n3770 rows")
        for mid, x in [("M2", 195), ("M3", 810)]:
            box(mid + "U", x, 630, 560, 110, 23)
            box(mid + "V", x, 825, 560, 110, 22)
            box(mid + "ETA", x, 1040, 560, 135, 24)
            box(mid + "Y", x, 1230, 560, 147, 24)
            path(f"M{x+280} 935 L{x+280} 1038")
            path(f"M{x+35} 740 L{x+35} 766 L{x-23} 766 L{x-23} 1105 L{x-2} 1105")
            path(f"M{x+280} 1175 L{x+280} 1228")
        path("M70 490 L70 550 L43 550 L43 1130 L193 1130")
        path("M1395 490 L1395 1130 L1372 1130")
        box("CONFIG", 55, 1460, 1340, 215, 21)
        text(40, 1710, "Note. Original AI-assisted reconstruction from author code and inspected archive metadata. Student review pending.", 19)
        text(40, 1736, "Historical Stata build and internal quadrature details remain incompletely pinned. See execution_specification.md.", 19)
    lines += ["</g></svg>"]
    name = "model_diagram_m1" if ordinal else "model_diagram"
    (FIGS / (name + ".svg")).write_text("\n".join(lines), encoding="utf-8")
    raster.save(FIGS / (name + ".png"), dpi=(300, 300))
    return placements


def guide():
    text = """# Model diagrams and equation-to-code map

Updated on 20 October 2026. These are original AI-assisted reconstructions from
the author syntax and inspected input metadata. They document the models that
were executed, with student review still pending. They are not presented as a
student's pre-AI sketch or as pre-estimation approval.

**Figure 1**

*Separate three-level models of directed-reference outrage and recognition*

![Figure 1](figures/model_diagram.svg)

*Note.* Each model has its own five fixed slopes, intercept, item variance and
actor/statement variance. M2 and M3 are fitted separately. No shared coefficients
or cross-outcome covariance is estimated. Within a model, the Gaussian item and
actor random intercepts are independent of one another and of the covariates.
The reference level is nested within originating actor/statement groups within
items. Countries and media categories are fixed predictors, not random levels.

Open the [editable Mermaid source](model_diagram.mmd),
[vector figure](figures/model_diagram.svg),
[PNG copy](figures/model_diagram.png) or
[node-to-equation/code/matrix map](model_diagram_map.csv).

The five indicator definitions and their raw-to-analysis recodes are shown in
the figure. All covariates retain their original categories. No centering,
interaction, indirect effect, random slope, weight, prior or imputation was used.
No additional auxiliary metadata has been introduced as a control variable.
The figure does not imply that compromise, identity boundaries or gatekeeping
were directly measured mediators.

## Exact advanced-model specification

For model t=2 (outrage) or t=3 (recognition), fitted separately,

`Y_t,raj | u_t,j,v_t,aj ~ Bernoulli(p_t,raj)`

`logit(p_t,raj) = beta_t,0 + X_j beta_t + u_t,j + v_t,aj`

`u_t,j ~ Normal(0,sigma_t,item^2)` and
`v_t,aj ~ Normal(0,sigma_t,actor^2)`.

The actor/statement key is `act_id=text_id+'_'+akteur_id`. It identifies a unit
within an item and does not track a person across the corpus. The observation
counts are 3770 references, 2453 actor/statement groups and 1183 news items.
The model is frequentist marginal maximum likelihood, not Bayesian estimation.
Both random intercepts use seven-node adaptive Gauss-Hermite integration in the
primary calculation. The original author command explicitly specifies seven
points. The Python implementation uses recursive mean/variance adaptation.
Historical executable builds and internal finite-node details were not fully
recovered and are not invented here. These are implementation boundaries, not
additional paths in the substantive model.

The executing syntax is

```stata
melogit actrefoutbin i.polsys i.socdiv i.mediatype || text_id: || act_id:, intpoints(7)
melogit actrefrecbin i.polsys i.socdiv i.mediatype || text_id: || act_id:, intpoints(7)
```

This is source syntax for reference. The executed implementation is
`analysis/run_binary_models.py` calling `analysis/nested_logit.py`. Coding and
grouping are implemented in `analysis/prepare_replication.py`. Conditional odds
ratios from these models differ from the prior-marginal probabilities and
discrete contrasts in `analysis/binary_predictions.py`.

**Figure 2**

*Item-level proportional-odds model of outrage tone*

![Figure 2](figures/model_diagram_m1.svg)

*Note.* This companion model uses the 1700 original item rows. The copied tone
field in the reference archive is not a different M1 analysis sample. Four
ordered cutpoints identify the ordinal likelihood without a separate free
intercept. There are five fixed slopes and no random effects.

Open the [editable M1 Mermaid source](model_diagram_m1.mmd),
[M1 vector figure](figures/model_diagram_m1.svg) or
[M1 PNG copy](figures/model_diagram_m1.png).

The upper-tail equation is
`logit Pr(tone_i>k)=X_i beta1-c_k` for k=0,1,2,3, with ordered cutpoints.
Its implied category probabilities are the differences of adjacent cumulative
logistic probabilities. This sign convention agrees with the author's positive
slopes meaning greater outrage. The faithful sample uses archive tone minus one
and the same five dummy predictors as the binary models. The execution is in
`analysis/ordinal_reproduction.py`.

## Follow a diagram element to its evidence

The [mapping CSV](model_diagram_map.csv) gives each node's measurement or
distribution, equation, model ID, matrix row IDs, exact executing functions and
source locator. Every source path is an existing file. The column named
`planned_script_path` is retained for the first skill's original contract, but
the rows explicitly identify these paths as executed implementations.

POL, SEC and MED explain coding. X contains all five derived fixed-effect
indicators. M2U/M3U and M2V/M3V represent separate random intercepts, not measured
latent psychological constructs. M2ETA/M3ETA are linear predictors and M2Y/M3Y
are the actual binary outcomes. M1ETA/M1C/M1Y give the fixed predictor,
identification thresholds and ordinal outcome. CONFIG nodes state model-wide
restrictions. Node labels and SVG placements come from a single saved registry.
Mermaid and SVG are two exports of that registry, not separate scientific models.

For each original directional contrast, follow the corresponding
[matrix row](hypothesis_matrix.csv). Mixed-system coefficients remain additional
comparisons. The [dictionary guide](variable_dictionary.md) explains the source
names, indicators, categories and preserved coding-rule exceptions.

## Report and review use

The model diagram requirement is documented here with figure numbers, titles,
notes, editable source and equation/code/matrix links. A suitable report
cross-reference is, "Figure 1 in the repository documents the two separately
estimated nested binary models, including their category coding and random
intercepts." The individual final report was not edited during this task.
Its final cross-reference and the student's review can be added during the next
report revision. No review or authorship declaration is supplied on the
student's behalf.
"""
    (DOCS / "model_diagram.md").write_text(text, encoding="utf-8")


def main():
    registry()
    mermaid()
    places = {"Figure 1": svg(), "Figure 2": svg(True)}
    functions = {
        "analysis/prepare_replication.py": ["design", "recode", "load_data"],
        "analysis/ordinal_reproduction.py": ["design", "prepare", "CommonOrdinal", "fit_common"],
        "analysis/nested_logit.py": ["NestedBernoulli", "fit_model"],
        "analysis/run_binary_models.py": ["run"],
    }
    for n in NODES:
        bindings = []
        for path in n["planned_script_path"].split(" | "):
            src = (ROOT / path).read_text(encoding="utf-8").splitlines()
            for name in functions.get(path, []):
                hits = [i for i, line in enumerate(src, 1) if re.match(r"^(def|class) " + re.escape(name) + r"\b", line)]
                if hits:
                    bindings.append(f"{path}:{hits[0]} ({name})")
        n["executing_functions"] = " | ".join(bindings) or "Entry point in " + n["planned_script_path"]
    with (DOCS / "model_diagram_map.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        w = csv.DictWriter(stream, fieldnames=list(NODES[0]))
        w.writeheader()
        w.writerows(NODES)
    record = ROOT / "records/skill_invocations/2026-10-20_design_completion"
    (record / "diagram_registry.json").write_text(json.dumps(NODES, indent=2), encoding="utf-8")
    (record / "diagram_placements.json").write_text(json.dumps(places, indent=2), encoding="utf-8")
    guide()
    print(json.dumps({"nodes": len(NODES), "figures": 2, "formats": ["Mermaid", "SVG", "PNG"], "research_models_rerun": False}))


if __name__ == "__main__":
    main()
