from __future__ import annotations

import argparse
import csv
import textwrap
from pathlib import Path

from common import repo_root


def t(value: str) -> str:
    return textwrap.dedent(value).strip()


TRANSLATIONS = {
    "MtMoon_1F_Text_MarcosIntro": t("""
        VÁ!
        Þú brá mér!
        ...Ó, þú ert bara krakki!
    """),
    "MtMoon_1F_Text_MarcosDefeat": t("""
        Vá!
        Þú brást mér aftur!
    """),
    "MtMoon_1F_Text_MarcosPostBattle": t("""
        Krakkar eins og þú ættu ekki að
        ráfa hér um í myrkrinu.
    """),
    "MtMoon_1F_Text_JoshIntro": t("""
        Komstu líka til að kanna hellinn?
    """),
    "MtMoon_1F_Text_JoshDefeat": t("""
        Það er ömurlegt að tapa!
        Algjörlega ókúl.
    """),
    "MtMoon_1F_Text_JoshPostBattle": t("""
        Ég kom alla leið hingað niður til að
        sýna mig fyrir stelpum.
    """),
    "MtMoon_1F_Text_MiriamIntro": t("""
        Vá!
        Hér er miklu stærra en ég hélt!
    """),
    "MtMoon_1F_Text_MiriamDefeat": t("""
        Ó!
        Ég missti þetta!
    """),
    "MtMoon_1F_Text_MiriamPostBattle": t("""
        Hvernig kemst maður út héðan?
        Þetta er svo stórt að ég gæti
        villst.
    """),
    "MtMoon_1F_Text_JovanIntro": t("""
        Hvað!
        Ekki læðast aftan að mér!
    """),
    "MtMoon_1F_Text_JovanDefeat": t("""
        Vasaskrímslin mín duga ekki!
    """),
    "MtMoon_1F_Text_JovanPostBattle": t("""
        Ég verð að finna sterkari
        vasaskrímsli.
        Hvar ætli þau séu?
    """),
    "MtMoon_1F_Text_IrisIntro": t("""
        Hvað?
        Ég er að bíða eftir að vinir mínir
        finni mig hér.
    """),
    "MtMoon_1F_Text_IrisDefeat": t("""
        Ég tapaði?
    """),
    "MtMoon_1F_Text_IrisPostBattle": t("""
        Ég kom því ég heyrði að hér væru
        mjög sjaldgæfir steingervingar.
    """),
    "MtMoon_1F_Text_KentIntro": t("""
        Grunsamlegir menn eru í hellinum.
        Hvað með þig?
    """),
    "MtMoon_1F_Text_KentDefeat": t("""
        Þú náðir mér!
    """),
    "MtMoon_1F_Text_KentPostBattle": t("""
        Ég sá þá!
        Ég er viss um að þeir eru úr
        ROCKET-GENGINU!
    """),
    "MtMoon_1F_Text_RobbyIntro": t("""
        Þú þarft að fara í gegnum þennan
        helli til að komast til CERULEAN
        BORGAR.
    """),
    "MtMoon_1F_Text_RobbyDefeat": t("""
        Ég tapaði.
    """),
    "MtMoon_1F_Text_RobbyPostBattle": t("""
        BLAKILDI er harðgert!
        En ef þú nærð einu geturðu treyst á
        það.
    """),
    "MtMoon_1F_Text_ZubatIsABloodsucker": t("""
        Varúð!
        BLAKILDI sýgur blóð!
    """),
    "MtMoon_1F_Text_BrockHelpsExcavateFossils": t("""
        Hæ, ég er að grafa eftir
        steingervingum hér undir MÁNAFJALLI.

        Stundum hjálpar BROCK úr
        PEWTER-SALNUM mér.
    """),
    "MtMoon_B2F_Text_MiguelIntro": t("""
        Heyrðu, stoppaðu!

        Ég fann þessa steingervinga!
        Þeir eru báðir mínir!
    """),
    "MtMoon_B2F_Text_MiguelDefeat": t("""
        Allt í lagi!
        Ég skal deila!
    """),
    "MtMoon_B2F_Text_WellEachTakeAFossil": t("""
        Við tökum hvort sinn steingerving!
        Enga græðgi!
    """),
    "MtMoon_B2F_Text_ThenThisFossilIsMine": t("""
        Allt í lagi.
        Þá er þessi steingervingur minn!
    """),
    "MtMoon_B2F_Text_LabOnCinnabarRegeneratesFossils": t("""
        Langt í burtu, á CINNABAR ISLAND,
        er vasaskrímsla-RANNSÓKNARSTOFA.

        Þar er rannsakað hvernig endurlífga
        má steingervinga.
    """),
    "MtMoon_B2F_Text_Grunt1Intro": t("""
        Við, ROCKET-GENGIÐ, munum finna
        steingervingana!

        Ef við endurlífgum vasaskrímsli úr
        þeim græðum við stórfé!
    """),
    "MtMoon_B2F_Text_Grunt1Defeat": t("""
        Urgh!
        Nú er ég reiður!
    """),
    "MtMoon_B2F_Text_Grunt1PostBattle": t("""
        Þú gerðir mig reiðan!
        ROCKET-GENGIÐ setur þig á svartan
        lista!
    """),
    "MtMoon_B2F_Text_Grunt2Intro": t("""
        Við í ROCKET-GENGINU erum
        glæpamenn vasaskrímslaheimsins!
        Við vekjum ótta með styrk okkar!
    """),
    "MtMoon_B2F_Text_Grunt2Defeat": t("""
        Ég klúðraði þessu!
    """),
    "MtMoon_B2F_Text_Grunt2PostBattle": t("""
        Fjandinn hafi það!
        Félagar mínir sætta sig ekki við
        þetta!
    """),
    "MtMoon_B2F_Text_Grunt3Intro": t("""
        Við erum með stórt verk hér!
        Hypjaðu þig, krakki!
    """),
    "MtMoon_B2F_Text_Grunt3Defeat": t("""
        Þú ert þá góður...
    """),
    "MtMoon_B2F_Text_Grunt3PostBattle": t("""
        Ef þú finnur steingerving, láttu mig
        fá hann og hypjaðu þig!
    """),
    "MtMoon_B2F_Text_Grunt4Intro": t("""
        Lítil börn ættu ekki að flækjast í
        mál fullorðinna!

        Það gæti endað illa!
    """),
    "MtMoon_B2F_Text_Grunt4Defeat": t("""
        Ég er brjálaður!
    """),
    "MtMoon_B2F_Text_Grunt4PostBattle": t("""
        Vasaskrímsli bjuggu hér löngu áður
        en menn komu.
    """),
    "MtMoon_B2F_Text_YouWantDomeFossil": t("""
        Viltu HVOLFGERVING?
    """),
    "MtMoon_B2F_Text_YouWantHelixFossil": t("""
        Viltu SPÍRALGERVING?
    """),
    "MtMoon_B2F_Text_ObtainedHelixFossil": t("""
        Fékkst SPÍRALGERVING!
    """),
    "MtMoon_B2F_Text_ObtainedDomeFossil": t("""
        Fékkst HVOLFGERVING!
    """),
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-after-v3.csv")
    parser.add_argument("--output", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-mtmoon-v1.csv")
    args = parser.parse_args()

    with args.queue.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    out = []
    seen: set[str] = set()
    for row in rows:
        label = row["label"]
        if not row["file"].startswith("data/maps/MtMoon"):
            continue
        if label not in TRANSLATIONS:
            continue
        row = dict(row)
        row["icelandic"] = TRANSLATIONS[label]
        row["notes"] = "codex curated Mt Moon v1"
        out.append(row)
        seen.add(label)

    missing = sorted(set(TRANSLATIONS) - seen)
    if missing:
        raise SystemExit("labels not found in queue: " + ", ".join(missing))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out)

    print(f"wrote {args.output} rows={len(out)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
