from __future__ import annotations

import argparse
import csv
import textwrap
from pathlib import Path

from common import repo_root


def t(value: str) -> str:
    return textwrap.dedent(value).strip()


TRANSLATIONS = {
    "Route16_Text_LaoIntro": t("""
        Hvað viltu?
    """),
    "Route16_Text_LaoDefeat": t("""
        Ekki voga þér að hlæja!
    """),
    "Route16_Text_LaoPostBattle": t("""
        Okkur finnst bara gott að hanga hér.
        Hvað kemur það þér við?
    """),
    "Route16_Text_KojiIntro": t("""
        Flott HJÓL!
        Láttu mig fá það!
    """),
    "Route16_Text_KojiDefeat": t("""
        Rot!
    """),
    "Route16_Text_KojiPostBattle": t("""
        Gleymdu því, hver þarf á HJÓLINU þínu
        að halda!
    """),
    "Route16_Text_LukeIntro": t("""
        Komdu út að leika, litla mús!
    """),
    "Route16_Text_LukeDefeat": t("""
        Þú litla rotta!
    """),
    "Route16_Text_LukePostBattle": t("""
        Ég hata að tapa!
        Farðu úr andlitinu á mér!
    """),
    "Route16_Text_HideoIntro": t("""
        Hey, þú rakst í mig!
    """),
    "Route16_Text_HideoDefeat": t("""
        Kabúmm!
    """),
    "Route16_Text_HideoPostBattle": t("""
        Við munum alltaf hanga hér, hvort sem
        þér líkar það eða ekki.

        Þú getur farið hjáleið til VERMILION
        frá FUCHSIA meðfram ströndinni.
    """),
    "Route16_Text_CamronIntro": t("""
        Ég er svangur og illur!
        Ég þarf kýlipoka!
    """),
    "Route16_Text_CamronDefeat": t("""
        Slæmt, slæmt, slæmt!
    """),
    "Route16_Text_CamronPostBattle": t("""
        Ef ég ætla að eiga vasaskrímsli mega
        þau alveg vera grimm.

        Ég myndi nota þau til að tæta óvini
        mína í sundur.
    """),
    "Route16_Text_RubenIntro": t("""
        Heyrðu þarna!
        Skemmtum okkur almennilega!
    """),
    "Route16_Text_RubenDefeat": t("""
        Ekki gera mig reiðan!
    """),
    "Route16_Text_RubenPostBattle": t("""
        Ég fæ mitt fjör úr því að angra fólk
        með stinkandi vasaskrímslunum mínum.

        Þau eru frábær til að hræða fólk.
        Og þau bíta líka.
    """),
    "Route16_Text_MonSprawledOutInSlumber": t("""
        Vasaskrímsli liggur endilangt í djúpum
        og notalegum svefni.
    """),
    "Route16_Text_CyclingRoadSign": t("""
        Njóttu brekkunnar!
        HJÓLAVEGUR
    """),
    "Route16_Text_RouteSign": t("""
        ROUTE 16
        CELADON BORG - FUCHSIA BORG
    """),
    "Route16_Text_JedIntro": t("""
        JED: Ást okkar þekkir engin mörk.
        Við erum ástfangin og sýnum það!
    """),
    "Route16_Text_JedDefeat": t("""
        JED: Ó, nei!
        Ástin mín sá mig sem tapara!
    """),
    "Route16_Text_JedPostBattle": t("""
        JED: Hlustaðu, LEA. Þú þarft að hugsa
        aðeins minna um mig.
    """),
    "Route16_Text_JedNotEnoughMons": t("""
        JED: Þú átt bara eitt vasaskrímsli?
        Er engin ást í hjarta þínu?
    """),
    "Route16_Text_LeaIntro": t("""
        LEA: Stundum hræðir styrkur ástar
        okkar mig.
    """),
    "Route16_Text_LeaDefeat": t("""
        LEA: Óó! En JED er svalur jafnvel
        þegar hann tapar!
    """),
    "Route16_Text_LeaPostBattle": t("""
        LEA: Ehehe, fyrirgefðu.
        JED er svo svalur.
    """),
    "Route16_Text_LeaNotEnoughMons": t("""
        LEA: Ó, þú ert ekki með tvö
        vasaskrímsli með þér?

        Finnst þér það ekki einmanalegt fyrir
        þig eða vasaskrímslið þitt?
    """),
    "Route16_House_Text_FoundMySecretRetreat": t("""
        Ó, góði minn. Þú fannst leynistaðinn
        minn.

        Vinsamlegast segðu engum að ég sé hér.
        Ég bæti þér það upp með þessu!
    """),
    "Route16_House_Text_ReceivedHM02FromGirl": t("""
        {PLAYER} fékk HM02 frá stúlkunni.
    """),
    "Route16_House_Text_ExplainHM02": t("""
        HM02 er FLUG.
        Þetta er dásamlega hentug hreyfing.

        Notaðu hana vel, gerðu það.
    """),
    "Route16_House_Text_DontHaveAnyRoomForThis": t("""
        Þú hefur ekkert pláss fyrir þetta.
    """),
    "Route16_House_Text_Fearow": t("""
        GEIGHEGRI: Kyueen!
    """),
    "Route16_NorthEntrance_1F_Text_NoPedestriansOnCyclingRoad": t("""
        Gangandi vegfarendur eru ekki leyfðir
        á HJÓLAVEGI!
    """),
    "Route16_NorthEntrance_1F_Text_CyclingRoadIsDownhillCourse": t("""
        HJÓLAVEGUR er niðurleið við sjóinn.
        Það er frábær ferð.
    """),
    "Route16_NorthEntrance_1F_Text_ExcuseMeWaitUp": t("""
        Afsakaðu!
        Bíddu aðeins!
    """),
    "Route16_NorthEntrance_1F_Text_HowdYouGetInGoodEffort": t("""
        Hvernig komst þú inn?
        Vel gert!
    """),
    "Route16_NorthEntrance_2F_Text_OnBikeRideWithGirlfriend": t("""
        Ég er í rólegri hjólaferð á nýja
        hjólinu mínu með kærustunni.
    """),
    "Route16_NorthEntrance_2F_Text_RidingTogetherOnNewBikes": t("""
        Við ætlum að hjóla saman á nýju
        hjólunum okkar.
    """),
    "Route16_NorthEntrance_2F_Text_ItsCeladonDeptStore": t("""
        Sjáum hvað sjónaukinn sýnir...

        Það er CELADON DEPT. STORE!
    """),
    "Route16_NorthEntrance_2F_Text_LongPathOverWater": t("""
        Sjáum hvað sjónaukinn sýnir...

        Það er löng leið yfir vatn langt í
        burtu.
    """),
    "Route16_NorthEntrance_2F_Text_GiveAmuletCoinIfCaught40": t("""
        Hæ! Manstu eftir mér?
        Ég er einn af AÐSTOÐARMÖNNUM PROF.
        OAK.

        Ef VasaDEX-ið þitt er með full gögn
        um 40 tegundir á ég að gefa þér
        verðlaun.

        PROF. OAK fól mér HEILLAPENING handa
        þér.

        Svo, {PLAYER}, leyfðu mér að spyrja.

        Hefurðu safnað gögnum um að minnsta
        kosti 40 gerðir vasaskrímsla?
    """),
    "Route16_NorthEntrance_2F_Text_GreatHereYouGo": t("""
        Frábært! Þú hefur náð eða átt
        {STR_VAR_3} gerðir vasaskrímsla!

        Til hamingju!
        Gjörðu svo vel!
    """),
    "Route16_NorthEntrance_2F_Text_ReceivedAmuletCoinFromAide": t("""
        {PLAYER} fékk HEILLAPENING frá
        AÐSTOÐARMANNINUM.
    """),
    "Route16_NorthEntrance_2F_Text_ExplainAmuletCoin": t("""
        HEILLAPENINGUR er hlutur sem
        vasaskrímsli heldur á.

        Ef vasaskrímslið birtist í sigruðum
        bardaga færðu meiri peninga.
    """),
    "Route17_Text_RaulIntro": t("""
        Það græðist ekkert hratt á því að
        berjast við krakka.
    """),
    "Route17_Text_RaulDefeat": t("""
        Brenndur út!
    """),
    "Route17_Text_RaulPostBattle": t("""
        Þú getur fundið góða hluti liggjandi
        á HJÓLAVEGI.

        Það eru góðir peningar í að hirða þá
        og selja.
    """),
    "Route17_Text_IsaiahIntro": t("""
        Ég er ótrúlega stoltur af kroppnum
        mínum, krakki.
        Komdu!
    """),
    "Route17_Text_IsaiahDefeat": t("""
        Hú!
    """),
    "Route17_Text_IsaiahPostBattle": t("""
        Ég gæti magaskellt þér héðan út!
    """),
    "Route17_Text_VirgilIntro": t("""
        Ertu á leið til FUCHSIA?
    """),
    "Route17_Text_VirgilDefeat": t("""
        Krass og bruni!
    """),
    "Route17_Text_VirgilPostBattle": t("""
        Ég elska að keppa niður brekkur!
    """),
    "Route17_Text_BillyIntro": t("""
        Við erum MÓTORHJÓLAMENN!
        Við ráðum vegunum, maður!
    """),
    "Route17_Text_BillyDefeat": t("""
        Reyktur!
    """),
    "Route17_Text_BillyPostBattle": t("""
        Ertu að leita að ævintýrum?
    """),
    "Route17_Text_NikolasIntro": t("""
        Láttu STUÐBOLTA rafmagna þig!
    """),
    "Route17_Text_NikolasDefeat": t("""
        Jarðtengdur!
    """),
    "Route17_Text_NikolasPostBattle": t("""
        Ég fékk STUÐBOLTANN minn í yfirgefna
        ORKUVERINU.
    """),
    "Route17_Text_ZeekIntro": t("""
        Ég hækkaði stigið á vasaskrímslinu
        mínu, en það þróast ekki. Af hverju?
    """),
    "Route17_Text_ZeekDefeat": t("""
        Af hverju, þú!
    """),
    "Route17_Text_ZeekPostBattle": t("""
        Kannski þurfa sum vasaskrímsli
        frumsteina til að þróast.
    """),
    "Route17_Text_JamalIntro": t("""
        Ég þarf smá hreyfingu!
    """),
    "Route17_Text_JamalDefeat": t("""
        Úff! Góð æfing!
    """),
    "Route17_Text_JamalPostBattle": t("""
        Ég er viss um að ég léttist þarna!
    """),
    "Route17_Text_CoreyIntro": t("""
        Vertu uppreisnarmaður!
    """),
    "Route17_Text_CoreyDefeat": t("""
        Aaaargh!
    """),
    "Route17_Text_CoreyPostBattle": t("""
        Vertu tilbúinn að berjast fyrir
        sannfæringu þinni!
    """),
    "Route17_Text_JaxonIntro": t("""
        Flott HJÓL!
        Hvernig stýrist það?
    """),
    "Route17_Text_JaxonDefeat": t("""
        Skot!
    """),
    "Route17_Text_JaxonPostBattle": t("""
        Hallinn gerir erfitt að stýra.
    """),
    "Route17_Text_WilliamIntro": t("""
        Láttu þig hverfa, krakki!
        Ég er örmagna!
    """),
    "Route17_Text_WilliamDefeat": t("""
        Ertu ánægður?
    """),
    "Route17_Text_WilliamPostBattle": t("""
        Ég þarf að leggja mig!
    """),
    "Route17_Text_WatchOutForDiscardedItems": t("""
        Þetta er tilkynning.

        Varist hluti sem hefur verið hent.
    """),
    "Route17_Text_SameSpeciesGrowDifferentRates": t("""
        ÞJÁLFARA-RÁÐ

        Öll vasaskrímsli eru einstök.

        Jafnvel vasaskrímsli af sömu tegund
        og sama stigi vaxa mishratt.
    """),
    "Route17_Text_PressBToStayInPlace": t("""
        ÞJÁLFARA-RÁÐ

        Ýttu á B hnappinn til að vera kyrr á
        hallandi leið.
    """),
    "Route17_Text_RouteSign": t("""
        ROUTE 17
        CELADON BORG - FUCHSIA BORG
    """),
    "Route17_Text_DontThrowGameThrowBalls": t("""
        Þetta er tilkynning!

        Ekki kasta leiknum frá þér, kastaðu
        VASA BOLTUM í staðinn!
    """),
    "Route17_Text_CyclingRoadSign": t("""
        HJÓLAVEGUR
        Hallinn endar hér!
    """),
    "Route18_Text_WiltonIntro": t("""
        Ég skoða alltaf hvert graslendi eftir
        nýjum vasaskrímslum.
    """),
    "Route18_Text_WiltonDefeat": t("""
        Tsk!
    """),
    "Route18_Text_WiltonPostBattle": t("""
        Ég vildi að ég ætti HJÓL!
    """),
    "Route18_Text_RamiroIntro": t("""
        Kurukkoo!
        Hvernig líst þér á fuglakallið mitt?
    """),
    "Route18_Text_RamiroDefeat": t("""
        Ég varð að angra þig!
    """),
    "Route18_Text_RamiroPostBattle": t("""
        Ég safna sjó-vasaskrímslum um helgar
        því sjórinn er svo nálægt.
    """),
    "Route18_Text_JacobIntro": t("""
        Þetta er mitt svæði!
        Komdu þér héðan!
    """),
    "Route18_Text_JacobDefeat": t("""
        Fjandinn!
    """),
    "Route18_Text_JacobPostBattle": t("""
        Þetta er uppáhaldssvæðið mitt til að
        ná vasaskrímslum.
    """),
    "Route18_Text_RouteSign": t("""
        ROUTE 18
        CELADON BORG - FUCHSIA BORG
    """),
    "Route18_Text_CyclingRoadSign": t("""
        HJÓLAVEGUR
        Gangandi vegfarendur bannaðir!
    """),
    "Route18_EastEntrance_1F_Text_NeedBicycleForCyclingRoad": t("""
        Þú þarft REIÐHJÓL til að fara út á
        HJÓLAVEG!
    """),
    "Route18_EastEntrance_1F_Text_CyclingRoadAllUphillFromHere": t("""
        HJÓLAVEGUR er allur upp í móti héðan.
    """),
    "Route18_EastEntrance_1F_Text_ExcuseMe": t("""
        Afsakaðu!
    """),
    "Route18_EastEntrance_2F_Text_PalletTownInWest": t("""
        Sjáum hvað sjónaukinn sýnir...

        PALLET TOWN er í vestri.
    """),
    "Route18_EastEntrance_2F_Text_PeopleSwimming": t("""
        Sjáum hvað sjónaukinn sýnir...

        Það er fólk að synda.
    """),
}


FILES = {
    "data/maps/Route16/text.inc",
    "data/maps/Route16_House/text.inc",
    "data/maps/Route16_NorthEntrance_1F/text.inc",
    "data/maps/Route16_NorthEntrance_2F/text.inc",
    "data/maps/Route17/text.inc",
    "data/maps/Route18/text.inc",
    "data/maps/Route18_EastEntrance_1F/text.inc",
    "data/maps/Route18_EastEntrance_2F/text.inc",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-after-v16.csv")
    parser.add_argument("--output", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-cycling-road-v1.csv")
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
        row["notes"] = "codex curated Cycling Road Route 16-18 v1"
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
