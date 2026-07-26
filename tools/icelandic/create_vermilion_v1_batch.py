from __future__ import annotations

import argparse
import csv
import textwrap
from pathlib import Path

from common import repo_root


def t(value: str) -> str:
    return textwrap.dedent(value).strip()


TRANSLATIONS = {
    "VermilionCity_Text_DidYouSeeSSAnneInHarbor": t("""
        Sástu S.S. ANNE liggja við akkeri í
        höfninni?
    """),
    "VermilionCity_Text_SSAnneHasDepartedForYear": t("""
        Jæja, S.S. ANNE er farin?

        Hún verður aftur í VERMILION um þetta
        leyti á næsta ári.
    """),
    "VermilionCity_Text_BuildingOnThisLand": t("""
        Ég er að reisa byggingu á þessari
        lóð.
        Ég á hana alla.

        Vasaskrímslið mitt þjappar jarðveginn
        undir grunninn.
    """),
    "VermilionCity_Text_MachopStompingLandFlat": t("""
        ÞREKANGI stappar jarðveginn flatan.
    """),
    "VermilionCity_Text_SSAnneVisitsOnceAYear": t("""
        S.S. ANNE er frægt lúxus-
        skemmtiferðaskip.

        Hún kemur til VERMILION einu sinni á
        ári.
    """),
    "VermilionCity_Text_CitySign": t("""
        VERMILION BORG
        Höfnin þar sem sólarlagið glóir
    """),
    "VermilionCity_Text_SnorlaxBlockingRoute12": t("""
        TILKYNNING!

        ROUTE 12 gæti verið lokuð af sofandi
        vasaskrímsli.

        Farðu hjáleið um ROCK TUNNEL til
        LAVENDER BORGAR.

        VERMILION LÖGREGLAN
    """),
    "VermilionCity_Text_PokemonFanClubSign": t("""
        VASASKRÍMSLA AÐDÁENDAKLÚBBUR
        Allir aðdáendur vasaskrímsla velkomnir!
    """),
    "VermilionCity_Text_GymSign": t("""
        VERMILION BORG VASASKRÍMSLA-SALUR
        SALSTJÓRI: LT. SURGE
        Eldingamaðurinn frá Ameríku!
    """),
    "VermilionCity_Text_WelcomeToTheSSAnne": t("""
        Velkomin um borð í S.S. ANNE!
    """),
    "VermilionCity_Text_DoYouHaveATicket": t("""
        Velkomin um borð í S.S. ANNE!

        Afsakið, ertu með miða?
    """),
    "VermilionCity_Text_FlashedSSTicket": t("""
        {FONT_NORMAL}{PLAYER} sýndi S.S. MIÐANN!

        {FONT_MALE}Frábært!
        Velkomin um borð í S.S. ANNE!
    """),
    "VermilionCity_Text_DontHaveNeededSSTicket": t("""
        {FONT_NORMAL}{PLAYER} er ekki með nauðsynlega
        S.S. MIÐANN.

        {FONT_MALE}Afsakið!

        Þú þarft miða til að fara um borð.
    """),
    "VermilionCity_Text_TheShipSetSail": t("""
        Skipið lagði úr höfn.
    """),
    "VermilionCity_Text_BoardSeagallopTriPass": t("""
        Ah, þú ert með ÞRÍPASSA.

        Viltu fara um borð í SEAGALLOP ferju?
    """),
    "VermilionCity_Text_Seagallop7Departing": t("""
        Allt í lagi, allt er í röð og reglu.

        SEAGALLOP HI-SPEED 7 leggur strax af
        stað.
    """),
    "VermilionCity_Text_BoardSeagallopRainbowPass": t("""
        Ah, þú ert með REGNBOGAPASSA.

        Viltu fara um borð í SEAGALLOP ferju?
    """),
    "VermilionCity_Text_OhMysticTicketTakeYouToNavelRock": t("""
        Ó! Þetta er MYSTICMIÐI!
        Hann er sannarlega sjaldgæfur.

        Við flytjum þig glöð til NAVEL ROCK
        hvenær sem er.
    """),
    "VermilionCity_Text_OhAuroraTicketTakeYouToBirthIsland": t("""
        Ó! Þetta er AURORAMIÐI!
        Hann er sannarlega sjaldgæfur.

        Við flytjum þig glöð til BIRTH
        ISLAND hvenær sem er.
    """),
    "VermilionCity_Text_BoardSeagallopFerry": t("""
        Viltu fara um borð í SEAGALLOP ferju?
    """),
    "VermilionCity_Text_Seagallop10Departing": t("""
        Allt í lagi, allt er klárt fyrir þig
        til að fara um borð í sérferju.

        SEAGALLOP HI-SPEED 10 leggur strax
        af stað.
    """),
    "VermilionCity_Text_Seagallop12Departing": t("""
        Allt í lagi, allt er klárt fyrir þig
        til að fara um borð í sérferju.

        SEAGALLOP HI-SPEED 12 leggur strax
        af stað.
    """),
    "VermilionCity_Text_Route2AideHasPackageForYou": t("""
        Ó, halló, {PLAYER}!
        Hvernig gengur?

        Þetta er ég, einn af AÐSTOÐARMÖNNUM
        PROF. OAK.

        Hittirðu hinn AÐSTOÐARMANNINN?

        Hann var með pakka frá PROF. OAK
        handa þér, {PLAYER}.

        Hann sagðist leita að þér í kringum
        ROUTE 2, {PLAYER}.

        Ef þú ert á ROUTE 2 svæðinu, vinsamlegast
        leitaðu að honum.
    """),
    "VermilionCity_Gym_Text_LtSurgeIntro": t("""
        Hey, krakki!
        Hvað heldurðu að þú sért að gera hér?

        Þú lifir ekki lengi í bardaga!
        Ekki með þennan vesæla kraft!

        Ég segi þér, krakki, rafmagns-
        vasaskrímsli björguðu mér í stríðinu!

        Þau lömuðu óvini mína með raflosti!

        Ég geri það sama við þig!{PLAY_BGM}{MUS_ENCOUNTER_GYM_LEADER}
    """),
    "VermilionCity_Gym_Text_LtSurgePostBattle": t("""
        Smá ráð, krakki!

        Rafmagn er sannarlega öflugt!

        En það gagnast ekkert gegn
        JARÐAR-gerðar vasaskrímslum!
    """),
    "VermilionCity_Gym_Text_ExplainThunderBadgeTakeThis": t("""
        ÞRUMUMERKIÐ hækkar SPEED hjá
        vasaskrímslunum þínum!

        Það leyfir vasaskrímslunum þínum líka
        að nota FLY eldingarhratt hvenær sem
        er, krakki!

        Þú ert sérstakur, krakki!
        Taktu þetta!
    """),
    "VermilionCity_Gym_Text_ReceivedTM34FromLtSurge": t("""
        {PLAYER} fékk TM34 frá LT. SURGE.
    """),
    "VermilionCity_Gym_Text_ExplainTM34": t("""
        TM34 inniheldur ÁFALLABYLGJU!

        Kenndu hana rafmagns-vasaskrímsli!
    """),
    "VermilionCity_Gym_Text_MakeRoomInYourBag": t("""
        Yo, krakki, gerðu pláss í TÖSKUNNI!
    """),
    "VermilionCity_Gym_Text_LtSurgeDefeat": t("""
        Nú er ég lostinn!

        Þú ert alvöru efni, krakki!

        Jæja þá, taktu ÞRUMUMERKIÐ!
    """),
    "VermilionCity_Gym_Text_TuckerIntro": t("""
        Þegar ég var í hernum var LT. SURGE
        strangur yfirforingi minn.

        Hann var harður húsbóndi.
    """),
    "VermilionCity_Gym_Text_TuckerDefeat": t("""
        Hættu!
        Þú ert mjög góður!
    """),
    "VermilionCity_Gym_Text_TuckerPostBattle": t("""
        Það er ekki auðvelt að opna þessa
        hurð.

        LT. SURGE var alltaf frægur fyrir
        varkára eðlið sitt í hernum.
    """),
    "VermilionCity_Gym_Text_BailyIntro": t("""
        Ég er léttavigtarmaður, en ég er
        góður með rafmagn!

        Þess vegna gekk ég í þennan SAL.
    """),
    "VermilionCity_Gym_Text_DwayneIntro": t("""
        Þetta er enginn staður fyrir krakka!
        Ekki einu sinni ef þú ert góður!
    """),
    "VermilionCity_Gym_Text_DwayneDefeat": t("""
        Vá!
        Þú kom mér á óvart!
    """),
    "VermilionCity_Gym_Text_DwaynePostBattle": t("""
        LT. SURGE setti gildrurnar í SALNUM
        upp sjálfur.

        Hann setti tvöfalda lása alls staðar.
        Ég skal gefa þér vísbendingu.

        Þegar þú opnar fyrsta lásinn er
        annar lásinn rétt hjá honum.
    """),
    "VermilionCity_Gym_Text_GymGuyAdvice": t("""
        Yo!
        Verðandi meistari!

        LT. SURGE hefur gælunafn.

        Fólk kallar hann Eldingamanninn frá
        Ameríku!

        Hann er sérfræðingur í rafmagns-
        vasaskrímslum.

        FLUG/VATNS-gerðar vasaskrímsli standa
        illa gegn RAFMAGNS gerðinni.

        Varastu lömun líka.

        LT. SURGE er mjög varkár.

        Hann hefur læst sig inni, svo það
        verður ekki auðvelt að komast til hans.
    """),
    "VermilionCity_Gym_Text_GymGuyPostVictory": t("""
        Úff!
        Þessi bardagi var rafmagnaður!
    """),
    "VermilionCity_Gym_Text_GymStatue": t("""
        VERMILION VASASKRÍMSLA-SALUR
        SALSTJÓRI: LT. SURGE

        SIGURÞJÁLFARAR:
        {RIVAL}
    """),
    "VermilionCity_Gym_Text_GymStatuePlayerWon": t("""
        VERMILION VASASKRÍMSLA-SALUR
        SALSTJÓRI: LT. SURGE

        SIGURÞJÁLFARAR:
        {RIVAL}, {PLAYER}
    """),
    "VermilionCity_Gym_Text_SwitchUnderTrashFirstLockOpened": t("""
        Hey! Það er rofi undir ruslinu!
        Kveiktu á honum!

        Fyrsti raflásinn opnaðist!
    """),
    "VermilionCity_Gym_Text_SecondLockOpened": t("""
        Annar raflásinn opnaðist!
        Vélknúna hurðin opnaðist!
    """),
    "VermilionCity_Gym_Text_OnlyTrashLocksWereReset": t("""
        Neibb!
        Hér er bara rusl.

        Hey!
        Raflásarnir endurstilltust!
    """),
    "VermilionCity_House1_Text_ImFishingGuruDoYouLikeToFish": t("""
        Ég er VEIÐIMEISTARINN!

        Ég einfaldlega eeeelska að veiða!
        Ég þoli ekki að vera án þess.

        Segðu mér, finnst þér gaman að veiða?
    """),
    "VermilionCity_House1_Text_TakeThisAndFish": t("""
        Stórgott!
        Mér líkar stíllinn þinn.
        Ég held að við getum orðið vinir.

        Taktu þetta og veiddu, ungi vinur!
    """),
    "VermilionCity_House1_Text_ReceivedOldRodFromFishingGuru": t("""
        {PLAYER} fékk GAMLA STÖNG frá
        VEIÐIMEISTARANUM.
    """),
    "VermilionCity_House1_Text_FishingIsAWayOfLife": t("""
        Veiði er lífsstíll!
        Hún er eins og fínasta ljóðlist.

        Frá sjó til áa, farðu út og landaðu
        þeim stóra, vinur minn.
    """),
    "VermilionCity_House1_Text_OhThatsSoDisappointing": t("""
        Ó...
        Það veldur svo miklum vonbrigðum...
    """),
    "VermilionCity_House1_Text_HowAreTheFishBiting": t("""
        Halló, {PLAYER}!

        Bíta fiskarnir vel?
    """),
    "VermilionCity_House1_Text_NoRoomForNiceGift": t("""
        Ó, nei!

        Ég var með góða gjöf handa þér, en
        þú hefur ekkert pláss fyrir hana!
    """),
    "VermilionCity_House2_Text_DoYouHaveMonWantToTradeForMyMon": t("""
        Hæ!
        Áttu {STR_VAR_1}?

        Viltu skipta því fyrir minn
        {STR_VAR_2}?
    """),
    "VermilionCity_House2_Text_ThatsTooBad": t("""
        Það er leitt.
    """),
    "VermilionCity_House2_Text_ThisIsNoMon": t("""
        ...Þetta er ekki {STR_VAR_1}.

        Ef þú færð einn, vinsamlegast skiptu
        honum við mig!
    """),
    "VermilionCity_House2_Text_ThankYou": t("""
        Takk fyrir!
    """),
    "VermilionCity_House2_Text_HowIsMyOldMon": t("""
        Hvernig hefur gamli {STR_VAR_2} minn
        það?

        {STR_VAR_1} minn hefur það frábært!
    """),
    "VermilionCity_House3_Text_PidgeyFlyLetterToSaffron": t("""
        Ég læt DÚFUTETUR minn fljúga með bréf
        til SAFFRON í norðri.
    """),
    "VermilionCity_House3_Text_DearPippiLetter": t("""
        Kæra PIPPI,
        ég vona að ég sjái þig brátt.

        Ég heyrði að SAFFRON ætti í vandræðum
        með ROCKET-GENGIÐ.

        VERMILION virðist vera örugg.
    """),
    "VermilionCity_House3_Text_SendMyPidgeyToUnionRoom": t("""
        Ég vil skiptast á BRÉFUM við alls
        konar fólk.

        Ég sendi DÚFUTETUR minn í UNION ROOM
        til að skipta á BRÉFUM fyrir mig.
    """),
    "VermilionCity_Mart_Text_TeamRocketAreWickedPeople": t("""
        Það er til illt fólk sem notar
        vasaskrímsli í glæpsamlegum verkum.

        ROCKET-GENGIÐ verslar til dæmis með
        sjaldgæf vasaskrímsli.

        Þau yfirgefa líka vasaskrímsli sem
        þeim finnst óvinsæl eða gagnslaus.

        Svona hræðilegt fólk eru þau,
        ROCKET-GENGIÐ.
    """),
    "VermilionCity_Mart_Text_MonsGoodOrBadDependingOnTrainer": t("""
        Ég held að vasaskrímsli geti verið
        góð eða slæm.
        Það fer eftir ÞJÁLFARANUM.
    """),
    "VermilionCity_PokemonCenter_1F_Text_TrainerMonsStrongerThanWild": t("""
        Jafnvel á sama stigi geta vasaskrímsli
        haft mjög ólík gildi og hæfileika.

        Vasaskrímsli alið upp af ÞJÁLFARA er
        sterkara en villt vasaskrímsli.
    """),
    "VermilionCity_PokemonCenter_1F_Text_PoisonedMonFaintedWhileWalking": t("""
        Vasaskrímslið mitt var eitrað!
        Það rotaðist á meðan við gengum!
    """),
    "VermilionCity_PokemonCenter_1F_Text_AllMonWeakToSpecificTypes": t("""
        Það er satt að vasaskrímsli á hærra
        stigi verður öflugra...

        En öll vasaskrímsli hafa veika punkta
        gagnvart ákveðnum gerðum.

        Því virðist ekkert vasaskrímsli vera
        algilt sterkt.
    """),
    "VermilionCity_PokemonCenter_1F_Text_UrgeToBattleSomeoneAgain": t("""
        Löngunin til að berjast aftur við
        einhvern sem þú hefur áður mætt...

        Hefurðu nokkurn tíma fundið hana?
        Ég er viss um það.

        Mig langaði líka að berjast við
        ákveðið fólk aftur og aftur.

        Þess vegna hef ég verið að gefa
        þetta frá mér.
        Vinsamlegast, taktu einn!
    """),
    "VermilionCity_PokemonCenter_1F_Text_UseDeviceForRematches": t("""
        Notaðu þetta tæki og þú finnur
        ÞJÁLFARA sem vilja endurbardaga.

        Þú þarft samt að hlaða rafhlöðuna til
        að nota það.
    """),
    "VermilionCity_PokemonCenter_1F_Text_ExplainVSSeeker": t("""
        Hvernig notarðu VS LEITARA?
        Það er ekkert mál.

        Notaðu hann svona bíp-bíp-bíp, og
        ÞJÁLFARAR í kringum þig taka eftir.

        Ef einhver ÞJÁLFARI vill endurbardaga
        lætur hann þig vita strax.

        Hladdu rafhlöðuna og notaðu hann á
        vegi.
    """),
    "VermilionCity_PokemonFanClub_Text_AdmirePikachusTail": t("""
        Viltu ekki dást að yndislega halanum
        á LEIFTURSKO mínum?
    """),
    "VermilionCity_PokemonFanClub_Text_PikachuTwiceAsCute": t("""
        Hmph!

        LEIFTURSKO minn er tvöfalt sætari en
        þessi!
    """),
    "VermilionCity_PokemonFanClub_Text_AdoreMySeel": t("""
        Ég dýrka KÓPANGA minn!
        Hann er svo elskulegur!

        Hann tístir, Kyuuuh, þegar ég knúsa
        hann!
    """),
    "VermilionCity_PokemonFanClub_Text_SeelFarMoreAttractive": t("""
        Ó, kæri minn!

        KÓPANGI minn er miklu fallegri.
        Tvöfalt fallegri, myndi ég segja.
    """),
    "VermilionCity_PokemonFanClub_Text_DidYouComeToHearAboutMyMons": t("""
        Ég er formaður
        Vasaskrímsla-aðdáendaklúbbsins!

        Ég ala upp meira en hundrað
        vasaskrímsli!

        Ég er mjög vandlátur þegar kemur að
        vasaskrímslum!
        Sannarlega!

        Svo...

        Komstu í heimsókn til að heyra um
        vasaskrímslin mín?
    """),
    "VermilionCity_PokemonFanClub_Text_ChairmansStory": t("""
        Gott!
        Hlustaðu þá!

        Uppáhalds ELDKLÁRINN minn...

        Hann er... sætur... yndislegur...
        klár...
        og... magnaður... finnst þér ekki?...
        ó já... hann er... stórkostlegur...
        blíður... ég elska hann!

        Knúsa hann... þegar hann sefur...
        hlýr og mjúkur... glæsilegur...
        hrífandi...
        ...Úps! Sjáðu hvað klukkan er orðin!
        Ég hélt þér of lengi!

        Takk fyrir að hlusta á mig!
        Ég vil að þú fáir þetta!
    """),
    "VermilionCity_PokemonFanClub_Text_ReceivedBikeVoucherFromChairman": t("""
        {PLAYER} fékk REIÐHJÓLSMIÐA frá
        FORMANNINUM.
    """),
    "VermilionCity_PokemonFanClub_Text_ExplainBikeVoucher": t("""
        Farðu með REIÐHJÓLSMIÐANN í
        HJÓLABÚÐINA í CERULEAN BORG.

        Skiptu honum fyrir REIÐHJÓL, alveg
        ókeypis!

        Ekki hafa áhyggjur, uppáhalds
        GEIGHEGRINN minn getur FLY mig hvert
        sem ég þarf að fara.

        Þannig að ég þarf ekkert REIÐHJÓL.

        Ég vona að þér líki að hjóla!
    """),
    "VermilionCity_PokemonFanClub_Text_ComeBackToHearStory": t("""
        Ó.
        Komdu aftur þegar þú vilt heyra
        söguna mína!
    """),
    "VermilionCity_PokemonFanClub_Text_DidntComeToSeeAboutMonsAgain": t("""
        Halló, {PLAYER}!

        Komstu aftur til að heyra um
        vasaskrímslin mín?

        Nei?
        Verst!
    """),
    "VermilionCity_PokemonFanClub_Text_MakeRoomForThis": t("""
        Gerðu pláss fyrir þetta!
    """),
    "VermilionCity_PokemonFanClub_Text_ChairmanVeryVocalAboutPokemon": t("""
        FORMANNINUM okkar verður tíðrætt um
        vasaskrímsli.
    """),
    "VermilionCity_PokemonFanClub_Text_ListenPolitelyToOtherTrainers": t("""
        Við skulum öll hlusta kurteislega á
        aðra ÞJÁLFARA!
    """),
    "VermilionCity_PokemonFanClub_Text_SomeoneBragsBragBack": t("""
        Ef einhver montar sig, montaðu þig
        þá á móti!
    """),
    "VermilionCity_PokemonFanClub_Text_ChairmanReallyAdoresHisMons": t("""
        FORMANNINUM okkar þykir sannarlega
        vænt um vasaskrímslin sín.

        En manneskjan sem vasaskrímslum líkar
        best við er DAISY, held ég.
    """),
}


PREFIXES = ("data/maps/VermilionCity",)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-after-v7.csv")
    parser.add_argument("--output", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-vermilion-v1.csv")
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
        row["notes"] = "codex curated Vermilion city, gym, Fan Club, and houses v1"
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
