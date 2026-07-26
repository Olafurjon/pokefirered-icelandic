#include "global.h"
#include "link_rfu.h"
#include "mystery_gift_server.h"
#include "mystery_gift_client.h"
#include "constants/union_room.h"

ALIGNED(4) const u8 gText_UR_EmptyString[] = _("");
ALIGNED(4) const u8 gText_UR_Colon[] = _(":");
ALIGNED(4) const u8 gText_UR_ID[] = _("{ID}");
ALIGNED(4) const u8 gText_UR_PleaseStartOver[] = _("Vinsamlegast byrjaðu upp á nýtt frá byrjun.");
ALIGNED(4) const u8 gText_UR_WirelessSearchCanceled[] = _("Leitin að ÞRÁÐLAUSA SAMSKIPTA-\nKERFINU hefur verið hætt við.");
ALIGNED(4) static const u8 sText_AwaitingCommunucation2[] = _("Bíd eftir sambandi\nfrá vini.");
ALIGNED(4) const u8 gText_UR_AwaitingCommunication[] = _("{STR_VAR_1}! Bíð eftir\nsamskiptum frá öðrum leikmanni.");
ALIGNED(4) const u8 gText_UR_AwaitingLinkPressStart[] = _("{STR_VAR_1}! Bíð eftir tengingu!\nÝttu á START þegar allir eru tilbúnir.");

ALIGNED(4) static const u8 sText_SingleBattle[] = _("Halda einstaklingsbardaga");
ALIGNED(4) static const u8 sText_DoubleBattle[] = _("Halda tvíliðabardaga");
ALIGNED(4) static const u8 sText_MultiBattle[] = _("Halda fjölliðabardaga");
ALIGNED(4) static const u8 sText_TradePokemon[] = _("Halda vasaskrímslaskipti");
ALIGNED(4) static const u8 sText_Chat[] = _("Opna spjall");
ALIGNED(4) static const u8 sText_DistWonderCard[] = _("Dreifa Undrakorti");
ALIGNED(4) static const u8 sText_DistWonderNews[] = _("Dreifa Undrafréttum");
ALIGNED(4) static const u8 sText_DistMysteryEvent[] = _("Halda Leynividburð");
ALIGNED(4) static const u8 sText_HoldPokemonJump[] = _("Halda stökkleik");
ALIGNED(4) static const u8 sText_HoldBerryCrush[] = _("Halda berjamulning");
ALIGNED(4) static const u8 sText_HoldBerryPicking[] = _("Halda berjatínslu");
ALIGNED(4) static const u8 sText_HoldSpinTrade[] = _("Halda hringskipti");
ALIGNED(4) static const u8 sText_HoldSpinShop[] = _("Halda hringsjoppu");

// Unused
static const u8 *const sLinkGroupActionTexts[] = {
    sText_SingleBattle,
    sText_DoubleBattle,
    sText_MultiBattle,
    sText_TradePokemon,
    sText_Chat,
    sText_DistWonderCard,
    sText_DistWonderNews,
    sText_DistWonderCard,
    sText_HoldPokemonJump,
    sText_HoldBerryCrush,
    sText_HoldBerryPicking,
    sText_HoldBerryPicking,
    sText_HoldSpinTrade,
    sText_HoldSpinShop
};

static const u8 sText_1PlayerNeeded[] = _("1 leikmaður\nvantar.");
static const u8 sText_2PlayersNeeded[] = _("2 leikmenn\nvantar.");
static const u8 sText_3PlayersNeeded[] = _("3 leikmenn\nvantar.");
static const u8 sText_4PlayersNeeded[] = _("Vantar 4\nspilara");
static const u8 sText_2PlayerMode[] = _("2-LEIKMANNA\nHAMUR");
static const u8 sText_3PlayerMode[] = _("3-LEIKMANNA\nHAMUR");
static const u8 sText_4PlayerMode[] = _("4-LEIKMANNA\nHAMUR");
static const u8 sText_5PlayerMode[] = _("5-LEIKMANNA\nHAMUR");

const u8 *const gTexts_UR_PlayersNeededOrMode[][5] = {
    { // 2 players required
        sText_1PlayerNeeded,
        sText_2PlayerMode
    },
    { // 4 players required
        sText_3PlayersNeeded,
        sText_2PlayersNeeded,
        sText_1PlayerNeeded,
        sText_4PlayerMode
    },
    { // 2-5 players required
        sText_1PlayerNeeded,
        sText_2PlayerMode,
        sText_3PlayerMode,
        sText_4PlayerMode,
        sText_5PlayerMode
    },
    { // 3-5 players required
        sText_2PlayersNeeded,
        sText_1PlayerNeeded,
        sText_3PlayerMode,
        sText_4PlayerMode,
        sText_5PlayerMode
    }
};

ALIGNED(4) const u8 gText_UR_BButtonCancel[] = _("{B_BUTTON}HÆTTA VIÐ");
ALIGNED(4) static const u8 sText_SearchingForParticipants[] = _("Leita að\nþátttakendum!");
ALIGNED(4) const u8 gText_UR_PlayerContactedYouForXAccept[] = _("{STR_VAR_2} hafði samband við þig vegna\n{STR_VAR_1}. Samþykkja?");
ALIGNED(4) const u8 gText_UR_PlayerContactedYouShareX[] = _("{STR_VAR_2} hafði samband við þig.\nViltu deila {STR_VAR_1}?");
ALIGNED(4) const u8 gText_UR_PlayerContactedYouAddToMembers[] = _("{STR_VAR_2} hafði samband við þig.\nBæta við meðlimi?");
ALIGNED(4) const u8 gText_UR_AreTheseMembersOK[] = _("{STR_VAR_1}!\nEru þessir meðlimir í lagi?");
ALIGNED(4) const u8 gText_UR_CancelModeWithTheseMembers[] = _("Hætta við {STR_VAR_1} HAM\nmeð þessum meðlimum?");
ALIGNED(4) const u8 gText_UR_AnOKWasSentToPlayer[] = _("Eitt 'OK' var sent\ntil {STR_VAR_1}.");

