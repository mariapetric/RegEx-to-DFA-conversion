# Regex to DFA Converter

Acest proiect implementează un convertor de expresii regulate (Regex) în DFA (Automat Finit Determinist), trecând prin următorii pași intermediari:
- transformarea expresiei în notație postfixată (forma poloneză inversă),
- construirea unui lambda-NFA (automat nedeterminist cu tranziții lambda),
- convertirea acestuia într-un DFA,
- validarea unor șiruri de intrare folosind DFA-ul generat.

## Structura proiectului

- `LFA-Assignment2_Regex_DFA_v2.json`: Fișier JSON de intrare, care conține o listă de obiecte cu câte o expresie regulată și un set de șiruri de testat.
- Codul Python conține următoarele funcții principale:
  -> `convertToPostfixNotation()`: transformă expresia regulată în notație postfixată, adăugând explicit operatorul de concatenare `.`.
        - cu Algoritmul Shunting Yard, după stabilirea priorităților operatorilor din expresiile regulate
  -> `convertToLambdaNFA()`: construiește un NFA cu tranziții lambda, folosind construcția lui Thompson.
        - cât timp notația postfixată nu a fost redusă la un singur element, găsește poziția primului operator
        - stabilește dacă operatorul implică 1 sau 2 operanzi, apoi, dacă aceștia sunt încă simboluri sau sunt deja NFA-uri (din operații
            precedente) și evaluează corespunzător operația
        - la final, operandul/operanzii si operatorul sunt eliminați din notația postfixată si în locul lor este introdus rezultatul
  -> `convertToDFA()`: transformă NFA-ul într-un DFA, aplicând algoritmul de determinizare prin închideri lambda și BFS.
        - calculează pentru fiecare stare λ-închiderea sa și apoi, pentru fiecare simbol din nfa, in ce noua stare se ajunge cu λ*sλ* (s fiind
            un simbol)
        - după ce obține starea inițială a DFA-ului (din fosta stare inițială a NFA-ului --λ*-->), face un BFS și vede unde ajunge cu fiecare 
            simbol din fiecare stare nouă a DFA-ului (cea care este la momentul respectiv în capătul stânga al cozii)
        - noile stări finale sunt cele care conțin o stare finală a NFA-ului de la început
  -> `validateWithDFA()`: testează dacă un șir este acceptat de DFA-ul generat.

## Cum se rulează codul

1. Asigură-te că ai Python 3 instalat.
2. Salvează codul Python într-un fișier, de exemplu `main.py`.
3. Asigură-te că fișierul `LFA-Assignment2_Regex_DFA_v2.json` se află în același director cu scriptul.
4. Rulează codul:

    cd calea/către/folderul/cu/fișierul
    python3 main.py
