from __future__ import annotations

import argparse
import csv
import textwrap
from pathlib import Path

from common import repo_root


def t(value: str) -> str:
    return textwrap.dedent(value).strip()


TRANSLATIONS = {
    "CeruleanCity_Text_RivalDefeat": t("""
        Hey!
        Slakaðu á!
        Þú vannst nú þegar!
    """),
    "CeruleanCity_Text_OhRightLittlePresentAsFavor": t("""
        Ó, já, rétt.

        Ég vorkenni þér. Í alvöru.
        Þú ert alltaf að dragast á eftir mér.

        Svo hér, ég gef þér smá gjöf sem
        greiða.
    """),
    "CeruleanCity_Text_ExplainFameCheckerSmellYa": t("""
        Slúðurkjaftur eins og þú...
        Þetta tæki er fullkomið.

        Ég þarf það ekki því mér er alveg
        sama um aðra.

        Jæja, nú er ég í alvöru farinn.
        Sjáumst!
    """),
    "CeruleanCity_Text_RivalVictory": t("""
        Auðvitað!
        Ég er nefnilega snillingur!
    """),
    "CeruleanCity_Text_GruntIntro": t("""
        Hey! Haltu þig frá!
        Þetta er ekki garðurinn þinn!

        ...Ha?
        Ég?

        Ég er saklaus vegfarandi!
        Trúirðu mér ekki?{PLAY_BGM}{MUS_ENCOUNTER_ROCKET}
    """),
    "CeruleanCity_Text_GruntDefeat": t("""
        LIÐI: Hættu! Ég gefst upp!
        Ég fer hljóðlega!
    """),
    "CeruleanCity_Text_OkayIllReturnStolenTM": t("""
        ...Allt í lagi.
        Ég skila TM-inu sem ég stal.
    """),
    "CeruleanCity_Text_RecoveredTM28FromGrunt": t("""
        {PLAYER} endurheimti TM28 frá
        ROCKET-LIÐANUM.
    """),
    "CeruleanCity_Text_BetterGetMovingBye": t("""
        Ég ætti að koma mér af stað!
        Bæ!
    """),
    "CeruleanCity_Text_MakeRoomForThisCantRun": t("""
        Gerðu pláss fyrir þetta!
        Ég kemst ekki burt fyrr en ég gef
        þér það!
    """),
    "CeruleanCity_Text_TrainerLifeIsToughIsntIt": t("""
        Ert þú líka ÞJÁLFARI?

        Að safna, berjast...
        Þetta er erfitt líf, ekki satt?
    """),
    "CeruleanCity_Text_YouCanCutDownSmallTrees": t("""
        Vissirðu að þú getur notað CUT á
        lítil tré?

        Jafnvel litla tréð fyrir framan
        búðina má CUT-a niður.

        Ég held samt að það sé leið í kring.
    """),
    "CeruleanCity_Text_PeopleHereWereRobbed": t("""
        Fólkið hér varð fyrir ráni.

        Það er augljóst að ROCKET-GENGIÐ
        stendur á bak við þetta ódæðisverk!

        Jafnvel LÖGREGLAN okkar á í
        vandræðum með ROCKET-GENGIÐ!
    """),
    "CeruleanCity_Text_NoYouBlewItAgain": t("""
        Nei!
        Þú klúðraðir þessu aftur!
    """),
    "CeruleanCity_Text_WantBrightRedBicycle": t("""
        Mig langar í skærrautt reiðhjól.

        Ég geymi það heima svo það verði
        ekki skítugt.
    """),
    "CeruleanCity_Text_CitySign": t("""
        CERULEAN BORG
        Dularfullur blár ljómi umlykur hana
    """),
    "CeruleanCity_Text_BikeShopSign": t("""
        Gras og hellar verða auðveldir!
        HJÓLABÚÐ
    """),
    "CeruleanCity_BikeShop_Text_WelcomeToBikeShop": t("""
        Halló!
        Velkomin í HJÓLABÚÐINA.

        Við eigum einmitt REIÐHJÓLIÐ fyrir
        þig!
    """),
    "CeruleanCity_BikeShop_Text_SorryYouCantAffordIt": t("""
        Afsakið!
        Þú hefur ekki efni á því!
    """),
    "CeruleanCity_BikeShop_Text_OhBikeVoucherHereYouGo": t("""
        Ó, þetta er...

        REIÐHJÓLSMIÐI!

        Allt í lagi!
        Gjörðu svo vel!
    """),
    "CeruleanCity_BikeShop_Text_ExchangedVoucherForBicycle": t("""
        {PLAYER} skipti REIÐHJÓLSMIÐA
        fyrir REIÐHJÓL.
    """),
    "CeruleanCity_BikeShop_Text_ThankYouComeAgain": t("""
        Takk fyrir!
        Komdu aftur seinna!
    """),
    "CeruleanCity_BikeShop_Text_HowDoYouLikeNewBicycle": t("""
        Hvernig líkar þér nýja REIÐHJÓLIÐ?
        Rennur það vel?

        Þú getur farið með það á
        HJÓLALEIÐINA og jafnvel inn í hella!
    """),
    "CeruleanCity_BikeShop_Text_MakeRoomForBicycle": t("""
        Þú þarft að gera pláss fyrir
        REIÐHJÓLIÐ!
    """),
    "CeruleanCity_BikeShop_Text_CityBikeGoodEnoughForMe": t("""
        Venjulegt borgarhjól nægir mér.

        Enda er ekki hægt að setja
        innkaupakörfu á fjallahjól.
    """),
    "CeruleanCity_BikeShop_Text_BikesCoolButExpensive": t("""
        Þessi hjól eru flott, en þau eru
        hrikalega dýr!
    """),
    "CeruleanCity_BikeShop_Text_WowYourBikeIsCool": t("""
        Vá.
        REIÐHJÓLIÐ þitt er virkilega flott!
    """),
    "CeruleanCity_BikeShop_Text_GermanFoldableBicyleFinallyOnMarket": t("""
        Loksins komið á markað!

        Þýskt hágæða samanbrjótanlegt
        reiðhjól!
    """),
    "CeruleanCity_BikeShop_Text_ShinyNewBicycle": t("""
        Gljáandi nýtt REIÐHJÓL!
    """),
    "CeruleanCity_Gym_Text_ReceivedTM03FromMisty": t("""
        {PLAYER} fékk TM03 frá MISTY.
    """),
    "CeruleanCity_Gym_Text_BetterMakeRoomForThis": t("""
        Þú þarft að gera pláss fyrir þetta!
    """),
    "CeruleanCity_Gym_Text_MistyDefeat": t("""
        Vá!
        Þú ert alltof góður!

        Allt í lagi!

        Þú mátt fá FOSSMERKIÐ til marks um
        að þú hafir sigrað mig.
    """),
    "CeruleanCity_Gym_Text_DianaIntro": t("""
        Hvað? Þú?
        Ég duga meira en vel fyrir þig!

        MISTY þarf ekki að hafa fyrir þessu.
    """),
    "CeruleanCity_Gym_Text_DianaDefeat": t("""
        Þú kaffærðir mig!
    """),
    "CeruleanCity_Gym_Text_DianaPostBattle": t("""
        Þú verður að mæta öðrum ÞJÁLFURUM
        til að sjá hversu góður þú ert.
    """),
    "CeruleanCity_Gym_Text_LuisIntro": t("""
        Skvamp!

        Ég er fyrstur!
        Byrjum!
    """),
    "CeruleanCity_Gym_Text_LuisDefeat": t("""
        Það getur ekki verið!
    """),
    "CeruleanCity_Gym_Text_LuisPostBattle": t("""
        MISTY er ÞJÁLFARI sem á eftir að
        halda áfram að bæta sig.

        Hún tapar ekki fyrir einhverjum eins
        og þér!
    """),
    "CeruleanCity_Gym_Text_WeMakePrettyGoodTeam": t("""
        Þú vannst MISTY!
        Sérðu, hvað sagði ég?

        Við tvö, krakki, erum ansi gott
        teymi!
    """),
    "CeruleanCity_House1_Text_DescribeWhichBadge": t("""
        Jæja...

        Hvaða af átta MERKJUNUM viltu að ég
        lýsi?
    """),
    "CeruleanCity_House1_Text_ComeVisitAnytime": t("""
        Komdu hvenær sem þú vilt.
    """),
    "CeruleanCity_House2_Text_TeamRocketTryingToDigIntoNoGood": t("""
        ROCKET-GENGIÐ hlýtur að vera að
        grafa sig inn í eitthvað misjafnt!
    """),
    "CeruleanCity_House2_Text_TeamRocketLeftWayOut": t("""
        ROCKET-GENGIÐ skildi eftir
        útgönguleið!
    """),
    "CeruleanCity_House4_Text_NothingEntertaining": t("""
        Andvarp...
        Of mikill tími, of lítið að gera...

        Gerist ekkert skemmtilegt einhvers
        staðar?
    """),
    "CeruleanCity_House4_Text_NewNewsInformativeHaveThis": t("""
        Ah!
        Ný frétt!

        Hmm...

        Ég skil!
        Þetta var býsna fróðlegt!

        Ég hrósa þér fyrir að hafa áhuga á
        fréttum á svona ungum aldri.

        Sem þökk fyrir að deila fréttunum
        með mér vil ég að þú fáir þetta.
    """),
    "CeruleanCity_House4_Text_IncredibleNewsHaveBerries": t("""
        Ó, ó!
        Þ-þessi frétt!

        Hmm...

        Magnað!
        Hvílík ótrúleg frétt!

        Ég hef ekki séð svona magnaða frétt
        í langan tíma!

        Takk fyrir að deila þessari frábæru
        frétt. Fáðu slatta af BERJUM!
    """),
    "CeruleanCity_House4_Text_WishCouldShareNewsWithOthers": t("""
        Það er synd að deila ekki þessari
        frétt með fleira fólki...

        Ég vildi að ég gæti sagt einhverjum...
        Látið aðra vita af fréttunum...
    """),
    "CeruleanCity_House4_Text_ThanksForSpreadingNewsTakeThis": t("""
        Ah, hefurðu dreift fréttunum fyrir
        mig?

        Góðar fréttir verða verðmætar þegar
        alls konar fólk deilir þeim.

        Sem þökk fyrir að dreifa fréttunum
        skaltu taka þetta!
    """),
    "CeruleanCity_House4_Text_MagnificentNewsSpreadHaveBerries": t("""
        Hefurðu dreift fréttunum enn meira?
        Stórkostlegt!

        Þessi frétt hlýtur að vera ánægð
        með að ganga svona á milli.

        Já, svo sannarlega!

        Líttu á þetta sem þakklætisvott frá
        mér og fréttinni.

        Ég gef þér fleiri BER en venjulega.
    """),
    "CeruleanCity_House4_Text_EnjoyingMyselfWithAllSortsOfNews": t("""
        Ég nýt mín vel með alls konar
        fréttum.

        Já, ég er sáttur!
        Mér mun ekki leiðast um stund.
    """),
    "CeruleanCity_House4_Text_YourBerryPouchIsFull": t("""
        Hm? BERJAPOKINN þinn er fullur.
        Gjöfin mín bíður þá áfram.
    """),
    "CeruleanCity_House1_Text_AnyInterestInBerries": t("""
        Ég blanda alls konar lyf úr
        BERJADUFTI.

        Með góðu BERJADUFTI get ég búið til
        hvaða lyf sem er.

        Segðu mér nú, hefurðu áhuga á
        BERJUM?
    """),
    "CeruleanCity_House1_Text_HaveJustTheThing": t("""
        Ah, gott!
        Þá hef ég einmitt rétta hlutinn
        fyrir þig.
    """),
    "CeruleanCity_House1_Text_WhyMustYouLieNoBerries": t("""
        Hvers vegna þarftu að ljúga að mér?

        Hvað ertu með mörg BER?
        Ekki eitt einasta!
    """),
    "CeruleanCity_House1_Text_TakeInterestInAllSortsOfThings": t("""
        Hefurðu engan áhuga á BERJUM?

        Unga manneskja, það er mikilvægt að
        sýna alls konar hlutum áhuga.
    """),
    "CeruleanCity_House1_Text_HaveYouBroughtBerryPowder": t("""
        Hrm!
        Komstu með BERJADUFT handa mér?
    """),
    "CeruleanCity_House5_Text_ExchangeWithWhat": t("""
        Fyrir hvað viltu skipta því?
    """),
    "CeruleanCity_House1_Text_YoullExchangeBerryPowderForItem": t("""
        Gott, þú ætlar að skipta BERJADUFTINU
        þínu fyrir eitt {STR_VAR_1}?
    """),
    "CeruleanCity_House1_Text_DontHaveEnoughBerryPowder": t("""
        Hm?
        Þú átt ekki nóg BERJADUFT.
    """),
    "CeruleanCity_House1_Text_TradeMoreBerryPowder": t("""
        Þetta er sannarlega fínt BERJADUFT.
        Það verður að frábæru lyfi.

        Viltu skipta meira BERJADUFTI fyrir
        eitthvað annað?
    """),
    "CeruleanCity_House1_Text_HopeToSeeYouAgain": t("""
        Það er allt í lagi.
        Ég vona að þú komir aftur.
    """),
    "CeruleanCity_House1_Text_SeeMeIfYoudLikeToTradePowder": t("""
        Komdu til mín ef þú vilt skipta
        BERJADUFTINU þínu.
    """),
    "Route24_Text_JustEarnedFabulousPrize": t("""
        Til hamingju! Þú sigraðir fimm
        keppnis-ÞJÁLFARANA okkar!

        Þú vannst stórkostleg verðlaun!
    """),
    "Route24_Text_ReceivedNuggetFromMysteryTrainer": t("""
        {PLAYER} fékk GULLKLUMP frá
        dularfulla ÞJÁLFARANUM!
    """),
    "Route24_Text_YouDontHaveAnyRoom": t("""
        Þú hefur ekkert pláss!
    """),
    "Route24_Text_RocketDefeat": t("""
        Arrgh!
        Þú ert góður!
    """),
    "Route24_Text_YoudBecomeTopRocketLeader": t("""
        Með hæfileikum þínum gætirðu orðið
        toppleiðtogi í ROCKET-GENGINU.

        Komdu nú, hugsaðu um tækifærið!
        Ekki láta þetta fara til spillis.
    """),
    "Route24_Text_ShaneIntro": t("""
        Ég sá afrekið þitt úr grasinu!
    """),
    "Route24_Text_ShaneDefeat": t("""
        Ég hélt það ekki!
    """),
    "Route24_Text_ShanePostBattle": t("""
        Ég faldi mig því fólkið á brúnni
        hræddi mig.
    """),
    "Route24_Text_EthanIntro": t("""
        Allt í lagi! Ég er nr. 5!
        Ég stappa þig niður!
    """),
    "Route24_Text_EthanDefeat": t("""
        Vá!
        Of mikið!
    """),
    "Route24_Text_EthanPostBattle": t("""
        Ég gerði mitt besta.
        Ég sé ekki eftir neinu!
    """),
    "Route24_Text_ReliIntro": t("""
        Ég er nr. 4!
        Ertu orðinn þreyttur?
    """),
    "Route24_Text_ReliDefeat": t("""
        Ég tapaði líka!
    """),
    "Route24_Text_ReliPostBattle": t("""
        Ég gerði mitt besta, svo ég sé ekki
        eftir neinu!
    """),
    "Route24_Text_TimmyIntro": t("""
        Hér kemur nr. 3!
        Ég verð ekki auðveldur!
    """),
    "Route24_Text_TimmyDefeat": t("""
        Ái!
        Flattur út!
    """),
    "Route24_Text_TimmyPostBattle": t("""
        Ég gerði mitt besta.
        Ég sé ekki eftir neinu!
    """),
    "Route24_Text_AliIntro": t("""
        Ég er númer tvö!
        Nú er alvara!
    """),
    "Route24_Text_AliDefeat": t("""
        Hvernig gat ég tapað?
    """),
    "Route24_Text_AliPostBattle": t("""
        Ég gerði mitt besta.
        Ég sé ekki eftir neinu!
    """),
    "Route24_Text_CaleIntro": t("""
        Fólk kallar þetta GULLBRÚNA!

        Sigraðu okkur fimm ÞJÁLFARA og
        vinndu frábær verðlaun!

        Heldurðu að þú getir það?
    """),
    "Route24_Text_CaleDefeat": t("""
        Úhú!
        Vel gert!
    """),
    "Route24_Text_CalePostBattle": t("""
        Ég gerði mitt besta.
        Ég sé ekki eftir neinu!
    """),
    "Route25_Text_JoeyIntro": t("""
        ÞJÁLFARAR hér í nágrenninu koma
        hingað að æfa sig.
    """),
    "Route25_Text_JoeyDefeat": t("""
        Þú ert sæmilegur.
    """),
    "Route25_Text_DanIntro": t("""
        Pabbi fór með mig í frábært partí á
        S.S. ANNE í VERMILION BORG.
    """),
    "Route25_Text_DanDefeat": t("""
        Ég er ekki reiður!
    """),
    "Route25_Text_DanPostBattle": t("""
        Á S.S. ANNE sá ég ÞJÁLFARA frá
        öllum heiminum.
    """),
    "Route25_Text_FlintIntro": t("""
        Ég er svalur gaur.
        Ég á kærustu!
    """),
    "Route25_Text_FlintDefeat": t("""
        Æ, bölvað...
    """),
    "Route25_Text_FlintPostBattle": t("""
        Jæja.
        Kærastan mín hressir mig við.
    """),
    "Route25_Text_KelseyIntro": t("""
        Hæ!
        Kærastinn minn er svalur!
    """),
    "Route25_Text_KelseyDefeat": t("""
        Formið mitt er ekki upp á það besta...
    """),
    "Route25_Text_KelseyPostBattle": t("""
        Ég vildi að kærastinn minn væri jafn
        góður og þú.
    """),
    "Route25_Text_ChadIntro": t("""
        Ég fékk þessa tilfinningu...
        Ég vissi að ég þyrfti að berjast
        við þig!
    """),
    "Route25_Text_ChadDefeat": t("""
        Ég vissi líka að ég myndi tapa!
    """),
    "Route25_Text_HaleyDefeat": t("""
        Ég er ekkert svo öfundsjúk!
    """),
    "Route25_Text_FranklinIntro": t("""
        Ég var að koma niður af MT. MOON, en
        ég á enn bensín á tanknum!
    """),
    "Route25_Text_FranklinDefeat": t("""
        Þú lagðir hart að þér!
    """),
    "Route25_Text_NobIntro": t("""
        Ég er á leið að sjá safn hjá
        vasaskrímslaæðingi úti á höfðanum.
    """),
    "Route25_Text_NobDefeat": t("""
        Þú náðir mér, og það rækilega!
    """),
    "Route25_Text_WayneIntro": t("""
        Þú ætlar að hitta BILL?
        Fyrst berjumst við!
    """),
    "Route25_Text_WayneDefeat": t("""
        Þú ert nokkuð magnaður.
    """),
    "Route25_Text_WaynePostBattle": t("""
        Stígurinn fyrir neðan er stytting
        til CERULEAN BORGAR.
    """),
    "Route25_Text_SeaCottageSign": t("""
        SJÁVARHÚSIÐ
        BILL býr hér!
    """),
    "Route25_Text_MistyHighHopesAboutThisPlace": t("""
        Þessi höfði er frægur
        stefnumótastaður.

        MISTY, SALSTJÓRINN, bindur miklar
        vonir við þennan stað.
    """),
    "Route25_Text_AreYouHereAlone": t("""
        Halló, ertu hér án fylgdar?

        Ef þú ferð út á höfðann við
        CERULEAN...
        Þá ætti það að vera í pari.
    """),
    "Route25_SeaCottage_Text_RunCellSeparationOnPC": t("""
        Bíddu þar til ég er kominn inn í
        TELEPORTER.

        Þegar ég er kominn inn skaltu fara í
        PC-inn minn og keyra frumuskiljuna.
    """),
    "Route25_SeaCottage_Text_NoPleaseChief": t("""
        Nei!?
        Vertu nú ekki svona kaldur!

        Komdu nú, þú verður að hjálpa manni
        í verulegum vandræðum!

        Hvað segirðu, stjóri?
        Plís?
        Allt í lagi?
        Jæja!
    """),
    "Route25_SeaCottage_Text_NoPleaseBeautiful": t("""
        Nei!?
        Vertu nú ekki svona köld!

        Komdu nú, þú verður að hjálpa manni
        í verulegum vandræðum!

        Hvað segirðu, dama?
        Plís?
        Allt í lagi?
        Jæja!
    """),
    "Route25_SeaCottage_Text_ReceivedSSTicketFromBill": t("""
        {PLAYER} fékk S.S. MIÐA frá BILL.
    """),
    "Route25_SeaCottage_Text_YouveGotTooMuchStuff": t("""
        Þú ert með of mikið dót!
    """),
    "Route25_SeaCottage_Text_SSAnnePartyYouGoInstead": t("""
        Skemmtiferðaskipið S.S. ANNE er í
        VERMILION BORG.

        Ég heyri að margir ÞJÁLFARAR séu
        líka um borð.

        Þeir buðu mér í partíið sitt, en ég
        þoli ekki fín boð.

        Af hverju ferð þú ekki í staðinn
        fyrir mig?
        Farðu og skemmtu þér vel.
    """),
    "Route25_SeaCottage_Text_TeleporterIsDisplayed": t("""
        TELEPORTER birtist á PC skjánum.
    """),
    "Route25_SeaCottage_Text_InitiatedTeleportersCellSeparator": t("""
        {PLAYER} ræsti frumuskilju
        TELEPORTER-sins.
    """),
}


PREFIXES = (
    "data/maps/CeruleanCity",
    "data/maps/Route24/",
    "data/maps/Route25/",
    "data/maps/Route25_",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-after-v5.csv")
    parser.add_argument("--output", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-cerulean-v1.csv")
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
        row["notes"] = "codex curated Cerulean, Nugget Bridge, and Bill v1"
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