ALIGNED(4) static const u8 sText_OtherTrainerUnavailableNow[] = _("Hinn ÞJÁLFARI virðist ekki vera\ntiltækur núna…");
ALIGNED(4) static const u8 sText_CantTransmitTrainerTooFar[] = _("Þú getur ekki haft samband við\nÞJÁLFARA sem er of langt í burtu.");
ALIGNED(4) static const u8 sText_TrainersNotReadyYet[] = _("Hinir ÞJÁLFARARNIR eru ekki\ntilbúnir enn.");

const u8 *const gTexts_UR_CantTransmitToTrainer[] = {
    sText_CantTransmitTrainerTooFar,
    sText_TrainersNotReadyYet
};

ALIGNED(4) const u8 gText_UR_ModeWithTheseMembersWillBeCanceled[] = _("{STR_VAR_1} HAMURINN með\nþessum meðlimum verður hættur við.{PAUSE 90}");
ALIGNED(4) static const u8 sText_MemberNoLongerAvailable[] = _("Það er meðlimur sem getur ekki\nlengur verið tiltækur.");

const u8 *const gTexts_UR_PlayerUnavailable[] = {
    sText_OtherTrainerUnavailableNow,
    sText_MemberNoLongerAvailable
};

ALIGNED(4) static const u8 sText_TrainerAppearsUnavailable[] = _("Hinn ÞJÁLFARI virðist\nekki tiltækur…");
ALIGNED(4) const u8 gText_UR_PlayerSentBackOK[] = _("{STR_VAR_1} sendi til baka 'OK'!");
ALIGNED(4) const u8 gText_UR_PlayerOKdRegistration[] = _("{STR_VAR_1} samþykkti skráningu þína sem\nmeðlim.");
ALIGNED(4) static const u8 sText_PlayerRepliedNo[] = _("{STR_VAR_1} replied, 'No…'");
ALIGNED(4) const u8 gText_UR_AwaitingOtherMembers[] = _("{STR_VAR_1}!\nBíð eftir öðrum meðlimum!");
ALIGNED(4) const u8 gText_UR_QuitBeingMember[] = _("Hætta að vera meðlimur?");
ALIGNED(4) static const u8 sText_StoppedBeingMember[] = _("Þú hættir að vera meðlimur.");

const u8 *const gTexts_UR_PlayerDisconnected[] = {
    [RFU_STATUS_OK]                  = NULL,
    [RFU_STATUS_FATAL_ERROR]         = sText_MemberNoLongerAvailable,
    [RFU_STATUS_CONNECTION_ERROR]    = sText_TrainerAppearsUnavailable,
    [RFU_STATUS_CHILD_SEND_COMPLETE] = NULL,
    [RFU_STATUS_NEW_CHILD_DETECTED]  = NULL,
    [RFU_STATUS_JOIN_GROUP_OK]       = NULL,
    [RFU_STATUS_JOIN_GROUP_NO]       = sText_PlayerRepliedNo,
    [RFU_STATUS_WAIT_ACK_JOIN_GROUP] = NULL,
    [RFU_STATUS_LEAVE_GROUP_NOTICE]  = NULL,
    [RFU_STATUS_LEAVE_GROUP]         = sText_StoppedBeingMember
};

ALIGNED(4) const u8 gText_UR_WirelessLinkEstablished[] = _("Tenging við ÞRÁÐLAUSA SAMSKIPTA-\nKERFIÐ hefur verið stofnuð.");
ALIGNED(4) const u8 gText_UR_WirelessLinkDropped[] = _("Tenging við ÞRÁÐLAUSA SAMSKIPTA-\nKERFIÐ hefur rofnað…");
ALIGNED(4) const u8 gText_UR_LinkWithFriendDropped[] = _("Tengingin við vin þinn hefur\nrofnað…");
ALIGNED(4) static const u8 sText_PlayerRepliedNo2[] = _("{STR_VAR_1} replied, 'No…'");

const u8 *const gTexts_UR_LinkDropped[] = {
    [RFU_STATUS_OK]                  = NULL,
    [RFU_STATUS_FATAL_ERROR]         = gText_UR_LinkWithFriendDropped,
    [RFU_STATUS_CONNECTION_ERROR]    = gText_UR_LinkWithFriendDropped,
    [RFU_STATUS_CHILD_SEND_COMPLETE] = NULL,
    [RFU_STATUS_NEW_CHILD_DETECTED]  = NULL,
    [RFU_STATUS_JOIN_GROUP_OK]       = NULL,
    [RFU_STATUS_JOIN_GROUP_NO]       = sText_PlayerRepliedNo2,
    [RFU_STATUS_WAIT_ACK_JOIN_GROUP] = NULL,
    [RFU_STATUS_LEAVE_GROUP_NOTICE]  = NULL,
    [RFU_STATUS_LEAVE_GROUP]         = NULL
};

ALIGNED(4) static const u8 sText_DoYouWantXMode[] = _("Viltu {STR_VAR_2}\nHAMINN?");
ALIGNED(4) static const u8 sText_DoYouWantXMode2[] = _("Viltu {STR_VAR_2}\nHAMINN?");

