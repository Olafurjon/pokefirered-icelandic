@ These are event scripts. They should not be moved to C.

#include "constants/global.h"
#include "constants/flags.h"
#include "constants/moves.h"
#include "constants/songs.h"
#include "constants/species.h"
#include "constants/vars.h"
#include "constants/items.h"
#include "constants/region_map_sections.h"
	.include "asm/macros.inc"
	.include "asm/macros/event.inc"
	.include "constants/constants.inc"

	.section .rodata
	
	.align 2
MysteryEventScript_StampCard::
	setvaddress MysteryEventScript_StampCard
	setorcopyvar VAR_RESULT, 1
	specialvar VAR_0x8008, GetMysteryGiftCardStat
	setorcopyvar VAR_RESULT, 0
	specialvar VAR_0x8009, GetMysteryGiftCardStat
	subvar VAR_0x8008, VAR_0x8009
	buffernumberstring STR_VAR_1, VAR_0x8008
	lock
	faceplayer
	vmessage sText_MysteryGiftStampCard
	waitmessage
	waitbuttonpress
	release
	end

sText_MysteryGiftStampCard:
	.string "Takk fyrir að nota\n"
	.string "STIMPILKORTAKERFIÐ.\p"
	.string "Þú þarft {STR_VAR_1} í viðbót til að\n"
	.string "fylla STIMPILKORTIÐ.$"

MysteryEventScript_SurfPichu::
	setvaddress MysteryEventScript_SurfPichu
	vgoto_if_unset FLAG_MYSTERY_GIFT_DONE, SurfPichu_GiveIfPossible
	returnram

SurfPichu_GiveIfPossible:
	specialvar VAR_EVENT_PICHU_SLOT, CalculatePlayerPartyCount
	vgoto_if_eq VAR_EVENT_PICHU_SLOT, PARTY_SIZE, SurfPichu_FullParty
	setflag FLAG_MYSTERY_GIFT_DONE
	vcall SurfPichu_GiveEgg
	lock
	faceplayer
	vmessage sText_MysteryGiftEgg
	waitmessage
	waitbuttonpress
	playfanfare MUS_OBTAIN_ITEM
	waitfanfare
	release
	end

SurfPichu_FullParty:
	lock
	faceplayer
	vmessage sText_FullParty
	waitmessage
	waitbuttonpress
	release
	end

SurfPichu_GiveEgg:
	giveegg SPECIES_PICHU
	setmonmodernfatefulencounter VAR_EVENT_PICHU_SLOT
	setmonmetlocation VAR_EVENT_PICHU_SLOT, METLOC_FATEFUL_ENCOUNTER
	vgoto_if_eq VAR_EVENT_PICHU_SLOT, 1, SurfPichu_Slot1
	vgoto_if_eq VAR_EVENT_PICHU_SLOT, 2, SurfPichu_Slot2
	vgoto_if_eq VAR_EVENT_PICHU_SLOT, 3, SurfPichu_Slot3
	vgoto_if_eq VAR_EVENT_PICHU_SLOT, 4, SurfPichu_Slot4
	vgoto_if_eq VAR_EVENT_PICHU_SLOT, 5, SurfPichu_Slot5
	return

SurfPichu_Slot1:
	setmonmove 1, 2, MOVE_SURF
	return

SurfPichu_Slot2:
	setmonmove 2, 2, MOVE_SURF
	return

SurfPichu_Slot3:
	setmonmove 3, 2, MOVE_SURF
	return

SurfPichu_Slot4:
	setmonmove 4, 2, MOVE_SURF
	return

SurfPichu_Slot5:
	setmonmove 5, 2, MOVE_SURF
	return

sText_MysteryGiftEgg:
	.string "Ó, liðið þitt virðist vera fullt.\p"
	.string "Vinsamlegast komdu aftur til mín\n"
	.string "eftir að þú hefur geymt Vasaskrímsli\p"
	.string "í tölvu.$"

sText_FullParty:
	.string "Ó, liðið þitt virðist vera fullt.\p"
	.string "Vinsamlegast komdu aftur til mín\n"
	.string "eftir að þú hefur geymt Vasaskrímsli\p"
	.string "í tölvu.$"

MysteryEventScript_VisitingTrainer::
	setvaddress MysteryEventScript_VisitingTrainer
	special ValidateEReaderTrainer
	vgoto_if_eq VAR_RESULT, 0, MysteryEventScript_VisitingTrainerArrived
	lock
	faceplayer
	vmessage sText_MysteryGiftVisitingTrainer
	waitmessage
	waitbuttonpress
	release
	end

MysteryEventScript_VisitingTrainerArrived:
	lock
	faceplayer
	vmessage sText_MysteryGiftVisitingTrainer_2
	waitmessage
	waitbuttonpress
	release
	end

