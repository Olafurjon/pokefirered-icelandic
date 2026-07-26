from __future__ import annotations

import argparse
import csv
import textwrap
from pathlib import Path

from common import repo_root


def t(value: str) -> str:
    return textwrap.dedent(value).strip()


TRANSLATIONS = {
    "DiglettsCave_NorthEntrance_RockTunnelPitchBlack": t("""
        Ég fór inn í ROCK TUNNEL, en þar inni
        er kolniðamyrkur og óhugnanlegt.

        Ef ég gæti fengið vasaskrímsli til að
        nota LEIFTUR og lýsa upp...
    """),
    "DiglettsCave_SouthEntrance_Text_DiglettDugThisTunnel": t("""
        Jæja, þetta kemur á óvart!
        GRAFLARI gróf þessi löngu göng!

        Mér er sagt að þau liggi beint til
        VIRIDIAN BORGAR.
    """),
    "Route11_Text_HugoIntro": t("""
        Vinna, tapa eða jafntefli!
    """),
    "Route11_Text_HugoDefeat": t("""
        Atcha!
        Þetta fór ekki eins og ég vildi!
    """),
    "Route11_Text_HugoPostBattle": t("""
        Vasaskrímsli eru lífið!
        Og að lifa er að spila leiki!
    """),
    "Route11_Text_JasperIntro": t("""
        Keppni!
        Ég fæ aldrei nóg!
    """),
    "Route11_Text_JasperDefeat": t("""
        Ég átti möguleika!
    """),
    "Route11_Text_JasperPostBattle": t("""
        Þú mátt ekki vera huglaus í heimi
        vasaskrímsla!
    """),
    "Route11_Text_EddieIntro": t("""
        Byrjum, en ekki svindla!
    """),
    "Route11_Text_EddieDefeat": t("""
        Ha?
        Þetta er ekki rétt!
    """),
    "Route11_Text_EddiePostBattle": t("""
        Ég gerði mitt besta.
        Ég sé ekki eftir neinu.
    """),
    "Route11_Text_BraxtonIntro": t("""
        Varlega!
        Ég er að leggja kapla!
    """),
    "Route11_Text_BraxtonDefeat": t("""
        Þetta var rafmagnað!
    """),
    "Route11_Text_BraxtonPostBattle": t("""
        Dreifðu boðskapnum um að spara orku!
    """),
    "Route11_Text_DillonIntro": t("""
        Ég varð nýlega ÞJÁLFARI.
        En ég held að ég geti unnið.
    """),
    "Route11_Text_DillonDefeat": t("""
        Vasaskrímslin mín gátu ekki unnið...
        Hafa þau ekki vaxið nóg?
    """),
    "Route11_Text_DillonPostBattle": t("""
        Hvað nú?
        Láttu mig í friði!
    """),
    "Route11_Text_DirkIntro": t("""
        Fwahaha!
        Ég hef aldrei tapað!
    """),
    "Route11_Text_DirkDefeat": t("""
        Fyrsta tapið mitt!
    """),
    "Route11_Text_DirkPostBattle": t("""
        Þú varst bara heppinn, það er allt.
    """),
    "Route11_Text_DarianIntro": t("""
        Ég hef aldrei unnið áður...
    """),
    "Route11_Text_DarianDefeat": t("""
        Ég sá þetta fyrir...
    """),
    "Route11_Text_DarianPostBattle": t("""
        Ég var óheppinn, eins og alltaf.
    """),
    "Route11_Text_YasuIntro": t("""
        Ég er bestur í bekknum mínum.
        Ég æfi á hverjum morgni.
    """),
    "Route11_Text_YasuDefeat": t("""
        Fjandinn!
        Vasaskrímslin mín þurfa að verða
        sterkari!
    """),
    "Route11_Text_YasuPostBattle": t("""
        Það er feitlagið vasaskrímsli sem
        kemur niður úr fjöllunum.

        Ég veðja að það væri sterkt ef þú
        næðir því.
    """),
    "Route11_Text_BernieIntro": t("""
        Varastu spennusetta víra!
    """),
    "Route11_Text_BernieDefeat": t("""
        Vá!
        Þú litla kveikjukerti!
    """),
    "Route11_Text_BerniePostBattle": t("""
        Jæja, best að fara aftur að vinna.
    """),
    "Route11_Text_DaveIntro": t("""
        Ég ól vasaskrímslin mín vandlega upp.
        Þau ættu að vera tilbúin núna!
    """),
    "Route11_Text_DaveDefeat": t("""
        Bæ-bæ!
        Takk fyrir og bless!
    """),
    "Route11_Text_DavePostBattle": t("""
        Tsk...
        Ég ætti að fara og finna sterkari.
    """),
    "Route11_Text_DiglettsCave": t("""
        GRAFLARAHELLIR
    """),
    "Route11_EastEntrance_1F_Text_ManInLavenderRatesNames": t("""
        Finnst þér ekki erfitt að finna góð
        nöfn fyrir vasaskrímsli?

        Sérstaklega ef þú hefur náð heilum
        helling?

        Í LAVENDER BORG er maður sem metur
        gælunöfn vasaskrímsla.

        Hann getur jafnvel hjálpað þér að
        endurnefna vasaskrímslin þín.
    """),
    "Route11_EastEntrance_1F_Text_RockTunnelToReachLavender": t("""
        Ef þú stefnir á LAVENDER BORG skaltu
        fara um ROCK TUNNEL.

        Þú kemst að ROCK TUNNEL frá CERULEAN
        BORG.
    """),
    "Route11_EastEntrance_2F_Text_GiveItemfinderIfCaught30": t("""
        Hæ! Manstu eftir mér?
        Ég er einn af AÐSTOÐARMÖNNUM PROF.
        OAK.

        Ef VasaDEX-ið þitt er með full gögn
        um {STR_VAR_1} tegundir á ég að gefa þér
        verðlaun.

        PROF. OAK fól mér {STR_VAR_2} handa
        þér.

        Svo, {PLAYER}, leyfðu mér að spyrja.

        Hefurðu safnað gögnum um að minnsta
        kosti {STR_VAR_1} gerðir vasaskrímsla?
    """),
    "Route11_EastEntrance_2F_Text_GreatHereYouGo": t("""
        Frábært! Þú hefur náð eða átt
        {STR_VAR_3} gerðir vasaskrímsla!

        Til hamingju!
        Gjörðu svo vel!
    """),
    "Route11_EastEntrance_2F_Text_ReceivedItemfinderFromAide": t("""
        {PLAYER} fékk {STR_VAR_2} frá
        AÐSTOÐARMANNINUM.
    """),
    "Route11_EastEntrance_2F_Text_ExplainItemfinder": t("""
        Það eru hlutir á jörðinni sem gætu
        verið faldir.

        Notaðu HLUTALEITARA til að finna
        falda hluti nálægt þér.

        Tækið er dálítið takmarkað.
        Það getur ekki staðsett hlutina
        nákvæmlega.

        Það sýnir bara í hvaða átt hluturinn
        er.

        Notaðu það til að ná áttum, leitaðu
        svo sjálfur á grunsamlega svæðinu.
    """),
    "Route11_EastEntrance_2F_Text_BigMonAsleepOnRoad": t("""
        Sjáum hvað sjónaukinn sýnir...

        Stórt vasaskrímsli sefur á vegi!
    """),
    "Route11_EastEntrance_2F_Text_WhatABreathtakingView": t("""
        Sjáum hvað sjónaukinn sýnir...

        Hvílíkt stórkostlegt útsýni!
    """),
    "Route11_EastEntrance_2F_Text_RockTunnelGoodRouteToLavender": t("""
        Sjáum hvað sjónaukinn sýnir...

        Til að komast til LAVENDER BORGAR frá
        CERULEAN BORG...

        ROCK TUNNEL virðist vera góð leið.
    """),
    "Route2_Text_RouteSign": t("""
        ROUTE 2
        VIRIDIAN BORG - PEWTER BORG
    """),
    "Route2_Text_DiglettsCave": t("""
        GRAFLARAHELLIR
    """),
    "Route2_EastBuilding_Text_GiveHM05IfSeen10Mons": t("""
        Hæ! Manstu eftir mér?
        Ég er einn af AÐSTOÐARMÖNNUM PROF.
        OAK.

        Ef VasaDEX-ið þitt er með full gögn
        um tíu tegundir á ég að gefa þér
        verðlaun.

        PROF. OAK fól mér HM05 handa þér.

        Svo, {PLAYER}, leyfðu mér að spyrja.

        Hefurðu safnað gögnum um að minnsta
        kosti tíu gerðir vasaskrímsla?
    """),
    "Route2_EastBuilding_Text_GreatHereYouGo": t("""
        Frábært! Þú hefur náð eða átt
        {STR_VAR_3} gerðir vasaskrímsla!

        Til hamingju!
        Gjörðu svo vel!
    """),
    "Route2_EastBuilding_Text_ReceivedHM05FromAide": t("""
        {PLAYER} fékk HM05 frá
        AÐSTOÐARMANNINUM.
    """),
    "Route2_EastBuilding_Text_ExplainHM05": t("""
        HM05 inniheldur földu hreyfinguna
        LEIFTUR.

        LEIFTUR lýsir upp jafnvel dimmustu
        hella og dýflissur.
    """),
    "Route2_EastBuilding_Text_CanGetThroughRockTunnel": t("""
        Þegar vasaskrímsli lærir LEIFTUR
        kemstu í gegnum ROCK TUNNEL.
    """),
    "Route2_House_Text_FaintedMonsCanUseFieldMoves": t("""
        Rotað vasaskrímsli hefur bara enga
        orku eftir til að berjast.

        Það getur samt notað hreyfingar eins
        og CUT utan bardaga.
    """),
    "Route2_ViridianForest_NorthEntrance_Text_ManyMonsOnlyInForests": t("""
        Mörg vasaskrímsli lifa aðeins í skógum
        og hellum.

        Þú þarft að vera þrautseigur og leita
        alls staðar til að finna ólíkar gerðir.
    """),
    "Route2_ViridianForest_NorthEntrance_Text_CanCutSkinnyTrees": t("""
        Hefurðu tekið eftir mjóu trjánum við
        veginn?

        Ég heyri að sérstök
        vasaskrímslahreyfing geti fellt þau.
    """),
    "Route2_ViridianForest_NorthEntrance_Text_CanCancelEvolution": t("""
        Þekkirðu tæknina til að stöðva þróun?

        Þegar vasaskrímsli er að þróast geturðu
        stöðvað ferlið.

        Þetta er tækni til að ala upp
        vasaskrímsli eins og þau eru.
    """),
    "Route2_ViridianForest_SouthEntrance_Text_ForestIsMaze": t("""
        Ertu að fara í VIRIDIAN-SKÓG?
        Þar inni er náttúrulegt völundarhús.
        Gættu þess að villast ekki.
    """),
    "Route2_ViridianForest_SouthEntrance_Text_RattataHasWickedBite": t("""
        ROTTÓTTUR er kannski lítill, en ekki
        vanmeta illvígt bit hans.

        Hefurðu þegar náð einum?
    """),
}


FILES = {
    "data/maps/DiglettsCave_NorthEntrance/text.inc",
    "data/maps/DiglettsCave_SouthEntrance/text.inc",
    "data/maps/Route11/text.inc",
    "data/maps/Route11_EastEntrance_1F/text.inc",
    "data/maps/Route11_EastEntrance_2F/text.inc",
    "data/maps/Route2/text.inc",
    "data/maps/Route2_EastBuilding/text.inc",
    "data/maps/Route2_House/text.inc",
    "data/maps/Route2_ViridianForest_NorthEntrance/text.inc",
    "data/maps/Route2_ViridianForest_SouthEntrance/text.inc",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-after-v9.csv")
    parser.add_argument("--output", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-route11-diglett-route2-v1.csv")
    args = parser.parse_args()

    with args.queue.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    out = []
    seen: set[str] = set()
    for row in rows:
        label = row["label"]
        if row["file"] not in FILES:
            continue
        if label not in TRANSLATIONS:
            continue
        row = dict(row)
        row["icelandic"] = TRANSLATIONS[label]
        row["notes"] = "codex curated Route 11, Diglett Cave, and Route 2 v1"
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