// Unused
static const u8 *const sDoYouWantModeTexts[] = {
    sText_DoYouWantXMode,
    sText_DoYouWantXMode2
};

ALIGNED(4) static const u8 sText_CommunicatingPleaseWait[] = _("Hef samband...\nBíddu augnablik."); // Unused
ALIGNED(4) const u8 gText_UR_AwaitingPlayersResponseAboutTrade[] = _("Bíð eftir svari {STR_VAR_1} varðandi\nviðskiptin…");

ALIGNED(4) static const u8 sText_Communicating[] = _("Samskipti í gangi{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.\n{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.");
ALIGNED(4) static const u8 sText_CommunicatingWithPlayer[] = _("Samskipti við {STR_VAR_1} í gangi{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.\n{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.");
ALIGNED(4) static const u8 sText_PleaseWaitAWhile[] = _("Vinsamlegast bíddu smá{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.\n{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.");

const u8 *const gTexts_UR_CommunicatingWait[] = {
    sText_Communicating,
    sText_CommunicatingWithPlayer,
    sText_PleaseWaitAWhile
};

ALIGNED(4) static const u8 sText_HiDoSomethingMale[] = _("Hæ! Er eitthvað sem þú\nvildir gera?");
ALIGNED(4) static const u8 sText_HiDoSomethingFemale[] = _("Halló!\nViltu gera eitthvað?");
ALIGNED(4) static const u8 sText_HiDoSomethingAgainMale[] = _("{STR_VAR_1}: Hæ, við hittumst aftur!\nHvað ætlarðu að gera núna?");
ALIGNED(4) static const u8 sText_HiDoSomethingAgainFemale[] = _("{STR_VAR_1}: Ó! {PLAYER}, halló!\nViltu gera eitthvað?");

const u8 *const gTexts_UR_HiDoSomething[][GENDER_COUNT] = {
    {
        sText_HiDoSomethingMale,
        sText_HiDoSomethingFemale
    }, {
        sText_HiDoSomethingAgainMale,
        sText_HiDoSomethingAgainFemale
    }
};

ALIGNED(4) static const u8 sText_DoSomethingMale[] = _("Viltu gera eitthvað?");
ALIGNED(4) static const u8 sText_DoSomethingFemale[] = _("Viltu gera eitthvað?");
ALIGNED(4) static const u8 sText_DoSomethingAgainMale[] = _("{STR_VAR_1}: Hvað viltu gera\nnúna?");
ALIGNED(4) static const u8 sText_DoSomethingAgainFemale[] = _("{STR_VAR_1}'また なにかする？");

// Unused
static const u8 *const sDoSomethingTexts[][GENDER_COUNT] = {
    {
        sText_DoSomethingMale,
        sText_DoSomethingFemale
    }, {
        sText_DoSomethingAgainMale,
        sText_DoSomethingAgainMale // was probably supposed to be sText_DoSomethingAgainFemale
    }
};

ALIGNED(4) static const u8 sText_SomebodyHasContactedYou[] = _("Einhver hefur haft samband við þig.{PAUSE 60}");
ALIGNED(4) static const u8 sText_PlayerHasContactedYou[] = _("{STR_VAR_1} hefur haft samband við þig.{PAUSE 60}");

const u8 *const gTexts_UR_PlayerContactedYou[] = {
    sText_SomebodyHasContactedYou,
    sText_PlayerHasContactedYou
};

ALIGNED(4) static const u8 sText_AwaitingResponseFromTrainer[] = _("Bíð eftir svari frá\nhinum ÞJÁLFARA…");
ALIGNED(4) static const u8 sText_AwaitingResponseFromPlayer[] = _("Bíð eftir svari frá\n{STR_VAR_1}…");

const u8 *const gTexts_UR_AwaitingResponse[] = {
    sText_AwaitingResponseFromTrainer,
    sText_AwaitingResponseFromPlayer
};

ALIGNED(4) static const u8 sText_AwaitingResponseCancelBButton[] = _("Bíð eftir svari.\nB-takki hættir við.");

ALIGNED(4) const u8 gText_UR_ShowTrainerCard[] = _("Hinn ÞJÁLFARI sýndi þér\nsitt ÞJÁLFARAKORT.\pViltu sýna þitt\nÞJÁLFARAKORT?");
ALIGNED(4) const u8 gText_UR_BattleChallenge[] = _("Hinn ÞJÁLFARI skorar á þig\ní bardaga.\pViltu taka áskoruninni?");
ALIGNED(4) const u8 gText_UR_ChatInvitation[] = _("Hinn ÞJÁLFARI býður þér\ní spjall.\pViltu taka boðinu?");
ALIGNED(4) const u8 gText_UR_OfferToTradeMon[] = _("Það er tilboð um að skipta þínu\nskráða Lv. {DYNAMIC 0} {DYNAMIC 1}\pfyrir\nLv. {DYNAMIC 2} {DYNAMIC 3}.\pViltu samþykkja þetta skipti-\ntilboð?");
ALIGNED(4) const u8 gText_UR_OfferToTradeEgg[] = _("Það er tilboð um að skipta þínu\nskráða EGGi.\nViltu samþykkja þetta skiptitilboð?");
ALIGNED(4) const u8 gText_UR_ChatDropped[] = _("Spjallinu hefur verið hætt.");
ALIGNED(4) const u8 gText_UR_OfferDeclined1[] = _("Þú hafnaðir tilboðinu.");
ALIGNED(4) const u8 gText_UR_OfferDeclined2[] = _("Þú hafnaðir tilboðinu.");
ALIGNED(4) const u8 gText_UR_ChatEnded[] = _("Spjallinu var lokið.");

