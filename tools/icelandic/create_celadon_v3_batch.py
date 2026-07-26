from __future__ import annotations

import argparse
import csv
import textwrap
from pathlib import Path

from common import repo_root


def t(value: str) -> str:
    return textwrap.dedent(value).strip()


TRANSLATIONS = {
    "CeladonCity_Text_KeepOutOfTeamRocketsWay": t("""
        Haltu þig frá ROCKET-GENGINU!
    """),
    "CeladonCity_Text_ExplainXAccuracyDireHit": t("""
        ÞJÁLFARARÁÐ

        X ACCURACY eykur nákvæmni bragða.

        DIRE HIT hækkar líkurnar á
        rothöggi.

        Kauptu hlutina þína í
        CELADON-STÓRVERSLUN!
    """),
    "CeladonCity_Text_CitySign": t("""
        CELADON BORG
        Borg regnbogadrauma
    """),
    "CeladonCity_Text_GymSign": t("""
        CELADON BORGAR
        VASASKRÍMSLA-LIÐSMEISTARASALUR

        SALSTJÓRI: ERIKA
        Prinsessan sem elskar náttúruna!
    """),
    "CeladonCity_Text_GuardSpecProtectsFromStatus": t("""
        ÞJÁLFARARÁÐ

        GUARD SPEC. verndar vasaskrímsli
        gegn brögðum sem lækka stöður í
        bardaga.

        Kauptu hlutina þína í
        CELADON-STÓRVERSLUN!
    """),
    "CeladonCity_Text_GameCornerSign": t("""
        ROCKET-SPILASALUR
        Leikvöllur fullorðna fólksins!
    """),
    "Text_SoftboiledTeach": t("""
        Hæ þarna!

        Ég hef séð þig á ferli en aldrei
        fengið tækifæri til að spjalla.

        Það hlýtur að vera heppnin sem
        loksins leiddi okkur saman.

        Ég vil fagna því með því að kenna
        þér bragðið MJÚKSOÐIÐ.
    """),
    "Text_SoftboiledWhichMon": t("""
        Jæja, hvaða vasaskrímsli á að fá
        tækifæri til að læra MJÚKSOÐIÐ?
    """),
    "CeladonCity_Text_SomeoneStoleSilphScope": t("""
        Ó, hvað á ég að gera...

        Einhver stal SILPH SCOPE okkar.

        Þjófurinn hljóp þessa leið, ég er
        viss um það.

        En ég missti sjónar á honum!
        Hvert fór hann?
    """),
    "CeladonCity_Condominiums_2F_Text_GameFreakMeetingRoom": t("""
        GAME FREAK
        Fundarherbergi
    """),
    "CeladonCity_Condominiums_3F_Text_GameFreakDevelopmentRoom": t("""
        GAME FREAK
        Þróunarherbergi
    """),
    "CeladonCity_Condominiums_RoofRoom_Text_BoxIsFull": t("""
        Það er fullt af vasaskrímslum.
        Skiptu um BOX og komdu aftur.
    """),
    "CeladonCity_Condominiums_RoofRoom_Text_TheresNothingIDontKnow": t("""
        Það er ekkert sem ég veit ekki,
        alveg eins og ég skrifaði á töfluna.

        Ég veit allt um heim vasaskrímsla í
        GAME BOY ADVANCE tækinu þínu!

        Hittu vini þína og njóttu þess að
        skiptast á vasaskrímslum!
    """),
    "CeladonCity_Condominiums_RoofRoom_Text_PamphletOnTMs": t("""
        Þetta er bæklingur um TM-brögð.

        ... ...

        Alls eru fimmtíu TM-brögð.

        Það eru líka sjö HM-brögð sem má
        nota aftur og aftur.

        SILPH CO.
    """),
    "CeladonCity_DepartmentStore_1F_Text_WelcomeToDeptStore": t("""
        Halló!
        Velkomin í CELADON-STÓRVERSLUN.

        Taflan til hægri sýnir skipulag
        verslunarinnar.
    """),
    "CeladonCity_DepartmentStore_1F_Text_FloorDescriptions": t("""
        1F: ÞJÓNUSTUBORÐ

        2F: ÞJÁLFARAMARKAÐUR

        3F: TÖLVULEIKJABÚÐ

        4F: GJAFIR FRÁ VITRINGUM

        5F: LYFJABÚÐ

        ÞAKSVÆÐI: SJÁLFSALAR
    """),
    "CeladonCity_DepartmentStore_1F_Text_ServiceCounter": t("""
        1F: ÞJÓNUSTUBORÐ
    """),
    "CeladonCity_DepartmentStore_2F_Text_BuyReviveForLongOutings": t("""
        Fyrir langar ferðir er gott að
        kaupa LÍFGUNARLYF.
    """),
    "CeladonCity_DepartmentStore_2F_Text_FloorSign": t("""
        Úrvalsvarningur fyrir ÞJÁLFARA!

        2F: ÞJÁLFARAMARKAÐUR
    """),
    "CeladonCity_DepartmentStore_2F_Text_LanceComesToBuyCapes": t("""
        Við eigum viðskiptavin, LANCE, sem
        kemur stundum.

        Hann kaupir alltaf skikkjur.

        Ég velti fyrir mér... á hann margar
        alveg eins skikkjur heima?
    """),
    "CeladonCity_DepartmentStore_3F_Text_BuddyTradingKangaskhanForHaunter": t("""
        Allt í lagi!

        Félagi minn ætlar að láta mig fá
        KENGÚRILL í skiptum fyrir REIMNI!
    """),
    "CeladonCity_DepartmentStore_3F_Text_ItsSuperNES": t("""
        Þetta er Super NES.
    """),
    "CeladonCity_DepartmentStore_3F_Text_AnRPG": t("""
        RPG-leikur!
        Það er enginn tími fyrir það!
    """),
    "CeladonCity_DepartmentStore_3F_Text_SportsGame": t("""
        Íþróttaleikur!
        Pabbi kann að meta hann!
    """),
    "CeladonCity_DepartmentStore_3F_Text_PuzzleGame": t("""
        Þrautaleikur!
        Hann virðist ávanabindandi!
    """),
    "CeladonCity_DepartmentStore_3F_Text_FightingGame": t("""
        Bardagaleikur!
        Hann virðist erfiður!
    """),
    "CeladonCity_DepartmentStore_3F_Text_TVGameShop": t("""
        3F: TÖLVULEIKJABÚÐ
    """),
    "Text_CounterTeach": t("""
        Ó, hæ!
        Ég kláraði loksins leikinn um
        vasaskrímsli.

        Ertu ekki búinn enn?
        Hvernig væri að ég kenndi þér gott
        bragð?

        Bragðið sem ég hef í huga er
        GAGNÁTAK.

        Ekki afgreiðsluborðið sem ég halla
        mér á, athugaðu það!
    """),
    "Text_CounterDeclined": t("""
        Hefurðu ekki áhuga?
        Komdu aftur ef þú skiptir um
        skoðun.
    """),
    "CeladonCity_DepartmentStore_4F_Text_GettingPokeDollAsPresent": t("""
        Ég er að kaupa gjöf handa
        kærustunni minni.

        Ég held að VASASKRÍMSLA-DÚKKA verði
        fyrir valinu.
        Hún er vinsæl núna.
    """),
    "CeladonCity_DepartmentStore_4F_Text_FloorSign": t("""
        Tjáðu þig með gjöfum!
        4F: GJAFIR FRÁ VITRINGUM

        Sértilboð fyrir þróun!
        ÞRÓUNARSTEINAR á útsölu núna!
    """),
    "CeladonCity_DepartmentStore_5F_Text_Drugstore": t("""
        5F: LYFJABÚÐ
    """),
    "CeladonCity_DepartmentStore_Roof_Text_ImThirstyGiveHerDrink": t("""
        Ég er þyrst!
        Mig langar í eitthvað að drekka!

        {FONT_NORMAL}Gefurðu henni drykk?
    """),
    "CeladonCity_DepartmentStore_Roof_Text_GiveWhichDrink": t("""
        Hvaða drykk viltu gefa henni?
    """),
    "CeladonCity_DepartmentStore_Roof_Text_YayFreshWaterHaveThis": t("""
        Jibbí!

        FERSKT VATN!

        Takk fyrir!
        Þú mátt fá þetta frá mér!
    """),
    "Text_ReceivedItemFromLittleGirl": t("""
        {PLAYER} fékk {STR_VAR_2}
        frá litlu stelpunni.
    """),
    "CeladonCity_DepartmentStore_Roof_Text_ExplainTM16": t("""
        TM16 inniheldur LIGHT SCREEN.

        Bragðið veikir kraft sérárása
        andstæðingsins.
    """),
    "CeladonCity_DepartmentStore_Roof_Text_YaySodaPopHaveThis": t("""
        Jibbí!

        GOSDRYKKUR!

        Takk fyrir!
        Þú mátt fá þetta frá mér!
    """),
    "CeladonCity_DepartmentStore_Roof_Text_YayLemonadeHaveThis": t("""
        Jibbí!

        SÍTRÓNULAÐI!

        Takk fyrir!
        Þú mátt fá þetta frá mér!
    """),
    "CeladonCity_DepartmentStore_Roof_Text_ExplainTM33": t("""
        TM33 inniheldur REFLECT.

        Bragðið veikir kraft líkamlegra
        árása andstæðingsins.
    """),
    "CeladonCity_DepartmentStore_Roof_Text_DontHaveSpaceForThis": t("""
        Þú hefur ekki pláss fyrir þetta!
    """),
    "CeladonCity_DepartmentStore_Roof_Text_ImNotThirstyAfterAll": t("""
        Nei, takk!
        Ég er víst ekki þyrst lengur!
    """),
    "CeladonCity_DepartmentStore_Roof_Text_MySisterIsImmature": t("""
        Systir mín er ÞJÁLFARI, hvort sem
        þú trúir því eða ekki.

        En hún er svo óþroskuð að hún gerir
        mig alveg vitlausa!
    """),
    "CeladonCity_DepartmentStore_Roof_Text_ImThirstyIWantDrink": t("""
        Ég er þyrst!
        Mig langar í eitthvað að drekka!
    """),
    "CeladonCity_DepartmentStore_Roof_Text_FloorSign": t("""
        ÞAKSVÆÐI:
        SJÁLFSALAR
    """),
    "CeladonCity_DepartmentStore_Roof_Text_VendingMachineWhatDoesItHave": t("""
        Sjálfsali!
        Hvað er í honum?
    """),
    "CeladonCity_DepartmentStore_Roof_Text_NotEnoughMoney": t("""
        Æ, ekki nægir peningar!
    """),
    "CeladonCity_DepartmentStore_Roof_Text_DrinkCanPoppedOut": t("""
        Dós af {STR_VAR_1} datt út!
    """),
    "CeladonCity_DepartmentStore_Roof_Text_NoMoreRoomForStuff": t("""
        Það er ekki meira pláss fyrir dót!
    """),
    "CeladonCity_DepartmentStore_Roof_Text_NotThirsty": t("""
        Ekki þyrst!
    """),
    "CeladonCity_GameCorner_Text_CanExchangeCoinsNextDoor": t("""
        Velkomin!

        Þú getur skipt PENINGUM fyrir
        glæsilega vinninga í næsta húsi.
    """),
    "CeladonCity_GameCorner_Text_WelcomeBuySomeCoins": t("""
        Velkomin í ROCKET-SPILASALINN!

        Vantar þig leik-PENINGA?
        Viltu kaupa nokkra?
    """),
    "CeladonCity_GameCorner_Text_ComePlaySometime": t("""
        Nei?
        Komdu endilega að spila seinna!
    """),
    "CeladonCity_GameCorner_Text_SorryDontHaveCoinCase": t("""
        Æ, fyrirgefðu.
        Þú ert ekki með PENINGAVESKI.
    """),
    "CeladonCity_GameCorner_Text_CoinCaseIsFull": t("""
        Úbbs!
        PENINGAVESKIÐ þitt er fullt.
    """),
    "CeladonCity_GameCorner_Text_CantAffordCoins": t("""
        Þú átt ekki fyrir PENINGUNUM.
    """),
    "CeladonCity_GameCorner_Text_HereAreYourCoins": t("""
        Takk fyrir.
        Hér eru PENINGARNIR þínir!
    """),
    "CeladonCity_GameCorner_Text_RumoredTeamRocketRunsThisPlace": t("""
        Hafðu þetta lágt.

        Sagt er að ROCKET-GENGIÐ reki
        þennan stað.
    """),
    "CeladonCity_GameCorner_Text_ThinkMachinesHaveDifferentOdds": t("""
        Ég held að vélarnar hafi
        mismunandi vinningslíkur.
    """),
    "CeladonCity_GameCorner_Text_DoYouWantToPlay": t("""
        Heyrðu, krakki, viltu spila?
    """),
    "CeladonCity_GameCorner_Text_Received10CoinsFromMan": t("""
        {PLAYER} fékk 10 PENINGA
        frá manninum.
    """),
    "CeladonCity_GameCorner_Text_DontNeedMyCoins": t("""
        Þú þarft ekki á PENINGUNUM mínum að
        halda!
    """),
    "CeladonCity_GameCorner_Text_WinsComeAndGo": t("""
        Vinningar koma og fara.
        Ekkert er öruggt.
    """),
    "CeladonCity_GameCorner_Text_WinOrLoseItsOnlyLuck": t("""
        Þessir spilakassar...
        Hvort maður vinnur eða tapar er
        bara heppni.
    """),
    "CeladonCity_GameCorner_Text_SoEasyToGetHooked": t("""
        Spil eru varasöm!
        Það er svo auðvelt að ánetjast
        þeim!
    """),
    "CeladonCity_GameCorner_Text_WantSomeCoins": t("""
        Hvað segirðu?
        Viltu PENINGA?
    """),
    "CeladonCity_GameCorner_Text_Received20CoinsFromNiceGuy": t("""
        {PLAYER} fékk 20 PENINGA
        frá vingjarnlega manninum.
    """),
    "CeladonCity_GameCorner_Text_YouHaveLotsOfCoins": t("""
        Þú átt fullt af PENINGUM!
    """),
    "CeladonCity_GameCorner_Text_HereAreSomeCoinsShoo": t("""
        Heyrðu, hvað?
        Þú truflar mig!

        Hér eru nokkrir PENINGAR, hypjaðu
        þig!
    """),
    "CeladonCity_GameCorner_Text_Received20CoinsFromMan": t("""
        {PLAYER} fékk 20 PENINGA
        frá manninum.
    """),
    "CeladonCity_GameCorner_Text_YouveGotPlentyCoins": t("""
        Þú átt nóg af eigin PENINGUM!
    """),
    "CeladonCity_GameCorner_Text_WatchReelsClosely": t("""
        Bragðið er að fylgjast vel með
        hjólunum.
    """),
    "CeladonCity_GameCorner_Text_GruntIntro": t("""
        Ég gæti þessa veggspjalds!
        Farðu burt, annars...
    """),
    "CeladonCity_GameCorner_Text_GruntDefeat": t("""
        Ansans!
    """),
    "CeladonCity_GameCorner_Text_GruntPostBattle": t("""
        Felustaður ROCKET-GENGISINS gæti
        uppgötvast!

        Ég verð að segja FORINGJANUM!
    """),
    "CeladonCity_GameCorner_Text_SwitchBehindPosterPushIt": t("""
        Hey!

        Rofi bak við veggspjaldið!?
        Ýtum á hann!
    """),
    "CeladonCity_GameCorner_Text_CoinCaseIsRequired": t("""
        PENINGAVESKI er nauðsynlegt...
    """),
    "CeladonCity_GameCorner_Text_DontHaveCoinCase": t("""
        Úbbs!
        Ekkert PENINGAVESKI!
    """),
    "CeladonCity_GameCorner_Text_SlotMachineWantToPlay": t("""
        Spilakassi!
        Viltu spila?
    """),
    "CeladonCity_GameCorner_Text_OutOfOrder": t("""
        BILAÐ
        Þessi er bilaður.
    """),
    "CeladonCity_GameCorner_Text_OutToLunch": t("""
        Í MATARHLÉI
        Þessi er frátekinn.
    """),
    "CeladonCity_GameCorner_Text_SomeonesKeys": t("""
        Lyklar einhvers!
        Eigandinn kemur aftur.
    """),
    "CeladonCity_GameCorner_PrizeRoom_Text_RakedItInToday": t("""
        Gahaha!
        Ég rakaði inn vinninga í dag!
        Ef bara hver dagur væri svona...
    """),
    "CeladonCity_GameCorner_PrizeRoom_Text_CoinCaseRequired": t("""
        PENINGAVESKI er nauðsynlegt...
    """),
    "CeladonCity_GameCorner_PrizeRoom_Text_WeExchangeCoinsForPrizes": t("""
        Við skiptum PENINGUM fyrir vinninga.
    """),
    "CeladonCity_GameCorner_PrizeRoom_Text_WhichPrize": t("""
        Hvaða vinning viltu?
    """),
    "CeladonCity_GameCorner_PrizeRoom_Text_HereYouGo": t("""
        Gjörðu svo vel.
    """),
    "CeladonCity_GameCorner_PrizeRoom_Text_YouWantPrize": t("""
        Þannig að þú vilt {STR_VAR_1}?
    """),
    "CeladonCity_GameCorner_PrizeRoom_Text_YouWantTM": t("""
        Allt í lagi, þú vilt TM með
        {STR_VAR_2}?
    """),
    "CeladonCity_GameCorner_PrizeRoom_Text_NeedMoreCoins": t("""
        Því miður, þú þarft fleiri PENINGA
        en það.
    """),
    "CeladonCity_GameCorner_PrizeRoom_Text_OopsNotEnoughRoom": t("""
        Þú getur ekki borið meira, vinur.
    """),
    "CeladonCity_GameCorner_PrizeRoom_Text_OhFineThen": t("""
        Jæja, þá það.
    """),
    "CeladonCity_Gym_Text_ErikaDefeat": t("""
        Ó!
        Ég játa mig sigraða.
        Styrkur þinn er aðdáunarverður.

        Ég verð að veita þér RAINBOWBADGE.
    """),
    "CeladonCity_Gym_Text_ReceivedTM19FromErika": t("""
        {PLAYER} fékk TM19
        frá ERIKA.
    """),
    "CeladonCity_Gym_Text_ExplainTM19": t("""
        TM19 inniheldur GIGA DRAIN.

        Helmingur skaðans sem það veldur
        rennur til baka og læknar
        vasaskrímslið þitt.

        Værirðu ekki sammála því að þetta
        sé dásamlegt bragð?
    """),
    "CeladonCity_Gym_Text_ShouldMakeRoomForThis": t("""
        Þú þarft að búa til pláss fyrir
        þetta.
    """),
    "CeladonCity_Gym_Text_KayIntro": t("""
        Ég ætti að segja þér frá þessum
        LIÐSMEISTARASAL.

        Aðeins sannar dömur mega vera hér
        inni!
    """),
    "CeladonCity_Gym_Text_KayDefeat": t("""
        Þetta var of harkalegt!
    """),
    "CeladonCity_Gym_Text_KayPostBattle": t("""
        Bleee!
        Ég vona að ERIKA rústi þér!
    """),
    "CeladonCity_Gym_Text_BridgetIntro": t("""
        Ó, þú komst.
        Mér var farið að leiðast.
    """),
    "CeladonCity_Gym_Text_BridgetDefeat": t("""
        Förðunin mín!
    """),
    "CeladonCity_Gym_Text_BridgetPostBattle": t("""
        GRAS-gerðar vasaskrímsli standa vel
        gegn VATNS-gerðinni.

        Þau hafa líka yfirhöndina gagnvart
        STEIN- og JARÐAR-gerðar
        vasaskrímslum.
    """),
    "CeladonCity_Gym_Text_TinaIntro": t("""
        ...Varstu ekki að gægjast hér inn
        áðan?
    """),
    "CeladonCity_Gym_Text_TinaDefeat": t("""
        Þú kemur á óvart!
    """),
    "CeladonCity_Gym_Text_TinaPostBattle": t("""
        Ó, þú varst að horfa á ERIKU...
        Þú varst ekki að horfa á mig...
    """),
    "CeladonCity_Gym_Text_TamiaIntro": t("""
        Sjáðu, sjáðu!
        Sjáðu vasaskrímslin mín!

        Mér líkar við GRAS-gerðina.
        Mér finnst þau auðveld í uppeldi.
    """),
    "CeladonCity_Gym_Text_TamiaDefeat": t("""
        Nei!
    """),
    "CeladonCity_Gym_Text_TamiaPostBattle": t("""
        Við notum aðeins GRAS-gerðar
        vasaskrímsli í salnum okkar.

        Af hverju?
        Við notum þau líka í
        blómaskreytingar!
    """),
    "CeladonCity_Gym_Text_LisaIntro": t("""
        Ó, hæ!

        Okkur líkar ekki við BUG- eða
        ELDS-gerðar vasaskrímsli hér inni!
    """),
    "CeladonCity_Gym_Text_LisaDefeat": t("""
        Ó!
        Þú!
    """),
    "CeladonCity_Gym_Text_LisaPostBattle": t("""
        SALSTJÓRINN okkar, ERIKA, er
        kannski hljóðlát, en hún er fræg
        hér um slóðir.
    """),
    "CeladonCity_Gym_Text_LoriIntro": t("""
        Gaman að kynnast þér.
        Áhugamálið mitt er
        vasaskrímslaþjálfun.
    """),
    "CeladonCity_Gym_Text_LoriDefeat": t("""
        Ó!
        Glæsilegt!
    """),
    "CeladonCity_Gym_Text_LoriPostBattle": t("""
        Ég á stefnumót í blindni á næstunni.
        Ég þarf að læra að vera kurteis,
        sérstaklega ef ég þarf að berjast.
    """),
    "CeladonCity_Gym_Text_MaryIntro": t("""
        Velkomin í CELADON-SALINN!

        Þú skalt ekki vanmeta þessar
        indælu dömur.
    """),
    "CeladonCity_Gym_Text_MaryDefeat": t("""
        Ó!
        Sigruð!
    """),
    "CeladonCity_Gym_Text_MaryPostBattle": t("""
        Ég tók ekki bestu vasaskrímslin mín
        með.
        Bíddu bara þangað til næst!
    """),
    "CeladonCity_Gym_Text_GymStatue": t("""
        CELADON VASASKRÍMSLA-SALUR
        SALSTJÓRI: ERIKA

        SIGURSÆLIR ÞJÁLFARAR:
        {RIVAL}
    """),
    "CeladonCity_Gym_Text_GymStatuePlayerWon": t("""
        CELADON VASASKRÍMSLA-SALUR
        SALSTJÓRI: ERIKA

        SIGURSÆLIR ÞJÁLFARAR:
        {RIVAL}, {PLAYER}
    """),
    "CeladonCity_Hotel_Text_ThisHotelIsForPeople": t("""
        Vasaskrímsli?
        Nei, þetta er hótel fyrir fólk.

        Því miður er allt uppbókað.
    """),
    "CeladonCity_Hotel_Text_OnVacationWithBrotherAndBoyfriend": t("""
        Ég er í fríi með bróður mínum og
        kærastanum.

        CELADON er svo falleg borg!
    """),
    "CeladonCity_Hotel_Text_WhyDidSheBringBrother": t("""
        Af hverju?
        Af hverju tók hún bróður sinn með?
    """),
    "CeladonCity_Hotel_Text_SisBroughtMeOnVacation": t("""
        Jibbí!
        Ég er í fríi!

        Systir mín tók mig með!
        Geggjað!
    """),
    "CeladonCity_House1_Text_SlotsReelInTheDough": t("""
        Hehehe!

        Spilakassarnir moka inn peningum,
        heldur betur!
    """),
    "CeladonCity_House1_Text_ShippedMonsAsSlotPrizes": t("""
        FORINGI!

        Við sendum aftur tvö þúsund
        vasaskrímsli í vinninga fyrir
        spilakassana í dag!
    """),
    "CeladonCity_House1_Text_DontTouchGameCornerPoster": t("""
        Ekki snerta veggspjaldið í
        SPILASALNUM!

        Það er enginn leynirofi bak við
        það!
    """),
    "Text_ItsABuddhistAltar": t("""
        Þetta er búddískt altari...
    """),
    "CeladonCity_PokemonCenter_1F_Text_PokeFluteAwakensSleepingMons": t("""
        VASAFLAUTA vekur sofandi
        vasaskrímsli.
        Þú veist það.

        Hún gerir það með hljóði sem aðeins
        þau heyra.
    """),
    "CeladonCity_PokemonCenter_1F_Text_RodeHereFromFuchsia": t("""
        Ég hjólaði hingað frá FUCHSIA.

        CYCLING ROAD liggur upp í móti, svo
        ég er örmagna.
    """),
    "CeladonCity_PokemonCenter_1F_Text_GoToCyclingRoadIfIHadBike": t("""
        Ef ég ætti HJÓL færi ég á
        CYCLING ROAD!
    """),
    "CeladonCity_Restaurant_Text_TakingBreakRightNow": t("""
        Hæ!

        Því miður, við erum í pásu núna.
    """),
    "CeladonCity_Restaurant_Text_OftenGoToDrugstore": t("""
        Vasaskrímslin mín eru veikburða, svo
        ég þarf oft að fara í LYFJABÚÐINA.
    """),
    "CeladonCity_Restaurant_Text_PsstBasementUnderGameCorner": t("""
        Psst!
        Ég heyri að það sé kjallari undir
        SPILASALNUM.
    """),
    "CeladonCity_Restaurant_Text_ManLostItAllAtSlots": t("""
        Namm...

        Maðurinn við borðið tapaði öllu í
        spilakössunum.
    """),
    "CeladonCity_Restaurant_Text_TakeThisImBusted": t("""
        Gjörðu svo vel!
        Hlæðu bara!
        Ég er gjörsamlega blankur!

        Engir fleiri spilakassar fyrir mig!
        Ég ætla að taka mig á!

        Hér!
        Ég þarf ekki á þessu að halda lengur!
    """),
    "CeladonCity_Restaurant_Text_ReceivedCoinCaseFromMan": t("""
        {PLAYER} fékk PENINGAVESKI
        frá manninum.
    """),
    "CeladonCity_Restaurant_Text_MakeRoomForThis": t("""
        Búðu til pláss fyrir þetta!
    """),
    "CeladonCity_Restaurant_Text_ThoughtIdWinItBack": t("""
        Ég hélt alltaf að ég myndi vinna
        þetta til baka...
    """),
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-after-v2.csv")
    parser.add_argument("--output", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-celadon-v3.csv")
    args = parser.parse_args()

    with args.queue.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    out = []
    seen: set[str] = set()
    for row in rows:
        label = row["label"]
        if label not in TRANSLATIONS:
            continue
        row = dict(row)
        row["icelandic"] = TRANSLATIONS[label]
        row["notes"] = "codex curated Celadon v3"
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