sText_MysteryGiftVisitingTrainer:
	.string "Takk fyrir að nota MYSTERY GIFT\n"
	.string "kerfið.\p"
	.string "ÞJÁLFARI er kominn til SEVII EYJA og\n"
	.string "leitar að þér.\p"
	.string "Við vonum að þú njótir þess að\n"
	.string "berjast við heimsóknar ÞJÁLFARANN.\p"
	.string "Þú getur boðið öðrum ÞJÁLFÖRUM með\n"
	.string "því að slá inn önnur lykilorð.\p"
	.string "Reyndu að leita að öðrum lykilorðum\n"
	.string "sem gætu virkað.$"

sText_MysteryGiftVisitingTrainer_2:
	.string "Takk fyrir að nota MYSTERY GIFT\n"
	.string "kerfið.\p"
	.string "ÞJÁLFARI er kominn til SEVII EYJA og\n"
	.string "leitar að þér.\p"
	.string "Við vonum að þú njótir þess að\n"
	.string "berjast við heimsóknar ÞJÁLFARANN.\p"
	.string "Þú getur boðið öðrum ÞJÁLFÖRUM með\n"
	.string "því að slá inn önnur lykilorð.\p"
	.string "Reyndu að leita að öðrum lykilorðum\n"
	.string "sem gætu virkað.$"

MysteryEventScript_BattleCard::
	setvaddress MysteryEventScript_BattleCard
	vgoto_if_set FLAG_MYSTERY_GIFT_DONE, MysteryEventScript_BattleCardInfo
	setorcopyvar VAR_RESULT, 2
	specialvar VAR_0x8008, GetMysteryGiftCardStat
	vgoto_if_ne VAR_0x8008, 3, MysteryEventScript_BattleCardInfo
	lock
	faceplayer
	vmessage sText_MysteryGiftBattleCountCard_2
	waitmessage
	waitbuttonpress
	giveitem ITEM_POTION
	release
	setflag FLAG_MYSTERY_GIFT_DONE
	end

MysteryEventScript_BattleCardInfo:
	lock
	faceplayer
	vmessage sText_MysteryGiftBattleCountCard
	waitmessage
	waitbuttonpress
	release
	end

sText_MysteryGiftBattleCountCard:
	.string "Takk fyrir að nota LEYNIGJAFAKERFIÐ.\p"
	.string "Til hamingju!\p"
	.string "Þú vannst verðlaun fyrir að vinna\n"
	.string "þrjá bardaga!\p"
	.string "Við vonum að þetta hvetji þig til\n"
	.string "fleiri bardaga.$"

sText_MysteryGiftBattleCountCard_2:
	.string "Takk fyrir að nota LEYNIGJAFAKERFIÐ.\p"
	.string "Til hamingju!\p"
	.string "Þú vannst verðlaun fyrir að vinna\n"
	.string "þrjá bardaga!\p"
	.string "Við vonum að þetta hvetji þig til\n"
	.string "fleiri bardaga.$"

MysteryEventScript_AuroraTicket::
	setvaddress MysteryEventScript_AuroraTicket
	lock
	faceplayer
	vgoto_if_set FLAG_RECEIVED_AURORA_TICKET, AuroraTicket_Obtained
	vgoto_if_set FLAG_FOUGHT_DEOXYS, AuroraTicket_Obtained
	checkitem ITEM_AURORA_TICKET, 1
	vgoto_if_eq VAR_RESULT, TRUE, AuroraTicket_Obtained
	vmessage sText_AuroraTicket1
	waitmessage
	waitbuttonpress
	checkitemspace ITEM_AURORA_TICKET, 1
	vgoto_if_eq VAR_RESULT, FALSE, AuroraTicket_NoBagSpace
	giveitem ITEM_AURORA_TICKET
	setflag FLAG_ENABLE_SHIP_BIRTH_ISLAND
	setflag FLAG_RECEIVED_AURORA_TICKET
	vmessage sText_AuroraTicket2
	waitmessage
	waitbuttonpress
	release
	end

AuroraTicket_NoBagSpace:
	vmessage sText_AuroraTicketNoPlace
	waitmessage
	waitbuttonpress
	release
	end

AuroraTicket_Obtained:
	vmessage sText_AuroraTicketGot
	waitmessage
	waitbuttonpress
	release
	end

sText_AuroraTicket1:
	.string "Ó, fyrirgefðu, {PLAYER}.\n"
	.string "LYKILHLUTAHÓLFIÐ í TÖSKUNNI þinni er\p"
	.string "fullt.\p"
	.string "Vinsamlegast geymdu eitthvað á\n"
	.string "tölvunni þinni, komdu svo aftur.$"

sText_AuroraTicket2:
	.string "Ó, fyrirgefðu, {PLAYER}.\n"
	.string "LYKILHLUTAHÓLFIÐ í TÖSKUNNI þinni er\p"
	.string "fullt.\p"
	.string "Vinsamlegast geymdu eitthvað á\n"
	.string "tölvunni þinni, komdu svo aftur.$"