// Unused
static const u8 *const sInvitationTexts[] = {
    gText_UR_ShowTrainerCard,
    gText_UR_BattleChallenge,
    gText_UR_ChatInvitation,
    gText_UR_OfferToTradeMon
};

ALIGNED(4) static const u8 sText_JoinChatMale[] = _("Ó, hæ! Við erum í spjalli núna.\nViltu vera með?");
ALIGNED(4) static const u8 sText_PlayerJoinChatMale[] = _("{STR_VAR_1}: Hæ, {PLAYER}!\nVið erum í spjalli núna.\nViltu vera með?");
ALIGNED(4) static const u8 sText_JoinChatFemale[] = _("Ó, hæ! Við erum í spjalli núna.\nViltu vera með?");
ALIGNED(4) static const u8 sText_PlayerJoinChatFemale[] = _("{STR_VAR_1}: Ó, hæ, {PLAYER}!\nVið erum í spjalli núna.\nViltu vera með?");

const u8 *const gTexts_UR_JoinChat[][GENDER_COUNT] = {
    {
        sText_JoinChatMale,
        sText_JoinChatFemale
    }, {
        sText_PlayerJoinChatMale,
        sText_PlayerJoinChatFemale
    }
};

ALIGNED(4) const u8 gText_UR_TrainerAppearsBusy[] = _("……\nÞJÁLFARINN virðist vera upptekinn…");
ALIGNED(4) static const u8 sText_WaitForBattleMale[] = _("Bardagi, ha?\nAllt í lagi, gefðu mér bara smá tíma.");
ALIGNED(4) static const u8 sText_WaitForChatMale[] = _("Þú vilt spjalla, ha?\nJú, bíddu bara aðeins.");
ALIGNED(4) static const u8 sText_ShowTrainerCardMale[] = _("Sure thing! As my 'Greetings,'\nhere's my ÞJÁLFARAKORT.");
ALIGNED(4) static const u8 sText_WaitForBattleFemale[] = _("Bardagi? Auðvitað, en ég þarf\ntíma til að undirbúa mig.");
ALIGNED(4) static const u8 sText_WaitForChatFemale[] = _("Vildirðu spjalla?\nÓkei, en vinsamlegast bíddu smá.");
ALIGNED(4) static const u8 sText_ShowTrainerCardFemale[] = _("Sem kynningu mun ég sýna þér\nmitt ÞJÁLFARAKORT.");

const u8 *const gTexts_UR_WaitOrShowCard[GENDER_COUNT][4] = {
    {
        sText_WaitForBattleMale,
        sText_WaitForChatMale,
        NULL,
        sText_ShowTrainerCardMale
    }, {
        sText_WaitForBattleFemale,
        sText_WaitForChatFemale,
        NULL,
        sText_ShowTrainerCardFemale
    }
};

ALIGNED(4) static const u8 sText_WaitForChatMale2[] = _("Spjall, já!\nAllt í lagi, bíddu aðeins!");
ALIGNED(4) static const u8 sText_DoneWaitingBattleMale[] = _("Takk fyrir biðina!\nByrjum bardagann!{PAUSE 60}");
ALIGNED(4) static const u8 sText_DoneWaitingChatMale[] = _("Allt í lagi!\nSpjöllum!{PAUSE 60}");
ALIGNED(4) static const u8 sText_DoneWaitingBattleFemale[] = _("Fyrirgefðu að ég lét þig bíða!\nByrjum!{PAUSE 60}");
ALIGNED(4) static const u8 sText_DoneWaitingChatFemale[] = _("Fyrirgefðu að ég lét þig bíða!\nSpjöllum.{PAUSE 60}");
ALIGNED(4) static const u8 sText_TradeWillBeStarted[] = _("Viðskiptin verða hafin.{PAUSE 60}");
ALIGNED(4) static const u8 sText_BattleWillBeStarted[] = _("Bardaginn verður hafinn.{PAUSE 60}");
ALIGNED(4) static const u8 sText_EnteringChat[] = _("Gengið inn í spjallið…{PAUSE 60}");

const u8 *const gTexts_UR_StartActivity[][GENDER_COUNT][3] = {
    {
        {
            sText_BattleWillBeStarted,
            sText_EnteringChat,
            sText_TradeWillBeStarted
        }, {
            sText_BattleWillBeStarted,
            sText_EnteringChat,
            sText_TradeWillBeStarted
        }
    }, {
        {
            sText_DoneWaitingBattleMale,
            sText_DoneWaitingChatMale,
            sText_TradeWillBeStarted
        }, {
            sText_DoneWaitingBattleFemale,
            sText_DoneWaitingChatFemale,
            sText_TradeWillBeStarted
        }
    }
};

ALIGNED(4) static const u8 sText_BattleDeclinedMale[] = _("Fyrirgefðu! Vasaskrímslin mín\nvirðast ekki vera í góðu formi núna.\nBerjumst annan tíma.");
ALIGNED(4) static const u8 sText_BattleDeclinedFemale[] = _("Mér þykir það leitt, en\nVasaskrímslunum mínum líður ekki vel…\pBerjumst annan tíma.");

const u8 *const gTexts_UR_BattleDeclined[GENDER_COUNT] = {
    sText_BattleDeclinedMale,
    sText_BattleDeclinedFemale
};

ALIGNED(4) static const u8 sText_ShowTrainerCardDeclinedMale[] = _("Ha? Mitt ÞJÁLFARAKORT…\nHvert fór það núna?\nFyrirgefðu! Ég sýni þér það annan tíma!");
ALIGNED(4) static const u8 sText_ShowTrainerCardDeclinedFemale[] = _("Ó? Hvar setti ég mitt\nÞJÁLFARAKORT?…\nFyrirgefðu! Ég sýni þér það seinna!");

