from __future__ import annotations

import argparse
import csv
import textwrap
from pathlib import Path

from common import repo_root


def t(value: str) -> str:
    return textwrap.dedent(value).strip()


TRANSLATIONS = {
    "Route19_Text_RichardIntro": t("""
        Ég þarf að æfa mig og hita upp áður
        en ég fer út að synda.
    """),
    "Route19_Text_RichardDefeat": t("""
        Alveg orðinn heitur!
    """),
    "Route19_Text_RichardPostBattle": t("""
        Takk, krakki!
        Ég er tilbúinn í sund.
    """),
    "Route19_Text_ReeceIntro": t("""
        Bíddu! Hægðu á þér!
        Þú færð hjartaáfall!
    """),
    "Route19_Text_ReeceDefeat": t("""
        Úú!
        Þetta er kalt!
    """),
    "Route19_Text_ReecePostBattle": t("""
        Passaðu þig á HOLSEPI.
        Þau stinga svo sársaukafullt.
    """),
    "Route19_Text_MatthewIntro": t("""
        Ég elska sund!
        Hvað með þig?
    """),
    "Route19_Text_MatthewDefeat": t("""
        Magalending!
    """),
    "Route19_Text_MatthewPostBattle": t("""
        Ég get meira að segja unnið
        sjó-vasaskrímsli í sundi.
    """),
    "Route19_Text_DouglasIntro": t("""
        Hvað er handan sjóndeildarhringsins?
    """),
    "Route19_Text_DouglasDefeat": t("""
        Glúbb!
    """),
    "Route19_Text_DouglasPostBattle": t("""
        Ég sé nokkrar eyjar þarna úti!
    """),
    "Route19_Text_DavidIntro": t("""
        Ég reyndi að kafa eftir vasaskrímslum,
        en það gekk ekkert.
    """),
    "Route19_Text_DavidDefeat": t("""
        Hjálp!
    """),
    "Route19_Text_DavidPostBattle": t("""
        Ætli maður þurfi að veiða
        sjó-vasaskrímsli.
    """),
    "Route19_Text_TonyIntro": t("""
        Ég horfi á sjóinn til að gleyma öllu
        slæmu sem gerðist.
    """),
    "Route19_Text_TonyDefeat": t("""
        Úú!
        Áfall!
    """),
    "Route19_Text_TonyPostBattle": t("""
        Ég horfi á sjóinn til að gleyma því
        slæma sem gerðist!
    """),
    "Route19_Text_AnyaIntro": t("""
        Ó, ég elska fararskjótann þinn!
        Má ég fá hann ef ég vinn?
    """),
    "Route19_Text_AnyaDefeat": t("""
        Ó!
        Ég tapaði!
    """),
    "Route19_Text_AnyaPostBattle": t("""
        Það er enn langt til SEAFOAM EYJA...

        Mig langar aftur til FUCHSIA...
    """),
    "Route19_Text_AliceIntro": t("""
        Sund er frábært!
        Sólbruni er það ekki!
    """),
    "Route19_Text_AliceDefeat": t("""
        Stuð!
    """),
    "Route19_Text_AlicePostBattle": t("""
        Kærastinn minn vildi synda til
        SEAFOAM EYJA.
    """),
    "Route19_Text_AxleIntro": t("""
        Ahoy, þarna!
        Þessi vötn eru varasöm!
    """),
    "Route19_Text_AxleDefeat": t("""
        Úú!
        Hættulegt!
    """),
    "Route19_Text_AxlePostBattle": t("""
        F-fæturnir mínir!
        Þeir krumpuðust!
        Glúbb, glúbb...
    """),
    "Route19_Text_ConnieIntro": t("""
        Ég synti hingað með vinum mínum...
        Ég er þreytt...
    """),
    "Route19_Text_ConnieDefeat": t("""
        Ég er örmagna...
    """),
    "Route19_Text_ConniePostBattle": t("""
        Ef ég ætti að ríða vasaskrímsli á
        sjónum myndi ég vilja LAGARGANDU.

        LAGARGANDU er svo stór að ég veðja að
        hún héldi mér þurrum á vatninu.
    """),
    "Route19_Text_RouteSign": t("""
        SJÓLEIÐ 19
        FUCHSIA BORG - SEAFOAM EYJAR
    """),
    "Route19_Text_LiaIntro": t("""
        LIA: Ég passa litla bróður minn.
        Hann varð nýlega ÞJÁLFARI.
    """),
    "Route19_Text_LiaDefeat": t("""
        LIA: Svona kemur maður ekki fram við
        litla bróður minn!
    """),
    "Route19_Text_LiaPostBattle": t("""
        LIA: Áttu yngri bróður?

        Ég vona að þú sért að kenna honum
        alls konar hluti.
    """),
    "Route19_Text_LiaNotEnoughMons": t("""
        LIA: Ég vil berjast með litla bróður
        mínum.

        Áttu ekki tvö vasaskrímsli?
    """),
    "Route19_Text_LucIntro": t("""
        LUC: Stóra systir kenndi mér að synda
        og þjálfa vasaskrímsli.
    """),
    "Route19_Text_LucDefeat": t("""
        LUC: Ó, vá!
        Einhver sterkari en stóra systir!
    """),
    "Route19_Text_LucPostBattle": t("""
        LUC: Stóra systir er sterk og góð.
        Mér finnst hún frábær!
    """),
    "Route19_Text_LucNotEnoughMons": t("""
        LUC: Ég vil ekki gera þetta nema ég
        geti barist við þig með stóru systur.

        Áttu ekki tvö vasaskrímsli?
    """),
    "Route20_Text_BarryIntro": t("""
        Vatnið er grunnt hér.
        Margt fólk er að synda.
    """),
    "Route20_Text_BarryDefeat": t("""
        Skvamp!
    """),
    "Route20_Text_BarryPostBattle": t("""
        Ég vildi að ég gæti riðið
        vasaskrímslinu mínu.
        Ég veðja að þú sért ekki þreyttur.
    """),
    "Route20_Text_ShirleyIntro": t("""
        SEAFOAM er kyrrlátur felustaður.
        Ég er í fríi hér.
    """),
    "Route20_Text_ShirleyDefeat": t("""
        Hættu þessu!
    """),
    "Route20_Text_ShirleyPostBattle": t("""
        Það er risastór hellir undir þessari
        eyju.
    """),
    "Route20_Text_TiffanyIntro": t("""
        Ég elska að fljóta með fiskunum hér
        á öldunum.
    """),
    "Route20_Text_TiffanyDefeat": t("""
        Ái!
    """),
    "Route20_Text_TiffanyPostBattle": t("""
        Viltu fljóta með mér?
    """),
    "Route20_Text_IreneIntro": t("""
        Ertu líka í fríi?
    """),
    "Route20_Text_IreneDefeat": t("""
        Engin miskunn!
    """),
    "Route20_Text_IrenePostBattle": t("""
        SEAFOAM var ein stór eyja í fjarlægri
        fortíð.
    """),
    "Route20_Text_DeanIntro": t("""
        Skoðaðu stælta skrokkinn minn!
    """),
    "Route20_Text_DeanDefeat": t("""
        Aumingjalegt!
    """),
    "Route20_Text_DeanPostBattle": t("""
        Ég hefði átt að styrkja vasaskrímslin
        mín, ekki sjálfan mig!
    """),
    "Route20_Text_DarrinIntro": t("""
        Af hverju ríðurðu vasaskrímsli?
        Kanntu ekki að synda?
    """),
    "Route20_Text_DarrinDefeat": t("""
        Ái!
        Torpedó!
    """),
    "Route20_Text_DarrinPostBattle": t("""
        Það lítur sannarlega skemmtilega út að
        ríða vasaskrímsli!
    """),
    "Route20_Text_RogerIntro": t("""
        Ég reið fugla-vasaskrímslinu mínu
        hingað.
    """),
    "Route20_Text_RogerDefeat": t("""
        Ó, nei!
        Hvað á ég nú að gera?
    """),
    "Route20_Text_RogerPostBattle": t("""
        Fuglarnir mínir eru örmagna.
        Þeir geta ekki flogið mér til baka!
    """),
    "Route20_Text_NoraIntro": t("""
        Kærastinn minn gaf mér stórar perlur.
    """),
    "Route20_Text_NoraDefeat": t("""
        Ó, nei!
        Perlurnar mínar voru í þeim!
    """),
    "Route20_Text_NoraPostBattle": t("""
        Munu perlurnar mínar stækka inni í
        VÍGULKERI?
    """),
    "Route20_Text_MissyIntro": t("""
        Ég synti hingað frá CINNABAR EYJU.
        Það var ekki auðvelt, segi ég þér.
    """),
    "Route20_Text_MissyDefeat": t("""
        Ég er svo vonsvikin!
    """),
    "Route20_Text_MissyPostBattle": t("""
        Vasaskrímsli hafa lagt undir sig
        yfirgefið herrasetur á CINNABAR.

        Þau kalla það VASASKRÍMSLAHERRASETRIÐ
        núna.
    """),
    "Route20_Text_MelissaIntro": t("""
        CINNABAR í vestri er með rannsóknarstofu
        fyrir vasaskrímsli.

        Pabbi minn vinnur þar.
    """),
    "Route20_Text_MelissaDefeat": t("""
        Bíddu!
        Þú átt að bíða!
    """),
    "Route20_Text_MelissaPostBattle": t("""
        CINNABAR er eldfjallaeyja.

        Ég heyrði að hún hafi risið úr sjónum
        þegar eldfjall gaus.
    """),
    "Route20_Text_SeafoamIslands": t("""
        SEAFOAM EYJAR
    """),
    "Route20_Text_MistyTrainsHere": t("""
        Sterkir ÞJÁLFARAR og
        VATNS-vasaskrímsli sjást oft hér um
        slóðir.

        Þeir segja að MISTY úr CERULEAN SAL
        æfi hér.
    """),
    "Route21_North_Text_RonaldIntro": t("""
        Viltu vita hvort fiskarnir séu að bíta?
    """),
    "Route21_North_Text_RonaldDefeat": t("""
        Fjandinn!
    """),
    "Route21_North_Text_RonaldPostBattle": t("""
        Ég næ engu góðu.
        Ekki eitt gott vasaskrímsli að fá!
    """),
    "Route21_North_Text_WadeIntro": t("""
        Ég fékk stóran afla!
        Viltu reyna?
    """),
    "Route21_North_Text_WadeDefeat": t("""
        Heheh, GREYSLEPPUR standast ekki
        kröfurnar, er það nokkuð?
    """),
    "Route21_North_Text_WadePostBattle": t("""
        Ég virðist bara ná GREYSLEPPUM!
    """),
    "Route21_North_Text_SpencerIntro": t("""
        Sjórinn hreinsar líkama minn og sál!
    """),
    "Route21_North_Text_SpencerDefeat": t("""
        Ayah!
    """),
    "Route21_North_Text_SpencerPostBattle": t("""
        Sjórinn er frábær og allt það, en mér
        líkar líka við fjöllin.
    """),
    "Route21_North_Text_CueBallIntro": t("""
        Ég kem nú stundum líka að synda!
    """),
    "Route21_North_Text_CueBallDefeat": t("""
        Gwaa!
    """),
    "Route21_North_Text_CueBallPostBattle": t("""
        Heldurðu að ég fljóti auðveldlega?
        Þegiðu, það kemur þér ekkert við!
    """),
    "Route21_South_Text_JackIntro": t("""
        Ég náði vasaskrímslinu mínu úti á sjó.
    """),
    "Route21_South_Text_JackDefeat": t("""
        Kafari!!
        Niður!!
    """),
    "Route21_South_Text_JackPostBattle": t("""
        Hvar náðir þú vasaskrímslinu þínu?
    """),
    "Route21_South_Text_JeromeIntro": t("""
        Núna er ég í þríþrautarmóti.
    """),
    "Route21_South_Text_JeromeDefeat": t("""
        Más... Más... Más...
    """),
    "Route21_South_Text_JeromePostBattle": t("""
        Ég er búinn!
        En ég á enn hjólakeppnina og
        maraþonið eftir!
    """),
    "Route21_South_Text_RolandIntro": t("""
        Ahh!
        Finndu sólina og vindinn!
    """),
    "Route21_South_Text_RolandDefeat": t("""
        Vá!
        Ég tapaði!
    """),
    "Route21_South_Text_RolandPostBattle": t("""
        Ég er brunninn eins og skorpa!
    """),
    "Route21_South_Text_ClaudeIntro": t("""
        Hey, ekki fæla fiskana burt!
    """),
    "Route21_South_Text_ClaudeDefeat": t("""
        Fyrirgefðu!
        Ég er bara svo pirraður yfir að ná
        engu.
    """),
    "Route21_South_Text_ClaudePostBattle": t("""
        Ansans, ég hef ekki náð neinu.

        Gæti þessi staður í raun verið risastór
        sundlaug eða eitthvað?
    """),
    "Route21_South_Text_NolanIntro": t("""
        Haltu mér félagsskap þar til það bítur.
    """),
    "Route21_South_Text_NolanDefeat": t("""
        Þetta drap smá tíma.
    """),
    "Route21_South_Text_NolanPostBattle": t("""
        Ó, bíddu!
        Það beit á!
        Já!
    """),
    "Route21_North_Text_LilIntro": t("""
        LIL: Ha? Bardagi?
        IAN, geturðu ekki gert þetta einn?
    """),
    "Route21_North_Text_LilDefeat": t("""
        LIL: Ó, sérðu?
        Við töpuðum. Ánægður núna?
    """),
    "Route21_North_Text_LilPostBattle": t("""
        LIL: Ég er þreytt.
        Getum við ekki farið heim nú þegar?
    """),
    "Route21_North_Text_LilNotEnoughMons": t("""
        LIL: Ha? Bardagi?
        Ég nenni ekki að gera þetta ein.

        Komdu með tvö vasaskrímsli, viltu?
    """),
    "Route21_North_Text_IanIntro": t("""
        IAN: Systir mín hreyfir sig ekki
        nóg, svo ég lét hana koma.
    """),
    "Route21_North_Text_IanDefeat": t("""
        IAN: Æææ, systir!
        Taktu þig saman!
    """),
    "Route21_North_Text_IanPostBattle": t("""
        IAN: Komdu nú, systir!

        Þú léttist ekki svona!
    """),
    "Route21_North_Text_IanNotEnoughMons": t("""
        IAN: Við viljum tveir-á-tveir bardaga.
        Geturðu komið með tvö vasaskrímsli?
    """),
    "Text_RockSlideTeach": t("""
        Þegar þú ert uppi á grýttu fjalli eins
        og þessu eru grjóthrun hættuleg.

        Geturðu ímyndað þér það?
        Stórgrýti veltandi niður á þig?

        Það væri svona, vááááááááá!
        Algjör hryllingur!

        Þú virðist ekki hræddur.
        Viltu prófa að nota GRJÓTHRUN?
    """),
    "Text_RockSlideDeclined": t("""
        Ó, svo þú ert hræddur eftir allt.
    """),
    "Text_RockSlideWhichMon": t("""
        Hvaða vasaskrímsli á ég að kenna
        GRJÓTHRUN?
    """),
    "Text_RockSlideTaught": t("""
        Það gæti verið ógnvekjandi að nota það
        í þessum göngum...
    """),
    "SeafoamIslands_B4F_Text_BouldersMightChangeWaterFlow": t("""
        Vísbending: Stórgrýti gæti breytt
        vatnsrennsli.
    """),
    "SeafoamIslands_B4F_Text_DangerFastCurrent": t("""
        HÆTTA
        Stríður straumur!
    """),
}


FILES = {
    "data/maps/Route19/text.inc",
    "data/maps/Route20/text.inc",
    "data/maps/Route21_North/text.inc",
    "data/maps/Route21_South/text.inc",
    "data/maps/SeafoamIslands_B4F/text.inc",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-after-v16.csv")
    parser.add_argument("--output", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-water-routes-v1.csv")
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
        row["notes"] = "codex curated water routes Route 19-21 and Seafoam B4F v1"
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
