from __future__ import annotations

import argparse
import csv
import textwrap
from pathlib import Path

from common import repo_root


def t(value: str) -> str:
    return textwrap.dedent(value).strip()


TRANSLATIONS = {
    "Route3_Text_TunnelFromCeruleanTiring": t("""
        Púff... ég ætti að hvíla mig...
        Styn...

        Göngin frá CERULEAN taka verulega á!
    """),
    "Route3_Text_ColtonIntro": t("""
        Hey!
        Ég sá þig í VIRIDIAN-SKÓGI!
    """),
    "Route3_Text_ColtonDefeat": t("""
        Þú vannst mig aftur!
    """),
    "Route3_Text_ColtonPostBattle": t("""
        Það eru til aðrar gerðir vasaskrímsla
        en þær sem þú finnur í skógum.
    """),
    "Route3_Text_BenIntro": t("""
        Hæ!
        Mér finnst stuttbuxur frábærar!

        Þær eru dásamlega þægilegar og
        auðveldar í notkun!
    """),
    "Route3_Text_BenDefeat": t("""
        Ég trúi þessu ekki!
    """),
    "Route3_Text_BenPostBattle": t("""
        Notarðu PC í vasaskrímslamiðstöð til
        að geyma vasaskrímslin þín?

        Hvert BOX rúmar allt að 30
        vasaskrímsli.
    """),
    "Route3_Text_JaniceIntro": t("""
        Afsakaðu!
        Þú horfðir á mig, ekki satt?
    """),
    "Route3_Text_JaniceDefeat": t("""
        Þú ert vondur!
    """),
    "Route3_Text_JanicePostBattle": t("""
        Þú ættir ekki að stara ef þú vilt
        ekki berjast!
    """),
    "Route3_Text_GregIntro": t("""
        Ertu ÞJÁLFARI?
        Byrjum þá strax!
    """),
    "Route3_Text_GregDefeat": t("""
        Ef ég ætti ný vasaskrímsli hefði ég
        unnið!
    """),
    "Route3_Text_GregPostBattle": t("""
        Ef vasaskrímsla-BOX í PC fyllist
        skaltu bara skipta yfir í annað BOX.
    """),
    "Route3_Text_SallyIntro": t("""
        Þetta augnaráð sem þú gafst mér...
        Það er svo spennandi!
    """),
    "Route3_Text_SallyDefeat": t("""
        Vertu almennilegur!
    """),
    "Route3_Text_SallyPostBattle": t("""
        Þú getur forðast bardaga með því að
        láta ÞJÁLFARA ekki sjá þig.
    """),
    "Route3_Text_CalvinIntro": t("""
        Hey!
        Þú ert ekki í stuttbuxum!
        Hvað er að þér?
    """),
    "Route3_Text_CalvinDefeat": t("""
        Tapaði!
        Tapaði! Tapaði!
    """),
    "Route3_Text_CalvinPostBattle": t("""
        Ég geng alltaf í stuttbuxum, jafnvel
        á veturna. Það er mín regla.
    """),
    "Route3_Text_JamesIntro": t("""
        Ég berst við þig með vasaskrímslunum
        sem ég náði rétt áðan.
    """),
    "Route3_Text_JamesDefeat": t("""
        Kláraður eins og kvöldmatur!
    """),
    "Route3_Text_JamesPostBattle": t("""
        Þjálfuð vasaskrímsli eru sterkari
        en villt.
    """),
    "Route3_Text_RobinIntro": t("""
        Ííík!
        Snertirðu mig?
    """),
    "Route3_Text_RobinDefeat": t("""
        Var það allt?
    """),
    "Route3_Text_RobinPostBattle": t("""
        VEGUR 4 er við rætur MÁNAFJALLS.
    """),
    "Route3_Text_RouteSign": t("""
        VEGUR 3
        MÁNAFJALL FRAMUNDAN
    """),
    "Route4_Text_TrippedOverGeodude": t("""
        Ái!
        Ég hrasaði um grýtt vasaskrímsli,
        AURGAUR!
    """),
    "Route4_Text_CrissyIntro": t("""
        Ég kom til MÁNAFJALLS í leit að
        sveppavasaskrímslum.
    """),
    "Route4_Text_CrissyDefeat": t("""
        Eftir allt sem ég lagði á mig til að
        ná þeim!
    """),
    "Route4_Text_CrissyPostBattle": t("""
        Það eru kannski ekki fleiri sveppir
        hér.

        Ég held ég hafi náð þeim öllum.
    """),
    "Route4_Text_MtMoonEntrance": t("""
        MÁNAFJALL
        INNGANGUR
    """),
    "Route4_Text_RouteSign": t("""
        VEGUR 4
        MÁNAFJALL - CERULEAN BORG
    """),
    "Text_MegaPunchTeach": t("""
        Högg af öskrandi hörku!

        Hlaðið eyðileggjandi krafti!

        Þegar allt er undir er MEGAHÖGG
        fullkomna árásin!
        Þú samþykkir það, ekki satt?

        Nú!
        Leyfðu mér að kenna vasaskrímslinu
        þínu það!
    """),
    "Text_MegaPunchDeclined": t("""
        Þú kemur aftur þegar þú skilur
        gildi MEGAHÖGGS.
    """),
    "Text_MegaPunchWhichMon": t("""
        Gott!
        Hvaða vasaskrímsli á að læra það?
    """),
    "Text_MegaPunchTaught": t("""
        Nú erum við félagar á vegi högganna!

        Þú ættir að fara áður en sá villti
        kjáni sem æfir bara spörk sér þig.
    """),
    "Text_MegaKickTeach": t("""
        Spark af grimmilegri hörku!

        Hlaðið eyðileggjandi krafti!

        Þegar öllu er á botninn hvolft er
        MEGASPARK fullkomna árásin!
        Ertu ekki sammála?

        Allt í lagi!
        Ég skal kenna vasaskrímslinu þínu
        það!
    """),
    "Text_MegaKickDeclined": t("""
        Þú skríður aftur þegar þú skilur
        gildi MEGASPARKS.
    """),
    "Text_MegaKickWhichMon": t("""
        Allt í lagi!
        Hvaða vasaskrímsli vill læra það?
    """),
    "Text_MegaKickTaught": t("""
        Nú erum við sálufélagar á vegi
        sparkanna!

        Þú ættir að hlaupa áður en sá
        ruglaði kjáni sem æfir bara einföld
        högg sér þig.
    """),
    "Route4_Text_PeopleLikeAndRespectBrock": t("""
        Ó, vá, þetta er STEINMERKIÐ!
        Þú fékkst það frá BROCK, ekki satt?

        BROCK er flottur. Hann er ekki bara
        sterkur.
        Fólk kann vel við hann og ber
        virðingu fyrir honum.

        Ég vil verða SALSTJÓRI eins og hann.
    """),
    "Route4_PokemonCenter_1F_Text_CanHaveSixMonsWithYou": t("""
        Allt í lagi, sex VASA BOLTAR á
        beltið...

        Já, þetta ætti að duga.
        Þú getur mest haft sex vasaskrímsli
        með þér.
    """),
    "Route4_PokemonCenter_1F_Text_TeamRocketAttacksCerulean": t("""
        ROCKET-GENGIÐ ræðst á borgara í
        CERULEAN...

        Það líður ekki dagur án þess að
        ROCKET-GENGIÐ sé í fréttunum.
    """),
    "Route4_PokemonCenter_1F_Text_LaddieBuyMagikarpForJust500": t("""
        MAÐUR: Sæll, strákur!
        Ég er með tilboð handa þér!

        Ég læt þig fá leynilegt
        vasaskrímsli - GREYSLEPPA - fyrir
        aðeins ¥500!

        Þú kaupir það, ekki satt?
    """),
    "Route4_PokemonCenter_1F_Text_SweetieBuyMagikarpForJust500": t("""
        MAÐUR: Sæl, elskan!
        Ég er með tilboð handa þér!

        Ég læt þig fá leynilegt
        vasaskrímsli - GREYSLEPPA - fyrir
        aðeins ¥500!

        Þú kaupir það, ekki satt?
    """),
    "Route4_PokemonCenter_1F_Text_PaidOutrageouslyForMagikarp": t("""
        {PLAYER} greiddi fáránlegar ¥500
        og keypti GREYSLEPPA...
    """),
    "Route4_PokemonCenter_1F_Text_OnlyDoingThisAsFavorToYou": t("""
        Nei?
        Segirðu nei?
        Ég geri þetta bara sem greiða fyrir
        þig!
    """),
    "Route4_PokemonCenter_1F_Text_NoRoomForMorePokemon": t("""
        Það virðist ekki vera pláss fyrir
        fleiri vasaskrímsli.
    """),
    "Route4_PokemonCenter_1F_Text_YoullNeedMoreMoney": t("""
        Þú þarft meiri peninga en það!
    """),
    "Route4_PokemonCenter_1F_Text_IDontGiveRefunds": t("""
        MAÐUR: Jæja, ég endurgreiði ekki.
        Þú vissir hvað þú varst að fá!
    """),
    "Route4_PokemonCenter_1F_Text_ShouldStoreMonsUsingPC": t("""
        Stundum ertu með of mörg
        vasaskrímsli til að bæta fleirum við.

        Þá ættirðu bara að geyma nokkur með
        hvaða PC sem er.
    """),
    "Route4_PokemonCenter_1F_Text_ItsANewspaper": t("""
        Þetta er dagblað.
    """),
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-after-v4.csv")
    parser.add_argument("--output", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-route3-route4-v1.csv")
    args = parser.parse_args()

    with args.queue.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    out = []
    seen: set[str] = set()
    for row in rows:
        label = row["label"]
        if not (row["file"].startswith("data/maps/Route3") or row["file"].startswith("data/maps/Route4")):
            continue
        if label not in TRANSLATIONS:
            continue
        row = dict(row)
        row["icelandic"] = TRANSLATIONS[label]
        row["notes"] = "codex curated Route 3 and Route 4 v1"
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
