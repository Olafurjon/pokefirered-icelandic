from __future__ import annotations

import argparse
import csv
import textwrap
from pathlib import Path

from common import repo_root


def t(value: str) -> str:
    return textwrap.dedent(value).strip()


TRANSLATIONS = {
    "FuchsiaCity_Text_DidYouTrySafariGame": t("""
        Prófaðirðu SAFARI-LEIKINN?

        Þar eru nokkur sjaldgæf vasaskrímsli
        sem aðeins er hægt að ná þar.
    """),
    "FuchsiaCity_Text_SafariZoneZooInFront": t("""
        SAFARI ZONE er með dýragarð fyrir
        framan innganginn.

        Fyrir aftan er SAFARI-LEIKURINN þar
        sem hægt er að ná vasaskrímslum.
    """),
    "FuchsiaCity_Text_WheresSara": t("""
        ERIK: Hvar er SARA?
        Ég sagðist ætla að hitta hana hér.
    """),
    "FuchsiaCity_Text_ItemBallInThere": t("""
        Þessi hlutabolti þarna inni...
        Vildirðu fá hann?

        Ég líka!
        ...Ha? Er þetta vasaskrímsli?
    """),
    "FuchsiaCity_Text_CitySign": t("""
        FUCHSIA BORG
        Sjáðu! Þetta er ástríðubleikt!
    """),
    "FuchsiaCity_Text_SafariZoneSign": t("""
        VASASKRÍMSLA-PARADÍS
        SAFARI ZONE
    """),
    "FuchsiaCity_Text_SafariGameSign": t("""
        SAFARI-LEIKUR
        VASASKRÍMSLI SEM ÞÚ GRÍPUR!
    """),
    "FuchsiaCity_Text_WardensHomeSign": t("""
        SAFARI ZONE
        HEIMILI VARÐARINS
    """),
    "FuchsiaCity_Text_SafariZoneOfficeSign": t("""
        VASASKRÍMSLA-PARADÍS!
        Velkomin í SAFARI ZONE!
        SKRIFSTOFA SAFARI ZONE
    """),
    "FuchsiaCity_Text_GymSign": t("""
        FUCHSIA BORGAR VASASKRÍMSLA-SALUR
        SALSTJÓRI: KOGA
        Eitraði ninjameistarinn
    """),
    "FuchsiaCity_Text_ChanseySign": t("""
        Nafn: SÆLEGG
        Að ná einu er allt undir heppni komið.
    """),
    "FuchsiaCity_Text_VoltorbSign": t("""
        Nafn: STUÐBOLTI
        Lifandi ímynd VASABOLTA.
    """),
    "FuchsiaCity_Text_KangaskhanSign": t("""
        Nafn: KENGÚRILL

        Móðurlegt vasaskrímsli sem elur unga
        sína í poka á maganum.
    """),
    "FuchsiaCity_Text_SlowpokeSign": t("""
        Nafn: SLJÓN
        Vinalegt og fer mjög hægt.
    """),
    "FuchsiaCity_Text_LaprasSign": t("""
        Nafn: LAGARGANDU
        Einnig þekkt sem konungur hafsins.
    """),
    "FuchsiaCity_Text_OmanyteSign": t("""
        Nafn: KUÐUNGI
        Afar sjaldgæft vasaskrímsli sem var
        endurvakið úr steingervingi.
    """),
    "FuchsiaCity_Text_KabutoSign": t("""
        Nafn: BOTNSETI
        Afar sjaldgæft vasaskrímsli sem var
        endurvakið úr steingervingi.
    """),
    "FuchsiaCity_Text_Ellipsis": t("""
        ...
    """),
    "Text_SubstituteTeach": t("""
        Æ, ég vildi að ég væri KENGÚRILL-barn.

        Ég myndi elska að vera staðgengill
        barnsins...

        Og kúra í magapoka móður
        KENGÚRILLSINS.

        En aðeins vasaskrímsli geta notað
        tæknina STAÐGENGILL...

        Viltu að ég kenni einu af
        vasaskrímslunum þínum STAÐGENGIL?
    """),
    "Text_SubstituteDeclined": t("""
        Ó, í alvöru?
        STAÐGENGILL virðist svo skemmtilegur...
    """),
    "Text_SubstituteWhichMon": t("""
        Hvaða vasaskrímsli vill læra
        STAÐGENGIL?
    """),
    "Text_SubstituteTaught": t("""
        Svei, hvað ég myndi gefa fyrir að
        skríða inn í magapoka KENGÚRILLS...
    """),
    "FuchsiaCity_Text_MyFatherIsGymLeader": t("""
        Faðir minn er SALSTJÓRI þessa bæjar.

        Ég æfi mig líka í að nota
        EITUR-vasaskrímsli eins vel og hann.
    """),
    "FuchsiaCity_Gym_Text_KogaIntro": t("""
        KOGA: Fwahahaha!

        Dirfist venjulegt barn eins og þú að
        skora á mig?

        Bara hugmyndin fær mig til að titra
        af kátínu!

        Jæja þá, ég skal sýna þér sannan
        ótta ninjameistara.

        Eitur færir hægan dauðadóm.
        Svefn gerir óvini varnarlausa.

        Óttastu læðandi hrylling
        EITUR-vasaskrímsla!{PLAY_BGM}{MUS_ENCOUNTER_GYM_LEADER}
    """),
    "FuchsiaCity_Gym_Text_KogaDefeat": t("""
        Humph!
        Þú hefur sannað gildi þitt!

        Hér!
        Taktu SÁLMERKIÐ!
    """),
    "FuchsiaCity_Gym_Text_KogaPostBattle": t("""
        Þegar vasaskrímsli þjáist af EITRUN
        þjáist það meira og meira.

        Skaðinn versnar eftir því sem bardaginn
        dregst á langinn!

        Þetta mun hræða óvini!
    """),
    "FuchsiaCity_Gym_Text_KogaExplainSoulBadge": t("""
        Nú þegar þú ert með SÁLMERKIÐ hækkar
        VÖRN vasaskrímslanna þinna.

        Það leyfir þér líka að nota BRIM utan
        bardaga.

        Ah!
        Taktu þetta líka!
    """),
    "FuchsiaCity_Gym_Text_ReceivedTM06FromKoga": t("""
        {PLAYER} fékk TM06 frá KOGA.
    """),
    "FuchsiaCity_Gym_Text_KogaExplainTM06": t("""
        Inni í þessu TM06 er EITRUN innsigluð!

        Þetta er leynitækni frá því fyrir um
        fjögur hundruð árum.
    """),
    "FuchsiaCity_Gym_Text_MakeSpaceForThis": t("""
        Búðu til pláss fyrir þetta, barn!
    """),
    "FuchsiaCity_Gym_Text_KaydenIntro": t("""
        Styrkur er ekki lykillinn hjá
        vasaskrímslum.
        Skilurðu það?

        Vasaskrímsli snúast um kænsku!

        Ég skal sýna þér hvernig kænska
        sigrar hráan kraft.
    """),
    "FuchsiaCity_Gym_Text_KaydenDefeat": t("""
        Hvað?
        Ótrúlegt!
    """),
    "FuchsiaCity_Gym_Text_KaydenPostBattle": t("""
        Svo þú blandar vöðvum og viti?
        Góð kænska!

        Það er merkilegt fyrir barn sem er
        ÞJÁLFARI.
    """),
    "FuchsiaCity_Gym_Text_KirkIntro": t("""
        Ég var einu sinni töframaður.

        En mig dreymdi um að verða ninja, svo
        ég gekk í þennan SAL.
    """),
    "FuchsiaCity_Gym_Text_KirkDefeat": t("""
        Ég er búinn!
    """),
    "FuchsiaCity_Gym_Text_KirkPostBattle": t("""
        Þótt ég hafi tapað held ég áfram að
        æfa eftir kenningum KOGA,
        ninjameistara míns.
    """),
    "FuchsiaCity_Gym_Text_NateIntro": t("""
        Sjáum hvort þú sigrar sértæknina mína!
    """),
    "FuchsiaCity_Gym_Text_NateDefeat": t("""
        Þú gabbaðir mig!
    """),
    "FuchsiaCity_Gym_Text_NatePostBattle": t("""
        Mér líkar við eitur- og svefntækni,
        því þær vara eftir bardaga!
    """),
    "FuchsiaCity_Gym_Text_PhilIntro": t("""
        Stoppaðu þar!

        Hafa frægu ósýnilegu veggirnir í
        FUCHSIA SAL pirrað þig?
    """),
    "FuchsiaCity_Gym_Text_PhilDefeat": t("""
        Vá!
        Þú náðir þessu!
    """),
    "FuchsiaCity_Gym_Text_PhilPostBattle": t("""
        Þú heillaðir mig!
        Hér er vísbending!

        Horfðu mjög vel eftir bilum í
        ósýnilegu veggjunum!
    """),
    "FuchsiaCity_Gym_Text_EdgarIntro": t("""
        Ég læri líka leið ninjans hjá meistara
        KOGA!

        Ninjar eiga langa sögu í að nota dýr!
    """),
    "FuchsiaCity_Gym_Text_EdgarDefeat": t("""
        Awoo!
    """),
    "FuchsiaCity_Gym_Text_EdgarPostBattle": t("""
        Ég á enn mikið ólært.
    """),
    "FuchsiaCity_Gym_Text_ShawnIntro": t("""
        Meistari KOGA kemur úr langri ætt
        ninja.

        Hvaðan kemur þú?
    """),
    "FuchsiaCity_Gym_Text_ShawnDefeat": t("""
        Þú ert færari en ég hélt!
    """),
    "FuchsiaCity_Gym_Text_ShawnPostBattle": t("""
        Þar sem ljós er, þar er skuggi!

        Ljós og skuggi!
        Hvort velur þú?
    """),
    "FuchsiaCity_Gym_Text_GymGuyAdvice": t("""
        Jæja! Verðandi meistari!

        FUCHSIA SALUR er hrekkjafullur staður.
        Hann er fullur af ósýnilegum veggjum!

        KOGA virðist nálægt, en hann er
        lokaður af.

        Þú verður að finna bil í veggjunum til
        að komast til hans.
    """),
    "FuchsiaCity_Gym_Text_GymGuyPostVictory": t("""
        Það er magnað að ninjar skuli enn geta
        vakið ótta!
    """),
    "FuchsiaCity_Gym_Text_GymStatue": t("""
        FUCHSIA VASASKRÍMSLA-SALUR
        SALSTJÓRI: KOGA

        SIGRANDI ÞJÁLFARAR: {RIVAL}
    """),
    "FuchsiaCity_Gym_Text_GymStatuePlayerWon": t("""
        FUCHSIA VASASKRÍMSLA-SALUR
        SALSTJÓRI: KOGA

        SIGRANDI ÞJÁLFARAR: {RIVAL}, {PLAYER}
    """),
    "FuchsiaCity_House1_Text_WardenIsOldHasFalseTeeth": t("""
        VÖRÐUR SAFARI ZONE er gamall, en hann
        er enn mjög virkur.

        Allar tennurnar hans eru þó
        gervitennur.
    """),
    "FuchsiaCity_House1_Text_BillIsMyGrandson": t("""
        Hmm?
        Hefurðu hitt BILL?

        Hann er barnabarnið mitt!

        Honum fannst alltaf gaman að safna
        hlutum, jafnvel sem barn!
    """),
    "FuchsiaCity_House1_Text_BillFilesHisOwnMonData": t("""
        BILL skráir sín eigin vasaskrímslagögn
        á tölvunni sinni.

        Sýndi hann þér það?
    """),
    "FuchsiaCity_House2_Text_DoYouLikeToFish": t("""
        Ég er eldri bróðir VEIÐISPEKINGSINS.

        Ég eeeelska einfaldlega veiði!
        Ég þoli ekki að vera án hennar.

        Segðu mér, finnst þér gaman að veiða?
    """),
    "FuchsiaCity_House2_Text_LikeYourStyleTakeThis": t("""
        Stórkostlegt! Mér líkar stíllinn þinn.
        Ég held að við getum orðið vinir.

        Taktu þetta og veiddu, ungi vinur!
    """),
    "FuchsiaCity_House2_Text_ReceivedGoodRod": t("""
        {PLAYER} fékk GÓÐA STÖNG frá bróður
        VEIÐISPEKINGSINS.
    """),
    "FuchsiaCity_House2_Text_GoodRodCanCatchBetterMons": t("""
        Veiði er lífsmáti!
        Hún er eins og fínasti skáldskapur.

        Lúin GÖMUL STÖNG gat bara veitt
        GREYSLEPPU, ekki satt?

        En með GÓÐRI STÖNG geturðu veitt
        miklu betri vasaskrímsli.
    """),
    "FuchsiaCity_House2_Text_OhThatsDisappointing": t("""
        Ó...
        Það veldur svo miklum vonbrigðum...
    """),
    "FuchsiaCity_House2_Text_HowAreTheFishBiting": t("""
        Halló þarna, {PLAYER}!

        Hvernig bíta fiskarnir?
    """),
    "FuchsiaCity_House2_Text_YouHaveNoRoomForGift": t("""
        Ó, nei!

        Ég var með gjöf handa þér, en þú
        hefur ekkert pláss fyrir hana!
    """),
    "FuchsiaCity_House3_Text_WouldYouLikeToForgetMove": t("""
        Uh...
        Ó, já, ég er HREYFINGAEYÐIRINN.

        Ég get látið vasaskrímsli gleyma
        hreyfingum sínum.

        Viltu að ég geri það?
    """),
    "FuchsiaCity_House3_Text_WhichMonShouldForgetMove": t("""
        Hvaða vasaskrímsli á að gleyma
        hreyfingu?
    """),
    "FuchsiaCity_House3_Text_WhichMoveShouldBeForgotten": t("""
        Hvaða hreyfingu á að gleyma?
    """),
    "FuchsiaCity_House3_Text_MonOnlyKnowsOneMove": t("""
        {STR_VAR_1} virðist aðeins kunna eina
        hreyfingu...
    """),
    "FuchsiaCity_House3_Text_MonsMoveShouldBeForgotten": t("""
        Hm! {STR_VAR_2} hjá {STR_VAR_1}?
        Á að gleyma þeirri hreyfingu?
    """),
    "FuchsiaCity_House3_Text_MonHasForgottenMoveCompletely": t("""
        Það heppnaðist fullkomlega!

        {STR_VAR_1} hefur alveg gleymt
        {STR_VAR_2}.
    """),
    "FuchsiaCity_House3_Text_ComeAgainToForgetOtherMoves": t("""
        Komdu aftur ef það eru aðrar
        hreyfingar sem þarf að gleyma.
    """),
    "FuchsiaCity_House3_Text_NoEggShouldKnowMoves": t("""
        Hvað?
        Ekkert EGG ætti að kunna neinar
        hreyfingar.
    """),
    "FuchsiaCity_Mart_Text_DontTheyHaveSafariZonePennants": t("""
        Eiga þeir enga fána til að auglýsa
        SAFARI ZONE?

        Hvað með pappírsluktir?
        Eru ekki einu sinni til dagatöl?
    """),
    "FuchsiaCity_Mart_Text_DidYouTryXSpeed": t("""
        Prófaðirðu X SPEED?
        Það hraðar vasaskrímsli í bardaga.
    """),
    "FuchsiaCity_PokemonCenter_1F_Text_CantBecomeGoodTrainerWithOneMon": t("""
        Þú verður ekki góður ÞJÁLFARI með
        aðeins eitt sterkt vasaskrímsli.

        En það er heldur ekki auðvelt að ala
        mörg vasaskrímsli jafnt upp.
    """),
    "FuchsiaCity_PokemonCenter_1F_Text_PokemonLeagueWestOfViridian": t("""
        Það er mjór stígur vestan við
        VIRIDIAN BORG.

        Hann liggur að höfuðstöðvum
        VASASKRÍMSLADEILDARINNAR.
        Hún stjórnar öllum ÞJÁLFURUM.
    """),
    "FuchsiaCity_PokemonCenter_1F_Text_VisitSafariZoneForPokedex": t("""
        Ef þú ert að vinna í VasaDEX skaltu
        heimsækja SAFARI ZONE.

        Þar fjölga sér alls konar sjaldgæf
        vasaskrímsli.
    """),
    "FuchsiaCity_SafariZone_Entrance_Text_WelcomeToSafariZone": t("""
        Velkomin í SAFARI ZONE!
    """),
    "FuchsiaCity_SafariZone_Entrance_Text_PlaySafariGameFor500": t("""
        Fyrir aðeins ¥500 geturðu spilað
        SAFARI-LEIKINN.

        Þú getur farið um opna safarið og
        náð því sem þú vilt.

        Viltu spila?
    """),
    "FuchsiaCity_SafariZone_Entrance_Text_ThatllBe500WeOnlyUseSpecialBalls": t("""
        Það verða ¥500, takk!

        Hér notum við aðeins sérstaka gerð af
        VASA BOLTUM.
    """),
    "FuchsiaCity_SafariZone_Entrance_Text_PlayerReceived30SafariBalls": t("""
        {PLAYER} fékk 30 SAFARIBOLTA frá
        afgreiðslumanninum.
    """),
    "FuchsiaCity_SafariZone_Entrance_Text_CallYouOnPAWhenYouRunOut": t("""
        Við köllum í kallkerfið þegar tíminn
        eða SAFARIBOLTARNIR klárast.

        Jæja, ég óska þér góðs gengis!
    """),
    "FuchsiaCity_SafariZone_Entrance_Text_OkayPleaseComeAgain": t("""
        Allt í lagi.
        Komdu endilega aftur!
    """),
    "FuchsiaCity_SafariZone_Entrance_Text_OopsNotEnoughMoney": t("""
        Úps!
        Ekki nægir peningar!
    """),
    "FuchsiaCity_SafariZone_Entrance_Text_GoingToLeaveSafariZoneEarly": t("""
        Ætlarðu að yfirgefa SAFARI ZONE
        snemma?
    """),
    "FuchsiaCity_SafariZone_Entrance_Text_PleaseReturnSafariBalls": t("""
        Skilaðu öllum SAFARIBOLTUM sem þú
        gætir átt eftir.
    """),
    "FuchsiaCity_SafariZone_Entrance_Text_GoodLuck": t("""
        Gangi þér vel!
    """),
    "FuchsiaCity_SafariZone_Entrance_Text_CatchFairShareComeAgain": t("""
        Náðirðu þínum skerfi?
        Komdu aftur!
    """),
    "FuchsiaCity_SafariZone_Entrance_Text_FirstTimeAtSafariZone": t("""
        Hæ! Er þetta í fyrsta sinn sem þú
        kemur í SAFARI ZONE?
    """),
    "FuchsiaCity_SafariZone_Entrance_Text_ExplainSafariZone": t("""
        SAFARI ZONE hefur í raun fjögur svæði.

        Á hverju svæði eru ólíkar tegundir
        vasaskrímsla, jafnvel sjaldgæfar.

        Notaðu SAFARIBOLTANA sem þú færð til
        að ná þeim.

        Þú getur líka kastað BEITU eða STEINUM
        auk SAFARIBOLTANNA.

        Ef þú kastar BEITU verður vasaskrímslið
        ólíklegra til að flýja, en erfiðara að
        ná.

        Ef þú kastar STEINUM verður það
        líklegra til að flýja, en auðveldara
        að ná.

        Þegar tíminn eða SAFARIBOLTARNIR
        klárast er leiknum lokið hjá þér!
    """),
    "FuchsiaCity_SafariZone_Entrance_Text_SorryYoureARegularHere": t("""
        Fyrirgefðu, þú ert fastagestur hér!
    """),
    "FuchsiaCity_SafariZone_Office_Text_NicknamedWardenSlowpoke": t("""
        Við gáfum VERÐINUM gælunafnið
        "SLJÓN."

        Þú veist, hann er með tóma svipinn
        eins og SLJÓN.
    """),
    "FuchsiaCity_SafariZone_Office_Text_WardenIsVeryKnowledgeable": t("""
        VÖRÐUR SLJÓN veit mjög mikið um
        vasaskrímsli.

        Hann á meira að segja nokkra steingervinga
        af sjaldgæfum, útdauðum vasaskrímslum.
    """),
    "FuchsiaCity_SafariZone_Office_Text_CouldntUnderstandWarden": t("""
        VÖRÐUR SLJÓN kom inn, en ég skildi
        hann ekki.

        Ég held að hann eigi í talvandræðum!
    """),
    "FuchsiaCity_SafariZone_Office_Text_PrizeInSafariZone": t("""
        VÖRÐUR SLJÓN stendur fyrir kynningarherferð
        núna.

        Reyndu að komast í fjarlægasta hornið
        á SAFARI ZONE.

        Ef þér tekst það vinnurðu mjög
        hentug verðlaun.
    """),
    "FuchsiaCity_WardensHouse_Text_HifFuffHefifoo": t("""
        VÖRÐUR: Hif fuff hefifú!

        Ha lof ha feef í hafahi ho.
        Heff hee fví!
    """),
    "FuchsiaCity_WardensHouse_Text_AhHowheeHoHoo": t("""
        Ah howhee ho hoo!
        Eef ee hafahi ho!
    """),
    "FuchsiaCity_WardensHouse_Text_HeOhayHeHaHoo": t("""
        Ha?
        He ohay heh ha hoo ee haheh!
    """),
    "FuchsiaCity_WardensHouse_Text_GaveGoldTeethToWarden": t("""
        {PLAYER} gaf VERÐINUM GULLTENNURNAR.
    """),
    "FuchsiaCity_WardensHouse_Text_WardenPoppedInHisTeeth": t("""
        VÖRÐURINN smellti tönnunum í sig!
    """),
    "FuchsiaCity_WardensHouse_Text_ThanksSonGiveYouSomething": t("""
        VÖRÐUR: Takk, drengur!
        Þú bjargaðir mér sannarlega!

        Enginn skildi orð sem ég sagði,
        ekki nokkur maður!

        Ég skammaðist mín jafnvel of mikið til
        að sýna mig á SKRIFSTOFUNNI.

        Leyfðu mér að gefa þér eitthvað fyrir
        ómakið.
    """),
    "FuchsiaCity_WardensHouse_Text_ThanksLassieGiveYouSomething": t("""
        VÖRÐUR: Takk, stúlka!
        Þú bjargaðir mér sannarlega!

        Enginn skildi orð sem ég sagði,
        ekki nokkur maður!

        Ég skammaðist mín jafnvel of mikið til
        að sýna mig á SKRIFSTOFUNNI.

        Leyfðu mér að gefa þér eitthvað fyrir
        ómakið.
    """),
    "FuchsiaCity_WardensHouse_Text_ReceivedHM04FromWarden": t("""
        {PLAYER} fékk HM04 frá VERÐINUM.
    """),
    "FuchsiaCity_WardensHouse_Text_ExplainStrength": t("""
        VÖRÐUR: Í HM04 finnurðu STYRK.

        Hann leyfir vasaskrímslum að færa
        stórgrýti þegar þú ert utan bardaga.

        Ó já, fannstu LEYNIHÚSIÐ í SAFARI
        ZONE?
    """),
    "FuchsiaCity_WardensHouse_Text_YouHaveTooMuchStuff": t("""
        Þú ert með of mikið dót!
    """),
    "FuchsiaCity_WardensHouse_Text_MonPhotosFossilsOnDisplay": t("""
        Myndir af vasaskrímslum og steingervingar
        eru til sýnis.
    """),
    "FuchsiaCity_WardensHouse_Text_OldMonMerchandiseOnDisplay": t("""
        Gamall vasaskrímslavarningur er til
        sýnis.
    """),
    "SafariZone_Center_Text_RestHouse": t("""
        HVÍLDARHÚS
    """),
    "SafariZone_Center_Text_PressStartToCheckTime": t("""
        ÞJÁLFARA-RÁÐ

        Ýttu á START til að athuga tímann sem
        er eftir.
    """),
    "SafariZone_Center_Text_CenterArea": t("""
        MIÐSVÆÐI
    """),
    "SafariZone_Center_Text_WhereDidErikGo": t("""
        SARA: Hvert fór kærastinn minn,
        ERIK?
    """),
    "SafariZone_Center_Text_CatchingMonsAsGifts": t("""
        Ég er að ná vasaskrímslum til að fara
        með heim sem gjafir.
    """),
    "SafariZone_East_Text_RestHouse": t("""
        HVÍLDARHÚS
    """),
    "SafariZone_East_Text_TimeDeclinesOnlyWhileYouWalk": t("""
        ÞJÁLFARA-RÁÐ

        Tíminn sem er eftir minnkar aðeins
        þegar þú gengur.
    """),
    "SafariZone_East_Text_AreaSign": t("""
        SVÆÐI 1
        VESTUR: MIÐSVÆÐI
    """),
    "SafariZone_East_Text_HowManyDidYouCatch": t("""
        Hversu mörg náðirðu?
        Ég er örmagna eftir átakið!
    """),
    "SafariZone_East_Text_CaughtChanseyAllWorthwhile": t("""
        Ég náði SÆLEGGI!

        Það gerir þetta allt þess virði.
    """),
    "SafariZone_East_Text_TiredFromAllTheFun": t("""
        Úff!
        Ég er þreyttur eftir alla skemmtunina!
    """),
    "SafariZone_North_Text_RestHouse": t("""
        HVÍLDARHÚS
    """),
    "SafariZone_North_Text_SecretHouseStillAhead": t("""
        ÞJÁLFARA-RÁÐ

        LEYNIHÚSIÐ er enn framundan.
    """),
    "SafariZone_North_Text_Area2": t("""
        SVÆÐI 2
    """),
    "SafariZone_North_Text_ZigzagThroughTallGrass": t("""
        ÞJÁLFARA-RÁÐ

        Vasaskrímsli fela sig í háu grasi.

        Farðu í sikksakk í gegnum grasið til
        að fæla þau fram.
    """),
    "SafariZone_North_Text_WinFreeHMFindSecretHouse": t("""
        ÞJÁLFARA-RÁÐ

        Vinndu ókeypis HM með því að finna
        LEYNIHÚSIÐ.
    """),
    "SafariZone_East_Text_KeepAnyItemFoundOnSafari": t("""
        Þú mátt halda öllum hlutum sem þú
        finnur í SAFARI ZONE.

        En tíminn rennur út ef þú reynir að
        ná þeim öllum í einu.
    """),
    "SafariZone_East_Text_PrizeInDeepestPartOfSafariZone": t("""
        Farðu í dýpsta hluta SAFARI ZONE.
        Þú vinnur verðlaun!
    """),
    "SafariZone_East_Text_MyEeveeEvolvedIntoFlareon": t("""
        SNIÐDÝRIÐ mitt þróaðist í GLÓÐBÚA.

        En SNIÐDÝR vinar míns varð að
        MARBÚA. Ég velti fyrir mér hvers vegna.
    """),
    "SafariZone_SecretHouse_Text_CongratsYouveWon": t("""
        Ah! Loksins!

        Þú ert fyrsta manneskjan sem kemst í
        LEYNIHÚSIÐ!

        Þótt ég hafi sett af stað herferð fyrir
        glæsilega opnun okkar,

        var ég farinn að hafa áhyggjur af því
        að enginn myndi vinna verðlaunin.

        Til hamingju!
        Þú hefur unnið!
    """),
    "SafariZone_SecretHouse_Text_ReceivedHM03FromAttendant": t("""
        {PLAYER} fékk HM03 frá
        afgreiðslumanninum!
    """),
    "SafariZone_SecretHouse_Text_ExplainSurf": t("""
        HM03 er BRIM.

        Vasaskrímsli geta flutt þig yfir vatn
        með því.

        Og þetta HM er ekki einnota, svo þú
        getur notað það aftur og aftur.

        Þú ert ofurheppinn að vinna þessi
        frábæru verðlaun!
    """),
    "SafariZone_SecretHouse_Text_DontHaveRoomForPrize": t("""
        Þú hefur ekki pláss fyrir þessi
        frábæru verðlaun!
    """),
    "SafariZone_West_Text_RestHouse": t("""
        HVÍLDARHÚS
    """),
    "SafariZone_West_Text_PleaseFindWardensLostTeeth": t("""
        TILKYNNING UM BEIÐNI

        Finnið týndar GULLTENNUR
        SAFARI-VARÐARINS.
        Þær eru einhvers staðar hér.

        Verðlaun í boði!
        Hafið samband: VÖRÐUR
    """),
    "SafariZone_West_Text_SearchForSecretHouse": t("""
        ÞJÁLFARA-RÁÐ

        Svæðiskönnunarherferð!
        Leitin að LEYNIHÚSINU!
    """),
    "SafariZone_West_Text_AreaSign": t("""
        SVÆÐI 3
        AUSTUR: MIÐSVÆÐI
    """),
    "SafariZone_West_Text_KogaPatrolsSafariEverySoOften": t("""
        SAFARI ZONE er risastór, finnst þér
        ekki?

        SALSTJÓRI FUCHSIA, KOGA, fer öðru
        hvoru um svæðið á eftirliti.

        Honum að þakka getum við leikið hér
        vitandi að við erum örugg.
    """),
    "SafariZone_West_Text_RocksMakeMonRunButEasierCatch": t("""
        Að kasta STEINUM í vasaskrímsli gæti
        látið þau flýja, en þau verða
        auðveldari að ná.
    """),
    "SafariZone_West_Text_BaitMakesMonStickAround": t("""
        BEITA gerir líklegra að vasaskrímsli
        haldi sig nálægt ef þau byrja að éta.
    """),
    "SafariZone_West_Text_HikedLotsDidntSeeMonIWanted": t("""
        Ég gekk mikið, en sá engin vasaskrímsli
        sem mig langaði í.
    """),
}


