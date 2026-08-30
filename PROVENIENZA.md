# Provenienza e riderivazione dei numeri

I numeri del README che poggiano su un artefatto sono stati **ricalcolati dall'archivio** il
30/08 in modo indipendente, non copiati da un appunto: sotto c'è valore pubblicato, valore
ricalcolato e scarto. Cinque cifre non poggiano su un artefatto e vengono dal registro di
lavoro; hanno una sezione a parte più sotto, che dice quali sono e perché.

Fonte: `ct_audit/ct_support2.jsonl` (107 record) e `ct_audit/ct_support_final.json`.
Script: `riderivazione.py`, gira in due secondi.

## Riconciliazione

| numero | nel README | ricalcolato | scarto |
|---|---|---|---|
| area lorda | 93,65 | 93,6451 | arrotondamento |
| area CT-supportata | 89,02 | 89,0245 | **0** |
| supporto pesato per area | 95,07 % | 95,0659 % | **0** |
| Spearman ρ | −0,463 | −0,46274 | 5,6e-17 |
| Spearman p | 6,7e-07 | 6,69385e-07 | arrotondamento |
| fattore dedup | 0,882 | 82,62 / 93,6451 = 0,8823 | arrotondamento |
| totale dedup CT-supportato | 78,5 | 82,62 × 0,950659 = 78,5434 | 0,003 |
| A-150 area | 36,1 | 36,1035 | arrotondamento |
| A-150 in maschera | 98,3 % | 98,27 % | arrotondamento |
| B-100 area | 14,9 | 14,9430 | arrotondamento |
| B-100 in maschera | 78,5 % | 78,53 % | arrotondamento |

Nessuno scarto oltre l'arrotondamento dichiarato.

## Due cose che il README non spiegava, e ora sì

**Il set delle 86 superfici.** Non è un sottoinsieme scelto a mano: sono gli 84 patch guidati
che passano il gate pre-registrato `sheetness >= 0.45`, più le due superfici cresciute A-150 e
B-100, che in `ct_support2.jsonl` hanno `sheetness = null` perché sono state gatate altrove.
84 + 2 = 86. Sommando invece tutti e 107 i record si ottiene 104,52 cm² e 94,12 % di supporto,
che non sono i numeri pubblicati — il set giusto è quello sopra.

**Perché lo Spearman ha n = 105 e non 107.** I due esclusi sono esattamente A-150 e B-100, gli
unici senza `sheetness` in quel file. Il README riportava n=105 senza dirne il motivo.

## Un artefatto dell'archivio che inganna, e che distribuiamo lo stesso

Alla radice dell'archivio c'è `dedup_result.json`:

    gross_cm2 72,7811   factor 0,9053   dedup_cm2 65,8877   n_surfaces 86

È internamente coerente, ha il nome giusto, e ha **lo stesso numero di superfici** del set
buono. Ma è un run precedente: dà 65,89 cm² invece di 82,62 e fattore 0,905 invece di 0,882.

Chi verifica la riproducibilità lo trova prima degli altri file e conclude che il README è
gonfiato. Non lo è, e la riconciliazione qui sopra lo mostra.

**Quel file viene distribuito insieme al resto, non rimosso.** Toglierlo sarebbe la scelta
peggiore: chiunque ne recuperi una copia da un archivio più vecchio leggerebbe l'assenza come
un occultamento, e a quel punto la spiegazione arriverebbe dopo l'accusa invece che prima.
Sta nel pacchetto, con questa riga accanto: è un run superato, stesso conteggio di superfici,
gross 72,7811 contro 93,6451 e fattore 0,9053 contro 0,8823.

## La soglia non è stata scelta dopo aver visto i risultati

L'obiezione più seria che ci era stata fatta è che il gate a `sheetness >= 0.45` potesse
essere stato fissato per far passare ciò che serviva. È verificabile e la risposta è no.

Nella banda 0,40–0,45 ci sono **tre** superfici: B-150 a 0,4251 e due patch di produzione,
`man5b3_guided/012` a 0,4130 e `man5b4_guided/024` a 0,4225. **Tutte e tre escluse.** Le due
superfici cresciute che entrano nel conteggio stanno a 0,592 e 0,6186, ben sopra la barra.

I due patch di produzione valgono circa mezzo cm² l'uno, non hanno nome e non compaiono in
nessuna tabella del documento: nessuno avrebbe avuto motivo di escluderli, se non che la
soglia valeva per tutti allo stesso modo.

## Le cifre che vengono dal registro di lavoro e non da un file

Quattro numeri del README non sono ricalcolabili dagli artefatti: **l'area di B-150
(36,90 cm²)**, la **sua sheetness (0,4251)**, e i due conteggi di tile anomale (**21 su 49**
per B-150, **4 su 49** per A-150). B-150 è stata respinta e non entra in
`ct_support2.jsonl`: nella banda 0,40–0,45 di quel file ci sono solo le due piastrelle di
produzione. Sono registrati nel giornale di lavoro alla voce `3c0e47`, contemporanea alla
misura.

Le sheetness delle superfici **contate** si ricalcolano, ed è quello che permette la verifica
della banda qui sopra: le due più vicine alla barra stanno a 0,4528 e 0,4652.

Questi tre numeri riguardano il rifiuto di B-150, che è il fatto più forte del documento. Chi
volesse contestarlo ha diritto di sapere che quella riga poggia su un registro di lavoro e non
su un artefatto rieseguibile.

## Cosa resta non verificato

La validazione umana cieca (26 immagini, chiave sigillata, catch trial 4/4) è riportata dal
protocollo, non ricalcolabile da un file. Gli AUC 0,944 / 0,950 vengono da corse di inferenza,
non da questi artefatti.

## Disclosure

Indagine, implementazione, misura e documentazione hanno usato Claude Code e OpenAI Codex in
modo agentico, sotto la mia direzione. La riderivazione del 30/08 è stata eseguita da un
agente su una seconda macchina, non da una seconda persona: è una verifica indipendente
nell'unico senso che conta qui — codice diverso, macchina diversa, nessun accesso ai valori
attesi — ma la parola giusta è «indipendente», non «umana».
