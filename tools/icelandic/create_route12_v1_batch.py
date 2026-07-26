from __future__ import annotations

import argparse
import csv
import textwrap
from pathlib import Path

from common import repo_root


def t(value: str) -> str:
    return textwrap.dedent(value).strip()


TRANSLATIONS = {
    "Route12_Text_MonSprawledOutInSlumber": t("""
        Vasaskrímsli liggur endilangt og sefur
        djúpum, værum svefni.
    """),
    "Text_SnorlaxWokeUp": t("""
        HROTÞURS vaknaði!

        Hann réðst á í fúlu bræði!
    """),
    "Text_SnorlaxReturnedToMountains": t("""
        HROTÞURS róaðist.
        Hann geispaði risastórt...
        Og sneri aftur til fjallanna.
    """),
    "Text_WantToUsePokeFlute": t("""
        Viltu nota VASAFLAUTU?
    """),
    "Text_PlayedPokeFlute": t("""
        {PLAYER} lék á VASAFLAUTU.
    """),
    "Route12_Text_NedIntro": t("""
        Já!
        Það beit á hér!
    """),
    "Route12_Text_NedDefeat": t("""
        Tsk!
        Bara smáfiskur...
    """),
    "Route12_Text_NedPostBattle": t("""
        Bíddu!
        Línan mín festist!
    """),
    "Route12_Text_ChipIntro": t("""
        Vertu þolinmóður.
        Veiði er biðleikur.
    """),
    "Route12_Text_ChipDefeat": t("""
        Þessi slapp!
    """),
    "Route12_Text_ChipPostBattle": t("""
        Með betri stöng gæti ég veitt betri
        vasaskrímsli...
    """),
    "Route12_Text_JustinIntro": t("""
        Ég er að leita að TUNGLSTEINI.
        Hefurðu fundið einn?
    """),
    "Route12_Text_JustinDefeat": t("""
        Ái!
    """),
    "Route12_Text_JustinPostBattle": t("""
        Ég hefði getað látið vasaskrímslið
        mitt þróast með TUNGLSTEINI.

        Þá hefði ég unnið, held ég.
    """),
    "Route12_Text_LucaIntro": t("""
        Rafmagn er mín sérgrein.

        Ég veit samt ekkert um vasaskrímsli
        hafsins.
    """),
    "Route12_Text_LucaDefeat": t("""
        Tekinn úr sambandi!
    """),
    "Route12_Text_LucaPostBattle": t("""
        Vatn leiðir rafmagn, svo þú ættir að
        stuðla sjó-vasaskrímsli.
    """),
    "Route12_Text_HankIntro": t("""
        VEIÐIFÍKILLINN gegn
        VASASKRÍMSLAKRAKKANUM!
    """),
    "Route12_Text_HankDefeat": t("""
        Aðeins of mikið!
    """),
    "Route12_Text_HankPostBattle": t("""
        Ætli maður verði góður í því sem
        manni finnst skemmtilegt.

        Þú vannst mig í vasaskrímslum, en
        nærð mér ekki í veiði.
    """),
    "Route12_Text_ElliotIntro": t("""
        Ég elska veiði, ekki misskilja mig.

        En það væri best ef ég hefði líka
        meiri vinnu.
    """),
    "Route12_Text_ElliotDefeat": t("""
        Það er ekki auðvelt...
    """),
    "Route12_Text_ElliotPostBattle": t("""
        Það er í lagi.
        Töpin fara ekki lengur í taugarnar á
        mér.
    """),
    "Route12_Text_AndrewIntro": t("""
        Hvað er að bíta?

        Maður veit aldrei hvað gæti komið á
        öngulinn!
    """),
    "Route12_Text_AndrewDefeat": t("""
        Missti það!
    """),
    "Route12_Text_AndrewPostBattle": t("""
        Hvað, GREYSLEPPA?

        Ég veiði þær alltaf, jú.
        En þær eru nú ansi veikburða.
    """),
    "Route12_Text_RouteSign": t("""
        ROUTE 12
        Norður til LAVENDER
    """),
    "Route12_Text_SportfishingArea": t("""
        SPORTVEIÐISVÆÐI
    """),
    "Route12_Text_JesIntro": t("""
        JES: Ef ég vinn ætla ég að biðja GIA
        um að giftast mér.
    """),
    "Route12_Text_JesDefeat": t("""
        JES: Ó, gerðu það, af hverju máttum
        við ekki vinna?
    """),
    "Route12_Text_JesPostBattle": t("""
        JES: Ó, GIA, fyrirgefðu mér,
        ástin mín!
    """),
    "Route12_Text_JesNotEnoughMons": t("""
        JES: GIA og ég verðum saman að eilífu.

        Við berjumst ekki nema þú sért með
        tvö eigin vasaskrímsli.
    """),
    "Route12_Text_GiaIntro": t("""
        GIA: Heyrðu, JES...

        Ef við vinnum giftist ég þér!
    """),
    "Route12_Text_GiaDefeat": t("""
        GIA: Ó, en hvers vegna?
    """),
    "Route12_Text_GiaPostBattle": t("""
        GIA: JES, kjáninn þinn!
        Þú eyðilagðir þetta!
    """),
    "Route12_Text_GiaNotEnoughMons": t("""
        GIA: Ég þoli ekki að berjast án
        JES míns!

        Áttu ekki eitt vasaskrímsli í viðbót?
    """),
    "Route12_FishingHouse_Text_DoYouLikeToFish": t("""
        Ég er yngri bróðir VEIÐISPEKINGSINS.

        Ég eeeelska einfaldlega veiði!
        Ég þoli ekki að vera án hennar.

        Segðu mér, finnst þér gaman að veiða?
    """),
    "Route12_FishingHouse_Text_TakeThisAndFish": t("""
        Stórkostlegt! Mér líkar stíllinn þinn.
        Ég held að við getum orðið vinir.

        Taktu þetta og veiddu, ungi vinur!
    """),
    "Route12_FishingHouse_Text_ReceivedSuperRod": t("""
        {PLAYER} fékk OFURSTÖNG frá bróður
        VEIÐISPEKINGSINS.
    """),
    "Route12_FishingHouse_Text_IfYouCatchBigMagikarpShowMe": t("""
        Veiði er lífsmáti!
        Hún er eins og fínasti skáldskapur.

        Frá höfum til áa, farðu út og náðu
        þeim stóra, vinur minn.

        Nú hef ég eina bón.

        Ef þú veiðir stóra GREYSLEPPU með
        þessari stöng vil ég sjá hana.

        Eins mikið og ég elska að veiða, elska
        ég líka að sjá risastórar GREYSLEPPUR.
    """),
    "Route12_FishingHouse_Text_OhThatsDisappointing": t("""
        Ó...
        Það veldur svo miklum vonbrigðum...
    """),
    "Route12_FishingHouse_Text_TryFishingBringMeMagikarp": t("""
        Halló þarna, {PLAYER}!
        Hefurðu verið að veiða?

        Prófaðu OFURSTÖNGINA í hvaða vatni
        sem er.

        Þú finnur ólík vasaskrímsli á ólíkum
        stöðum.

        Ó, og gleymdu ekki að færa mér
        risavaxna GREYSLEPPU.
    """),
    "Route12_FishingHouse_Text_OhMagikarpAllowMeToSee": t("""
        Ó? {PLAYER}?
        Er þetta ekki GREYSLEPPA!

        Leyfðu mér að sjá hana, fljótt!
    """),
    "Route12_FishingHouse_Text_WhoaXInchesTakeThis": t("""
        ... ... ...Vá!
        {STR_VAR_2} tommur!

        Þú kannt greinilega að meta hina
        fínu, ljóðrænu hlið veiðinnar!

        Þú verður að taka þetta.
        Ég heimta það!
    """),
    "Route12_FishingHouse_Text_LookForwardToGreaterRecords": t("""
        Ég hlakka til að sjá enn stærri met
        frá þér!
    """),
    "Route12_FishingHouse_Text_HuhXInchesSameSizeAsLast": t("""
        Ha?
        {STR_VAR_2} tommur?

        Hún er jafnstór og sú sem ég sá áður.
    """),
    "Route12_FishingHouse_Text_HmmXInchesDoesntMeasureUp": t("""
        Hmm...
        Þessi er {STR_VAR_2} tommur á lengd.

        Hún jafnast ekki á við
        {STR_VAR_3} tommu GREYSLEPPUNA sem þú
        færðir mér áður.
    """),
    "Route12_FishingHouse_Text_DoesntLookLikeMagikarp": t("""
        Uh...
        Þetta lítur ekki mikið út eins og
        GREYSLEPPA.
    """),
    "Route12_FishingHouse_Text_NoRoomForGift": t("""
        Ó, nei!

        Ég var með gjöf handa þér, en þú
        hefur ekkert pláss fyrir hana.
    """),
    "Route12_FishingHouse_Text_MostGiganticMagikarpXInches": t("""
        Stærsta GREYSLEPPA sem ég hef nokkru
        sinni séð...

        {STR_VAR_3} tommur!
    """),
    "Route12_FishingHouse_Text_BlankChartOfSomeSort": t("""
        Þetta er einhvers konar autt tafla.

        Þar eru reitir til að skrá einhvers
        konar met.
    """),
    "Route12_NorthEntrance_1F_Text_LookoutSpotUpstairs": t("""
        Það er útsýnisstaður á efri hæðinni.
        Útsýnið er stórfenglegt.
    """),
    "Route12_NorthEntrance_2F_Text_TakeTMDontNeedAnymoreMale": t("""
        Aska vasaskrímslisins míns er geymd í
        VASASKRÍMSLATURNI.

        Þú mátt fá þetta TM.
        Ég þarf það ekki lengur...
    """),
    "Route12_NorthEntrance_2F_Text_TakeTMDontNeedAnymoreFemale": t("""
        Aska vasaskrímslisins míns er geymd í
        VASASKRÍMSLATURNI.

        Þú mátt fá þetta TM.
        Ég þarf það ekki lengur...
    """),
    "Route12_NorthEntrance_2F_Text_ReceivedTM27FromLittleGirl": t("""
        {PLAYER} fékk TM27 frá litlu
        stúlkunni.
    """),
    "Route12_NorthEntrance_2F_Text_ExplainTM27": t("""
        TM27 er hreyfing sem kallast
        ENDURGJALD...

        Ef þú kemur vel fram við vasaskrímslið
        þitt endurgeldur það ástina með því
        að leggja sig allt fram í bardaga.
    """),
    "Route12_NorthEntrance_2F_Text_DontHaveRoomForThis": t("""
        Þú hefur ekkert pláss fyrir þetta.
    """),
    "Route12_NorthEntrance_2F_Text_TheresManFishing": t("""
        Sjáum hvað sjónaukinn sýnir...

        Það er maður að veiða!
    """),
    "Route12_NorthEntrance_2F_Text_ItsPokemonTower": t("""
        Sjáum hvað sjónaukinn sýnir...

        Það er VASASKRÍMSLATURN!
    """),
}


FILES = {
    "data/maps/Route12/text.inc",
    "data/maps/Route12_FishingHouse/text.inc",
    "data/maps/Route12_NorthEntrance_1F/text.inc",
    "data/maps/Route12_NorthEntrance_2F/text.inc",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-after-v13.csv")
    parser.add_argument("--output", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-route12-v1.csv")
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
        row["notes"] = "codex curated Route 12 and fishing house v1"
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
