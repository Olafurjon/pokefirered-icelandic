from __future__ import annotations

import argparse
import csv
import textwrap
from pathlib import Path

from common import repo_root


def t(value: str) -> str:
    return textwrap.dedent(value).strip()


TRANSLATIONS = {
    "LavenderTown_Text_DoYouBelieveInGhosts": t("""
        Trúirðu á drauga?
    """),
    "LavenderTown_Text_SoThereAreBelievers": t("""
        Í alvöru?
        Þá eru til trúaðir eftir allt...
    """),
    "LavenderTown_Text_JustImaginingWhiteHand": t("""
        Hahaha, líklega ekki.

        Þessi hvíta hönd á öxlinni á þér...
        Ég er bara að ímynda mér hana.
    """),
    "LavenderTown_Text_TownKnownAsMonGraveSite": t("""
        Þessi bær er þekktur sem grafreitur
        vasaskrímsla.

        Minningarathafnir eru haldnar í
        VASASKRÍMSLATURNI.
    """),
    "LavenderTown_Text_GhostsAppearedInTower": t("""
        Draugar birtust í VASASKRÍMSLATURNI.

        Ég held að þeir séu andar
        vasaskrímsla sem ROCKET-liðar drápu.
    """),
    "LavenderTown_Text_TownSign": t("""
        LAVENDER BORG
        Hin göfuga fjólubláa borg
    """),
    "LavenderTown_Text_SilphScopeNotice": t("""
        Nýr SILPH SCOPE!
        Gerir hið ósýnilega sýnilegt!

        SILPH CO.
    """),
    "LavenderTown_Text_VolunteerPokemonHouse": t("""
        LAVENDER SJÁLFBOÐA
        VASASKRÍMSLAHÚS
    """),
    "LavenderTown_Text_PokemonTowerSign": t("""
        VASASKRÍMSLATURN
        Róið anda vasaskrímsla
    """),
    "LavenderTown_House1_Text_Cubone": t("""
        BEINFARI: Kyarugoo!
    """),
    "LavenderTown_House1_Text_RocketsKilledCubonesMother": t("""
        Þessir hræðilegu ROCKET-liðar!
        Þeir eiga enga miskunn skilið!

        Vesalings móðir BEINFARA...

        Hún var drepin þegar hún reyndi að
        flýja frá TEAM ROCKET.
    """),
    "LavenderTown_House1_Text_GhostOfPokemonTowerIsGone": t("""
        Draugurinn í VASASKRÍMSLATURNI er
        horfinn!

        Einhver hlýtur að hafa sefað
        órólega sál hans!
    """),
    "LavenderTown_House2_Text_WantMeToRateNicknames": t("""
        Halló, halló!
        Ég er opinberi NAFNADÓMARINN!

        Viltu að ég meti gælunöfnin á
        vasaskrímslunum þínum?
    """),
    "LavenderTown_House2_Text_CritiqueWhichMonsNickname": t("""
        Gælunafn hvaða vasaskrímslis á ég
        að dæma?
    """),
    "LavenderTown_House2_Text_GiveItANicerName": t("""
        {STR_VAR_1}, segirðu?
        Það er sæmilegt gælunafn!

        En viltu að ég gefi því fallegra nafn?

        Hvað segirðu?
    """),
    "LavenderTown_House2_Text_WhatShallNewNicknameBe": t("""
        Ah, gott. Hvert á nýja gælunafnið
        þá að vera?
    """),
    "LavenderTown_House2_Text_FromNowOnShallBeKnownAsName": t("""
        Búið! Héðan í frá skal þetta
        vasaskrímsli heita {STR_VAR_1}!

        Það er betra nafn en áður!
        Hvílík heppni fyrir þig!
    """),
    "LavenderTown_House2_Text_ISeeComeVisitAgain": t("""
        Ég skil.
        Komdu endilega aftur í heimsókn.
    """),
    "LavenderTown_House2_Text_FromNowOnShallBeKnownAsSameName": t("""
        Búið! Héðan í frá skal þetta
        vasaskrímsli heita {STR_VAR_1}!

        Það lítur ekkert öðruvísi út, en
        samt er þetta miklu betra!

        Hvílík heppni fyrir þig!
    """),
    "LavenderTown_House2_Text_TrulyImpeccableName": t("""
        {STR_VAR_1}, segirðu?
        Það er sannarlega óaðfinnanlegt nafn!

        Gættu {STR_VAR_1} vel!
    """),
    "LavenderTown_House2_Text_ThatIsMerelyAnEgg": t("""
        Nú, nú.
        Þetta er bara EGG!
    """),
    "LavenderTown_Mart_Text_SearchingForStatRaiseItems": t("""
        Ég leita að hlutum sem hækka
        tölugildi vasaskrímsla.

        Þeir virka aðeins út einn bardaga.

        X ATTACK, X DEFEND, X SPEED og
        X SPECIAL eru það sem mig vantar.

        Veistu hvar ég fæ þá?
    """),
    "LavenderTown_Mart_Text_DidYouBuyRevives": t("""
        Keyptirðu ENDURLÍFGARA?
        Þeir vekja rotið vasaskrímsli aftur!
    """),
    "LavenderTown_Mart_Text_TrainerDuosCanChallengeYou": t("""
        Stundum skorar ÞJÁLFARA-tvennd á
        þig með tveimur vasaskrímslum í einu.

        Þá þarftu líka að senda út tvö
        vasaskrímsli í bardaga.
    """),
    "LavenderTown_Mart_Text_SoldNuggetFromMountainsFor5000": t("""
        Um daginn fann ég GULLKLUMP djúpt
        inni í fjöllunum!

        Hann nýtist ekkert sem hlutur, en
        þegar ég seldi hann fékk ég heilar
        5000¥!
    """),
    "LavenderTown_PokemonCenter_1F_Text_RocketsDoAnythingForMoney": t("""
        TEAM ROCKET gerir hvað sem er fyrir
        peninga!

        Ekkert verk er of skítugt, enginn
        verknaður of svívirðilegur, enginn
        glæpur of illur!
    """),
    "LavenderTown_PokemonCenter_1F_Text_CubonesMotherKilledByRockets": t("""
        Ég sá móður BEINFARA reyna að flýja
        frá TEAM ROCKET.

        Hún var drepin þegar hún reyndi að
        komast undan...
    """),
    "LavenderTown_PokemonCenter_1F_Text_PeoplePayForCuboneSkulls": t("""
        Þú veist að BEINFARI-tegundin ber
        höfuðkúpur, ekki satt?

        Fólk borgar mikið fyrir eina slíka.
    """),
    "LavenderTown_PokemonCenter_1F_Text_HearMrFujiNotFromAroundHere": t("""
        Ég flutti nýlega í þennan bæ.

        Ég heyri að MR. FUJI sé ekki héðan
        upprunalega heldur.
    """),
    "LavenderTown_VolunteerPokemonHouse_Text_WhereDidMrFujiGo": t("""
        Þetta er skrýtið, MR. FUJI er ekki
        hér.
        Hvert fór hann?
    """),
    "LavenderTown_VolunteerPokemonHouse_Text_MrFujiWasPrayingForCubonesMother": t("""
        MR. FUJI hafði verið einn að biðja
        fyrir móður BEINFARA.
    """),
    "LavenderTown_VolunteerPokemonHouse_Text_MrFujiLooksAfterOrphanedMons": t("""
        Þetta er í raun húsið hans MR. FUJI.

        Hann er einstaklega góður.

        Hann annast yfirgefin og munaðarlaus
        vasaskrímsli.
    """),
    "LavenderTown_VolunteerPokemonHouse_Text_MonsNiceToHug": t("""
        Það er svo hlýtt!
        Það er svo gott að faðma vasaskrímsli.
    """),
    "LavenderTown_VolunteerPokemonHouse_Text_Nidorino": t("""
        NÁLHERRA: Gaoo!
    """),
    "LavenderTown_VolunteerPokemonHouse_Text_Psyduck": t("""
        MÍGRENDI: Gwappa!
    """),
    "LavenderTown_VolunteerPokemonHouse_Text_IdLikeYouToHaveThis": t("""
        MR. FUJI: {PLAYER}...

        VasaDEX-leiðangurinn þinn krefst
        mikillar staðfestu.

        Án djúprar ástar á vasaskrímslum
        gæti leiðangurinn mistekist.

        Ég veit ekki hvort þetta hjálpar, en
        ég vil að þú fáir þetta.
    """),
    "LavenderTown_VolunteerPokemonHouse_Text_ReceivedPokeFluteFromMrFuji": t("""
        {PLAYER} fékk VASAFLAUTU frá
        MR. FUJI.
    """),
    "LavenderTown_VolunteerPokemonHouse_Text_ExplainPokeFlute": t("""
        Þegar VASAFLAUTA heyrist hrökkva
        sofandi vasaskrímsli vakandi.

        Prófaðu að nota hana á vasaskrímsli
        sem sofa í vegi þínum.
    """),
    "LavenderTown_VolunteerPokemonHouse_Text_MustMakeRoomForThis": t("""
        Þú verður að búa til pláss fyrir
        þetta!
    """),
    "LavenderTown_VolunteerPokemonHouse_Text_HasPokeFluteHelpedYou": t("""
        MR. FUJI: Hefur VASAFLAUTAN mín
        hjálpað þér?
    """),
    "LavenderTown_VolunteerPokemonHouse_Text_GrandPrizeDrawingClipped": t("""
        VASASKRÍMSLA-AÐDÁENDABLAÐ
        Mánaðarlegur stórvinningur!

        Umsóknarblaðið er...

        Horfið! Það hefur verið klippt út.
        Einhver hlýtur að hafa sótt um.
    """),
    "LavenderTown_VolunteerPokemonHouse_Text_PokemonMagazinesLineShelf": t("""
        Vasaskrímslablöð raða sér í hilluna.

        VASASKRÍMSLA INNSÝN...

        VASASKRÍMSLA AÐDÁANDI...
    """),
    "PokemonTower_1F_Text_ErectedInMemoryOfDeadMons": t("""
        VASASKRÍMSLATURN var reist til
        minningar um vasaskrímsli sem dóu.
    """),
    "PokemonTower_1F_Text_ComeToPayRespectsSon": t("""
        Komstu til að votta virðingu þína?

        Blessað sé vasaskrímslaelskandi
        hjarta þitt, drengur.
    """),
    "PokemonTower_1F_Text_ComeToPayRespectsGirl": t("""
        Komstu til að votta virðingu þína?

        Blessað sé vasaskrímslaelskandi
        hjarta þitt, stúlka.
    """),
    "PokemonTower_1F_Text_CameToPrayForDepartedClefairy": t("""
        Ég kom til að biðja fyrir mínum
        ástkæra, látna BLEIKÁLFI.

        Snökt!
        Ég er að drukkna í tárum...
    """),
    "PokemonTower_1F_Text_GrowlitheWhyDidYouDie": t("""
        BLYSRAKKINN minn...
        Af hverju þurftirðu að deyja?
    """),
    "PokemonTower_1F_Text_SenseSpiritsUpToMischief": t("""
        Ég er MIÐILL.

        Hér eru andar með ólátum.
        Ég finn fyrir þeim ofar í TURNINUM.
    """),
    "PokemonTower_2F_Text_RivalIntro": t("""
        {RIVAL}: Hæ, {PLAYER}!
        Hvað ert þú að gera hér?
        Er vasaskrímslið þitt dautt?

        Hæ! Það er lifandi!

        Ég get að minnsta kosti rotað þau!
        Byrjum!
    """),
    "PokemonTower_2F_Text_RivalDefeat": t("""
        Hvað?
        Þú óþokki!

        Ég fór meira að segja létt með þig!
    """),
    "PokemonTower_2F_Text_RivalVictory": t("""
        {RIVAL}: Æ, æ...!
        Það hrundi í alvöru!

        Veikt!
        Þú verður að ala það betur upp!
    """),
    "PokemonTower_2F_Text_RivalPostBattle": t("""
        Hvernig gengur með VasaDEX-ið þitt?
        Ég náði rétt í BEINFARA!

        Ég finn ekki stærri HNAUSKÚPUNA.
        Hvar gætu þær verið?

        Ég veðja að engar eru eftir!

        Jæja, ég ætti að koma mér.
        Ég hef margt að gera, ólíkt þér.

        Sé þig seinna!
    """),
    "PokemonTower_2F_Text_SilphScopeCouldUnmaskGhosts": t("""
        Ekki einu sinni við gátum borið
        kennsl á villuráfandi draugana.

        SILPH SCOPE gæti afhjúpað þá.
    """),
    "PokemonTower_3F_Text_HopeIntro": t("""
        Urrg... Awaa...
        Huhu... Graa...
    """),
    "PokemonTower_3F_Text_HopeDefeat": t("""
        Hwa!
        Mér er bjargað!
    """),
    "PokemonTower_3F_Text_HopePostBattle": t("""
        SILPH SCOPE getur borið kennsl á
        draugana.
    """),
    "PokemonTower_3F_Text_CarlyIntro": t("""
        Kekeke...
        Kwaaah!
    """),
    "PokemonTower_3F_Text_CarlyDefeat": t("""
        Hmm?
        Hvað er ég að gera?
    """),
    "PokemonTower_3F_Text_CarlyPostBattle": t("""
        Fyrirgefðu!
        Ég var andsetin!
    """),
    "PokemonTower_3F_Text_PatriciaIntro": t("""
        Burt með þig!
        Illgjarni andi!
    """),
    "PokemonTower_3F_Text_PatriciaDefeat": t("""
        Úff!
        Andinn fór!
    """),
    "PokemonTower_3F_Text_PatriciaPostBattle": t("""
        Hin fyrir ofan...
        Þær hljóta að vera andsetnar.
    """),
    "PokemonTower_4F_Text_PaulaIntro": t("""
        Draugur! Nei!
        Kwaaah!
    """),
    "PokemonTower_4F_Text_PaulaDefeat": t("""
        Hvar er draugurinn?
    """),
    "PokemonTower_4F_Text_PaulaPostBattle": t("""
        Mig hlýtur að hafa verið að dreyma...
    """),
    "PokemonTower_4F_Text_LaurelIntro": t("""
        Vertu bölvaður með mér!
        Kwaaah!
    """),
    "PokemonTower_4F_Text_LaurelDefeat": t("""
        Hvað!
    """),
    "PokemonTower_4F_Text_LaurelPostBattle": t("""
        Við getum ekki greint hverjir
        draugarnir eru...
    """),
    "PokemonTower_4F_Text_JodyIntro": t("""
        Huhuhu...
        Sigraðu mig ekki!
    """),
    "PokemonTower_4F_Text_JodyDefeat": t("""
        Ha?
        Hver? Hvað?
    """),
    "PokemonTower_4F_Text_JodyPostBattle": t("""
        Megi látin vasaskrímsli hvíla í friði...
    """),
    "PokemonTower_5F_Text_RestHereInPurifiedSpace": t("""
        Komdu, barn!
        Ég hef hreinsað þetta svæði.
        Þú getur hvílt þig hér.
    """),
    "PokemonTower_5F_Text_TammyIntro": t("""
        Gefðu...mér...
        allt...þitt...
    """),
    "PokemonTower_5F_Text_TammyDefeat": t("""
        Andkaf!
    """),
    "PokemonTower_5F_Text_TammyPostBattle": t("""
        Ég var undir andsetningu.
    """),
    "PokemonTower_5F_Text_RuthIntro": t("""
        Þú...skalt...
        ganga...til...liðs...við...okkur...
    """),
    "PokemonTower_5F_Text_RuthDefeat": t("""
        Hvílík martröð!
    """),
    "PokemonTower_5F_Text_RuthPostBattle": t("""
        Ég var andsetin.
    """),
    "PokemonTower_5F_Text_KarinaIntro": t("""
        Uppvakningar!
    """),
    "PokemonTower_5F_Text_KarinaDefeat": t("""
        Ha?
    """),
    "PokemonTower_5F_Text_KarinaPostBattle": t("""
        Ég náði áttum aftur.
    """),
    "PokemonTower_5F_Text_JanaeIntro": t("""
        Urgah...
        Urff...
    """),
    "PokemonTower_5F_Text_JanaeDefeat": t("""
        Hú!
    """),
    "PokemonTower_5F_Text_JanaePostBattle": t("""
        Ég féll fyrir illum öndum þrátt fyrir
        þjálfun mína í fjöllunum...
    """),
    "PokemonTower_5F_Text_PurifiedZoneMonsFullyHealed": t("""
        Gengið inn á hreinsað og verndað
        svæði.

        Vasaskrímsli {PLAYER} voru læknuð að
        fullu.
    """),
    "PokemonTower_6F_Text_AngelicaIntro": t("""
        Gefðu...mér...
        blóð...
    """),
    "PokemonTower_6F_Text_AngelicaDefeat": t("""
        Stuna!
    """),
    "PokemonTower_6F_Text_AngelicaPostBattle": t("""
        Ég er blóðlítil og máttvana...
    """),
    "PokemonTower_6F_Text_EmiliaIntro": t("""
        Urff...
        Kwaah!
    """),
    "PokemonTower_6F_Text_EmiliaDefeat": t("""
        Eitthvað datt af!
    """),
    "PokemonTower_6F_Text_EmiliaPostBattle": t("""
        Hárið mitt datt ekki af!
        Þetta var illgjarn andi!
    """),
    "PokemonTower_6F_Text_JenniferIntro": t("""
        Ke...ke...ke...
        ke...ke...ke!
    """),
    "PokemonTower_6F_Text_JenniferDefeat": t("""
        Keee!
    """),
    "PokemonTower_6F_Text_JenniferPostBattle": t("""
        Hvað er eiginlega í gangi hér?
    """),
    "PokemonTower_6F_Text_BeGoneIntruders": t("""
        Burt með ykkur...
        Aðkomufólk...
    """),
    "PokemonTower_6F_Text_GhostWasCubonesMother": t("""
        Draugurinn var óróleg sál móður
        BEINFARA!
    """),
    "PokemonTower_6F_Text_MothersSpiritWasCalmed": t("""
        Andi móðurinnar var sefaður.

        Hún hélt yfir í handanheiminn...
    """),
    "PokemonTower_7F_Text_Grunt1Intro": t("""
        Hvað viltu?
        Af hverju ertu hér?
    """),
    "PokemonTower_7F_Text_Grunt1Defeat": t("""
        Ég gefst upp!
    """),
    "PokemonTower_7F_Text_Grunt1PostBattle": t("""
        Ég gleymi þessu ekki!
    """),
    "PokemonTower_7F_Text_Grunt2Intro": t("""
        Þessi gamli karl gekk beint upp að
        FELUSTAÐNUM okkar.

        Svo fór hann að tuða um að TEAM
        ROCKET misþyrmi vasaskrímslum.

        Við erum bara að ræða málið eins og
        fullorðið fólk.
    """),
    "PokemonTower_7F_Text_Grunt2Defeat": t("""
        Vinsamlegast!
        Ekki meira!
    """),
    "PokemonTower_7F_Text_Grunt2PostBattle": t("""
        Vasaskrímsli eru bara góð til að
        græða peninga. Af hverju ekki að
        nota þau?

        Haltu þér utan við okkar mál!
    """),
    "PokemonTower_7F_Text_Grunt3Intro": t("""
        Þú bjargar engum, krakki!
    """),
    "PokemonTower_7F_Text_Grunt3Defeat": t("""
        Ekki berjast við okkur ROCKET-liða!
    """),
    "PokemonTower_7F_Text_Grunt3PostBattle": t("""
        Þú kemst ekki upp með þetta!
    """),
    "PokemonTower_7F_Text_MrFujiThankYouFollowMe": t("""
        MR. FUJI: Ha?
        Komstu til að bjarga mér?

        Þakka þér. En ég kom hingað af
        fúsum og frjálsum vilja.

        Ég kom til að sefa anda móður
        BEINFARA.

        Ég held að andi HNAUSKÚPU hafi loks
        yfirgefið okkur.

        Ég verð að þakka þér fyrir hlýja
        umhyggju þína.

        Fylgdu mér heim til mín, í
        VASASKRÍMSLAHÚSIÐ við rætur turnsins.
    """),
}


FILES = {
    "data/maps/LavenderTown/text.inc",
    "data/maps/LavenderTown_House1/text.inc",
    "data/maps/LavenderTown_House2/text.inc",
    "data/maps/LavenderTown_Mart/text.inc",
    "data/maps/LavenderTown_PokemonCenter_1F/text.inc",
    "data/maps/LavenderTown_VolunteerPokemonHouse/text.inc",
    "data/maps/PokemonTower_1F/text.inc",
    "data/maps/PokemonTower_2F/text.inc",
    "data/maps/PokemonTower_3F/text.inc",
    "data/maps/PokemonTower_4F/text.inc",
    "data/maps/PokemonTower_5F/text.inc",
    "data/maps/PokemonTower_6F/text.inc",
    "data/maps/PokemonTower_7F/text.inc",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-after-v13.csv")
    parser.add_argument("--output", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-lavender-tower-v1.csv")
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
        row["notes"] = "codex curated Lavender Town and Pokemon Tower v1"
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