FILES = {
    "data/maps/FuchsiaCity/text.inc",
    "data/maps/FuchsiaCity_Gym/text.inc",
    "data/maps/FuchsiaCity_House1/text.inc",
    "data/maps/FuchsiaCity_House2/text.inc",
    "data/maps/FuchsiaCity_House3/text.inc",
    "data/maps/FuchsiaCity_Mart/text.inc",
    "data/maps/FuchsiaCity_PokemonCenter_1F/text.inc",
    "data/maps/FuchsiaCity_SafariZone_Entrance/text.inc",
    "data/maps/FuchsiaCity_SafariZone_Office/text.inc",
    "data/maps/FuchsiaCity_WardensHouse/text.inc",
    "data/maps/SafariZone_Center/text.inc",
    "data/maps/SafariZone_Center_RestHouse/text.inc",
    "data/maps/SafariZone_East/text.inc",
    "data/maps/SafariZone_East_RestHouse/text.inc",
    "data/maps/SafariZone_North/text.inc",
    "data/maps/SafariZone_North_RestHouse/text.inc",
    "data/maps/SafariZone_SecretHouse/text.inc",
    "data/maps/SafariZone_West/text.inc",
    "data/maps/SafariZone_West_RestHouse/text.inc",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-after-v14.csv")
    parser.add_argument("--output", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-fuchsia-safari-v1.csv")
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
        row["notes"] = "codex curated Fuchsia City and Safari Zone v1"
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
