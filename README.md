# Pythoni-projekt

Siin mängu eesmärkgit
Aardejahi mängu eesmärk:
Mäng leiab aset müstilises metsas, kus peategelane etk mängija ise aitab otsida kohalike kadunuid aardeid. 
Hetkel on olemas mängijale kaks ülesannet. Kohalikud Karu ja Konn annavab mängijale vihje, kuhu nad võisid enda aarde kaotada.
Mängija peab seejärel otsima üles õige koha ning kaevatud aarded tagasi õigele omanikule viima, et ülesanded täita.


Alfa versioon mängust (novembri algus):
* Esialgne versioon maailmast
*  hetkeline tegelane, sest animatsioonidega tekkisid probleemid (tehtud uus tegelane)
* mängu füüsika (gravitatsioon, collidimine plokkidega, kaamera liikumine)
* tegelase liigutamine maailmas

Beeta versioon mängust (detsembri lõpp):
* Maailm on välja töödeldud, vähemalt esimene leveli aste
* Kõikidel tegelastel (Mängija, Konn ja Karu) on ise joonistatud animatsioonid ning kõrvaltegelastega on võimalik suhelda, mille käigus animatsioonid muutuvad.
* Täiendatud füüsikat (enam ei ole võimalik ühe seina peal lõplikult hüpata)
* Mängijale on kaks ülesannet, mille lahendades on kohalikud õnnelikud, et kadunud aarde tagasi said.
* Mängule on lisatud "Q" tähega ligipääsetav juhend, mis seletab mängijale lihtsamad mängu liikumisvõimalused
* Mängul on lisatud peamenüü, kus on võimalik siseneda ja lahkuda mängust.

Tulevikus planeeritud tegevused:
* Mängule juurde lisada heli ja taustamuusika
* Rohkem ja põhjalikumad ülesanded
* Võimalik tekitada rohkem leveleid, mida täiendada vastavalt raskusastmele.
* Luua mängule huvitav taustalugu





Tekkinud probleemid:
* keeruline pygame mängu füüsikatest aru saada (aitasid paljud youtube tutorialid)
* Animatsioonide sisse kirjutamine, kuna pygame poolt pole seda sisse kirjutatud
* maailma genereerimine (otsustasime kasutada youtube'ist ühte tilemap editori, mis salvestab andmed json failina, ning sellega on lihtne maailma andmeid sisse lugeda)
* kaamera kasutamine tegelase ümber ja liikumine kaameraga

