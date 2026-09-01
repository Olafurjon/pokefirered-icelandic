from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path


DEFAULT_INCLUDE = (
    "data/maps",
    "data/scripts",
    "data/text",
    "src/data/text",
    "src/data/items.json",
    "src/data/pokemon/pokedex_text_fr.h",
    "src/data/pokemon/pokedex_text_lg.h",
    "src/data/text/nature_names.h",
    "src/data/region_map/region_map_sections.json",
    "src/battle_main.c",
    "src/battle_message.c",
    "src/move_descriptions.c",
    "src/strings.c",
    "src/trainer_tower_sets.c",
)

SKIP_DIRS = {
    ".git",
    "build",
    "graphics",
    "sound",
    "tools/agbcc",
    "tools/binutils",
    "translation_reports",
}


@dataclass(frozen=True)
class Rule:
    id: str
    pattern: re.Pattern[str]
    expected: str


RULES = [
    Rule("pokemon-term", re.compile(r"Pok[eé]mon|POK[eé]MON|POKeMON|POKEMON"), "Vasaskrímsli / VASaSKRÍMSLI"),
    Rule("poke-ball", re.compile(r"Pok[eé]\s*bolti|POK[EÉ]\s*BOLTI|POK[eé]\s*BALL|POK[EÉ]\s*BALL"), "Vasa bolti / VASA BOLTI"),
    Rule("trainer-tips", re.compile(r"TRAINER\s+TIPS|ÞJÁLFARI\s+TIPS|ÞJÁLFARA\s+TPIS|Þjálfari\s+Tips"), "ÞJÁLFARA RÁÐ"),
    Rule("route", re.compile(r"\bROUTE\s+\d+\b|\bRoute\s+\d+\b"), "VEGUR <nr> / Vegur <nr>"),
    Rule("mt-moon", re.compile(r"\bMT\.\s*MOON\b|\bMOONFJALL\b"), "MÁNAFJALL / MÁNAFJALLI / MÁNAFJALLS"),
    Rule("pallet-town", re.compile(r"PALLET\s+(TOWN|BAR)|Pallet\s+(Town|Bar)|Brettabar"), "PALLET BÆR / Pallet bær"),
    Rule("city", re.compile(r"\bCITY\b|\bCity\b"), "BORG / borg"),
    Rule("town", re.compile(r"\bTOWN\b|\bTown\b"), "BÆR / bær"),
    Rule("pocket", re.compile(r"\bPOCKET\b|\bPocket\b"), "HÓLF / hólf"),
    Rule("storage-system", re.compile(r"Storage\s+System|STORAGE\s+SYSTEM"), "Geymslukerfi"),
    Rule("pc-computer", re.compile(r"(?:^|\\[npl]|[^A-Za-z_])PC(?![A-Za-z_])"), "TÖLVA / tölva"),
    Rule("teleporter", re.compile(r"TELEPORTER(?![A-Za-z])"), "FJARFLUTNINGSTÆKI"),
    Rule(
        "capture-term",
        re.compile(
            r"\bHandteki(?:n|nn|ð|nir|nar|nu)?\b|\b(?:var|vera) veitt\b|\bGefa veiddu\b|"
            r"reynir að veiða það|vera veidd|sem veiddu þau|með því að veiða|"
            r"Erfitt er að veiða þá|veiða mér sterkari|Hversu mörg (?:veiddirðu|náðirðu)",
            re.IGNORECASE,
        ),
        "fanga / fangað / fangaði (veiða only for fishing)",
    ),
    Rule("summary-page-info", re.compile(r"Vasaskrímsli\s+INFO|Vasaskrímsli\s+SKILLS"), "Vasaskrímsli UPPL. / Vasaskrímsli HÆFNI"),
    Rule("nature-name", re.compile(r"\b(HARDY|LONELY|BRAVE|ADAMANT|NAUGHTY|BOLD|DOCILE|RELAXED|IMPISH|LAX|TIMID|HASTY|SERIOUS|JOLLY|NAIVE|MODEST|MILD|QUIET|BASHFUL|RASH|CALM|GENTLE|SASSY|CAREFUL|QUIRKY)\b"), "Icelandic nature names"),
    Rule("bag", re.compile(r"\bBAG\b|\bBag\b"), "TASKA / Taska"),
    Rule("attack", re.compile(r"\bATTACK\b|\bAttack\b"), "ÁRÁS / Árás"),
    Rule("attack-stat-alias", re.compile(r"\bSÓKN\b"), "ÁRÁS"),
    Rule("defense-stat", re.compile(r"\bDEFENSE\b|\bDefense\b"), "VÖRN / Vörn"),
    Rule("special-stat", re.compile(r"\bSP\.\s*(?:ATK|DEF)\b"), "SÉR. ÁRÁS / SÉR. VÖRN"),
    Rule("speed-stat", re.compile(r"\bSPEED\b|\bSpeed\b"), "HRAÐI / HRAÐA"),
    Rule("tv", re.compile(r"\bTV\b"), "SJÓNVARP / sjónvarp"),
    Rule("potion", re.compile(r"\bPOTIONS?\b|\bPotions?\b|\bDrykkir?\b|\bDRYKKIR?\b"), "SEYÐI / Seyði"),
    Rule("cancel", re.compile(r"\bHATTA\b|\bHatta\b"), "HÆTTA / Hætta"),
    Rule("town-map", re.compile(r"BAJARKORT|KORT BORGAR"), "BÆJARKORT / BÆJARKORTIÐ"),
    Rule("questionnaire-fill", re.compile(r"\bfyllja\b|\bFyllja\b"), "fylla / Fylla"),
    Rule("daycare-raise", re.compile(r"\balum\b|\bAlum\b"), "ölum / Ölum"),
    Rule("critical-hit", re.compile(r"Gagnhögg|GAGNHÖGG|gagnhögg"), "Gæfuhögg"),
    Rule("amulet-coin-alias", re.compile(r"VERNDARGRIP\w*|Verndargrip\w*"), "HEILLAPENINGUR / Heillapeningur"),
    Rule("surf", re.compile(r"\bSURF(?:A)?\b"), "BRIM / BRIMA"),
    Rule("cut-move", re.compile(r"\bCUT\b"), "HÖGGVA"),
    Rule("fly-move", re.compile(r"\bFLY\b"), "FLUG"),
    Rule("strength-move", re.compile(r"\bSTRENGTH\b"), "STYRKUR"),
    Rule("dig-move", re.compile(r"\bDIG\b"), "GRAFA"),
    Rule("flash-move", re.compile(r"\bFLASH\b"), "LEIFTUR"),
    Rule("shock-wave-move", re.compile(r"\bSHOCK\s+WAVE\b"), "STUÐBYLGJA"),
    Rule(
        "move-name-alias",
        re.compile(
            r"\b(?:GAGNÁTAK|LIGHT SCREEN|VERNDARHJÚP|REFLECT|GIGA DRAIN|ÁFALLABYLGJA|"
            r"ELDINGABYLGJA|RÓLEGUR HUGUR|EITURSTUNGA|FLJÚGA|ICE BEAM|BODY SLAM|"
            r"SUBSTITUTE|TOXIC|EXPLOSION|RETURN|EARTHQUAKE|FISSURE|MIMIC|SWORDS DANCE|ABSORB|"
            r"SAFEGUARD|BIND|MIST|UPROAR|STOCKPILE|RAGE|ENCORE|CURSE|SPIKES|TORMENT|TAUNT|WISH|"
            r"SAND TOMB|LEECH SEED|SKETCH|NIGHTMARE|PERISH(?: SONG)?|SPIT UP|SWALLOW|HEAT WAVE|"
            r"SOFTBOILED|MILK DRINK|ILMANGAN|KALA)\b"
        ),
        "canonical Icelandic name from src/data/text/move_names.h",
    ),
    Rule("sonic-boom-move", re.compile(r"\bSONICBOOM\b"), "HLJÓÐBYLGJA"),
    Rule("rock-smash", re.compile(r"\bROCK\s+SMASH\b"), "GRJÓTMÖLUN"),
    Rule("waterfall", re.compile(r"\bWATERFALL\b"), "FOSS"),
    Rule("nature-power", re.compile(r"\bNATURE\s+POWER\b"), "NÁTTÚRUKRAFTUR"),
    Rule("mirror-move", re.compile(r"\bMIRROR\s+MOVE\b"), "SPEGLUN"),
    Rule("x-accuracy", re.compile(r"\bX\s+ACCURACY\b"), "X HITTNI"),
    Rule(
        "item-name-alias",
        re.compile(
            r"\b(?:GOOD ROD|SUPER ROD|EXP\. SHARE|ITEMFINDER|AMULET COIN|FULL RESTORE|"
            r"SILPH SCOPE|DIRE HIT|GUARD SPEC\.|HP UP|CALCIUM|ZINC|CARBOS|PROTEIN|IRON|"
            r"PP UP|MAX REPEL|SUPER REPEL|REPEL|FULL HEAL|AWAKENING|ANTIDOTE|ICE HEAL|"
            r"PARLYZ HEAL|TINYMUSHROOMS|BIG MUSHROOM|LEMONADE|REVIVE|ENDURLÍFGANIR?|"
            r"RÁÐGÁTUBER|MYSTICMIÐI|METEORITE|RUBY|SAPPHIRE|OLD AMBER|RARE CANDY|"
            r"MOON STONE|NUGGET(?!\s+(?:BRIDGE|BRÚNA)))\b"
        ),
        "canonical Icelandic name from src/data/items.json",
    ),
    Rule("green-path", re.compile(r"\bGREEN\s+PATH\b"), "GRÆNN STÍGUR"),
    Rule("pattern-bush", re.compile(r"\bPATTERN\s+BUSH\b"), "MYNSTURRUNNI / MYNSTURRUNNA"),
    Rule("english-ability-name", re.compile(r"(?:BATTLE ARMOR|SHADOW TAG|CLEAR BODY|NATURAL CURE|INNER FOCUS|SOUNDPROOF|MARVEL SCALE|LIQUID OOZE|ROCK HEAD|ARENA TRAP|WHITE SMOKE|PURE POWER)"), "Icelandic ability name"),
    Rule("viridian-forest", re.compile(r"VIRIDIAN\s+FOREST|Viridian\s+Forest"), "VIRIDIAN SKÓGUR / VIRIDIAN SKÓGI"),
    Rule(
        "pokemon-center-alias",
        re.compile(r"vasaskrímsl(?:i|a)(?:-|\s*)miðstöð\w*", re.IGNORECASE),
        "Vasaskrímslasetur / Vasaskrímslasetri",
    ),
    Rule("poke-flute-alias", re.compile(r"vasaflaut\w*", re.IGNORECASE), "VASA FLAUTA (with a space)"),
    Rule("magnitude-move-alias", re.compile(r"STÆRÐ\s+\{B_BUFF1\}"), "STÆRÐARGRÁÐA {B_BUFF1}"),
    Rule("elite-four-alias", re.compile(r"ELÍTUFERNING(?:UR|INN|NUM)?"), "ELÍTA 4 / ELÍTU 4"),
    Rule("professor-oak-alias", re.compile(r"\b(?:PROF\.|PRÓF\.)\s+OAK\b|\bOAK:"), "PRÓF. EIK / EIK:"),
    Rule("biker-class-alias", re.compile(r"\bBIKERS\b"), "HJÓLARAR / HJÓLARA"),
    Rule("warden-alias", re.compile(r"\bWARDEN\b"), "VÖRÐUR / VÖRÐURINN"),
    Rule("nidoran-species", re.compile(r"\bNIDORAN(?:[♀♂])?\b"), "Náldur / NÁLDUR"),
    Rule("bug-species-phrase", re.compile(r"SKORDÝ\s+Vasaskrímsli|SKORDÝ\s+vasaskrímsli"), "SKORDÝRA Vasaskrímsli"),
    Rule("safari-zone", re.compile(r"SAFARI\s+ZONE|Safari\s+Zone"), "SAFARI SVÆÐI / Safari svæði"),
    Rule("cycling-road", re.compile(r"CYCLING\s+ROAD|Cycling\s+Road|cycling\s+road"), "HJÓLAVEGURINN"),
    Rule("rock-tunnel", re.compile(r"ROCK\s+TUNNEL|Rock\s+Tunnel|BERGGÖNG|STEINGÖNG"), "STEINA GÖNG"),
    Rule("seafoam-islands", re.compile(r"SEAFOAM(?:\s+EYJ(?:A|AR))?|Seafoam(?:\s+Islands?)?|SJÁFROÐUEYJAR"), "SJÁVARFROÐU EYJA / SJÁVARFROÐU EYJAR"),
    Rule("kindle-road", re.compile(r"KINDLE\s+ROAD|Kindle\s+Road|KINDLE\s+VEGUR"), "KYNDILVEGUR"),
    Rule("bond-bridge", re.compile(r"BOND\s+BRIDGE|Bond\s+Bridge|BOND\s+BRÚ"), "TENGIBRÚ"),
    Rule("sevii-one-island", re.compile(r"\bONE\s+(ISLAND|EYJA|EYJU|EYJAN)\b|\bEINN\s+EYJA\b|EINEY"), "EIN EYJA"),
    Rule("sevii-two-island", re.compile(r"\bTWO\s+(ISLAND|EYJA|EYJU|EYJAN)\b|TVÍEY"), "TVÖ EYJA"),
    Rule("sevii-three-island", re.compile(r"\bTHREE\s+(ISLAND|EYJA|EYJU|EYJAN)\b|ÞRÍEY"), "ÞRJÚ EYJA"),
    Rule("sevii-four-island", re.compile(r"\bFOUR\s+(ISLAND|EYJA|EYJU|EYJAN)\b|FJÓREY"), "FJÓR EYJA"),
    Rule("sevii-five-island", re.compile(r"\bFIVE\s+(ISLAND|EYJA|EYJU|EYJAN)\b|FIMMEY"), "FIMM EYJA"),
    Rule("sevii-six-island", re.compile(r"\bSIX\s+(ISLAND|EYJA|EYJU|EYJAN)\b|SEXEY"), "SEX EYJA"),
    Rule("sevii-seven-island", re.compile(r"\bSEVEN\s+(ISLAND|EYJA|EYJU|EYJAN)\b|SJÖEY"), "SJÖ EYJA"),
]


