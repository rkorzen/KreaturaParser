Q2 = {
1:[10, 20, "syrop"],
2:[20, 20, "syrop"],
3:[30, 20, "syrop"],
4:[40, 20, "syrop"],
5:[50, 20, "syrop"],
6:[50, 20, "syrop"]
}

Q11 = {
1: "Pneumolan Start",
2: "Pneumolan Forte",
3: "Pneumolan Noc",
4: "Pneumolan Express",
5: "Pneumolan Infect Blocker",
6: "Pneumolan Kaszel 2w1"
}
def func():
	out = ""
	for i in range(1, 7):
		out += """
B KONCEPT_{0}
Q S KONCEPT_{0}_Q1 Która z odpowiedzi najlepiej opisuje na ile byłaby Pani zainteresowana zakupem tego preparatu dla swojego dziecka, przy założeniu, że jego cena byłaby dla Pani akceptowalna. <br><br><img src="public/koncepty/{0}.jpg">
1 na pewno kupiłabym
2 raczej kupiłabym
3 może kupiłabym a może bym nie kupiła
4 raczej nie kupiłabym
5 zdecydowanie nie kupiłabym

Q S KONCEPT_{0}_Q2 A gdyby ten preparat kosztował {1} PLN za opakowanie {2}ml w formie {3}, która z odpowiedzi najlepiej opisuje na ile byłaby Pani zainteresowana zakupem tego preparatu.<br><br><img src="public/koncepty/{0}.jpg">
1 na pewno kupiłabym
2 raczej kupiłabym
3 może kupiłabym a może bym nie kupiła
4 raczej nie kupiłabym
5 zdecydowanie nie kupiłabym

Q S KONCEPT_{0}_Q3 Czy ten preparat Pani zdaniem pasuje do marki Pneumolan?<br><br><img src="public/koncepty/{0}.jpg">
1 zdecydowanie tak
2 raczej tak
3 raczej nie
4 zdecydowanie nie
5 nie wiem / trudno powiedzieć

Q M KONCEPT_{0}_Q4 Gdyby taki preparat pojawił się na rynku pod marką Pneumolan, to które z cech Pani zdaniem można by przypisać tej marce?<br><br><img src="public/koncepty/{0}.jpg"> --rot
1 Skuteczny
2 Szybki
3 Silny
4 Kompleksowy (działa na wiele objawów)
5 Działa jednocześnie na objawy i przyczyny
6 Przeciwbakteryjny 
7 Przeciwwirusowy
8 Przeciwzapalny
9 Leczniczy
10 Wysokiej jakości
11 Naturalny
12 Wspomagający
13 Profilaktyczny
14 Na silne objawy / dolegliwości
15 Bezpieczny
16 Nowoczesny
17 Sprawdzony 
18 Niezastąpiony 
19 Bez skutków ubocznych
20 Rekomendowany przez lekarzy 
21 Rekomendowany przez farmaceutów 
22 jest ekspertem
23 Ma dobry smak
24 Drogi 
25 Tradycyjny
26 Lepszy od innych
27 Wart swojej ceny
28 Godny zaufania
29 Wspiera mnie w trosce o dziecko
30 Rozumie potrzeby mojego dziecka
97 Żadne

Q O90_4 KONCEPT_{0}_Q5 Jakie są Pani zdaniem główne zalety tego preparatu?<br><br><img src="public/koncepty/{0}.jpg">

Q M KONCEPT_{0}_Q6 Gdyby kupiła Pani ten preparat dla swojego dziecka to czy podawałaby go Pani ...<br><br><img src="public/koncepty/{0}.jpg">
PRE if ($KONCEPT_{0}_Q2:1 == "1" || $KONCEPT_{0}_Q2:2 == "1" || $KONCEPT_{0}_Q2:3 == "1" );else;goto next;endif
1 Zapobiegawczo, przed pojawieniem się przeziębienia/infekcji dróg oddechowych
2 Na początku, przy pierwszych objawach, w fazie rozwoju  przeziębienia/infekcji dróg oddechowych
3 W fazie środkowej - przeziębienia/infekcji dróg oddechowych
4 Na koniec, w fazie wyciszenia przeziębienia/infekcji dróg oddechowych
5 Po zakończeniu leczenia przeziębienia/infekcji dróg oddechowych, aby wzmocnić organizm

Q M KONCEPT_{0}_Q7 Na jakie objawy stosowałaby Pani ten preparat? (możliwy wybór kilku odpowiedzi)	<br><br><img src="public/koncepty/{0}.jpg">
1 Katar lejący
2 Katar gęsty (żółty/zielony)
3 Katar przewlekły
4 Zatkany nos
5 Każdy rodzaj kataru/zatkanego nosa
6 Przeziębienie
7 Grypę
8 Kaszel suchy
9 Kaszel mokry
96.c Inne jakie?

Q S KONCEPT_{0}_Q8 A gdyby kupiła Pani ten preparat to czy podawałaby go Pani swojemu dziecku ...<br><br><img src="public/koncepty/{0}.jpg">
PRE if ($KONCEPT_{0}_Q2:1 == "1" || $KONCEPT_{0}_Q2:2 == "1" || $KONCEPT_{0}_Q2:3 == "1" );else;goto next;endif
1 zamiast obecnie / dotychczas stosowanego preparatu na przeziębienie/infekcję górnych dróg oddechowych
2 dodatkowo do obecnie stosowanego preparatu na przeziębienie/infekcję górnych dróg oddechowych

Q S KONCEPT_{0}_Q9. Czy podawałaby Pani ten preparat swojemu dziecku jako preparat ...<br><br><img src="public/koncepty/{0}.jpg">
PRE \\INF: Zadać jeśli w pytaniu Q2b odpowiedź 2
1 główny, działający leczniczo
2 dodatkowy, działający wspomagająco

Q G KONCEPT_{0}_Q10 Proszę powiedzieć, na ile zgadza się Pani z następującymi stwierdzeniami dotyczącymi tego opisu<br><br><img src="public/koncepty/{0}.jpg">
zdecydowanie zgadzam się
raczej zgadzam się
raczej nie zgadzam się
zdecydowanie nie zgadzam się
nie wiem / trudno powiedzieć	
_
1 jest zrozumiały
2 informacje w nim zawarte są dla mnie istotne
3 wierzę w przedstawione w nim korzyści płynące ze stosowania tego preparatu
4 opisany preparat jest inny niż znane mi preparaty na przeziębienie/infekcję dróg oddechowych
5 opisany preparat jest lepszy niż znane mi preparaty na przeziębienie/infekcję dróg oddechowych

Q S KONCEPT_{0}_Q11 Proszę teraz spojrzeć na nazwę tego preparatu. Proszę powiedzieć na ile podoba się Pani nazwa {4}. <br><br><img src="public/koncepty/{0}.jpg">
1 bardzo mi się podoba
2 raczej mi się podoba
3 ani mi się podoba, ani nie podoba
4 raczej mi się nie podoba
5 bardzo mi się nie podoba
98 trudno powiedzieć

Q S KONCEPT_{0}_Q12 Na ile ta nazwa Pani zdaniem pasuje do opisu preparatu, z którym zapoznała się Pani przed chwilą.<br><br><img src="public/koncepty/{0}.jpg">
1 bardzo pasuje
2 raczej pasuje
3 ani pasuje, ani nie pasuje
4 raczej nie pasuje
5 w ogóle nie pasuje
98 trudno powiedzieć

Q G KONCEPT_{0}_Q13. Poniżej znajduje się kilka opinii na temat marki Pneumolan. Na ile zgadza się Pani  z  następującymi stwierdzeniami? 
1 zdecydowanie się zgadzam
2 raczej się zgadzam
3 raczej się nie zgadzam
4 zdecydowanie się nie zgadzam
5 nie wiem/trudno powiedzieć	
_
1 Mam do niego zaufanie
2 Poleciłabym go znajomym, rodzinie
3 Jestem zadowolona z tego preparatu
""".format(i, Q2[i][0], Q2[i][1], Q2[i][2], Q11[i])

xxx=func()
print(xxx)