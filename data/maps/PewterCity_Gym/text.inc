PewterCity_Gym_Text_BrockIntro::
    .string "Svo þú ert kominn. Ég er BROCK. Ég\n"
    .string "er SALSTJÓRI PEWTER-SALARINS.\p"
    .string "Steinharður viljastyrkur minn sést\n"
    .string "jafnvel í vasaskrímslunum mínum.\p"
    .string "Vasaskrímslin mín eru öll grjóthörð\n"
    .string "og staðföst.\p"
    .string "Það er rétt - þau eru öll af\n"
    .string "STEINS-gerð!\p"
    .string "Fuhaha! Ætlarðu að skora á mig þótt\n"
    .string "þú vitir að þú tapar?\p"
    .string "Það er heiður ÞJÁLFARA sem knýr þig\n"
    .string "til að skora á mig.\p"
    .string "Jæja þá! Sýndu mér hvað þú\n"
    .string "getur!{PLAY_BGM}{MUS_ENCOUNTER_GYM_LEADER}$"

@ NOTE: This defeat text actually causes a buffer overflow. It's too long for the gDisplayedStringBattle
@ buffer that it's put into, and it stomps all over the gBattleTextBuffs after, as well as the otherwise
@ unused array after that, sFlickerArray. Perhaps that's the reason why said array exists.
PewterCity_Gym_Text_BrockDefeat::
    .string "Ég vanmat þig og þess vegna tapaði\n"
    .string "ég.\p"
    .string "Sem sönnun um sigur þinn veiti ég\n"
    .string "þér þetta... opinbera STEINMERKIÐ\p"
    .string "VASASKRÍMSLADEILDARINNAR.\p"
    .string "{FONT_NORMAL}{PLAYER} fékk\n"
    .string "STEINMERKIÐ frá\p"
    .string "BROCK!{PAUSE_MUSIC}{PLAY_BGM}{MUS_OBTAIN_BADGE}{PAUSE 0xFE}{PAUSE 0x56}{RESUME_MUSIC}\p"
    .string "{FONT_MALE}Það eitt að hafa\n"
    .string "STEINMERKIÐ gerir vasaskrímslin þín\p"
    .string "sterkari.\p"
    .string "Það gerir líka kleift að nota\n"
    .string "bragðið LEIFTUR utan bardaga.\p"
    .string "Að sjálfsögðu þarf vasaskrímsli að\n"
    .string "kunna LEIFTUR til að nota það.$"

PewterCity_Gym_Text_TakeThisWithYou::
    .string "Bíddu! Taktu þetta með þér.$"

PewterCity_Gym_Text_ReceivedTM39FromBrock::
    .string "{PLAYER} fékk TM39 frá BROCK.$"

PewterCity_Gym_Text_ExplainTM39::
    .string "TM, Technical Machine, inniheldur\n"
    .string "bragð fyrir vasaskrímsli.\p"
    .string "Með því að nota TM lærir\n"
    .string "vasaskrímsli bragðið sem það geymir.\p"
    .string "Hvert TM má aðeins nota einu sinni.\p"
    .string "Veldu því vasaskrímslið vandlega\n"
    .string "þegar þú notar eitt.\p"
    .string "Annars... TM39 inniheldur STEINGRÖF.\p"
    .string "Það þeytir steinum í andstæðinginn\n"
    .string "og lækkar SPEED.$"

PewterCity_Gym_Text_BrockPostBattle::
    .string "Það eru alls kyns ÞJÁLFARAR í þessum\n"
    .string "stóra heimi.\p"
    .string "Þú virðist mjög hæfileikaríkur\n"
    .string "vasaskrímslaþjálfari.\p"
    .string "Leyfðu mér því að leggja eitt til.\p"
    .string "Farðu í SALINN í CERULEAN og prófaðu\n"
    .string "hæfileika þína.$"

PewterCity_Gym_Text_DontHaveRoomForThis::
    .string "Þú hefur ekki pláss fyrir þetta.$"

PewterCity_Gym_Text_LiamIntro::
    .string "Stopp þar, krakki!\p"
    .string "Þú ert tíu þúsund ljósár frá því að\n"
    .string "mæta BROCK!$"

PewterCity_Gym_Text_LiamDefeat::
    .string "Ansans!\p"
    .string "Ljósár eru ekki tími... Þau mæla\n"
    .string "fjarlægð!$"

PewterCity_Gym_Text_LiamPostBattle::
    .string "Þú ert ansi heitur. ...En ekki jafn\n"
    .string "heitur og BROCK!$"

PewterCity_Gym_Text_LetMeTakeYouToTheTop::
    .string "Hæ! Viltu dreyma stórt?\p"
    .string "Þorirðu að dreyma um að verða\n"
    .string "meistari vasaskrímsla?\p"
    .string "Ég er ekki ÞJÁLFARI, en ég get\n"
    .string "ráðlagt þér hvernig þú vinnur.\p"
    .string "Leyfðu mér að koma þér á toppinn!$"

PewterCity_Gym_Text_LetsGetHappening::
    .string "Allt í lagi! Byrjum þetta!$"

PewterCity_Gym_Text_TryDifferentPartyOrders::
    .string "Fyrsta vasaskrímslið í bardaga er\n"
    .string "vinstra megin á\p"
    .string "vasaskrímslalistanum.\p"
    .string "Með því að breyta röð vasaskrímsla\n"
    .string "geturðu náð forskoti.\p"
    .string "Prófaðu mismunandi raðir eftir liði\n"
    .string "andstæðingsins.$"

PewterCity_Gym_Text_ItsFreeLetsGetHappening::
    .string "Þetta er ókeypis þjónusta! Byrjum\n"
    .string "þetta!$"

PewterCity_Gym_Text_YoureChampMaterial::
    .string "Eins og ég hélt! Þú ert efni í\n"
    .string "vasaskrímslameistara!$"

PewterCity_Gym_Text_GymStatue::
    .string "PEWTER VASASKRÍMSLA-SALUR SALSTJÓRI:\n"
    .string "BROCK\p"
    .string "SIGURSÆLIR ÞJÁLFARAR: {RIVAL}$"

PewterCity_Gym_Text_GymStatuePlayerWon::
    .string "PEWTER VASASKRÍMSLA-SALUR SALSTJÓRI:\n"
    .string "BROCK\p"
    .string "SIGURSÆLIR ÞJÁLFARAR: {RIVAL},\n"
    .string "{PLAYER}$"

