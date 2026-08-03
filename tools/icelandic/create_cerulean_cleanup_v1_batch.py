from __future__ import annotations

import argparse
import csv
import textwrap
from pathlib import Path

from common import repo_root


def t(value: str) -> str:
    return textwrap.dedent(value).strip()


TRANSLATIONS = {
    "CeruleanCity_Text_RivalIntro": t("""
        {RIVAL}: Jæja! {PLAYER}!

        Ertu enn að puða hér aftar?

        Mér gengur frábærlega!
        Ég náði fullt af sterkum og klókum
        vasaskrímslum!

        Komdu, sýndu mér hvað þú hefur náð,
        {PLAYER}!
    """),
    "CeruleanCity_Text_RivalPostBattle": t("""
        {RIVAL}: Hey, veistu hvað?

        Ég fór til BILL og fékk hann til að
        sýna mér sjaldgæfu vasaskrímslin sín.

        Það bætti helling af síðum í
        VasaDEX-ið mitt!

        Enda er BILL heimsfrægur sem
        vasaskrímslaæðingur.

        Hann fann líka upp geymslukerfið
        fyrir vasaskrímsli á PC.

        Þar sem þú notar kerfið hans ættirðu
        að fara og þakka honum.

        Jæja, ég þarf að rúlla!
        Sjáumst seinna!
    """),
    "CeruleanCity_Text_IfSlowbroWasntThereCouldCutTree": t("""
        Ef SLJÓNATAN væri ekki þarna gætirðu
        notað CUT á litla tréð.

        Þannig kæmistu hinum megin.

        Ég held samt að það sé leið í kring.
    """),
    "CeruleanCity_Text_PokemonEncyclopediaAmusing": t("""
        Ertu að búa til alfræðirit um
        vasaskrímsli?
        Það hljómar skemmtilega.
    """),
    "CeruleanCity_Text_SlowbroPayAttention": t("""
        Komdu nú, SLJÓNATAN, fylgstu með!
    """),
    "CeruleanCity_Text_HardToControlMonsObedience": t("""
        Nei! Þetta er rangt!
        Það er svo erfitt að stjórna
        vasaskrímslum!

        Hlýðni vasaskrímslisins þíns fer
        eftir hæfni þinni sem ÞJÁLFARI.
    """),
    "CeruleanCity_Text_SlowbroLoafingAround": t("""
        SLJÓNATAN er að slóra...
    """),
    "CeruleanCity_Text_ThisIsCeruleanCave": t("""
        Þetta er CERULEAN HELLIR.

        Hræðilega sterk vasaskrímsli búa þar
        inni.

        Aðeins mjög sérstakur ÞJÁLFARI fær
        að fara þar inn.

        Til að byrja með þarftu að vera nógu
        sterkur til að verða MEISTARI
        Vasaskrímsla-deildarinnar.

        Og þú þarft að hafa unnið mikið
        afrek.
    """),
    "CeruleanCity_Text_TrainerTipsHeldItems": t("""
        ÞJÁLFARA-RÁÐ

        Vasaskrímsli getur haldið á hlut.

        Sumir hlutir geta jafnvel nýst
        vasaskrímslinu sem heldur á þeim í
        bardaga.
    """),
    "CeruleanCity_Text_GymSign": t("""
        CERULEAN BORG VASASKRÍMSLA-SALUR
        SALSTJÓRI: MISTY
        Hressilega hafmeyjan!
    """),
    "CeruleanCity_Gym_Text_MistyIntro": t("""
        Hæ, nýtt andlit!

        Aðeins þeir ÞJÁLFARAR sem hafa stefnu
        um vasaskrímsli geta orðið atvinnumenn.

        Hver er þín nálgun þegar þú nærð og
        þjálfar vasaskrímsli?

        Mín stefna er sókn af fullum krafti
        með VATNS-gerðar vasaskrímslum!{PLAY_BGM}{MUS_ENCOUNTER_GYM_LEADER}
    """),
    "CeruleanCity_Gym_Text_ExplainTM03": t("""
        TM03 kennir VATNSBYLGJU.

        Notaðu hana á vatnavasaskrímsli!
    """),
    "CeruleanCity_Gym_Text_ExplainCascadeBadge": t("""
        FOSSMERKIÐ lætur öll vasaskrímsli
        upp að Lv. 30 hlýða.

        Það gildir líka um þau sem þú færð í
        skiptum.

        Og fleira: nú geturðu notað CUT
        hvenær sem er, jafnvel utan bardaga.

        Þú getur notað CUT til að fella lítil
        tré og opna nýjar leiðir.

        Þú mátt líka fá uppáhalds TM-ið mitt.
    """),
    "CeruleanCity_Gym_Text_GymGuyAdvice": t("""
        Yo!
        Verðandi meistari!

        Leyfðu mér að gefa þér ráð!

        SALSTJÓRINN, MISTY, er atvinnukona
        sem notar VATNS-gerðar vasaskrímsli.

        Þú getur sogið allt vatnið úr þeim
        með GRAS-gerðar vasaskrímslum.

        Eða þú getur notað RAFMAGNS-gerðar
        vasaskrímsli og lostið þau!
    """),
    "CeruleanCity_Gym_Text_GymStatue": t("""
        CERULEAN VASASKRÍMSLA-SALUR
        SALSTJÓRI: MISTY

        SIGURÞJÁLFARAR:
        {RIVAL}
    """),
    "CeruleanCity_Gym_Text_GymStatuePlayerWon": t("""
        CERULEAN VASASKRÍMSLA-SALUR
        SALSTJÓRI: MISTY

        SIGURÞJÁLFARAR:
        {RIVAL}, {PLAYER}
    """),
    "CeruleanCity_House1_Text_BadgesHaveAmazingSecrets": t("""
        Aðeins hæfir ÞJÁLFARAR geta safnað
        vasaskrímsla-MERKJUM.

        Ég sé að þú ert með að minnsta kosti
        eitt.

        Þessi MERKI geyma ótrúleg
        leyndarmál, vissirðu það?
    """),
    "CeruleanCity_House1_Text_AttackStatFlash": t("""
        ATTACK gildi allra vasaskrímslanna
        þinna hækkar örlítið.

        Það leyfir þér líka að nota FLASH
        utan bardaga.
    """),
    "CeruleanCity_House1_Text_ObeyLv30Cut": t("""
        Vasaskrímsli upp að Lv. 30 hlýða
        þér.

        Það gildir líka um þau sem þú færð í
        skiptum.

        Vasaskrímsli á hærri stigum verða þó
        óstýrilát í bardaga.

        Það leyfir þér líka að nota CUT utan
        bardaga.
    """),
    "CeruleanCity_House1_Text_SpeedStatFly": t("""
        SPEED gildi allra vasaskrímslanna
        þinna hækkar örlítið.

        Það leyfir þér líka að nota FLY utan
        bardaga.
    """),
    "CeruleanCity_House1_Text_ObeyLv50Strength": t("""
        Vasaskrímsli upp að Lv. 50 hlýða
        þér.

        Það gildir líka um þau sem þú færð í
        skiptum.

        Vasaskrímsli á hærri stigum verða þó
        óstýrilát í bardaga.

        Það leyfir þér líka að nota STRENGTH
        utan bardaga.
    """),
    "CeruleanCity_House1_Text_DefenseStatSurf": t("""
        DEFENSE gildi allra vasaskrímslanna
        þinna hækkar örlítið.

        Það leyfir þér líka að nota SURF utan
        bardaga.
    """),
    "CeruleanCity_House1_Text_ObeyLv70RockSmash": t("""
        Vasaskrímsli upp að Lv. 70 hlýða
        þér.

        Það gildir líka um þau sem þú færð í
        skiptum.

        Vasaskrímsli á hærri stigum verða þó
        óstýrilát í bardaga.

        Það leyfir þér líka að nota ROCK
        SMASH utan bardaga.
    """),
    "CeruleanCity_House1_Text_SpStatsWaterfall": t("""
        SP. ATK og SP. DEF gildi allra
        vasaskrímslanna þinna hækka örlítið.

        Það leyfir þér líka að nota WATERFALL
        utan bardaga.
    """),
    "CeruleanCity_House1_Text_AllMonsWillObeyYou": t("""
        Öll vasaskrímsli hlýða þér!
    """),
    "CeruleanCity_House2_Text_RocketsStoleTMForDig": t("""
        Þessir ömurlegu ROCKETAR!

        Sjáðu hvað þeir hafa gert við húsið
        mitt!

        Þeir stálu TM-i sem kennir
        vasaskrímslum að grafa holur með DIG!

        Ég ætlaði að nota það á SKAPKÖTT eða
        SANDSNJÁLD...

        Þetta kostaði mig skildinginn!
    """),
    "CeruleanCity_House2_Text_TeachDiglettDigWithoutTM": t("""
        Ég hugsa að það sem er glatað sé
        glatað.

        Ég ákvað að kenna GRAFLARA að nota
        DIG án TM.
    """),
    "CeruleanCity_House3_Text_PleaseTradeWithMyHusband": t("""
        Maðurinn minn hefur gaman af að
        skipta á vasaskrímslum.

        Þú ert að safna vasaskrímslum fyrir
        VasaDEX-ið þitt, ekki satt?

        Viltu gera svo vel að skipta við
        hann?
    """),
    "CeruleanCity_House1_Text_GoCrushBerriesAtDirectCorner": t("""
        Það er eitthvað nýtt á annarri hæð
        vasaskrímslamiðstöðva, í DIRECT
        CORNER.

        Þar var sett upp Wireless Adapter vél
        til að mylja BER.

        Þarna kemur þú til sögunnar.

        Ég þarf að biðja þig um greiða sem ég
        get aðeins treyst þér fyrir.

        Geturðu búið til BERJADUFT fyrir mig
        með vélinni?

        Ekki gleyma, vélin er í DIRECT CORNER
        í vasaskrímslamiðstöðvum.

        Ég blanda lyf fyrir þig ef þú kemur
        með BERJADUFT.

        Ekki gleyma, myldu BER í BERJADUFT
        og komdu með það til mín.
    """),
    "CeruleanCity_Mart_Text_RepelWorksOnWeakMons": t("""
        REPEL heldur ekki bara pöddum frá,
        það virkar líka á veik vasaskrímsli.

        Settu sterkasta vasaskrímslið þitt
        fremst á vasaskrímsla-LISTANN.

        Ef fyrsta vasaskrímslið þitt er
        sterkt verður áhrif REPEL meiri.
    """),
    "CeruleanCity_Mart_Text_DoYouKnowAboutRareCandy": t("""
        Veistu um RARE CANDY?
        Það er ekki selt í búðum.

        Ég held að það láti vasaskrímsli
        vaxa mjög hratt allt í einu.
    """),
    "CeruleanCity_PokemonCenter_1F_Text_BillDoesWhateverForRareMons": t("""
        Þessi BILL!

        Ég heyrði að hann geri hvað sem er
        til að ná sjaldgæfum vasaskrímslum.

        Hann hikar víst ekki við alls konar
        hluti.
    """),
    "CeruleanCity_PokemonCenter_1F_Text_EveryoneCallsBillPokemaniac": t("""
        Hefurðu heyrt um BILL?

        Allir kalla hann vasaskrímslaæðing!

        Ég held samt að fólk öfundi BILL
        bara.

        Hver myndi ekki vilja monta sig af
        vasaskrímslunum sínum?
    """),
    "CeruleanCity_PokemonCenter_1F_Text_BillCollectsRareMons": t("""
        BILL á fullt af vasaskrímslum!
        Hann safnar líka sjaldgæfum!
    """),
    "CeruleanCity_PokemonCenter_1F_Text_TryTradingUpstairs": t("""
        Af hverju ferðu ekki upp og prófar að
        skipta á vasaskrímslum við vini þína?

        Þú getur fengið miklu meiri
        fjölbreytni með skiptum.

        Vasaskrímslin sem þú færð í skiptum
        vaxa líka hratt.
    """),
    "Route24_Text_JoinTeamRocket": t("""
        Að öðru leyti, hvernig litist þér á
        að ganga í ROCKET-GENGIÐ?

        Við erum hópur atvinnuglæpamanna sem
        sérhæfir sig í vasaskrímslum!

        Viltu ganga í liðið?

        Ertu viss?

        Komdu nú, gakktu til liðs við okkur!

        Ég segi þér að ganga í liðið!

        ...Allt í lagi, þú þarft sannfæringu!

        Ég geri þér tilboð sem þú getur ekki
        hafnað!
    """),
    "Route25_Text_JoeyPostBattle": t("""
        Öll vasaskrímsli hafa veikleika.
        Jafnvel þau sterkustu.

        Þess vegna er best að þjálfa
        vasaskrímsli af ólíkum gerðum.
    """),
    "Route25_Text_ChadPostBattle": t("""
        Ef vasaskrímslið þitt ruglast skaltu
        skipta því út.

        Það er góð aðferð.
    """),
    "Route25_Text_HaleyIntro": t("""
        Vinkona mín á mörg sæt vasaskrímsli.
        Ég er svo öfundsjúk!
    """),
    "Route25_Text_HaleyPostBattle": t("""
        Komstu frá MÁNAFJALLI?
        Má ég fá BLEIKÁLF?
    """),
    "Route25_Text_FranklinPostBattle": t("""
        Fjandinn!
        BLAKILDI beit mig þarna inni í
        hellinum.
    """),
    "Route25_Text_NobPostBattle": t("""
        Vasaskrímslaæðingurinn stendur svo
        sannarlega undir nafninu.

        Safnið hans inniheldur margar
        sjaldgæfar tegundir vasaskrímsla.
    """),
    "Route25_SeaCottage_Text_ImBillHelpMeOutPal": t("""
        Hæ! Ég er vasaskrímsli...
        ...Nei, ég er það ekki!

        Kallaðu mig BILL!
        Ég er sannkallaður vasaskrímslaæðingur!

        Hey!
        Hvað á þetta tortryggna augnaráð að
        þýða?

        Ég er ekki að plata þig, félagi.

        Ég klúðraði tilraun og sameinaðist
        vasaskrímsli!

        Svo, hvað segirðu?
        Hjálpaðu mér hér!
    """),
    "Route25_SeaCottage_Text_ImBillHelpMeOutLady": t("""
        Hæ! Ég er vasaskrímsli...
        ...Nei, ég er það ekki!

        Kallaðu mig BILL!
        Ég er sannkallaður vasaskrímslaæðingur!

        Hey!
        Hvað á þetta tortryggna augnaráð að
        þýða?

        Ég er ekki að plata þig, dama.

        Ég klúðraði tilraun og sameinaðist
        vasaskrímsli!

        Svo, hvað segirðu?
        Hjálpaðu mér hér!
    """),
    "Route25_SeaCottage_Text_ThanksBudTakeThis": t("""
        BILL: Jááá!
        Takk, vinur! Ég skulda þér greiða!

        Komstu þá til að sjá
        vasaskrímslasafnið mitt?

        Ekki?
        Það er svekkjandi.

        Ég verð samt að þakka þér...
        Ó, hér, kannski dugar þetta.
    """),
    "Route25_SeaCottage_Text_ThanksLadyTakeThis": t("""
        BILL: Jááá!
        Takk, vinkona! Ég skulda þér greiða!

        Komstu þá til að sjá
        vasaskrímslasafnið mitt?

        Ekki?
        Það er svekkjandi.

        Ég verð samt að þakka þér...
        Ó, hér, kannski dugar þetta.
    """),
    "Route25_SeaCottage_Text_CheckOutRareMonsOnPC": t("""
        BILL: Viltu skoða nokkur af
        sjaldgæfu vasaskrímslunum mínum á
        PC-inum?

        Endilega, skoðaðu PC-inn minn.
    """),
    "Route25_SeaCottage_Text_BillsFavoriteMonList": t("""
        Uppáhalds vasaskrímslalisti BILL!
    """),
    "Route25_SeaCottage_Text_SeeWhichMon": t("""
        Hvaða vasaskrímsli viltu sjá?
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
    parser.add_argument("--queue", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-after-cerulean-v1.csv")
    parser.add_argument("--output", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-cerulean-cleanup-v1.csv")
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
        row["notes"] = "codex curated Cerulean semi-English cleanup v1"
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
