from __future__ import annotations

import argparse
import csv
import textwrap
from pathlib import Path

from common import repo_root


def t(value: str) -> str:
    return textwrap.dedent(value).strip()


GUARD_THIRSTY = t("""
    Ég er á varðgæslu.
    Úff, ég er samt þyrstur!

    Ó, bíddu, vegurinn er lokaður.
""")

GUARD_TEA = t("""
    Ó, þetta TE...
    Það lítur hrikalega girnilega út...
""")

GUARD_SHARE_TEA = t("""
    Ha? Má ég fá þennan drykk?
    Úff, takk!
    ... ...
    Glugg, glugg...
    ... ...
    Kyng...
    Ef þú vilt fara til SAFFRON BORGAR...
    ... ...
    Þú mátt fara í gegn.

    Ég deili þessu TE með hinum vörðunum!
""")

GUARD_HELLO = t("""
    Hæ, hvernig gengur?
""")


TRANSLATIONS = {
    "Route5_PokemonDayCare_Text_WantMeToRaiseMon": t("""
        Ég rek DAGVISTINA.

        Viltu að ég ali upp eitt af
        vasaskrímslunum þínum?
    """),
    "Route5_PokemonDayCare_Text_ComeAgain": t("""
        Komdu aftur.
    """),
    "Route5_PokemonDayCare_Text_WhichMonShouldIRaise": t("""
        Hvaða vasaskrímsli á ég að ala upp?
    """),
    "Route5_PokemonDayCare_Text_ComeAnytimeYouLike": t("""
        Gott.
        Komdu hvenær sem þú vilt.
    """),
    "Route5_PokemonDayCare_Text_LookAfterMonForAWhile": t("""
        Gott, ég lít eftir {STR_VAR_1} um
        stund.
    """),
    "Route5_PokemonDayCare_Text_ComeSeeMeInAWhile": t("""
        Komdu að hitta mig eftir smástund.
    """),
    "Route5_PokemonDayCare_Text_MonNeedsToSpendMoreTime": t("""
        Ertu strax aftur hér?

        {STR_VAR_1} þarf að eyða meiri tíma
        hjá mér.
    """),
    "Route5_PokemonDayCare_Text_OweMeXForMonsReturn": t("""
        Þú skuldar mér ¥{STR_VAR_2} fyrir að fá
        þetta vasaskrímsli til baka.
    """),
    "Route5_PokemonDayCare_Text_ThankYouHeresMon": t("""
        Takk fyrir!
        Hér er vasaskrímslið þitt.
    """),
    "Route5_PokemonDayCare_Text_PlayerGotMonBack": t("""
        {PLAYER} fékk {STR_VAR_1} aftur frá
        DAGVISTARMANNINUM.
    """),
    "Route5_PokemonDayCare_Text_OnlyHaveOneMonWithYou": t("""
        Ó? Þú ert bara með eitt vasaskrímsli
        með þér.
    """),
    "Route5_PokemonDayCare_Text_WhatWillYouBattleWith": t("""
        Ef þú skilur það vasaskrímsli eftir
        hjá mér, með hverju ætlarðu að
        berjast?
    """),
    "Route5_PokemonDayCare_Text_MonHasGrownByXLevels": t("""
        {STR_VAR_1} hefur vaxið mikið.
        Já, mjög mikið, myndi ég segja.

        Láttu mig sjá...
        Stigalega hefur það hækkað um
        {STR_VAR_2}.

        Er ég ekki frábær?
    """),
    "Route5_PokemonDayCare_Text_YouveGotNoRoomForIt": t("""
        Þú getur ekki tekið þetta vasaskrímsli
        til baka ef þú hefur ekkert pláss
        fyrir það.
    """),
    "Route5_PokemonDayCare_Text_DontHaveEnoughMoney": t("""
        Þú átt ekki nógan pening.
    """),
    "Route5_SouthEntrance_Text_ThirstyOnGuardDuty": GUARD_THIRSTY,
    "Route5_SouthEntrance_Text_ThatTeaLooksTasty": GUARD_TEA,
    "Route5_SouthEntrance_Text_ThanksIllShareTeaWithGuards": GUARD_SHARE_TEA,
    "Route5_SouthEntrance_Text_HiHowsItGoing": GUARD_HELLO,
    "Route6_Text_RickyDefeat": t("""
        Ég get bara ekki unnið!
    """),
    "Route6_Text_NancyIntro": t("""
        Afsakaðu!
        Þetta er einkasamtal!
    """),
    "Route6_Text_KeigoDefeat": t("""
        Nei!
        Þú hlýtur að vera að grínast!
    """),
    "Route6_Text_KeigoPostBattle": t("""
        Mér líkar við pöddur, svo ég fer
        aftur í VIRIDIAN-SKÓG.
    """),
    "Route6_Text_JeffIntro": t("""
        Ha?
        Viltu tala við mig?
    """),
    "Route6_Text_JeffDefeat": t("""
        Þetta er ömurlegt...
        Ég náði ekki að standast áskorunina
        þína...
    """),
    "Route6_Text_JeffPostBattle": t("""
        Ég ætti að taka fleiri vasaskrímsli
        með mér.
        Þá finnst mér ég öruggari.
    """),
    "Route6_Text_IsabelleIntro": t("""
        Ég?
        Jæja, allt í lagi. Ég skal leika!
    """),
    "Route6_Text_IsabellePostBattle": t("""
        Mig langar að verða sterkari.
        Hvert er leyndarmálið þitt?
    """),
    "Route6_Text_ElijahIntro": t("""
        Ég hef aldrei séð þig hér.
        Ertu góður?
    """),
    "Route6_Text_ElijahDefeat": t("""
        Þú ert of góður!
    """),
    "Route6_Text_ElijahPostBattle": t("""
        Eru vasaskrímslin mín veik?
        Eða er ég bara slæmur?
        Hvað heldurðu?
    """),
    "Route6_NorthEntrance_Text_ThirstyOnGuardDuty": GUARD_THIRSTY,
    "Route6_NorthEntrance_Text_ThatTeaLooksTasty": GUARD_TEA,
    "Route6_NorthEntrance_Text_ThanksIllShareTeaWithGuards": GUARD_SHARE_TEA,
    "Route6_NorthEntrance_Text_HiHowsItGoing": GUARD_HELLO,
    "UndergroundPath_EastEntrance_Text_DoYouGoToCeladonDeptStore": t("""
        STÓRVERSLUNIN í CELADON hefur
        frábært úrval.

        Ferðu þangað oft?
    """),
    "UndergroundPath_SouthEntrance_Text_PeopleLoseThingsInTheDarkness": t("""
        Fólk týnir oft hlutum í myrkrinu á
        JARÐGÖNGUSTÍGNUM.
    """),
    "UndergroundPath_WestEntrance_Text_SleepyMonNearCeladon": t("""
        Ég heyrði að syfjað vasaskrímsli
        hefði líka birst nærri CELADON BORG.
    """),
}


PREFIXES = (
    "data/maps/Route5",
    "data/maps/Route6",
    "data/maps/UndergroundPath_",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-after-v6.csv")
    parser.add_argument("--output", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-route5-route6-v1.csv")
    args = parser.parse_args()

    with args.queue.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    out = []
    seen: set[str] = set()
    for row in rows:
        label = row["label"]
        if not row["file"].startswith(PREFIXES):
            continue
        if label not in TRANSLATIONS:
            continue
        row = dict(row)
        row["icelandic"] = TRANSLATIONS[label]
        row["notes"] = "codex curated Route 5, Route 6, Day Care, and Underground Path v1"
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