const u8 *const gTexts_UR_ShowTrainerCardDeclined[GENDER_COUNT] = {
    sText_ShowTrainerCardDeclinedMale,
    sText_ShowTrainerCardDeclinedFemale
};

ALIGNED(4) static const u8 sText_IfYouWantToDoSomethingMale[] = _("Ef þú vilt gera eitthvað með\nmér, bara láttu mig vita!");
ALIGNED(4) static const u8 sText_IfYouWantToDoSomethingFemale[] = _("Ef þú vilt gera eitthvað með\nmér, ekki vera feimin.");

const u8 *const gTexts_UR_IfYouWantToDoSomething[GENDER_COUNT] = {
    sText_IfYouWantToDoSomethingMale,
    sText_IfYouWantToDoSomethingFemale
};

ALIGNED(4) const u8 gText_UR_TrainerBattleBusy[] = _("Úbbs! Fyrirgefðu, en ég þarf að\ngera eitthvað annað.\nTökum þetta seinna, allt í lagi?");
ALIGNED(4) const u8 gText_UR_NeedTwoMonsOfLevel30OrLower1[] = _("Ef þú vilt berjast þarftu tvö\nVasaskrímsli sem eru undir Lv. 30.");
ALIGNED(4) const u8 gText_UR_NeedTwoMonsOfLevel30OrLower2[] = _("Fyrir bardaga þarftu tvö\nVasaskrímsli sem eru undir Lv. 30.");

ALIGNED(4) static const u8 sText_DeclineChatMale[] = _("Ó, allt í lagi.\nKomdu að hitta mig hvenær sem er.");
ALIGNED(4) static const u8 stext_DeclineChatFemale[] = _("Ó…\nKomdu endilega hvenær sem er.");

// Response from partner when player declines chat
const u8 *const gTexts_UR_DeclineChat[GENDER_COUNT] = {
    sText_DeclineChatMale,
    stext_DeclineChatFemale
};

ALIGNED(4) static const u8 sText_ChatDeclinedMale[] = _("Ó, fyrirgefðu!\nÉg get það bara ekki núna.\nSpjöllum saman annan tíma.");
ALIGNED(4) static const u8 sText_ChatDeclinedFemale[] = _("Ó, mér þykir það leitt.\nÉg hef of mikið að gera núna.\nSpjöllum saman seinna.");

// Response from partner when they decline chat
const u8 *const gTexts_UR_ChatDeclined[GENDER_COUNT] = {
    sText_ChatDeclinedMale,
    sText_ChatDeclinedFemale
};

ALIGNED(4) static const u8 sText_YoureToughMale[] = _("Vá!\nÉg sé að þú ert ansi sterkur!");
ALIGNED(4) static const u8 sText_UsedGoodMoveMale[] = _("Þú notaðir þessa hreyfingu?\nÞað er góð stefna!");
ALIGNED(4) static const u8 sText_BattleSurpriseMale[] = _("Vel gert!\nÞetta var algjör opinberun!");
ALIGNED(4) static const u8 sText_SwitchedMonsMale[] = _("Ó! Hvernig datt þér í hug að nota\nþetta Vasaskrímsli við þessar\naðstæður?");
ALIGNED(4) static const u8 sText_YoureToughFemale[] = _("Þetta Vasaskrímsli…\nÞað hefur verið alið upp mjög vel!");
ALIGNED(4) static const u8 sText_UsedGoodMoveFemale[] = _("Þetta er það!\nÞetta er rétta hreyfingin núna!");
ALIGNED(4) static const u8 sText_BattleSurpriseFemale[] = _("Þetta er frábært!\nGeturðu barist svona?");
ALIGNED(4) static const u8 sText_SwitchedMonsFemale[] = _("Þú ert með frábæra tímasetningu\nþegar þú skiptir um Vasaskrímsli!");

const u8 *const gTexts_UR_BattleReaction[GENDER_COUNT][4] = {
    {
        sText_YoureToughMale,
        sText_UsedGoodMoveMale,
        sText_BattleSurpriseMale,
        sText_SwitchedMonsMale
    }, {
        sText_YoureToughFemale,
        sText_UsedGoodMoveFemale,
        sText_BattleSurpriseFemale,
        sText_SwitchedMonsFemale
    }
};

ALIGNED(4) static const u8 sText_LearnedSomethingMale[] = _("Ó, ég skil!\nÞetta er fræðandi!");
ALIGNED(4) static const u8 sText_ThatsFunnyMale[] = _("Ekki segja neitt fyndið lengur!\nÉg er aumur af hlátri!");
ALIGNED(4) static const u8 sText_RandomChatMale1[] = _("Ó?\nEitthvað svoleiðis gerðist.");
ALIGNED(4) static const u8 sText_RandomChatMale2[] = _("Hmhm… Hvað?\nEr þetta það sem þú ert að segja?");
ALIGNED(4) static const u8 sText_LearnedSomethingFemale[] = _("Er það rétt?\nÉg vissi það ekki.");
ALIGNED(4) static const u8 sText_ThatsFunnyFemale[] = _("Ahaha!\nUm hvað snýst þetta?");
ALIGNED(4) static const u8 sText_RandomChatFemale1[] = _("Já, það er nákvæmlega það!\nÞað var það sem ég meinti.");
ALIGNED(4) static const u8 sText_RandomChatFemale2[] = _("Með öðrum orðum…\nJá! Það er rétt!");