sText_AuroraTicketGot:
	.string "Ó, fyrirgefðu, {PLAYER}.\n"
	.string "LYKILHLUTAHÓLFIÐ í TÖSKUNNI þinni er\p"
	.string "fullt.\p"
	.string "Vinsamlegast geymdu eitthvað á\n"
	.string "tölvunni þinni, komdu svo aftur.$"

sText_AuroraTicketNoPlace:
	.string "Ó, fyrirgefðu, {PLAYER}.\n"
	.string "LYKILHLUTAHÓLFIÐ í TÖSKUNNI þinni er\p"
	.string "fullt.\p"
	.string "Vinsamlegast geymdu eitthvað á\n"
	.string "tölvunni þinni, komdu svo aftur.$"

MysteryEventScript_MysticTicket::
	setvaddress MysteryEventScript_MysticTicket
	lock
	faceplayer
	vgoto_if_set FLAG_RECEIVED_MYSTIC_TICKET, MysticTicket_Obtained
	vgoto_if_set FLAG_FOUGHT_LUGIA, MysticTicket_Obtained
	vgoto_if_set FLAG_FOUGHT_HO_OH, MysticTicket_Obtained
	checkitem ITEM_MYSTIC_TICKET, 1
	vgoto_if_eq VAR_RESULT, TRUE, MysticTicket_Obtained
	vmessage sText_MysticTicket2
	waitmessage
	waitbuttonpress
	checkitemspace ITEM_MYSTIC_TICKET, 1
	vgoto_if_eq VAR_RESULT, FALSE, MysticTicket_NoBagSpace
	giveitem ITEM_MYSTIC_TICKET
	setflag FLAG_ENABLE_SHIP_NAVEL_ROCK
	setflag FLAG_RECEIVED_MYSTIC_TICKET
	vmessage sText_MysticTicket1
	waitmessage
	waitbuttonpress
	release
	end

MysticTicket_NoBagSpace:
	vmessage sText_MysticTicketNoPlace
	waitmessage
	waitbuttonpress
	release
	end

MysticTicket_Obtained:
	vmessage sText_MysticTicketGot
	waitmessage
	waitbuttonpress
	release
	end

sText_MysticTicket2:
	.string "Ó, fyrirgefðu, {PLAYER}.\n"
	.string "LYKILHLUTAHÓLFIÐ í TÖSKUNNI þinni er\p"
	.string "fullt.\p"
	.string "Vinsamlegast geymdu eitthvað á\n"
	.string "tölvunni þinni, komdu svo aftur.$"

sText_MysticTicket1:
	.string "Ó, fyrirgefðu, {PLAYER}.\n"
	.string "LYKILHLUTAHÓLFIÐ í TÖSKUNNI þinni er\p"
	.string "fullt.\p"
	.string "Vinsamlegast geymdu eitthvað á\n"
	.string "tölvunni þinni, komdu svo aftur.$"

sText_MysticTicketGot:
	.string "Ó, fyrirgefðu, {PLAYER}.\n"
	.string "LYKILHLUTAHÓLFIÐ í TÖSKUNNI þinni er\p"
	.string "fullt.\p"
	.string "Vinsamlegast geymdu eitthvað á\n"
	.string "tölvunni þinni, komdu svo aftur.$"

sText_MysticTicketNoPlace:
	.string "Ó, fyrirgefðu, {PLAYER}.\n"
	.string "LYKILHLUTAHÓLFIÐ í TÖSKUNNI þinni er\p"
	.string "fullt.\p"
	.string "Vinsamlegast geymdu eitthvað á\n"
	.string "tölvunni þinni, komdu svo aftur.$"

MysteryEventScript_AlteringCave::
	setvaddress MysteryEventScript_AlteringCave
	addvar VAR_ALTERING_CAVE_WILD_SET, 1
	vgoto_if_ne VAR_ALTERING_CAVE_WILD_SET, 10, MysteryEventScript_AlteringCave_
	setvar VAR_ALTERING_CAVE_WILD_SET, 0
MysteryEventScript_AlteringCave_:
	lock
	faceplayer
	vmessage sText_MysteryGiftAlteringCave
	waitmessage
	waitbuttonpress
	release
	end

sText_MysteryGiftAlteringCave:
	.string "Takk fyrir að nota MYSTERY GIFT\n"
	.string "kerfið.\p"
	.string "Nýlega hafa verið sögusagnir um\n"
	.string "sjaldgæf Vasaskrímsli.\p"
	.string "Sögusagnirnar eru um ALTERING CAVE á\n"
	.string "OUTCAST ISLAND.\p"
	.string "Hvers vegna ekki að heimsækja þangað\n"
	.string "og athuga hvort sögusagnirnar séu\p"
	.string "sannar?$"
