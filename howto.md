# Juhend, kuidas collaboratida enda arvutist GitHubi failidega

Esmalt vaja alla laadida Git leheküljelt https://git-scm.com/download/win

Kontrolli Command Promtist (käsurealt) kas Git töötab - [git --version]

Git'i saab kasutada kas Windowsi enda käsurealt või VSCode terminalist.
Sandra kasutab teist. 

## Täpsemalt saab lugeda giti käskudest https://githowto.com


### Githubi repo arvutisse paigaldamine

1. Ava CMD ja kaust, kuhu soovid repositooriumi paigaldada.
2. Liigu CMD-s soovitud kausta käsuga [cd failitee]
3. Mine GitHubi ning kopeeri repositoorimi tee

![](image.png)

4. Sisesta CMD-s käsk [git clone kopeeritud_tee]
5. Kontrolli, kas leiad failid üles
6. Tee endale pai!

### GitHubi andmete taotlemine

[git fetch] - andmete alla laadimine
[git pull] - andmete arvutisse saamine

### Muudatuste tegemine

Võimalik muuta faili kaustas või Visual Studio Code'is.
VSC-s võimalik avada kogu kaust niimoodi, et teha muudatusi erinevates failides. [File -> Open folder ... -> ava kaust]

1. Tee muudatusi ja salvesta (VSC-is on Ctrl+S)
2. Ava terminal või CMD (CMD-s on vajalik siseneda failide asukoha kausta käsuga cd ...)
3. [git add .]
4. [git commit -m"Commiti pealkiri jutumärkide vahel"]
5. [git push] - Muudab vastavad failid ka GitHubis