def is_skipped(path: Path, root: Path) -> bool:
    rel = path.relative_to(root).as_posix()
    return any(rel == skipped or rel.startswith(skipped + "/") for skipped in SKIP_DIRS)


def iter_files(root: Path, include: tuple[str, ...]) -> list[Path]:
    files: list[Path] = []
    for entry in include:
        path = root / entry
        if path.is_file():
            files.append(path)
            continue
        if path.is_dir():
            files.extend(p for p in path.rglob("*") if p.is_file() and not is_skipped(p, root))
    return sorted(set(files))


def scan_file(path: Path, root: Path) -> list[dict[str, str | int]]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []

    rows: list[dict[str, str | int]] = []
    rel = path.relative_to(root).as_posix()
    for line_no, line in enumerate(text.splitlines(), start=1):
        visible_texts = extract_visible_texts(path, line)
        for visible_text in visible_texts:
            for rule in RULES:
                if rule.pattern.search(visible_text):
                    rows.append(
                        {
                            "file": rel,
                            "line": line_no,
                            "rule": rule.id,
                            "expected": rule.expected,
                            "text": line.strip(),
                        }
                    )
    return rows


def extract_visible_texts(path: Path, line: str) -> list[str]:
    suffix = path.suffix.lower()
    stripped = line.strip()

    if suffix == ".inc":
        if ".string" not in stripped:
            return []
        return quoted_strings(stripped)

    if suffix == ".json":
        if "/data/maps/" in path.as_posix().replace("\\", "/"):
            return []
        if stripped.startswith((
            '"name":',
            '"english":',
            '"description":',
            '"description_english":',
        )):
            return quoted_strings(stripped)[1:]
        return []

    if suffix in {".c", ".h"}:
        if "_(" not in stripped and " = \"" not in stripped and not stripped.startswith('"'):
            return []
        return quoted_strings(stripped)

    return []


def quoted_strings(text: str) -> list[str]:
    return [match.group(1) for match in re.finditer(r'"((?:\\"|[^"])*)"', text)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Check visible Icelandic text for inconsistent terminology.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--report", type=Path)
    parser.add_argument("--include", nargs="*", default=DEFAULT_INCLUDE)
    parser.add_argument("--max-errors", type=int, default=0, help="0 means report all matches.")
    args = parser.parse_args()

    root = args.root.resolve()
    rows: list[dict[str, str | int]] = []
    for path in iter_files(root, tuple(args.include)):
        rows.extend(scan_file(path, root))

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        with args.report.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["file", "line", "rule", "expected", "text"])
            writer.writeheader()
            writer.writerows(rows)

    limit = args.max_errors or len(rows)
    for row in rows[:limit]:
        print(f"{row['file']}:{row['line']}: {row['rule']} -> {row['expected']}: {row['text']}")

    if rows:
        print(f"Found {len(rows)} terminology suspects.")
        raise SystemExit(1)

    print("No terminology suspects found.")


if __name__ == "__main__":
    main()
