from __future__ import annotations

import argparse
import csv
import textwrap
from pathlib import Path

from common import repo_root


def t(value: str) -> str:
    return textwrap.dedent(value).strip()


TRANSLATIONS = {
    "CinnabarIsland_Text_DoorIsLocked": t("Hurðin er læst..."),
    "CinnabarIsland_Text_BlaineLivedHereSinceBeforeLab": t("""
        BLAINE úr CINNABAR SAL er ansi
        sérkennilegur náungi.

        Hann hefur búið á eyjunni síðan löngu
        áður en rannsóknarstofan var byggð.
    """),
    "CinnabarIsland_Text_ScientistsExperimentInMansion": t("""
        Vísindamenn gera tilraunir í brunna
        húsinu.

        Þú veist, húsinu sem þeir kalla
        VASASKRÍMSLAHERRASETRIÐ.
    """),
    "CinnabarIsland_Text_IslandSign": t("""
        CINNABAR EYJA
        Eldheitur bær brennandi þráar
    """),
    "CinnabarIsland_Text_PokemonLab": t("VASASKRÍMSLARANNSÓKNARSTOFA"),
    "CinnabarIsland_Text_GymSign": t("""
        CINNABAR EYJU VASASKRÍMSLA-SALUR
        SALSTJÓRI: BLAINE
        Eldheiti spurningameistarinn!
    """),
    "CinnabarIsland_Text_HeyIfItIsntPlayer": t("Ha? Heyrðu, er þetta ekki {PLAYER}!"),
    "CinnabarIsland_Text_ComeWithMeToOneIsland": t("""
        Sjáðu, þetta er ég, BILL.
        Langt síðan síðast!

        Ég vona að þú sért enn að nota
        tölvukerfið mitt.

        Heyrðu, fyrst við hittumst hér,
        hvernig væri að koma með mér?

        Það er lítil eyja langt í suðri sem
        heitir ONE ISLAND.

        Vinur bauð mér, svo ég er á leiðinni
        þangað.

        Hvað segirðu? Langar þig að koma með?
    """),
    "CinnabarIsland_Text_AllRightLetsGo": t("Allt í lagi þá. Förum!"),
    "CinnabarIsland_Text_IllBeWaitingInPokeCenter": t("""
        Hvað, ertu of upptekinn?

        Jæja, allt í lagi. Báturinn er hvort
        eð er ekki kominn enn.

        Ég bíð í VASASKRÍMSLAMIÐSTÖÐINNI
        þarna.

        Komdu til mín þegar þú ert búinn með
        erindin þín hér.
    """),
    "CinnabarIsland_Text_MyPalsBoatArrived": t("""
        Svo virðist sem bátur vinar míns sé
        líka kominn.

        Hann sendi hann sérstaklega hingað til
        CINNABAR að sækja mig.
    """),
    "CinnabarIsland_Text_IfYouHaveTriPassYouCanGoAgain": t("""
        Heyrðu, var þetta ekki löng sigling?

        Félagi minn CELIO virtist njóta
        félagsskapar þíns.

        Ég er viss um að hann tæki vel á móti
        þér ef þú heimsækir hann aftur.

        Ef þú ert með ÞRÍPASSA geturðu alltaf
        tekið ferju þangað frá VERMILION HÖFN.

        Jæja, takk fyrir félagsskapinn!
    """),
    "CinnabarIsland_Gym_Text_BlaineIntro": t("""
        Hah!

        Ég er BLAINE, eldheiti SALSTJÓRINN í
        CINNABAR SAL!

        Eldheitu vasaskrímslin mín eru öll
        grimm og tilbúin með brennandi hita!

        Þau brenna alla áskorendur til ösku!

        Hah! Þú ættir að hafa BRUNALYF!{PLAY_BGM}{MUS_ENCOUNTER_GYM_LEADER}
    """),
    "CinnabarIsland_Gym_Text_BlaineDefeat": t("""
        Ég hef brunnið niður í ekkert!
        Ekki einu sinni aska er eftir!

        Þú hefur unnið ELDFJALLSMERKIÐ.
    """),
    "CinnabarIsland_Gym_Text_FireBlastIsUltimateFireMove": t("""
        ELDGOS er fullkomna eldtæknin.

        Ekki eyða henni á VATNS-vasaskrímsli.
    """),
    "CinnabarIsland_Gym_Text_ExplainVolcanoBadge": t("""
        Hah!

        ELDFJALLSMERKIÐ hækkar SPECIAL tölur
        vasaskrímslanna þinna.

        Hér, þú mátt fá þetta líka!
    """),
    "CinnabarIsland_Gym_Text_ReceivedTM38FromBlaine": t("{PLAYER} fékk TM38 frá BLAINE."),
    "CinnabarIsland_Gym_Text_BlainePostBattle": t("""
        TM38 inniheldur ELDGOS. Kenndu það
        ELD-gerðar vasaskrímslum.

        HALATÓFA eða KAMELDLJÓN væru fullkomin
        fyrir þessa hreyfingu.
    """),
    "CinnabarIsland_Gym_Text_MakeSpaceForThis": t("Búðu til pláss fyrir þetta, barn!"),
    "CinnabarIsland_Gym_Text_ErikIntro": t("""
        Veistu hversu heitur eldandinn hjá
        vasaskrímslum getur orðið?
    """),
    "CinnabarIsland_Gym_Text_ErikDefeat": t("Ái! Heitt, heitt, heitt!"),
    "CinnabarIsland_Gym_Text_ErikPostBattle": t("""
        Eldur, eða nánar tiltekið bruni...

        ...Súrefni í loftinu... Bla, bla,
        bla, bla...
    """),
    "CinnabarIsland_Gym_Text_QuinnIntro": t("""
        Ég var þjófur, en gerðist heiðarlegur
        sem ÞJÁLFARI.
    """),
    "CinnabarIsland_Gym_Text_QuinnDefeat": t("Ég gefst upp!"),
    "CinnabarIsland_Gym_Text_QuinnPostBattle": t("""
        Ég fæ óstöðvandi löngun til að stela
        vasaskrímslum annarra.
    """),
    "CinnabarIsland_Gym_Text_AveryIntro": t("""
        Ég hef rannsakað vasaskrímsli í þaula.
        Þú getur ekki unnið!
    """),
    "CinnabarIsland_Gym_Text_AveryDefeat": t("Váá! Rannsóknir mínar dugðu ekki!"),
    "CinnabarIsland_Gym_Text_AveryPostBattle": t("""
        Kenningar mínar eru of flóknar til að
        þú skiljir þær.
    """),
    "CinnabarIsland_Gym_Text_RamonIntro": t("""
        Mér líkar að nota ELD-gerðar
        vasaskrímsli. Bara þannig er það.
    """),
    "CinnabarIsland_Gym_Text_RamonDefeat": t("Of heitt til að höndla!"),
    "CinnabarIsland_Gym_Text_RamonPostBattle": t("""
        Ég vildi að til væri þjófa-vasaskrímsli.
        Ég myndi nota það!
    """),
    "CinnabarIsland_Gym_Text_DerekIntro": t("Ég veit af hverju BLAINE varð ÞJÁLFARI."),
    "CinnabarIsland_Gym_Text_DerekDefeat": t("Ái!"),
    "CinnabarIsland_Gym_Text_DerekPostBattle": t("""
        SALSTJÓRINN okkar, BLAINE, villtist
        einu sinni í fjöllunum.

        Nótt skall á þegar eldheitt
        fugla-vasaskrímsli birtist.

        Ljósið frá því leyfði BLAINE að finna
        örugga leið niður.
    """),
    "CinnabarIsland_Gym_Text_DustyIntro": t("""
        Ég hef komið í marga SALI, en þessi
        passar best við minn stíl.
    """),
    "CinnabarIsland_Gym_Text_DustyDefeat": t("Vá! Of heitt!"),
    "CinnabarIsland_Gym_Text_DustyPostBattle": t("""
        LOGALD, NÍRÓFA...
        Þau eru vinsæl ELD-vasaskrímsli.
    """),
    "CinnabarIsland_Gym_Text_ZacIntro": t("Eldur er veikur gegn H2O."),
    "CinnabarIsland_Gym_Text_ZacDefeat": t("Ó! Slökktur!"),
    "CinnabarIsland_Gym_Text_ZacPostBattle": t("""
        Vatn sigrar eld, auðvitað.

        En eldur bræðir ís, svo ELD-gerðin
        sigrar ÍS-gerðar vasaskrímsli.
    """),
    "CinnabarIsland_Gym_Text_GymGuyAdvice": t("""
        Jæja! Verðandi meistari!

        Eldheiti BLAINE er sérfræðingur í
        ELD-vasaskrímslum.

        Slökktu baráttuvilja hans með vatni!

        Þú ættir líka að taka BRUNALYF.
    """),
    "CinnabarIsland_Gym_Text_GymGuyPostVictory": t("{PLAYER}! Þú sigraðir þennan eldhaus!"),
    "CinnabarIsland_Gym_Text_GymStatue": t("""
        CINNABAR VASASKRÍMSLA-SALUR
        SALSTJÓRI: BLAINE

        SIGRANDI ÞJÁLFARAR: {RIVAL}
    """),
    "CinnabarIsland_Gym_Text_GymStatuePlayerWon": t("""
        CINNABAR VASASKRÍMSLA-SALUR
        SALSTJÓRI: BLAINE

        SIGRANDI ÞJÁLFARAR: {RIVAL}, {PLAYER}
    """),
    "CinnabarIsland_Gym_Text_PokemonQuizRules": t("""
        Vasaskrímsla-spurningakeppni!

        Svaraðu rétt og dyrnar opnast í næsta
        herbergi.

        Svaraðu rangt og mættu ÞJÁLFARA!

        Ef þú vilt spara vasaskrímslin þín
        fyrir SALSTJÓRANN...

        Þá skaltu svara rétt!
        Byrjum!
    """),
    "CinnabarIsland_Gym_Text_QuizQuestion1": t("Þróast LIRFINGUR í PÚPISTI?"),
    "CinnabarIsland_Gym_Text_QuizQuestion2": t("""
        Eru níu opinber VASASKRÍMSLADEILDAR
        MERKI?
    """),
    "CinnabarIsland_Gym_Text_QuizQuestion3": t("Þróast POTTGORMUR þrisvar?"),
    "CinnabarIsland_Gym_Text_QuizQuestion4": t("""
        Virka rafmagnshreyfingar vel á
        JARÐ-gerðar vasaskrímsli?
    """),
    "CinnabarIsland_Gym_Text_QuizQuestion5": t("""
        Eru vasaskrímsli af sömu tegund og
        sama stigi ekki eins?
    """),
    "CinnabarIsland_Gym_Text_QuizQuestion6": t("Inniheldur TM28 GRAFSTEIN?"),
    "CinnabarIsland_Gym_Text_CorrectGoOnThrough": t("""
        Þú hefur algjörlega rétt fyrir þér!

        Haltu áfram inn!
    """),
    "CinnabarIsland_Gym_Text_SorryBadCall": t("""
        Fyrirgefðu!
        Rangt svar!
    """),
    "CinnabarIsland_Mart_Text_DontTheyHaveXAttack": t("""
        Eiga þau ekki X ATTACK?

        Mér líkar það af því að það hækkar
        ATTACK töluna í bardaga.
    """),
    "CinnabarIsland_Mart_Text_ExtraItemsNeverHurt": t("""
        Það sakar aldrei að hafa aukahluti.
        Maður veit aldrei hvað gæti gerst.
    """),
    "CinnabarIsland_PokemonCenter_1F_Text_CinnabarGymLocked": t("""
        Ég kom að heimsækja CINNABAR SAL, en
        dyrnar eru kyrfilega læstar.

        Það hlýtur að vera lykill að þeim
        einhvers staðar.

        Gæti hann verið í brunna herrasetrinu?

        Vinur SALSTJÓRANS bjó þar víst áður.
    """),
    "CinnabarIsland_PokemonCenter_1F_Text_VisitUnionRoom": t("""
        Áttu marga vini?

        Það er auðvitað gaman að tengjast
        venjulegu vinunum.

        En hvernig væri að heimsækja UNION
        ROOM öðru hvoru?

        Hver veit, kannski eignastu nýja vini.

        Ég held að það sé tímans virði að
        skoða UNION ROOM.
    """),
    "CinnabarIsland_PokemonCenter_1F_Text_EvolutionCanWaitForNewMoves": t("""
        Vasaskrímsli geta enn lært tækni eftir
        að þróun er stöðvuð.

        Þróun getur beðið þar til nýjar
        hreyfingar hafa lærst.
    """),
    "CinnabarIsland_PokemonCenter_1F_Text_ReadyToSailToOneIsland": t("""
        BILL: Heyrðu, þú lést mig bíða!
        Tilbúinn að sigla til ONE ISLAND?
    """),
    "CinnabarIsland_PokemonCenter_1F_Text_OhNotDoneYet": t("Ó, ertu ekki alveg búinn enn?"),
    "CinnabarIsland_PokemonCenter_1F_Text_LetsGo": t("Jæja, þá er það komið. Förum!"),
    "CinnabarIsland_Gym_Text_PhotoOfBlaineAndFuji": t("""
        Þetta er mynd af BLAINE og MR. FUJI.

        Þeir standa öxl við öxl og brosa
        breitt.
    """),
    "CinnabarIsland_PokemonLab_Entrance_Text_StudyMonsExtensively": t("""
        Við rannsökum vasaskrímsli ítarlega á
        hverjum degi.

        Fólk kemur oft með sjaldgæf
        vasaskrímsli til skoðunar.
    """),
    "CinnabarIsland_PokemonLab_Entrance_Text_PhotoOfLabFounderDrFuji": t("""
        Mynd af stofnanda rannsóknarstofunnar...
        DR. FUJI?!
    """),
    "CinnabarIsland_PokemonLab_Entrance_Text_MeetingRoomSign": t("VASASKRÍMSLARANNSÓKNARSTOFA Fundarherbergi"),
    "CinnabarIsland_PokemonLab_Entrance_Text_RAndDRoomSign": t("VASASKRÍMSLARANNSÓKNARSTOFA R & D herbergi"),
    "CinnabarIsland_PokemonLab_Entrance_Text_TestingRoomSign": t("VASASKRÍMSLARANNSÓKNARSTOFA Prófunarherbergi"),
    "Text_MetronomeTeach": t("""
        Tsk-tsk-tsk! Ég skal kenna þér
        snjalla hreyfingu.

        Kenndu hana vasaskrímsli og horfðu á
        fjörið hefjast!

        Hún heitir TAKTMÆLIR.
        Líst þér á hana?
    """),
    "Text_MetronomeDeclined": t("Ég segi þér, þetta er mjög skemmtilegt!"),
    "Text_MetronomeWhichMon": t("Allt í lagi! Hvaða vasaskrímsli á ég að kenna?"),
    "Text_MetronomeTaught": t("""
        Tsk-tsk-tsk!
        Svona hljómar TAKTMÆLIR.

        Hann potar í heilann á vasaskrímslinu
        og lætur það nota hreyfingar sem það
        kann ekki einu sinni.
    """),
    "CinnabarIsland_PokemonLab_ExperimentRoom_Text_HaveYouAFossilForMe": t("""
        Hæ!

        Ég er mikilvægur læknir. Já, mjög
        mikilvægur, sannarlega.

        Hér rannsaka ég sjaldgæfa
        vasaskrímslasteingervinga. Allan tímann
        rannsaka ég.

        Þú! Ertu með steingerving handa mér?
    """),
    "CinnabarIsland_PokemonLab_ExperimentRoom_Text_NoIsTooBad": t("Nei! Það er of slæmt!"),
    "CinnabarIsland_PokemonLab_ExperimentRoom_Text_TakesTimeGoForWalkJP": t("""
        Þetta tekur smá tíma!

        Farðu og röltaðu aðeins um nágrennið!
    """),
    "CinnabarIsland_PokemonLab_ExperimentRoom_Text_FossilMonBackToLife": t("""
        Þú seinn. Hvar varstu?

        Steingervingurinn þinn lifir aftur!
        Það var {STR_VAR_1}, eins og ég hélt!
    """),
    "CinnabarIsland_PokemonLab_ExperimentRoom_Text_ReceivedMonFromDoctor": t("""
        {PLAYER} fékk {STR_VAR_1} frá
        lækninum.
    """),
    "CinnabarIsland_PokemonLab_ExperimentRoom_Text_NoRoomForPokemon": t("""
        Þú ert með of mörg vasaskrímsli!
    """),
    "CinnabarIsland_PokemonLab_ExperimentRoom_Text_ThatFossilIsOfMonMakeItLiveAgain": t("""
        Ó! Þetta er {STR_VAR_2}, það er það!

        Þetta er steingervingur af {STR_VAR_1},
        vasaskrímsli sem er þegar útdautt!

        Upprisuvélin mín mun láta þetta
        vasaskrímsli lifa aftur!
    """),
    "CinnabarIsland_PokemonLab_ExperimentRoom_Text_HandedFossilToWeirdDoctor": t("""
        Svo! Flýttu þér og gefðu mér þetta!

        {FONT_NORMAL}{PLAYER} afhenti
        skrýtna lækninum {STR_VAR_2}.
    """),
    "CinnabarIsland_PokemonLab_ExperimentRoom_Text_TakesTimeGoForWalk": t("""
        Ég tek smá tíma!
        Þú ferð í göngutúr á meðan!
    """),
    "CinnabarIsland_PokemonLab_ExperimentRoom_Text_YouComeAgain": t("Aiyah! Þú kemur aftur!"),
    "CinnabarIsland_PokemonLab_Lounge_Text_FoundFossilInMtMoon": t("""
        Ég fann þennan afar merkilega
        steingerving inni í MT. MOON.

        Ég held að hann sé af sjaldgæfu,
        forsögulegu vasaskrímsli.
    """),
    "CinnabarIsland_PokemonLab_ResearchRoom_Text_EeveeCanEvolveIntroThreeMons": t("""
        SNIÐDÝR getur þróast í eina af þremur
        tegundum vasaskrímsla.
    """),
    "CinnabarIsland_PokemonLab_ResearchRoom_Text_LegendaryBirdEmail": t("""
        Það er tölvupóstur.

        ... ... ...

        Til eru þrjú goðsagnakennd
        fugla-vasaskrímsli.

        Þau eru ÉLJASKARFU, ÞÓRSHANI og
        BLOSSAGAUK.

        Dvalarstaðir þeirra eru óþekktir.

        Við ætlum að kanna hellinn nálægt
        CERULEAN.

        Frá: VASASKRÍMSLA-RANNSÓKNARHÓPUR...
    """),
    "CinnabarIsland_PokemonLab_ResearchRoom_Text_AnAmberPipe": t("Rafpípa úr rafi!"),
    "PokemonMansion_1F_Text_TedIntro": t("Hver ert þú? Það ætti enginn að vera hér."),
    "PokemonMansion_1F_Text_TedDefeat": t("Ái!"),
    "PokemonMansion_1F_Text_TedPostBattle": t("Lykill? Ég veit ekki hvað þú ert að tala um."),
    "PokemonMansion_1F_Text_JohnsonIntro": t("""
        V-v-váá!
        Þú brá mér! Ég hélt að þú værir draugur.
    """),
    "PokemonMansion_1F_Text_JohnsonDefeat": t("Tsk! Ég næ engum sigrum."),
    "PokemonMansion_1F_Text_JohnsonPostBattle": t("""
        Ég var að kanna hér einn, en mér er
        farið að bregða.

        Ég ætti að fara bráðum.
    """),
    "PokemonMansion_Text_PressSecretSwitch": t("""
        Leynirofi!

        Ýta á hann?
    """),
    "PokemonMansion_Text_WhoWouldnt": t("Hver myndi ekki gera það?"),
    "PokemonMansion_Text_NotQuiteYet": t("Ekki alveg strax!"),
    "PokemonMansion_1F_Text_ArnieIntro": t("""
        Ég kemst ekki út!
        Þessi gamli staður er ein stór þraut.
    """),
    "PokemonMansion_1F_Text_ArnieDefeat": t("Ó, nei! Ránsfengspokinn minn!"),
    "PokemonMansion_1F_Text_ArniePostBattle": t("""
        Rofarnir hér opna og loka til skiptis
        mismunandi dyrum.
    """),
    "PokemonMansion_1F_Text_NewMonDiscoveredInGuyanaJungle": t("""
        Dagbók: 5. júlí
        Guyana, Suður-Ameríka

        Nýtt vasaskrímsli fannst djúpt inni í
        frumskóginum.
    """),
    "PokemonMansion_1F_Text_ChristenedDiscoveredMonMew": t("""
        Dagbók: 10. júlí
        Við nefndum nýfundna vasaskrímslið
        MÝTU.
    """),
    "PokemonMansion_Text_PressSecretSwitchJP": t("""
        Leynirofi!

        Ýta á hann?
    """),
    "PokemonMansion_Text_LetsTryIt": t("Prófum það! ...Smell!"),
    "PokemonMansion_Text_GaveUpOnPressingSwitch": t("Hættir við að ýta á rofann."),
    "PokemonMansion_1F_Text_SimonIntro": t("Þessi staður er, sko, risastór!"),
    "PokemonMansion_1F_Text_SimonDefeat": t("Ayah!"),
    "PokemonMansion_1F_Text_SimonPostBattle": t("Ég velti fyrir mér hvert félagi minn fór."),
    "PokemonMansion_1F_Text_BraydonIntro": t("Leiðbeinandi minn bjó einu sinni hér."),
    "PokemonMansion_1F_Text_BraydonDefeat": t("Úff! Yfirþyrmandi!"),
    "PokemonMansion_1F_Text_BraydonPostBattle": t("""
        Svo þú ert fastur?
        Prófaðu að stökkva niður þarna!
    """),
    "PokemonMansion_1F_Text_MewGaveBirthToMewtwo": t("""
        Dagbók: 6. feb.
        MÝTA fæddi af sér.

        Við nefndum nýburann TVÍMÝTU.
    """),
    "PokemonMansion_B1F_Text_LewisIntro": t("Uh-oh... Hvar er ég núna?"),
    "PokemonMansion_B1F_Text_LewisDefeat": t("Awooh!"),
    "PokemonMansion_B1F_Text_LewisPostBattle": t("""
        Þú getur fundið hluti liggjandi hér.
        Íbúarnir hljóta að hafa skilið þá eftir.
    """),
    "PokemonMansion_B1F_Text_IvanIntro": t("""
        Þessi staður er fullkominn fyrir
        rannsóknarstofu. Sjáðu allt plássið.
    """),
    "PokemonMansion_B1F_Text_IvanDefeat": t("Til hvers var þetta?"),
    "PokemonMansion_B1F_Text_IvanPostBattle": t("""
        Mér líkar hér.
        Þetta stuðlar að rannsóknum mínum.
    """),
    "PokemonMansion_B1F_Text_MewtwoIsFarTooPowerful": t("""
        Dagbók: 1. sept.
        TVÍMÝTA er allt of kraftmikil.

        Okkur tókst ekki að hemja illvígar
        hneigðir hennar...
    """),
}


FILES = {
    "data/maps/CinnabarIsland/text.inc",
    "data/maps/CinnabarIsland_Gym/text.inc",
    "data/maps/CinnabarIsland_Mart/text.inc",
    "data/maps/CinnabarIsland_PokemonCenter_1F/text.inc",
    "data/maps/CinnabarIsland_PokemonLab_Entrance/text.inc",
    "data/maps/CinnabarIsland_PokemonLab_ExperimentRoom/text.inc",
    "data/maps/CinnabarIsland_PokemonLab_Lounge/text.inc",
    "data/maps/CinnabarIsland_PokemonLab_ResearchRoom/text.inc",
    "data/maps/PokemonMansion_1F/text.inc",
    "data/maps/PokemonMansion_2F/text.inc",
    "data/maps/PokemonMansion_3F/text.inc",
    "data/maps/PokemonMansion_B1F/text.inc",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-after-v17.csv")
    parser.add_argument("--output", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-cinnabar-v1.csv")
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
        row["notes"] = "codex curated Cinnabar Island, Lab, Gym, Mansion v1"
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
