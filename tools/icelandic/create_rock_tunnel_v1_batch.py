from __future__ import annotations

import argparse
import csv
import textwrap
from pathlib import Path

from common import repo_root


def t(value: str) -> str:
    return textwrap.dedent(value).strip()


TRANSLATIONS = {
    "RockTunnel_1F_Text_LennyIntro": t("""
        Þessi göng ná langt, krakki!
    """),
    "RockTunnel_1F_Text_LennyDefeat": t("""
        Doh!
        Þú vinnur!
    """),
    "RockTunnel_1F_Text_LennyPostBattle": t("""
        Passaðu þig á GRÁNAMAÐKU.
        Þær birtast bara öðru hvoru.

        Þær á háu stigi geta kreist þig
        rækilega!
    """),
    "RockTunnel_1F_Text_OliverIntro": t("""
        Hmm.
        Kannski er ég týndur hér inni...
    """),
    "RockTunnel_1F_Text_OliverDefeat": t("""
        Slakaðu á!
        Hvað er ég að gera?
        Hver er leiðin út?
    """),
    "RockTunnel_1F_Text_OliverPostBattle": t("""
        Þetta sofandi vasaskrímsli á ROUTE 12
        neyddi mig til að taka þessa hjáleið.
    """),
    "RockTunnel_1F_Text_LucasIntro": t("""
        Utanaðkomandi eins og þú þurfa að
        sýna mér smá virðingu!
    """),
    "RockTunnel_1F_Text_LucasDefeat": t("""
        Ég gefst upp!
    """),
    "RockTunnel_1F_Text_LucasPostBattle": t("""
        Þú ert nógu hæfileikaríkur til að
        ganga fjöll!
    """),
    "RockTunnel_1F_Text_AshtonIntro": t("""
        Vasaskrímsli berjast!
        Tilbúin, byrja!
    """),
    "RockTunnel_1F_Text_AshtonDefeat": t("""
        Leik lokið!
    """),
    "RockTunnel_1F_Text_AshtonPostBattle": t("""
        Jæja, ég næ mér í BLAKILDA á leiðinni!
    """),
    "RockTunnel_1F_Text_LeahIntro": t("""
        Ííík!

        Ekki reyna neitt skrýtið í myrkrinu!
    """),
    "RockTunnel_1F_Text_LeahDefeat": t("""
        Það var of dimmt...
    """),
    "RockTunnel_1F_Text_LeahPostBattle": t("""
        Ég sá ÞREKANGA í þessum göngum.
    """),
    "RockTunnel_1F_Text_DanaIntro": t("""
        Ég kom alla þessa leið í leit að
        villtum vasaskrímslum.
    """),
    "RockTunnel_1F_Text_DanaDefeat": t("""
        Ég er uppiskroppa með vasaskrímsli!
    """),
    "RockTunnel_1F_Text_DanaPostBattle": t("""
        Þú leitst út fyrir að vera sætur og
        meinlaus.
        Þar hafði ég heldur betur rangt fyrir
        mér!
    """),
    "RockTunnel_1F_Text_ArianaIntro": t("""
        Þú ert með vasaskrímsli!
        Byrjum!
    """),
    "RockTunnel_1F_Text_ArianaDefeat": t("""
        Þú spilar hart!
    """),
    "RockTunnel_1F_Text_ArianaPostBattle": t("""
        Úff!
        Ég er orðin öll sveitt.
    """),
    "RockTunnel_1F_Text_RouteSign": t("""
        ROCK TUNNEL
        CERULEAN BORG - LAVENDER BORG
    """),
    "RockTunnel_B1F_Text_SofiaIntro": t("""
        Veistu hvernig þú getur forðast að
        villast í fjöllunum?

        Þú getur beygt greinar sem
        leiðarmerki.
    """),
    "RockTunnel_B1F_Text_SofiaDefeat": t("""
        Óóó!
        Ég gerði mitt besta!
    """),
    "RockTunnel_B1F_Text_SofiaPostBattle": t("""
        Mig langar heim!
    """),
    "RockTunnel_B1F_Text_DudleyIntro": t("""
        Hahaha!
        Geturðu sigrað kraftinn minn?
    """),
    "RockTunnel_B1F_Text_DudleyDefeat": t("""
        Úps!
        Þú varst sterkari!
    """),
    "RockTunnel_B1F_Text_DudleyPostBattle": t("""
        Ég vel kraft því ég hata að hugsa.
    """),
    "RockTunnel_B1F_Text_CooperIntro": t("""
        Ertu með VasaDEX?
        Mig langar líka í svoleiðis.
    """),
    "RockTunnel_B1F_Text_CooperDefeat": t("""
        Skot!
        Ég er svo öfundsjúkur!
    """),
    "RockTunnel_B1F_Text_CooperPostBattle": t("""
        Þegar þú klárar VasaDEX-ið þitt, má
        ég þá fá það?
    """),
    "RockTunnel_B1F_Text_SteveIntro": t("""
        Umm... Veistu um
        vasaskrímsla-búningaleik?
    """),
    "RockTunnel_B1F_Text_SteveDefeat": t("""
        Jæja, þá er það það.
    """),
    "RockTunnel_B1F_Text_StevePostBattle": t("""
        Vasaskrímsla-búningaleikur er að
        klæða sig eins og vasaskrímsli til
        gamans.

        BLEIKÁLFUR er vinsæll kostur.
    """),
    "RockTunnel_B1F_Text_AllenIntro": t("""
        Vasaskrímslatæknin mín lætur þig
        gráta!
    """),
    "RockTunnel_B1F_Text_AllenDefeat": t("""
        Ég gefst upp!
        Þú ert betri tæknimaður!
    """),
    "RockTunnel_B1F_Text_AllenPostBattle": t("""
        Í fjöllum finnurðu oft STEIN-gerðar
        vasaskrímsli.
    """),
    "RockTunnel_B1F_Text_MarthaIntro": t("""
        Ég kem ekki oft hingað, en ég ætla að
        berjast við þig.
    """),
    "RockTunnel_B1F_Text_MarthaDefeat": t("""
        Ó!
        Ég tapaði!
    """),
    "RockTunnel_B1F_Text_MarthaPostBattle": t("""
        Mér líkar við pínulítil vasaskrímsli.
        Þau stóru eru of ógnvekjandi!
    """),
    "RockTunnel_B1F_Text_EricIntro": t("""
        Skelltu þínu besta á mig!
    """),
    "RockTunnel_B1F_Text_EricDefeat": t("""
        Skotið af!
    """),
    "RockTunnel_B1F_Text_EricPostBattle": t("""
        Ég ala vasaskrímslin mín upp til að
        sigra þín, krakki.
    """),
    "RockTunnel_B1F_Text_WinstonIntro": t("""
        Ég teikna myndir af vasaskrímslum
        þegar ég er heima.
    """),
    "RockTunnel_B1F_Text_WinstonDefeat": t("""
        Úff...
        Ég er örmagna...
    """),
    "RockTunnel_B1F_Text_WinstonPostBattle": t("""
        Ég er listamaður, ekki bardagamaður.
        Ég fer heim að teikna.
    """),
    "Route10_Text_MarkIntro": t("""
        Vá, komstu alla leið hingað?
        Kannski ertu líka vasaskrímslaæðingur?
        Viltu sjá safnið mitt?
    """),
    "Route10_Text_MarkDefeat": t("""
        Hmph.
        Ég er ekki reiður!
    """),
    "Route10_Text_MarkPostBattle": t("""
        Ég á fleiri sjaldgæf vasaskrímsli
        heima!
    """),
    "Route10_Text_ClarkIntro": t("""
        Ha-hahah-ah-ha!
    """),
    "Route10_Text_ClarkDefeat": t("""
        Ha-haha!
        Ekki að hlæja!
        Ha-hay fever! Haha-ha-tjí!
    """),
    "Route10_Text_ClarkPostBattle": t("""
        Haha-ha-tjí!
        Ha-tjí!
        Snökt! Snökt!
    """),
    "Route10_Text_HermanIntro": t("""
        Hæ, krakki!
        Viltu sjá vasaskrímslið mitt?
    """),
    "Route10_Text_HermanDefeat": t("""
        Ó, nei!
        Vasaskrímslið mitt!
    """),
    "Route10_Text_HermanPostBattle": t("""
        Mér líkar ekki við þig.
        Mér líkar ekki við neinn sem er betri
        en ég!
    """),
    "Route10_Text_HeidiIntro": t("""
        Ég hef nokkrum sinnum komið út úr
        vasaskrímsla-SAL.

        ...En ég tapa alltaf.
    """),
    "Route10_Text_HeidiDefeat": t("""
        Óó!
        Eftir alla þjálfunina!
    """),
    "Route10_Text_HeidiPostBattle": t("""
        Ég tók eftir nokkrum
        vasaskrímslaæðingum á ráfi.

        Geturðu ímyndað þér það?
        Þau?
        Hér uppi í fjöllunum?
    """),
    "Route10_Text_TrentIntro": t("""
        Ah!
        Þetta fjallaloft er ljúffengt!
    """),
    "Route10_Text_TrentDefeat": t("""
        Þetta hreinsaði höfuðið!
    """),
    "Route10_Text_TrentPostBattle": t("""
        Ég er útþaninn af fjallalofti!
    """),
    "Route10_Text_CarolIntro": t("""
        Mér er dálítið yfirliða.
        Ég hef ekki gengið á fjöll lengi.
    """),
    "Route10_Text_CarolDefeat": t("""
        Ég er of þreytt.
        Ég var ekki tilbúin í þetta.
    """),
    "Route10_Text_CarolPostBattle": t("""
        Vasaskrímslin hér í fjöllunum eru svo
        þybbin...

        Ég vildi að til væru bleik
        vasaskrímsli með blómamynstri!
    """),
    "Route10_Text_RockTunnelDetourToLavender": t("""
        ROCK TUNNEL
        Hjáleið til LAVENDER BORGAR
    """),
    "Route10_Text_RockTunnel": t("""
        ROCK TUNNEL
    """),
    "Route10_Text_PowerPlant": t("""
        ORKUVER
    """),
    "Route10_PokemonCenter_1F_Text_EveryTypeStrongerThanOthers": t("""
        Gerðir vasaskrímsla virka ólíkt hver
        gagnvart annarri.

        Hver gerð er sterkari en sumar gerðir
        og veikari en aðrar.
    """),
    "Route10_PokemonCenter_1F_Text_NuggetUselessSoldFor5000": t("""
        GULLKLUMPUR nýtist mér ekkert.
        Svo ég seldi hann fyrir ¥5000.
    """),
    "Route10_PokemonCenter_1F_Text_HeardGhostsHauntLavender": t("""
        Ég heyrði að draugar ásæki LAVENDER
        BORG.
    """),
    "Route10_PokemonCenter_1F_Text_GiveEverstoneIfCaught20Mons": t("""
        Ó... {PLAYER}!
        Ég hef verið að leita að þér!

        Þetta er ég, einn af síviðstöddum
        AÐSTOÐARMÖNNUM PROF. OAK.

        Ef VasaDEX-ið þitt er með full gögn
        um tuttugu tegundir á ég að gefa þér
        verðlaun frá PROF. OAK.

        Hann fól mér þennan EILÍFSTEIN.

        Svo, {PLAYER}, leyfðu mér að spyrja.

        Hefurðu safnað gögnum um að minnsta
        kosti tuttugu gerðir vasaskrímsla?
    """),
    "Route10_PokemonCenter_1F_Text_GreatHereYouGo": t("""
        Frábært! Þú hefur náð eða átt
        {STR_VAR_3} gerðir vasaskrímsla!

        Til hamingju!
        Gjörðu svo vel!
    """),
    "Route10_PokemonCenter_1F_Text_ReceivedEverstoneFromAide": t("""
        {PLAYER} fékk EILÍFSTEIN frá
        AÐSTOÐARMANNINUM.
    """),
    "Route10_PokemonCenter_1F_Text_ExplainEverstone": t("""
        Að láta vasaskrímsli þróast getur
        vissulega bætt við VasaDEX-ið.

        En stundum viltu kannski ekki að
        ákveðið vasaskrímsli þróist.

        Þá skaltu gefa því EILÍFSTEIN.

        Hann kemur í veg fyrir þróun, að sögn
        PRÓFESSORSINS.
    """),
    "Route9_Text_AliciaIntro": t("""
        Þú ert með vasaskrímsli með þér!
        Þú ert mín!
    """),
    "Route9_Text_AliciaDefeat": t("""
        Þú blekktir mig...
    """),
    "Route9_Text_AliciaPostBattle": t("""
        Göngin framundan eru kolniðamyrk að
        innan.

        Þú þarft LEIFTUR til að komast í
        gegnum þau.
    """),
    "Route9_Text_ChrisIntro": t("""
        Hver gengur þarna með þessi flottu
        vasaskrímsli?
    """),
    "Route9_Text_ChrisDefeat": t("""
        Slökktur eins og ljós!
    """),
    "Route9_Text_ChrisPostBattle": t("""
        Haltu áfram að ganga!
    """),
    "Route9_Text_DrewIntro": t("""
        Ég fer um ROCK TUNNEL til að komast
        til LAVENDER...
    """),
    "Route9_Text_DrewDefeat": t("""
        Ég stóðst ekki samanburð...
    """),
    "Route9_Text_DrewPostBattle": t("""
        Ertu líka á leið í ROCK TUNNEL?
    """),
    "Route9_Text_CaitlinIntro": t("""
        Ekki voga þér að líta niður á mig!
    """),
    "Route9_Text_CaitlinDefeat": t("""
        Nei!
        Þú ert of mikið.
    """),
    "Route9_Text_CaitlinPostBattle": t("""
        Þú ert augljóslega hæfileikaríkur.
        Gangi þér vel!
    """),
    "Route9_Text_JeremyIntro": t("""
        Bwahaha!
        Frábært! Mér leiddist, ha!
    """),
    "Route9_Text_JeremyDefeat": t("""
        Haltu þessu áfram, ha!

        Ó bíddu.
        Ég er uppiskroppa með vasaskrímsli!
    """),
    "Route9_Text_JeremyPostBattle": t("""
        Þú hafðir greinilega kjark til að
        standa uppi í hárinu á mér, ha?
    """),
    "Route9_Text_BriceIntro": t("""
        Hahaha!
        Ertu ekki svolítið harður af þér!
    """),
    "Route9_Text_BriceDefeat": t("""
        Hvað er þetta?
    """),
    "Route9_Text_BricePostBattle": t("""
        Hahaha!
        Krakkar eiga að vera harðir!
    """),
    "Route9_Text_BrentIntro": t("""
        Ég vaknaði snemma á hverjum degi til
        að ala vasaskrímslin mín úr púpunum!
    """),
    "Route9_Text_BrentDefeat": t("""
        HVAÐ?

        Hvílík tímasóun!
    """),
    "Route9_Text_BrentPostBattle": t("""
        Ég þarf að safna fleiru en pöddum til
        að verða sterkari...
    """),
    "Route9_Text_AlanIntro": t("""
        Hahahaha!
        Komdu með það!
    """),
    "Route9_Text_AlanDefeat": t("""
        Hahahaha!
        Þú vannst mig heiðarlega!
    """),
    "Route9_Text_AlanPostBattle": t("""
        Hahahaha!
        Við hraustu gaurarnir hlæjum alltaf!
    """),
    "Route9_Text_ConnerIntro": t("""
        Áfram, ofur PÖDDU-vasaskrímslin mín!
    """),
    "Route9_Text_ConnerDefeat": t("""
        Pöddurnar mínar...
    """),
    "Route9_Text_ConnerPostBattle": t("""
        Ef þér líkar ekki við
        PÖDDU-vasaskrímsli, þá pirrarðu mig!
    """),
    "Route9_Text_RouteSign": t("""
        ROUTE 9
        CERULEAN BORG - ROCK TUNNEL
    """),
}


FILES = {
    "data/maps/Route9/text.inc",
    "data/maps/Route10/text.inc",
    "data/maps/Route10_PokemonCenter_1F/text.inc",
    "data/maps/RockTunnel_1F/text.inc",
    "data/maps/RockTunnel_B1F/text.inc",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-after-v10.csv")
    parser.add_argument("--output", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-rock-tunnel-v1.csv")
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
        row["notes"] = "codex curated Route 9, Route 10, and Rock Tunnel v1"
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