const u8 *const gTexts_UR_ChatReaction[GENDER_COUNT][4] = {
    {
        sText_LearnedSomethingMale,
        sText_ThatsFunnyMale,
        sText_RandomChatMale1,
        sText_RandomChatMale2
    }, {
        sText_LearnedSomethingFemale,
        sText_ThatsFunnyFemale,
        sText_RandomChatFemale1,
        sText_RandomChatFemale2
    }
};

ALIGNED(4) static const u8 sText_ShowedTrainerCardMale1[] = _("I'm just showing my ÞJÁLFARAKORT\nas my way of greeting.");
ALIGNED(4) static const u8 sText_ShowedTrainerCardMale2[] = _("Ég vona að ég kynnist þér betur!");
ALIGNED(4) static const u8 sText_ShowedTrainerCardFemale1[] = _("Við sýnum hvort öðru\nÞJÁLFARAKORTIN okkar til að kynnast.");
ALIGNED(4) static const u8 sText_ShowedTrainerCardFemale2[] = _("Gaman að hitta þig.\nEkki vera ókunnugur!");

const u8 *const gTexts_UR_TrainerCardReaction[GENDER_COUNT][2] = {
    {
        sText_ShowedTrainerCardMale1,
        sText_ShowedTrainerCardMale2
    }, {
        sText_ShowedTrainerCardFemale1,
        sText_ShowedTrainerCardFemale2
    }
};

ALIGNED(4) static const u8 sText_MaleTraded1[] = _("Já!\nMig langaði rosalega í þetta\nVasaskrímsli!");
ALIGNED(4) static const u8 sText_MaleTraded2[] = _("Loksins fékk ég Vasaskrímslið\nsem mig hafði lengi langað í!");
ALIGNED(4) static const u8 sText_FemaleTraded1[] = _("I'm trading Vasaskrímsli right now.");
ALIGNED(4) static const u8 sText_FemaleTraded2[] = _("Ég fékk loksins það Vasaskrímsli\nsem ég vildi í skiptum!");

const u8 *const gTexts_UR_TradeReaction[GENDER_COUNT][4] = {
    {
        sText_MaleTraded1,
        sText_MaleTraded2
    }, {
        sText_FemaleTraded1,
        sText_FemaleTraded2
    }
};

const u8 gText_UR_XCheckedTradingBoard[] = _("{STR_VAR_1} skoðaði\nVIÐSKIPTABORÐIÐ.");
ALIGNED(4) const u8 gText_UR_RegisterMonAtTradingBoard[] = _("Velkomin á SKIPTIBORÐIÐ.\pÞú getur skráð Vasaskrímslið þitt\nog boðið það til skipta.\pViltu skrá eitt af\nVasaskrímslunum þínum?");
ALIGNED(4) const u8 gText_UR_TradingBoardInfo[] = _("This TRADING BOARD is used for\n"
                                                    "offering a Vasaskrímsli for a trade.\p"
                                                    "All you need to do is register a\n"
                                                    "Vasaskrímsli for a trade.\p"
                                                    "Another TRAINER may offer a party\n"
                                                    "Vasaskrímsli in return for the trade.\p"
                                                    "We hope you will register Vasaskrímsli\n"
                                                    "and trade them with many, many\l"
                                                    "other TRAINERS.\p"
                                                    "Would you like to register one of\n"
                                                    "Vasaskrímslið þitt?");
ALIGNED(4) static const u8 sText_ThankYouForRegistering[] = _("こうかんけいじばん の とうろくが\nかんりょう しました\pごりよう ありがとう\nございました！");
ALIGNED(4) static const u8 sText_NobodyHasRegistered[] = _("けいじばんに だれも ポケモンを\nとうろく していません");
ALIGNED(4) const u8 gText_UR_ChooseRequestedMonType[] = _("Veldu tegund Vasaskrímslisins\nsem þú vilt fá í skiptunum.");
ALIGNED(4) const u8 gText_UR_WhichMonWillYouOffer[] = _("Hvaða Vasaskrímsli úr hópnum þínum\nviltu bjóða í skiptum?");
ALIGNED(4) const u8 gText_UR_RegistrationCanceled[] = _("Skráningu hefur verið hætt.");
ALIGNED(4) const u8 gText_UR_RegistraionCompleted[] = _("Skráningu er lokið.");
ALIGNED(4) const u8 gText_UR_TradeCanceled[] = _("Viðskiptunum hefur verið hætt.");
ALIGNED(4) const u8 gText_UR_CancelRegistrationOfMon[] = _("Hætta við skráningu á þínu\nLv. {STR_VAR_2} {STR_VAR_1}?");
ALIGNED(4) const u8 gText_UR_CancelRegistrationOfEgg[] = _("Hætta við skráningu á þínu\nEGG?");
ALIGNED(4) const u8 gText_UR_RegistrationCanceled2[] = _("Skráningunni hefur verið hætt.");
ALIGNED(4) static const u8 sText_TradeTrainersWillBeListed[] = _("Sýni fólk sem vill\nskipta.");
ALIGNED(4) static const u8 sText_ChooseTrainerToTradeWith2[] = _("Veldu þjálfara\ntil að skipta við.");
ALIGNED(4) const u8 gText_UR_AskTrainerToMakeTrade[] = _("Viltu biðja {STR_VAR_1} um að\nskipta?");
ALIGNED(4) static const u8 sText_AwaitingResponseFromTrainer2[] = _("...\nBíð eftir svari.");
ALIGNED(4) static const u8 sText_NotRegisteredAMonForTrade[] = _("あなたが こうかんにだす\nポケモンが とうろくされていません");
ALIGNED(4) const u8 gText_UR_DontHaveTypeTrainerWants[] = _("Þú átt ekki {STR_VAR_2}-tegundar\nVasaskrímsli sem {STR_VAR_1} vill.");
ALIGNED(4) const u8 gText_UR_DontHaveEggTrainerWants[] = _("Þú átt ekki EGG sem\n{STR_VAR_1} vill.");

