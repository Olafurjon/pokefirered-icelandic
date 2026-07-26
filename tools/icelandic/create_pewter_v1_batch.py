from __future__ import annotations

import argparse
import csv
import textwrap
from pathlib import Path

from common import repo_root


def t(value: str) -> str:
    return textwrap.dedent(value).strip()


TRANSLATIONS = {
    "Text_DreamEaterTeach": t("""
        Geisp!
        Ég hlýt að hafa dottað í sólinni.

        Mig dreymdi skrýtinn draum um DÁVI
        sem át drauminn minn.

        Og...
        Ég lærði að éta drauma...

        Úff, þetta er allt of
        hrollvekjandi!

        Leyfðu mér að kenna vasaskrímsli
        þetta svo ég geti gleymt því!
    """),
    "Text_DreamEaterDeclined": t("""
        ...Hrot...
    """),
    "Text_DreamEaterWhichMon": t("""
        Hvaða vasaskrímsli vill læra
        DRAUMAÆTA?
    """),
    "Text_DreamEaterTaught": t("""
        ...ZZZ...
        Ég... get ekki étið... meira...
    """),
    "PewterCity_Text_ClefairyCameFromMoon": t("""
        BLEIKÁLFUR kom frá tunglinu.
        Það er orðrómurinn.

        Þau birtust eftir að TUNGLSTEINAR
        féllu á MT. MOON.
    """),
    "PewterCity_Text_BrockOnlySeriousTrainerHere": t("""
        Það eru ekki margir alvarlegir
        vasaskrímslaþjálfarar hér.

        Flestir eru eins og PÖDDUVEIÐARAR,
        bara áhugafólk.

        En BROCK í PEWTER-SALNUM er alls
        ekki þannig.
    """),
    "PewterCity_Text_DidYouCheckOutMuseum": t("""
        Skoðaðirðu SAFNIÐ?
    """),
    "PewterCity_Text_WerentThoseFossilsAmazing": t("""
        Voru steingervingarnir frá MT. MOON
        ekki stórkostlegir?
    """),
    "PewterCity_Text_ReallyYouHaveToGo": t("""
        Í alvöru?
        Þú verður endilega að fara!
    """),
    "PewterCity_Text_ThisIsTheMuseum": t("""
        Þetta er SAFNIÐ.

        Það kostar að fara inn, en það er
        þess virði. Sjáumst!
    """),
    "PewterCity_Text_DoYouKnowWhatImDoing": t("""
        Psssst!
        Veistu hvað ég er að gera?
    """),
    "PewterCity_Text_ThatsRightItsHardWork": t("""
        Rétt!
        Þetta er erfið vinna!
    """),
    "PewterCity_Text_SprayingRepelToKeepWildMonsOut": t("""
        Ég úða REPEL til að halda villtum
        vasaskrímslum frá garðinum mínum!
    """),
    "PewterCity_Text_BrocksLookingForChallengersFollowMe": t("""
        Þú ert ÞJÁLFARI, ekki satt?

        BROCK leitar að nýjum áskorendum.
        Fylgdu mér!
    """),
    "PewterCity_Text_GoTakeOnBrock": t("""
        Ef þú hefur það sem þarf skaltu
        skora á BROCK!
    """),
    "PewterCity_Text_TrainerTipsEarningEXP": t("""
        ÞJÁLFARARÁÐ

        Öll vasaskrímsli sem birtast í
        bardaga, þó stutt sé, fá EXP stig.
    """),
    "PewterCity_Text_CallPoliceIfInfoOnThieves": t("""
        TILKYNNING!

        Þjófar hafa verið að stela
        steingervingum vasaskrímsla úr
        MT. MOON.

        Vinsamlegast hafið samband við
        PEWTER-LÖGREGLUNA ef þið hafið
        upplýsingar.
    """),
    "PewterCity_Text_MuseumOfScience": t("""
        PEWTER VÍSINDASAFN
    """),
    "PewterCity_Text_GymSign": t("""
        PEWTER BORGAR VASASKRÍMSLA-SALUR
        SALSTJÓRI: BROCK
        Steinharði vasaskrímslaþjálfarinn!
    """),
    "PewterCity_Text_CitySign": t("""
        PEWTER BORG
        Steingrá borg
    """),
    "PewterCity_Text_DefeatedBrockYouCanHaveTreasure": t("""
        Ha! Þetta SALMERKI...
        Ótrúlegt, vannstu BROCK?

        Ég er svo snortinn að ég skal gefa
        þér fjársjóðinn minn!
    """),
    "PewterCity_Text_BerriesInsideUseCarefully": t("""
        Það eru BER inni í þessu.

        Sum þeirra koma að gagni, svo notaðu
        þau varlega!
    """),
    "PewterCity_Text_MonsWillUseHeldBerriesOnTheirOwn": t("""
        Ef vasaskrímsli heldur á BERI notar
        það það sjálfkrafa í bardaga.

        Það er einfaldara og þægilegra en
        SÁRALYF eða EITURMÓTEFNI, ekki satt?
    """),
    "PewterCity_Text_OhPlayer": t("""
        Ó, {PLAYER}{KUN}!
    """),
    "PewterCity_Text_AskedToDeliverThis": t("""
        Gott að ég náði þér.
        Ég er AÐSTOÐARMAÐUR PROF. OAK.

        Ég var beðinn um að afhenda þetta,
        svo gjörðu svo vel.
    """),
    "PewterCity_Text_ReceivedRunningShoesFromAide": t("""
        {PLAYER} fékk HLAUPASKÓNA
        frá AÐSTOÐARMANNINUM.
    """),
    "PewterCity_Text_SwitchedShoesWithRunningShoes": t("""
        {PLAYER} skipti yfir í HLAUPASKÓNA.
    """),
    "PewterCity_Text_ExplainRunningShoes": t("""
        Ýttu á B-hnappinn til að hlaupa.
        En bara þar sem er pláss til að
        hlaupa!
    """),
    "PewterCity_Text_MustBeGoingBackToLab": t("""
        Jæja, ég verð að fara aftur í
        RANNSÓKNARSTOFUNA.

        Bæ-bæ!
    """),
    "PewterCity_Text_RunningShoesLetterFromMom": t("""
        Bréf er fest við...

        Kæri {PLAYER},

        Hér eru HLAUPASKÓR fyrir minn
        ástkæra áskoranda.

        Mundu, ég mun alltaf hvetja þig
        áfram! Gefstu aldrei upp!

        Frá mömmu
    """),
    "PewterCity_Gym_Text_BrockIntro": t("""
        Svo þú ert kominn.
        Ég er BROCK.
        Ég er SALSTJÓRI PEWTER-SALARINS.

        Steinharður viljastyrkur minn sést
        jafnvel í vasaskrímslunum mínum.

        Vasaskrímslin mín eru öll grjóthörð
        og staðföst.

        Það er rétt - þau eru öll af
        STEINS-gerð!

        Fuhaha!
        Ætlarðu að skora á mig þótt þú
        vitir að þú tapar?

        Það er heiður ÞJÁLFARA sem knýr þig
        til að skora á mig.

        Jæja þá!
        Sýndu mér hvað þú getur!{PLAY_BGM}{MUS_ENCOUNTER_GYM_LEADER}
    """),
    "PewterCity_Gym_Text_BrockDefeat": t("""
        Ég vanmat þig og þess vegna tapaði
        ég.

        Sem sönnun um sigur þinn veiti ég
        þér þetta... opinbera STEINMERKIÐ
        VASASKRÍMSLADEILDARINNAR.

        {FONT_NORMAL}{PLAYER} fékk BOULDERBADGE frá
        BROCK!{PAUSE_MUSIC}{PLAY_BGM}{MUS_OBTAIN_BADGE}{PAUSE 0xFE}{PAUSE 0x56}{RESUME_MUSIC}

        {FONT_MALE}Það eitt að hafa STEINMERKIÐ gerir
        vasaskrímslin þín sterkari.

        Það gerir líka kleift að nota
        bragðið LEIFTUR utan bardaga.

        Að sjálfsögðu þarf vasaskrímsli að
        kunna LEIFTUR til að nota það.
    """),
    "PewterCity_Gym_Text_TakeThisWithYou": t("""
        Bíddu!
        Taktu þetta með þér.
    """),
    "PewterCity_Gym_Text_ReceivedTM39FromBrock": t("""
        {PLAYER} fékk TM39
        frá BROCK.
    """),
    "PewterCity_Gym_Text_ExplainTM39": t("""
        TM, Technical Machine, inniheldur
        bragð fyrir vasaskrímsli.

        Með því að nota TM lærir vasaskrímsli
        bragðið sem það geymir.

        Hvert TM má aðeins nota einu sinni.

        Veldu því vasaskrímslið vandlega
        þegar þú notar eitt.

        Annars...
        TM39 inniheldur STEINGRÖF.

        Það þeytir steinum í andstæðinginn
        og lækkar SPEED.
    """),
    "PewterCity_Gym_Text_BrockPostBattle": t("""
        Það eru alls kyns ÞJÁLFARAR í
        þessum stóra heimi.

        Þú virðist mjög hæfileikaríkur
        vasaskrímslaþjálfari.

        Leyfðu mér því að leggja eitt til.

        Farðu í SALINN í CERULEAN og
        prófaðu hæfileika þína.
    """),
    "PewterCity_Gym_Text_DontHaveRoomForThis": t("""
        Þú hefur ekki pláss fyrir þetta.
    """),
    "PewterCity_Gym_Text_LiamIntro": t("""
        Stopp þar, krakki!

        Þú ert tíu þúsund ljósár frá því
        að mæta BROCK!
    """),
    "PewterCity_Gym_Text_LiamDefeat": t("""
        Ansans!

        Ljósár eru ekki tími...
        Þau mæla fjarlægð!
    """),
    "PewterCity_Gym_Text_LiamPostBattle": t("""
        Þú ert ansi heitur.
        ...En ekki jafn heitur og BROCK!
    """),
    "PewterCity_Gym_Text_LetMeTakeYouToTheTop": t("""
        Hæ!
        Viltu dreyma stórt?

        Þorirðu að dreyma um að verða
        meistari vasaskrímsla?

        Ég er ekki ÞJÁLFARI, en ég get
        ráðlagt þér hvernig þú vinnur.

        Leyfðu mér að koma þér á toppinn!
    """),
    "PewterCity_Gym_Text_LetsGetHappening": t("""
        Allt í lagi!
        Byrjum þetta!
    """),
    "PewterCity_Gym_Text_TryDifferentPartyOrders": t("""
        Fyrsta vasaskrímslið í bardaga er
        vinstra megin á vasaskrímslalistanum.

        Með því að breyta röð vasaskrímsla
        geturðu náð forskoti.

        Prófaðu mismunandi raðir eftir liði
        andstæðingsins.
    """),
    "PewterCity_Gym_Text_ItsFreeLetsGetHappening": t("""
        Þetta er ókeypis þjónusta!
        Byrjum þetta!
    """),
    "PewterCity_Gym_Text_YoureChampMaterial": t("""
        Eins og ég hélt!
        Þú ert efni í vasaskrímslameistara!
    """),
    "PewterCity_Gym_Text_GymStatue": t("""
        PEWTER VASASKRÍMSLA-SALUR
        SALSTJÓRI: BROCK

        SIGURSÆLIR ÞJÁLFARAR:
        {RIVAL}
    """),
    "PewterCity_Gym_Text_GymStatuePlayerWon": t("""
        PEWTER VASASKRÍMSLA-SALUR
        SALSTJÓRI: BROCK

        SIGURSÆLIR ÞJÁLFARAR:
        {RIVAL}, {PLAYER}
    """),
    "PewterCity_House1_Text_Nidoran": t("""
        NÁLDUR♂: Voffvoff!
    """),
    "PewterCity_House1_Text_NidoranSit": t("""
        NÁLDUR, sestu!
    """),
    "PewterCity_House1_Text_TradeMonsAreFinicky": t("""
        Vasaskrímslið okkar er utanaðkomandi,
        svo það er dutlungafullt og erfitt í
        meðförum.

        Utanaðkomandi vasaskrímsli er eitt
        sem þú færð í skiptum.

        Það vex hratt, en gæti hunsað
        óreyndan ÞJÁLFARA í bardaga.

        Ef við bara ættum einhver MERKI...
    """),
    "PewterCity_House2_Text_MonsLearnTechniquesAsTheyGrow": t("""
        Vasaskrímsli læra ný brögð þegar
        þau vaxa.

        En sum brögð verða menn að kenna
        þeim.
    """),
    "PewterCity_House2_Text_MonsEasierCatchIfStatused": t("""
        Auðveldara er að ná vasaskrímsli ef
        það er með ástandsvandamál.

        Svefn, eitrun, bruni eða lömun...
        Allt þetta virkar.

        En það er aldrei öruggt að ná
        vasaskrímsli!
    """),
    "PewterCity_Mart_Text_BoughtWeirdFishFromShadyGuy": t("""
        Skuggalegur karl plataði mig til að
        kaupa þetta skrýtna fiskavasaskrímsli!

        Það er algjörlega máttlaust og
        kostaði ¥500!
    """),
    "PewterCity_Mart_Text_GoodThingsIfRaiseMonsDiligently": t("""
        Góðir hlutir geta gerst ef þú elur
        vasaskrímsli vandlega.

        Jafnvel veikburða geta komið á óvart
        ef þú gefst ekki upp á þeim.
    """),
    "PewterCity_Museum_1F_Text_Its50YForChildsTicket": t("""
        Já, já.
        Barnamiði kostar ¥50.

        Viltu koma inn?
    """),
    "PewterCity_Museum_1F_Text_ComeAgain": t("""
        Komdu aftur!
    """),
    "PewterCity_Museum_1F_Text_Right50YThankYou": t("""
        Rétt, ¥50!
        Takk fyrir!
    """),
    "PewterCity_Museum_1F_Text_DontHaveEnoughMoney": t("""
        Þú átt ekki næga peninga.
    """),
    "PewterCity_Museum_1F_Text_PleaseEnjoyYourself": t("""
        Góða skemmtun.
    """),
    "PewterCity_Museum_1F_Text_DoYouKnowWhatAmberIs": t("""
        Þú getur ekki laumast inn bakdyramegin!
        Góð tilraun, krakki, en nei.

        Æ, hvað um það!
        Veistu hvað AMBER er?
    """),
    "PewterCity_Museum_1F_Text_AmberContainsGeneticMatter": t("""
        AMBER inniheldur erfðaefni fornra
        vasaskrímsla.

        Einhvers staðar er RANNSÓKNARSTOFA
        að reyna að endurlífga vasaskrímsli
        úr AMBER.
    """),
    "PewterCity_Museum_1F_Text_AmberIsFossilizedSap": t("""
        AMBER er í raun trjákvoða, klístraða
        efnið sem lekur úr trjám.

        Forn trjákvoða steingerðist með
        tímanum og varð að grjóthörðu AMBER.
    """),
    "PewterCity_Museum_1F_Text_PleaseGoAround": t("""
        Vinsamlegast farðu hringinn.
    """),
    "PewterCity_Museum_1F_Text_ShouldBeGratefulForLongLife": t("""
        Ég ætti að vera þakklátur fyrir
        langa ævi.

        Aldrei hélt ég að ég fengi að sjá
        bein dreka!
    """),
    "PewterCity_Museum_1F_Text_WantYouToGetAmberExamined": t("""
        Suss!
        Heyrðu, ég þarf að deila leyndarmáli
        með einhverjum.

        Ég held að þessi AMBER-klumpur
        innihaldi DNA úr vasaskrímsli!

        Það yrði stórkostlegt vísindalegt
        gegnumbrot ef hægt væri að endurlífga
        vasaskrímsli úr honum.

        En samstarfsfólk mitt hunsar bara
        það sem ég segi.

        Svo ég þarf að biðja þig greiða!

        Ég vil að þú látir rannsaka þetta á
        einhverri rannsóknarstofu fyrir
        vasaskrímsli.
    """),
    "PewterCity_Museum_1F_Text_ReceivedOldAmberFromMan": t("""
        {PLAYER} fékk OLD AMBER
        frá manninum.
    """),
    "PewterCity_Museum_1F_Text_GetOldAmberChecked": t("""
        Suss!
        Láttu skoða OLD AMBER!
    """),
    "PewterCity_Museum_1F_Text_DontHaveSpaceForThis": t("""
        Þú hefur ekki pláss fyrir þetta.
    """),
    "PewterCity_Museum_1F_Text_WeHaveTwoFossilsOnExhibit": t("""
        Við sýnum tvo steingervinga
        sjaldgæfra, forsögulegra
        vasaskrímsla.
    """),
    "PewterCity_Museum_1F_Text_BeautifulPieceOfAmber": t("""
        Þarna er fallegur AMBER-klumpur í
        tærum gullnum lit.
    """),
    "PewterCity_Museum_1F_Text_AerodactylFossil": t("""
        HIMINVÁ steingervingur
        Frumstætt og sjaldgæft vasaskrímsli.
    """),
    "PewterCity_Museum_1F_Text_KabutopsFossil": t("""
        DJÚPSAXI steingervingur
        Frumstætt og sjaldgæft vasaskrímsli.
    """),
    "Text_SeismicTossTeach": t("""
        Leyndardómar geimsins...
        Leyndardómar jarðar...

        Það er svo margt sem við vitum lítið
        um.

        En það ætti að hvetja okkur til að
        læra meira, ekki gefast upp.

        Það eina sem þú ættir að kasta...

        Jæja, hvað með SEISMIC TOSS?
        Á ég að kenna vasaskrímsli það?
    """),
    "Text_SeismicTossDeclined": t("""
        Er það svo?
        Ég er viss um að þú kemur aftur
        eftir því.
    """),
    "Text_SeismicTossWhichMon": t("""
        Hvaða vasaskrímsli vill læra
        SEISMIC TOSS?
    """),
    "Text_SeismicTossTaught": t("""
        Ég vona að þú gefist ekki upp.
        Haltu áfram.
    """),
    "PewterCity_Museum_1F_Text_WhatsSpecialAboutMoonStone": t("""
        MOON STONE, ha?

        Hvað er svona sérstakt við hann?
        Hann lítur út eins og venjulegur
        steinn fyrir mér.
    """),
    "PewterCity_Museum_1F_Text_BoughtColorTVForMoonLanding": t("""
        20. júlí 1969!

        Mannkyn steig fyrst fæti á tunglið
        þann dag.

        Ég keypti litasjónvarp bara til að
        horfa á fréttirnar.
    """),
    "PewterCity_Museum_1F_Text_RunningSpaceExhibitThisMonth": t("""
        Í þessum mánuði erum við með
        geimsýningu.
    """),
    "PewterCity_Museum_1F_Text_AskedDaddyToCatchPikachu": t("""
        Mig langar í LEIFTURSKO!
        Það er svo krúttlegt!

        Ég bað pabba að ná LEIFTURSKO fyrir
        mig!
    """),
    "PewterCity_Museum_1F_Text_PikachuSoonIPromise": t("""
        Já, þú færð LEIFTURSKO bráðum,
        ég lofa!
    """),
    "PewterCity_Museum_1F_Text_SpaceShuttle": t("""
        Geimskutla
    """),
    "PewterCity_Museum_1F_Text_MeteoriteThatFellOnMtMoon": t("""
        Loftsteinn sem féll á MT. MOON.
        Talið er að hann sé MOON STONE.
    """),
    "PewterCity_PokemonCenter_1F_Text_TeamRocketMtMoonImOnPhone": t("""
        Hvað!?

        ROCKET-GENGIÐ er á MT. MOON?
        Ha?

        Ég er í símanum!
        Hypjaðu þig!
    """),
    "PewterCity_PokemonCenter_1F_Text_Jigglypuff": t("""
        KRÚTTÍPÚTT: Púú pupúú!
    """),
    "PewterCity_PokemonCenter_1F_Text_WhenJiggylypuffSingsMonsGetDrowsy": t("""
        Geisp!

        Þegar KRÚTTÍPÚTT syngur verða
        vasaskrímsli syfjuð...

        ...Ég líka...
        Hrot...
    """),
    "PewterCity_PokemonCenter_1F_Text_TradingMyClefairyForPikachu": t("""
        Mig langar virkilega í LEIFTURSKO,
        svo ég ætla að skipta BLEIKÁLFUR
        mínum fyrir LEIFTURSKO.
    """),
    "PewterCity_PokemonCenter_1F_Text_TradingPikachuWithKid": t("""
        Ég er að skipta á vasaskrímslum við
        krakkann þarna.

        Ég átti tvö LEIFTURSKO, svo mér
        fannst eins gott að skipta öðru
        þeirra.
    """),
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-after-v3.csv")
    parser.add_argument("--output", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-pewter-v1.csv")
    args = parser.parse_args()

    with args.queue.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    out = []
    seen: set[str] = set()
    for row in rows:
        label = row["label"]
        if not row["file"].startswith("data/maps/Pewter"):
            continue
        if label not in TRANSLATIONS:
            continue
        row = dict(row)
        row["icelandic"] = TRANSLATIONS[label]
        row["notes"] = "codex curated Pewter v1"
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
