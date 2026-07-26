from __future__ import annotations

import argparse
import csv
import textwrap
from pathlib import Path

from common import repo_root


def t(value: str) -> str:
    return textwrap.dedent(value).strip()


TRANSLATIONS = {
    "SSAnne_1F_Corridor_Text_LeStrongSilentType": t("""
        Bonjour!
        Ég er le þjónninn á þessu skipi!

        Ég þjóna þér með gleði hverju sem þú
        vilt!

        ... ...
        Ah! Le sterka þögla týpan!
    """),
    "SSAnne_1F_Corridor_Text_PassengersAreRestless": t("""
        Farþegarnir eru órólegir eftir þessa
        löngu siglingu.

        Þeir leiðari gætu skorað á þig!
    """),
    "SSAnne_1F_Room1_Text_ImAGlobalPoliceAgent": t("""
        Suss...!
        Ég er útsendari ALÞJÓÐALÖGREGLUNNAR.

        Ég er á slóð ROCKET-GENGISINS.
        Þau eru að bralla eitthvað slæmt!
    """),
    "SSAnne_1F_Room2_Text_TylerIntro": t("""
        Ég elska vasaskrímsli!
        Gerir þú það?
    """),
    "SSAnne_1F_Room2_Text_TylerDefeat": t("""
        Vá!
        Þú ert frábær!
    """),
    "SSAnne_1F_Room2_Text_TylerPostBattle": t("""
        Heyrðu, heyrðu!
        Leyfðu mér að vera vinur þinn, allt í
        lagi?

        Þá getum við skipt á vasaskrímslum og
        gert allskonar.
    """),
    "SSAnne_1F_Room2_Text_AnnIntro": t("""
        Ég safnaði þessum vasaskrímslum frá
        öllum heimshornum!
    """),
    "SSAnne_1F_Room2_Text_AnnDefeat": t("""
        Ó, nei!
        Ég fór um allan heim fyrir þau!
    """),
    "SSAnne_1F_Room2_Text_AnnPostBattle": t("""
        Þú meiddir greyið vasaskrímslin mín!

        Ég krefst þess að þú læknir þau í
        vasaskrímslamiðstöð!
    """),
    "SSAnne_1F_Room2_Text_CruisingAroundWorld": t("""
        Við erum í siglingu um heiminn, ég og
        börnin mín.
    """),
    "SSAnne_1F_Room3_Text_CruiseIsElegantAndCozy": t("""
        Heimssigling er svo glæsileg en samt
        notaleg!
    """),
    "SSAnne_1F_Room3_Text_AlwaysTravelWithWigglytuff": t("""
        Ég ferðast alltaf með KNÚSFÚS.
        Ég fer aldrei að heiman án hans.
    """),
    "SSAnne_1F_Room4_Text_WaiterCherryPiePlease": t("""
        Þjónn, ég vil fá kirsuberjaböku,
        takk!
    """),
    "SSAnne_1F_Room4_Text_WaitressCherryPiePlease": t("""
        Þjónustustúlka, ég vil fá
        kirsuberjaböku, takk!
    """),
    "SSAnne_1F_Room5_Text_ArthurIntro": t("""
        Þú ósvífni hvolpur!
        Hvernig vogarðu þér að ruddast inn!
    """),
    "SSAnne_1F_Room5_Text_ArthurDefeat": t("""
        Hmph! Þú ókurteisa barn!
        Þú hefur enga háttvísi!
    """),
    "SSAnne_1F_Room6_Text_TakeAShortRest": t("""
        Þú lítur þreytt út.
        Viltu hvíla þig smástund?
    """),
    "SSAnne_1F_Room6_Text_GladEveryoneIsRefreshed": t("""
        Það gleður mig að sjá að allir eru
        hressir og endurnærðir.
    """),
    "SSAnne_1F_Room6_Text_SorryYouLookLikeMyBrother": t("""
        Ó, afsakaðu að ég hugsaði svona um
        þig.
        Þú líkist litla bróður mínum...
    """),
    "SSAnne_1F_Room6_Text_SorryYouLookLikeMySister": t("""
        Ó, afsakaðu að ég hugsaði svona um
        þig.
        Þú líkist litlu systur minni...
    """),
    "SSAnne_1F_Room7_Text_ThomasIntro": t("""
        Ég er aðeins einmana ferðalangur...

        Eina félagsskapinn og vinina á ég í
        vasaskrímslum sem ég náði á ferðum
        mínum...
    """),
    "SSAnne_1F_Room7_Text_ThomasDefeat": t("""
        Vinir mínir, vinir mínir...
    """),
    "SSAnne_1F_Room7_Text_ThomasPostBattle": t("""
        Þú ættir að vera góður við vini!
    """),
    "SSAnne_2F_Corridor_Text_ThisShipIsLuxuryLiner": t("""
        Þetta skip, hún er lúxusskip fyrir
        ÞJÁLFARA heimsins!

        Í hverri höfn höldum við veislur með
        boðnum ÞJÁLFURUM.
    """),
    "SSAnne_2F_Corridor_Text_RivalIntro": t("""
        {RIVAL}: Bonjour!
        {PLAYER}!

        Hugsa sér að sjá þig hér!
        {PLAYER}, var þér í alvöru boðið?

        Hvernig gengur með VasaDEX-ið þitt?

        Ég hef þegar náð 40 tegundum, félagi.
        Mismunandi tegundir eru alls staðar.

        Skriðu um graslendi og leitaðu vel að
        þeim.
    """),
    "SSAnne_2F_Corridor_Text_RivalDefeat": t("""
        Hmph!

        Að minnsta kosti ertu að ala upp
        vasaskrímslin þín!
    """),
    "SSAnne_2F_Corridor_Text_RivalPostBattle": t("""
        {RIVAL}: Ég heyrði að það væri
        CUT-meistari um borð.

        En hann var bara sjóveikur gamall
        maður!

        CUT sjálft er mjög gagnlegt.
        Já, það mun koma sér vel.

        Þú ættir líka að fara að hitta hann.
        Sjáumst!
    """),
    "SSAnne_2F_Room1_Text_SleepingMonLookedLikeThis": t("""
        Ég hef ferðast vítt og breitt, en á
        öllum ferðum mínum hef ég aldrei séð
        neitt vasaskrímsli sofa svona!

        Það leit einhvern veginn svona út!
    """),
    "SSAnne_2F_Room2_Text_BrooksIntro": t("""
        Að keppa við unga fólkið heldur mér
        ungum.
    """),
    "SSAnne_2F_Room2_Text_BrooksDefeat": t("""
        Góður bardagi!
        Ah, mér finnst ég ungur aftur!
    """),
    "SSAnne_2F_Room2_Text_BrooksPostBattle": t("""
        Fyrir fimmtán árum hefði ég unnið!
    """),
    "SSAnne_2F_Room2_Text_DaleIntro": t("""
        Sjáðu hvað ég veiddi upp!
    """),
    "SSAnne_2F_Room2_Text_DaleDefeat": t("""
        Ég er búinn að missa allt!
    """),
    "SSAnne_2F_Room2_Text_DalePostBattle": t("""
        Veisla?

        Veislan á skemmtiferðaskipinu ætti að
        vera búin núna.
    """),
    "SSAnne_2F_Room3_Text_SeenMonsFerryPeople": t("""
        Ah, já, ég hef séð nokkur
        vasaskrímsli ferja fólk yfir vatnið!
    """),
    "SSAnne_2F_Room3_Text_SomeTreesCanBeCutDown": t("""
        Lítil tré má höggva niður með
        hreyfingunni CUT.

        En mundu þetta!
        CUT er HM tækni.

        Þegar hún hefur lærst er ekki auðvelt
        að losa sig við hana.
    """),
    "SSAnne_2F_Room4_Text_LamarIntro": t("""
        Hvort finnst þér verðmætara,
        sterkt eða sjaldgæft vasaskrímsli?
    """),
    "SSAnne_2F_Room4_Text_LamarDefeat": t("""
        Ég verð að heilsa þér að hermannasið!
    """),
    "SSAnne_2F_Room4_Text_LamarPostBattle": t("""
        Persónulega kýs ég sterk og sjaldgæf
        vasaskrímsli.
    """),
    "SSAnne_2F_Room4_Text_DawnIntro": t("""
        Ég man ekki eftir að hafa séð þig í
        veislunni?
    """),
    "SSAnne_2F_Room4_Text_DawnPostBattle": t("""
        Ó, ég dáist að sterku vasaskrímslunum
        þínum!
        Ó, hvað ég öfunda þig af þeim!
    """),
    "SSAnne_2F_Room5_Text_HaveYouGoneToSafariZone": t("""
        Hefurðu farið í SAFARI ZONE í
        FUCHSIA BORG?

        Þar eru margar gerðir af sjaldgæfum
        vasaskrímslum.
    """),
    "SSAnne_2F_Room5_Text_WeThinkSafariZoneIsAwesome": t("""
        Ég og pabbi minn höldum að SAFARI
        ZONE sé frábært!
        Ég vildi að við gætum farið þangað
        aftur.
    """),
    "SSAnne_2F_Room6_Text_CaptainIsAwfullySick": t("""
        SKIPSTJÓRINN sagði að hann væri
        hræðilega veikur.
        Hann var allur fölur.
    """),
    "SSAnne_3F_Corridor_Text_CaptainTeachesCutToMons": t("""
        SKIPSTJÓRINN okkar er sverðmeistari.
        Hann er magnaður í CUT.

        Þeir segja að hann kenni jafnvel CUT
        til vasaskrímsla!
    """),
    "SSAnne_B1F_Room1_Text_PhillipIntro": t("""
        Félagi, þú gengur plankann ef þú
        tapar!
    """),
    "SSAnne_B1F_Room1_Text_PhillipPostBattle": t("""
        Þegar við erum úti á sjó reka
        marglyttu-vasaskrímsli stundum hjá.
    """),
    "SSAnne_B1F_Room1_Text_BarnyIntro": t("""
        Halló, ókunnugi!

        Ég veit ekki hvort þú ert frá sjónum
        eða fjöllunum, en stoppaðu og spjallaðu.

        Öll vasaskrímslin mín eru úr sjónum.
    """),
    "SSAnne_B1F_Room1_Text_BarnyDefeat": t("""
        Fjandinn!
        Ég lét þennan sleppa!
    """),
    "SSAnne_B1F_Room1_Text_BarnyPostBattle": t("""
        Ég ætlaði líka að gera þig að
        aðstoðarmanni mínum!
    """),
    "SSAnne_B1F_Room2_Text_HueyIntro": t("""
        Jafnvel við sjómenn eigum líka
        vasaskrímsli!
    """),
    "SSAnne_B1F_Room2_Text_HueyDefeat": t("""
        Allt í lagi, þú ert ekki slæmur.
    """),
    "SSAnne_B1F_Room2_Text_HueyPostBattle": t("""
        Við náðum öllum vasaskrímslunum okkar
        þegar við vorum úti á sjó.
    """),
    "SSAnne_B1F_Room3_Text_DylanIntro": t("""
        Mér líkar við fjöruga krakka eins og
        þig!
    """),
    "SSAnne_B1F_Room3_Text_DylanPostBattle": t("""
        Sjávarvasaskrímsli búa í djúpu vatni.
        Þú þarft STÖNG til að veiða þau upp!
    """),
    "SSAnne_B1F_Room4_Text_LeonardIntro": t("""
        Þú veist hvað sagt er um sjómenn og
        bardaga!
    """),
    "SSAnne_B1F_Room4_Text_LeonardPostBattle": t("""
        Hahaha!
        Viltu verða sjómaður, félagi?
    """),
    "SSAnne_B1F_Room4_Text_DuncanIntro": t("""
        Komdu þá!
        Sjómaðurstolt mitt er í húfi!
    """),
    "SSAnne_B1F_Room4_Text_DuncanDefeat": t("""
        Andinn þinn sökkti mér!
    """),
    "SSAnne_B1F_Room4_Text_DuncanPostBattle": t("""
        Sástu VEIÐIMEISTARANN í VERMILION
        BORG?
    """),
    "SSAnne_B1F_Room5_Text_MachokeHasStrengthToMoveRocks": t("""
        Félagi minn AFLGARPUR er ofursterkur!

        Hann hefur nægan STRENGTH til að færa
        stóra steina!
    """),
    "SSAnne_CaptainsOffice_Text_CaptainIFeelSeasick": t("""
        SKIPSTJÓRI: Óaaargh...
        Mér líður hræðilega...
        Urrp! Sjóveiki...
    """),
    "SSAnne_CaptainsOffice_Text_RubbedCaptainsBack": t("""
        {PLAYER} nuddaði bakið á
        SKIPSTJÓRANUM!

        Nudd-nudd...
        Nudd-nudd...
    """),
    "SSAnne_CaptainsOffice_Text_ThankYouHaveHMForCut": t("""
        SKIPSTJÓRI: Úff! Takk fyrir!
        Mér líður miklu betur núna.

        Viltu sjá leynilegu CUT tæknina mína?

        Ég gæti sýnt þér dýrmætu CUT tæknina
        mína ef ég væri ekki svona veikur...

        Ég veit!
        Þú mátt fá þetta!
        Þessa FÖLDU VÉL!

        Kenndu vasaskrímslinu þínu CUT, og þú
        getur séð það CUT-a hvenær sem er!
    """),
    "SSAnne_CaptainsOffice_Text_ObtainedHM01FromCaptain": t("""
        {PLAYER} fékk HM01 frá
        SKIPSTJÓRANUM!
    """),
    "SSAnne_CaptainsOffice_Text_ExplainCut": t("""
        Með CUT geturðu höggvið niður lítil
        tré.

        Af hverju prófarðu það ekki á trjánum
        í kringum VERMILION BORG?
    """),
    "SSAnne_CaptainsOffice_Text_SSAnneWillSetSailSoon": t("""
        SKIPSTJÓRI: ...Úff!

        Nú þegar ég er ekki veikur lengur held
        ég að tíminn sé kominn.

        S.S. ANNE leggur fljótlega úr höfn!

        Vertu sæl, þar til við snúum aftur til
        VERMILION BORGAR!
    """),
    "SSAnne_CaptainsOffice_Text_YouHaveNoRoomForThis": t("""
        Ó, nei!
        Þú hefur ekkert pláss fyrir þetta!
    """),
    "SSAnne_CaptainsOffice_Text_YuckShouldntHaveLooked": t("""
        Oj!
        Hefði ekki átt að líta!
    """),
    "SSAnne_CaptainsOffice_Text_HowToConquerSeasickness": t("""
        Hvernig má sigrast á sjóveiki...
        SKIPSTJÓRINN er að lesa þetta!
    """),
    "SSAnne_Deck_Text_ShipDepartingSoon": t("""
        Veislan er búin.
        Skipið leggur fljótlega af stað.
    """),
    "SSAnne_Deck_Text_ScrubbingDecksHardWork": t("""
        Úff!
        Það er erfiðisvinna að skrúbba dekk!
    """),
    "SSAnne_Deck_Text_FeelSeasick": t("""
        Urr... mér líður illa...

        Ég varð sjóveikur, svo ég fór út til
        að fá loft...
    """),
    "SSAnne_Deck_Text_EdmondDefeat": t("""
        Þú ert tilkomumikill!
    """),
    "SSAnne_Deck_Text_EdmondPostBattle": t("""
        Hversu margar gerðir vasaskrímsla
        heldurðu að séu í þessum stóra heimi?
    """),
    "SSAnne_Deck_Text_TrevorIntro": t("""
        Ahoy!
        Ertu sjóveikur?
    """),
    "SSAnne_Deck_Text_TrevorPostBattle": t("""
        Pabbi minn sagði að til væru 100
        gerðir vasaskrímsla.
        Ég held að þær séu fleiri.
    """),
    "SSAnne_Kitchen_Text_BusyOutOfTheWay": t("""
        Þú, mon petit!
        Við erum upptekin hér!
        Úr vegi!
    """),
    "SSAnne_Kitchen_Text_SawOddBerryInTrash": t("""
        Ég sá skrýtið BER í ruslinu.
        Ég velti fyrir mér hvað það var.
    """),
    "SSAnne_Kitchen_Text_SoBusyImDizzy": t("""
        Ég er svo upptekinn að mig svimar!
        Þú verður að gefa mér pláss hér!
    """),
    "SSAnne_Kitchen_Text_HearAboutSnorlaxItsAGlutton": t("""
        Heyrðirðu um HROTÞURS?
        Hann er mathákur.

        Ekkert annað vasaskrímsli borðar og
        sefur eins og HROTÞURS getur og gerir!
    """),
    "SSAnne_Kitchen_Text_IAmLeChefMainCourseIs": t("""
        Hrm!
        Sannarlega er ég le KOKKUR!

        Le aðalrétturinn er
    """),
    "SSAnne_Kitchen_Text_EelsAuBarbecue": t("""
        Grillaðir álar!

        Ég óttast að les gestir geri uppreisn.
    """),
    "SSAnne_Kitchen_Text_PrimeBeefsteak": t("""
        Fyrsta flokks nautasteik!

        En hef ég nóg af nautafille?
    """),
}


PREFIXES = ("data/maps/SSAnne",)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-after-v8.csv")
    parser.add_argument("--output", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-ssanne-v1.csv")
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
        row["notes"] = "codex curated S.S. Anne v1"
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
