from __future__ import annotations

import argparse
import csv
import textwrap
from pathlib import Path

from common import repo_root


def t(value: str) -> str:
    return textwrap.dedent(value).strip()


TRANSLATIONS = {
    "Route13_Text_SebastianIntro": t("""
        Fugla-vasaskrímslin mín vilja berjast
        við þig!
    """),
    "Route13_Text_SebastianDefeat": t("""
        Týndu DÚFUTETUR og DÚFINN mínir
        saman?
    """),
    "Route13_Text_SebastianPostBattle": t("""
        Vasaskrímslin mín virðast glöð þótt
        þau hafi tapað.
    """),
    "Route13_Text_SusieIntro": t("""
        Mér er sagt að ég sé góð miðað við
        krakka.
    """),
    "Route13_Text_SusieDefeat": t("""
        Óó!
        Ég tapaði!
    """),
    "Route13_Text_SusiePostBattle": t("""
        Ég vil verða góður ÞJÁLFARI.
        Ég æfi stíft, sjáðu bara til.
    """),
    "Route13_Text_ValerieIntro": t("""
        Vá!
        MERKIN þín eru svo flott!
    """),
    "Route13_Text_ValerieDefeat": t("""
        Ekki nóg!
    """),
    "Route13_Text_ValeriePostBattle": t("""
        Þú fékkst þessi MERKI frá
        SALARLEIÐTOGUM. Ég veit það!
    """),
    "Route13_Text_GwenIntro": t("""
        Sætu vasaskrímslin mín óska eftir að
        kynnast þér.
    """),
    "Route13_Text_GwenDefeat": t("""
        Vel gert!
        Þú vannst algjörlega!
    """),
    "Route13_Text_GwenPostBattle": t("""
        Þú þarft að láta vasaskrímsli berjast
        til að herða þau.
    """),
    "Route13_Text_AlmaIntro": t("""
        Ég fann KOLEFNI í helli einu sinni
        þegar ég var að skríða um göng.
    """),
    "Route13_Text_AlmaDefeat": t("""
        Ó, svei!
        Ég klúðraði þessu!
    """),
    "Route13_Text_AlmaPostBattle": t("""
        KOLEFNI hækkaði HRAÐA
        vasaskrímslisins míns.
    """),
    "Route13_Text_PerryIntro": t("""
        Ég ætla ekki að tapa.
        Ekki þegar vindurinn blæs með mér!
    """),
    "Route13_Text_PerryDefeat": t("""
        Vindurinn snerist!
    """),
    "Route13_Text_PerryPostBattle": t("""
        Ég er búinn.
        Ég flýg líklega heim.
    """),
    "Route13_Text_LolaIntro": t("""
        Jú, ég skal leika við þig, elskan.
    """),
    "Route13_Text_LolaDefeat": t("""
        Ó!
        Þú litla skepna!
    """),
    "Route13_Text_LolaPostBattle": t("""
        Ég velti fyrir mér hvort karl- eða
        kvenkyns vasaskrímsli séu sterkari.
    """),
    "Route13_Text_SheilaIntro": t("""
        Viltu berjast við nokkur vasaskrímsli
        með mér?
    """),
    "Route13_Text_SheilaDefeat": t("""
        Er þessu þegar lokið?
    """),
    "Route13_Text_SheilaPostBattle": t("""
        Ég veit eiginlega ekkert um
        vasaskrímsli.

        Þau sem ég nota... Ég valdi þau bara
        eftir útlitinu!
    """),
    "Route13_Text_JaredIntro": t("""
        Á hvað ertu að glápa?
    """),
    "Route13_Text_JaredDefeat": t("""
        Fjandinn!
        Gírarnir rifnuðu!
    """),
    "Route13_Text_JaredPostBattle": t("""
        Láttu þig hverfa!
    """),
    "Route13_Text_RobertIntro": t("""
        Ég vel alltaf fugla-vasaskrímsli.
        Ég hef helgað mig þeim.
    """),
    "Route13_Text_RobertDefeat": t("""
        Orkan búin!
    """),
    "Route13_Text_RobertPostBattle": t("""
        Ég vildi að ég gæti flogið eins og
        DÚFUTETUR og DÚFINN...
    """),
    "Route13_Text_LookToLeftOfThatPost": t("""
        ÞJÁLFARA-RÁÐ

        Sjáðu, sjáðu! Horfðu til vinstri við
        þennan staur!
    """),
    "Route13_Text_SelectToSwitchItems": t("""
        ÞJÁLFARA-RÁÐ

        Notaðu SELECT til að færa hluti í
        HLUTA-glugganum.
    """),
    "Route13_Text_RouteSign": t("""
        ROUTE 13
        Norður til SILENCE BRIDGE
    """),
    "Route14_Text_CarterIntro": t("""
        Þú þarft að nota TM til að kenna
        vasaskrímslum góðar hreyfingar.
    """),
    "Route14_Text_CarterDefeat": t("""
        Ekki nógu gott ennþá.
    """),
    "Route14_Text_CarterPostBattle": t("""
        Þú átt einhver HM, ekki satt?
        Vasaskrímsli gleyma þeim hreyfingum
        ekki auðveldlega.
    """),
    "Route14_Text_MitchIntro": t("""
        Fugla-vasaskrímslin mín ættu að vera
        tilbúin í bardaga.
    """),
    "Route14_Text_MitchDefeat": t("""
        Ekki tilbúin enn!
    """),
    "Route14_Text_MitchPostBattle": t("""
        Fugla-vasaskrímslin mín þurfa að læra
        betri hreyfingar.
    """),
    "Route14_Text_BeckIntro": t("""
        Þeir selja TM í CELADON DEPT. STORE.

        TM eru ekki mjög sjaldgæf, en fáir
        eiga HM.
    """),
    "Route14_Text_BeckDefeat": t("""
        Æ, fúlt!
    """),
    "Route14_Text_BeckPostBattle": t("""
        Prófaðu að kenna vasaskrímsli
        hreyfingu af sömu gerð og það sjálft.

        Það á víst að auka kraft hreyfingarinnar.
    """),
    "Route14_Text_MarlonIntro": t("""
        Hefurðu kennt fugla-vasaskrímslinu þínu
        að FLJÚGA?

        Þá geturðu svifið með því upp í
        himininn!
    """),
    "Route14_Text_MarlonDefeat": t("""
        Skotinn niður í logum!
    """),
    "Route14_Text_MarlonPostBattle": t("""
        Fugla-vasaskrímsli eru mín eina sanna
        ást.
        Ég vil ekki ala neitt annað upp.
    """),
    "Route14_Text_DonaldIntro": t("""
        Hefurðu heyrt goðsögnina um vængjuðu
        hillingarnar?
    """),
    "Route14_Text_DonaldDefeat": t("""
        Af hverju?
        Af hverju tapaði ég?
    """),
    "Route14_Text_DonaldPostBattle": t("""
        Jú, vængjuðu hillingarnar eru
        goðsagnakenndu fugla-vasaskrímslin.

        Þau eru þrjú: ÉLJASKARFU, ÞÓRSHANI
        og BLOSSAGAUK.
    """),
    "Route14_Text_BennyIntro": t("""
        Ég er ekkert sérstaklega spenntur, en
        allt í lagi.
        Byrjum!
    """),
    "Route14_Text_BennyDefeat": t("""
        Ég vissi það!
    """),
    "Route14_Text_BennyPostBattle": t("""
        Sigur, tap...
        Það skiptir engu undir þessum
        víðáttumikla himni.
    """),
    "Route14_Text_LukasIntro": t("""
        Komdu, komdu.
        Byrjum, byrjum, byrjum!
    """),
    "Route14_Text_LukasDefeat": t("""
        Arrg!
        Tapaði! Farðu!
    """),
    "Route14_Text_LukasPostBattle": t("""
        Hvað, hvað, hvað?
        Hvað viltu enn?
    """),
    "Route14_Text_IsaacIntro": t("""
        Ég þarf að drepa tímann.
        Þegiðu og berstu.
    """),
    "Route14_Text_IsaacDefeat": t("""
        Hvað?
        Þú!?
    """),
    "Route14_Text_IsaacPostBattle": t("""
        Að ala upp vasaskrímsli er vesen,
        maður.
    """),
    "Route14_Text_GeraldIntro": t("""
        Við hjólum hérna út af opnu
        víðáttunum.
    """),
    "Route14_Text_GeraldDefeat": t("""
        Útafakstur!
    """),
    "Route14_Text_GeraldPostBattle": t("""
        Það er flott að þú gerðir vasaskrímslin
        þín svona sterk.

        Mátturinn ræður!
        Og þú veist það!
    """),
    "Route14_Text_MalikIntro": t("""
        Vasaskrímslabardagi?
        Svalt! Slagsmál!
    """),
    "Route14_Text_MalikDefeat": t("""
        Blásinn burt!
    """),
    "Route14_Text_MalikPostBattle": t("""
        Þú veist hver myndi vinna, þú og ég
        maður á mann!
    """),
    "Route14_Text_RouteSign": t("""
        ROUTE 14
        Vestur til FUCHSIA BORGAR
    """),
    "Route14_Text_KiriIntro": t("""
        KIRI: JAN, reynum alveg, alveg
        rosalega mikið saman.
    """),
    "Route14_Text_KiriDefeat": t("""
        KIRI: Snökt...
        Við töpuðum, er það ekki?
    """),
    "Route14_Text_KiriPostBattle": t("""
        KIRI: Töpuðum við mín vegna?
    """),
    "Route14_Text_KiriNotEnoughMons": t("""
        KIRI: Við getum barist ef þú ert með
        tvö vasaskrímsli.
    """),
    "Route14_Text_JanIntro": t("""
        JAN: KIRI, nú byrjum við!
        Við verðum að reyna vel!
    """),
    "Route14_Text_JanDefeat": t("""
        JAN: Eeeeh!
        Ósanngjarnt!
    """),
    "Route14_Text_JanPostBattle": t("""
        JAN: KIRI, ekki gráta!
        Við reynum bara betur næst.
    """),
    "Route14_Text_JanNotEnoughMons": t("""
        JAN: Viltu berjast?
        Þú átt ekki nógu mörg vasaskrímsli.
    """),
    "Route15_Text_KindraIntro": t("""
        Ég fékk nokkur vasaskrímsli í skiptum.
        Má ég prófa þau á þér?
    """),
    "Route15_Text_KindraDefeat": t("""
        Ekki nógu gott!
    """),
    "Route15_Text_KindraPostBattle": t("""
        Þú getur ekki breytt gælunafni
        vasaskrímslis sem þú fékkst í skiptum.

        Aðeins upphaflegi ÞJÁLFARINN getur
        látið breyta gælunafninu.
    """),
    "Route15_Text_BeckyIntro": t("""
        Þú lítur blíðlega út, svo ég held að
        ég geti unnið þig.

        Ég prófa!
    """),
    "Route15_Text_BeckyDefeat": t("""
        Nei, rangt!
    """),
    "Route15_Text_BeckyPostBattle": t("""
        Ég er hrædd við MÓTORHJÓLAMENN.
        Þeir líta svo ljótir og illir út!
    """),
    "Route15_Text_EdwinIntro": t("""
        Þegar ég flauta get ég kallað til
        fugla-vasaskrímsli.
    """),
    "Route15_Text_EdwinDefeat": t("""
        Ái!
        Þetta er sorglegt!
    """),
    "Route15_Text_EdwinPostBattle": t("""
        Kannski er ég ekki gerður fyrir bardaga.
        Ég er líklega röng gerð.
    """),
    "Route15_Text_ChesterIntro": t("""
        Hmm? Fuglarnir mínir skjálfa!
        Þú ert góður, er það ekki?
    """),
    "Route15_Text_ChesterDefeat": t("""
        Rétt eins og ég hélt!
    """),
    "Route15_Text_ChesterPostBattle": t("""
        Þetta er augljóst og þú ættir að vita
        það, en...

        Hreyfingar eins og JARÐSKJÁLFTI og
        SPRUNGA virka ekki á fugla-vasaskrímsli.
    """),
    "Route15_Text_GraceIntro": t("""
        Ó, þú ert lítill krúttlingur!
        Alveg eins og elskulegt vasaskrímsli!
    """),
    "Route15_Text_GraceDefeat": t("""
        Þú varst líka svo sætur!
    """),
    "Route15_Text_GracePostBattle": t("""
        Ég fyrirgef þér.
        Ég þoli þetta.
        Ég er orðin stór stelpa núna.
    """),
    "Route15_Text_OliviaIntro": t("""
        Ég ala upp vasaskrímsli til verndar
        af því að ég bý ein.
    """),
    "Route15_Text_OliviaDefeat": t("""
        Fyrir mér snúast vasaskrímsli ekki um
        sigur eða tap.
    """),
    "Route15_Text_OliviaPostBattle": t("""
        Mér þykir vænt um að vasaskrímslin mín
        taki á móti mér þegar ég kem heim.

        Það er svo traustvekjandi.
    """),
    "Route15_Text_ErnestIntro": t("""
        Heyrðu, krakki! Komdu!
        Ég fékk þessi af einhverjum aumingja!
    """),
    "Route15_Text_ErnestDefeat": t("""
        Af hverju ekki?
    """),
    "Route15_Text_ErnestPostBattle": t("""
        Lífið er of stutt.
        Það er svalt að lifa sem útlagi.
        TEAM ROCKET RÆÐUR!
    """),
    "Route15_Text_AlexIntro": t("""
        Láttu mig fá alla peningana þína þegar
        þú tapar fyrir mér, krakki!
    """),
    "Route15_Text_AlexDefeat": t("""
        Það getur ekki verið satt!
    """),
    "Route15_Text_AlexPostBattle": t("""
        Ég var bara að grínast með peningana.
        Ekki taka mig svona alvarlega.
    """),
    "Route15_Text_CeliaIntro": t("""
        Hvað er svalt og í gangi?
        Að skipta á vasaskrímslum!
    """),
    "Route15_Text_CeliaDefeat": t("""
        Ég sagði skipti!
    """),
    "Route15_Text_CeliaPostBattle": t("""
        Ég skipti á vasaskrímslum við vini
        mína allan tímann.
    """),
    "Route15_Text_YazminIntro": t("""
        Viltu leika við vasaskrímslin mín?
    """),
    "Route15_Text_YazminDefeat": t("""
        Ég var of óþolinmóð!
    """),
    "Route15_Text_YazminPostBattle": t("""
        Ég fer að æfa með veikara fólki.
    """),
    "Route15_Text_RouteSign": t("""
        ROUTE 15
        Vestur til FUCHSIA BORGAR
    """),
    "Route15_Text_MyaIntro": t("""
        MYA: Þú ert fullkominn.
        Hjálparðu mér að þjálfa litla bróður
        minn?
    """),
    "Route15_Text_MyaDefeat": t("""
        MYA: RON, þú verður að einbeita þér!
        Hugsaðu um það sem þú ert að gera!
    """),
    "Route15_Text_MyaPostBattle": t("""
        MYA: Allt í lagi, við herðum á þessu.
        Ég bæti við æfingaprógrammið okkar!
    """),
    "Route15_Text_MyaNotEnoughMons": t("""
        MYA: Viltu skora á okkur?
        Þú þarft samt tvö vasaskrímsli.
    """),
    "Route15_Text_RonIntro": t("""
        RON: Systir mín verður ógnvekjandi
        þegar við töpum.
    """),
    "Route15_Text_RonDefeat": t("""
        RON: Ó, nei, nei...
        Fyrirgefðu, systir!
    """),
    "Route15_Text_RonPostBattle": t("""
        RON: Ó, æ...
        Ég vildi að ég ætti góða systur...
    """),
    "Route15_Text_RonNotEnoughMons": t("""
        RON: Vildirðu berjast við mig og
        systur mína?

        Þá þarftu tvö vasaskrímsli.
    """),
    "Route15_WestEntrance_1F_Text_OaksAideCameByHere": t("""
        Ert þú krakkinn sem er að vinna í
        VasaDEX?

        AÐSTOÐARMAÐUR PROF. OAK kom hér við.
    """),
    "Route15_WestEntrance_2F_Text_GiveItemIfCaughtEnough": t("""
        Hæ! Manstu eftir mér?
        Ég er einn af AÐSTOÐARMÖNNUM PROF.
        OAK.

        Ef VasaDEX-ið þitt er með full gögn
        um {STR_VAR_1} tegundir á ég að gefa
        þér verðlaun.

        PROF. OAK fól mér {STR_VAR_2} handa
        þér.

        Svo, {PLAYER}, leyfðu mér að spyrja.

        Hefurðu safnað gögnum um að minnsta
        kosti {STR_VAR_1} gerðir vasaskrímsla?
    """),
    "Route15_WestEntrance_2F_Text_GreatHereYouGo": t("""
        Frábært! Þú hefur náð eða átt
        {STR_VAR_3} gerðir vasaskrímsla!

        Til hamingju!
        Gjörðu svo vel!
    """),
    "Route15_WestEntrance_2F_Text_ReceivedItemFromAide": t("""
        {PLAYER} fékk {STR_VAR_2} frá
        AÐSTOÐARMANNINUM.
    """),
    "Route15_WestEntrance_2F_Text_ExplainExpShare": t("""
        REYNSLUDEILIR er hlutur sem
        vasaskrímsli heldur á.

        Vasaskrímslið fær hlutdeild í
        REYNSLUSTIGUM án þess að berjast.
    """),
    "Route15_WestEntrance_2F_Text_LargeShiningBird": t("""
        Sjáum hvað sjónaukinn sýnir...

        Stór, skínandi fugl flýgur í átt að
        hafinu.
    """),
    "Route15_WestEntrance_2F_Text_SmallIslandOnHorizon": t("""
        Sjáum hvað sjónaukinn sýnir...

        Þetta lítur út eins og lítil eyja við
        sjóndeildarhringinn!
    """),
}


FILES = {
    "data/maps/Route13/text.inc",
    "data/maps/Route14/text.inc",
    "data/maps/Route15/text.inc",
    "data/maps/Route15_WestEntrance_1F/text.inc",
    "data/maps/Route15_WestEntrance_2F/text.inc",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-after-v13.csv")
    parser.add_argument("--output", type=Path, default=repo_root() / "translation_reports/manual_translation_queue-route13-15-v1.csv")
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
        row["notes"] = "codex curated Route 13 through Route 15 v1"
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