ALIGNED(4) static const u8 sText_PlayerCantTradeForYourMon[] = _("{STR_VAR_1} getur ekki skipt fyrir\nVasaskrímslið þitt núna.");
ALIGNED(4) static const u8 sText_CantTradeForPartnersMon[] = _("Þú getur ekki skipt fyrir\nVasaskrímsli {STR_VAR_1} núna.");

// Unused
static const u8 *const sCantTradeMonTexts[] = {
    sText_PlayerCantTradeForYourMon,
    sText_CantTradeForPartnersMon
};

ALIGNED(4) const u8 gText_UR_TradeOfferRejected[] = _("Viðskiptatilboði þínu var hafnað.");
ALIGNED(4) const u8 gText_UR_EggTrade[] = _("EGGJASKIPTI");
ALIGNED(4) const u8 gText_UR_ChooseJoinCancel[] = _("{DPAD_UPDOWN}VELJA  {A_BUTTON}TAKA ÞÁTT  {B_BUTTON}HÆTTA VIÐ");
ALIGNED(4) const u8 gText_UR_ChooseTrainer[] = _("Vinsamlegast veldu ÞJÁLFARA.");
ALIGNED(4) static const u8 sText_ChooseTrainerSingleBattle[] = _("Vinsamlegast veldu ÞJÁLFARA fyrir\nEINLEIK.");
ALIGNED(4) static const u8 sText_ChooseTrainerDoubleBattle[] = _("Vinsamlegast veldu ÞJÁLFARA fyrir\nTVÍLEIK.");
ALIGNED(4) static const u8 sText_ChooseLeaderMultiBattle[] = _("Vinsamlegast veldu LEIÐTOGANN\nfyrir FJÖLBARDAGA.");
ALIGNED(4) static const u8 sText_ChooseTrainerToTradeWith[] = _("Vinsamlegast veldu ÞJÁLFARANN til\nað skipta við.");
ALIGNED(4) static const u8 sText_ChooseTrainerToShareWonderCards[] = _("Veldu ÞJÁLFARANN sem er að deila\nUNDRAKORTUM.");
ALIGNED(4) static const u8 sText_ChooseTrainerToShareWonderNews[] = _("Veldu ÞJÁLFARANN sem er að deila\nUNDRASLÚÐRI.");
ALIGNED(4) static const u8 sText_ChooseLeaderPokemonJump[] = _("Hoppaðu með litlum Vasaskrímslum!\nVeldu LEIÐTOGANN.");
ALIGNED(4) static const u8 sText_ChooseLeaderBerryCrush[] = _("BERJAKVÖRN!\nVeldu LEIÐTOGANN.");
ALIGNED(4) static const u8 sText_ChooseLeaderBerryPicking[] = _("ÞRÍTRANA BERJATÍNSLA!\nVeldu LEIÐTOGANN.");

const u8 *const gTexts_UR_ChooseTrainer[] = {
    [LINK_GROUP_SINGLE_BATTLE] = sText_ChooseTrainerSingleBattle,
    [LINK_GROUP_DOUBLE_BATTLE] = sText_ChooseTrainerDoubleBattle,
    [LINK_GROUP_MULTI_BATTLE]  = sText_ChooseLeaderMultiBattle,
    [LINK_GROUP_TRADE]         = sText_ChooseTrainerToTradeWith,
    [LINK_GROUP_POKEMON_JUMP]  = sText_ChooseLeaderPokemonJump,
    [LINK_GROUP_BERRY_CRUSH]   = sText_ChooseLeaderBerryCrush,
    [LINK_GROUP_BERRY_PICKING] = sText_ChooseLeaderBerryPicking,
    [LINK_GROUP_WONDER_CARD]   = sText_ChooseTrainerToShareWonderCards,
    [LINK_GROUP_WONDER_NEWS]   = sText_ChooseTrainerToShareWonderNews
};

ALIGNED(4) const u8 gText_UR_SearchingForWirelessSystemWait[] = _("Leita að ÞRÁÐLAUSU SAMSKIPTA-\nKERFI. Bíddu...");
ALIGNED(4) static const u8 sText_MustHaveTwoMonsForDoubleBattle[] = _("ダブルバトルでは 2ひき いじょうの\nポケモンが ひつようです");
ALIGNED(4) const u8 gText_UR_AwaitingPlayersResponse[] = _("Bíð eftir svari {STR_VAR_1}…");
ALIGNED(4) const u8 gText_UR_PlayerHasBeenAskedToRegisterYouPleaseWait[] = _("{STR_VAR_1} hefur verið beðinn um að skrá\nþig sem meðlim. Vinsamlegast bíddu.");
ALIGNED(4) const u8 gText_UR_AwaitingResponseFromWirelessSystem[] = _("Bíð eftir svari frá\nÞRÁÐLAUSA SAMSKIPTAKERFINU.");
ALIGNED(4) static const u8 sText_PleaseWaitForOtherTrainersToGather[] = _("Bíddu þar til aðrir\nþátttakendur mæta.");

ALIGNED(4) static const u8 sText_NoCardsSharedRightNow[] = _("Engum KORTUM virðist vera deilt\nnúna.");
ALIGNED(4) static const u8 sText_NoNewsSharedRightNow[] = _("Engar FRÉTTIR virðast vera deilt\nakkúrat núna.");

const u8 *const gTexts_UR_NoWonderShared[] = {
    sText_NoCardsSharedRightNow,
    sText_NoNewsSharedRightNow
};

ALIGNED(4) const u8 gText_UR_Battle[] = _("BARDAGI");
ALIGNED(4) const u8 gText_UR_Chat2[] = _("SPJALL");
ALIGNED(4) const u8 gText_UR_Greetings[] = _("KVEÐJUR");
ALIGNED(4) const u8 gText_UR_Exit[] = _("HÆTTA");

ALIGNED(4) const u8 gText_UR_Exit2[] = _("HÆTTA");
ALIGNED(4) const u8 gText_UR_Info[] = _("UPPLÝSINGAR");
ALIGNED(4) const u8 gText_UR_NameWantedOfferLv[] = _("NAFN{CLEAR_TO 0x3C}ÓSKAÐ{CLEAR_TO 0x6E}TILBOÐ{CLEAR_TO 0xC6}STIG.");

ALIGNED(4) const u8 gText_UR_SingleBattle[] = _("EINBARDAGI");
ALIGNED(4) const u8 gText_UR_DoubleBattle[] = _("TVÍBARDAGI");
ALIGNED(4) const u8 gText_UR_MultiBattle[] = _("FJÖLBARDAGI");
ALIGNED(4) const u8 gText_UR_PokemonTrades[] = _("Vasaskrímsli TRADES");
ALIGNED(4) const u8 gText_UR_Chat[] = _("SPJALL");
ALIGNED(4) const u8 gText_UR_Cards[] = _("SPJÖLD");
ALIGNED(4) const u8 gText_UR_WonderCards[] = _("UNDURSPJÖLD");
ALIGNED(4) const u8 gText_UR_WonderNews[] = _("UNDURFRÉTTIR");
ALIGNED(4) const u8 gText_UR_PokemonJump[] = _("Vasaskrímsli JUMP");
ALIGNED(4) const u8 gText_UR_BerryCrush[] = _("BERJAKRAMNING");
ALIGNED(4) const u8 gText_UR_BerryPicking[] = _("BERJATÍNSLA");
ALIGNED(4) const u8 gText_UR_Search[] = _("LEITA");
ALIGNED(4) const u8 gText_UR_SpinTrade[] = _("Hringskipti");
ALIGNED(4) const u8 gText_UR_ItemTrade[] = _("Hlutaskipti");

ALIGNED(4) static const u8 sText_ItsNormalCard[] = _("Það er VENJULEGT KORT.");
ALIGNED(4) static const u8 sText_ItsBronzeCard[] = _("Það er BRONS KORT!");
ALIGNED(4) static const u8 sText_ItsCopperCard[] = _("Það er KOPAR KORT!");
ALIGNED(4) static const u8 sText_ItsSilverCard[] = _("Það er SILFUR KORT!");
ALIGNED(4) static const u8 sText_ItsGoldCard[] = _("Það er GULL KORT!");

const u8 *const gTexts_UR_CardColor[] = {
    sText_ItsNormalCard,
    sText_ItsBronzeCard,
    sText_ItsCopperCard,
    sText_ItsSilverCard,
    sText_ItsGoldCard
};

ALIGNED(4) const u8 gText_UR_TrainerCardInfoPage1[] = _("Þetta er ÞJÁLFARAKORTIÐ hans/hennar {DYNAMIC 0} {DYNAMIC 1}…\n{DYNAMIC 2}\pVasaDEX: {DYNAMIC 3}\nTIME:    {DYNAMIC 4}:{DYNAMIC 5}");
ALIGNED(4) const u8 gText_UR_TrainerCardInfoPage2[] = _("BATTLES: {DYNAMIC 0} WINS  {DYNAMIC 2} LOSSES\nTRADES:  {DYNAMIC 3} TIMES\p'{DYNAMIC 4} {DYNAMIC 5}\n{DYNAMIC 6} {DYNAMIC 7}'");
ALIGNED(4) static const u8 sText_GladToMeetYouMale[] = _("{DYNAMIC 1}: Gaman að hafa hitt þig!{PAUSE 60}");
ALIGNED(4) static const u8 sText_GladToMeetYouFemale[] = _("{DYNAMIC 1}: Gaman að hitta þig!{PAUSE 60}");

const u8 *const gTexts_UR_GladToMeetYou[GENDER_COUNT] = {
    sText_GladToMeetYouMale,
    sText_GladToMeetYouFemale
};

ALIGNED(4) const u8 gText_UR_FinishedCheckingPlayersTrainerCard[] = _("Finished checking {DYNAMIC 1}'s\nÞJÁLFARAKORT.{PAUSE 60}");
ALIGNED(4) static const u8 sText_CanceledReadingCard[] = _("Hætt við að lesa kortið.");

static const struct MysteryGiftClientCmd sClientScript_DynamicError[] = {
    {CLI_RECV, MG_LINKID_DYNAMIC_MSG},
    {CLI_COPY_MSG},
    {CLI_SEND_READY_END},
    {CLI_RETURN, CLI_MSG_BUFFER_FAILURE}
};

const struct MysteryGiftServerCmd gServerScript_ClientCanceledCard[] = {
    {SVR_LOAD_CLIENT_SCRIPT, PTR_ARG(sClientScript_DynamicError)},
    {SVR_SEND},
    {SVR_LOAD_MSG, PTR_ARG(sText_CanceledReadingCard)},
    {SVR_SEND},
    {SVR_RECV, MG_LINKID_READY_END},
    {SVR_RETURN, SVR_MSG_CLIENT_CANCELED}
};
