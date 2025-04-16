# Verifica Tracciati Stradali 1.0 | Documentazione 

# Cos’è? 

Verifica Tracciati Stradali 1 è un codice eseguibile che effettua le verifiche planimetriche ed altimetriche previste dal D.M. 6792 del 05/11/2001 sui parametri geometrici di un dato tracciato stradale. 

# Come si usa? 

All’avvio dell’applicazione viene richiesto il percorso assoluto o relativo della cartella nella quale devono essere già presenti i file testo di input, in particolare: 
- imp.txt per le impostazioni generali (opzionale, nel caso non si trovi il file verrà richiesto l’inserimento delle impostazioni generali del tracciato dopo l’importazione dei dati planimetrici); 
- pla.txt per i parametri planimetrici (minimo necessario per definire il tracciato, nel caso non si trovi il file non verrà effettuata alcuna verifica planimetrica o altimetrica); 
- lim.txt per i limiti di velocità locali (opzionale, per definire i tratti in cui si vuole imporre una velocità massima locale diversa da quella del tracciato, es. intersezioni segnalate con stop o dare precedenza, o zone a limite di velocità ridotto); 
- alt.txt per i parametri altimetrici (opzionale, per effettuare le verifiche basate sull’andamento altimetrico). 

I contenuti dei file testo devono essere delimitati da tabulazioni al seguente modo: 

### imp.txt: (unica riga da almeno una colonna fino a cinque colonne) 

- col1: numero della categoria stradale; §3.6 
- col2: distanza B fra asse di rotazione e estremità della carreggiata [m]; §5.2.6 
- col3: limite inferiore dell’intervallo di velocità di progetto [km/h]; §3.6 
- col4: limite superiore dell’intervallo di velocità di progetto [km/h]; §3.6 
- col5: progressiva iniziale del tracciato [m]. 

per le colonne da 2 a 5, nel caso in cui non si inserisca nessun valore il codice, di default, inserisce i valori nominali riportati nella normativa per le colonne 2, 3 e 4 e il valore 0 per la colonna 5. 

Le categorie stradali sono così numerate: §3.6

[A]	Autostrada extraurbana		(Strada principale) 
[A]	Autostrada extraurbana		(Strada di servizio) 
[A]	Autostrada urbana			(Strada principale) 
[A]	Autostrada urbana			(Strada di servizio) 
[B]	Strada extraurbana principale	(Strada principale) 
[B]	Strada extraurbana principale	(Strada di servizio) 
[C1]	Strada extraurbana secondaria 
[C2]	Strada extraurbana secondaria 
[D]	Strada urbana di scorrimento	(Strada principale) 
[D]	Strada urbana di scorrimento	(Strada di servizio) 
[E]	Strada urbana di quartiere 
[F1]	Strada extraurbana locale 
[F2]	Strada extraurbana locale 
[F]	Strada urbana locale 


### pla.txt: (un elemento per riga a tre o, eventualmente, quattro colonne) 

- col1: tipologia di elemento specificando la parola completa {rettifilo, clotoide, arco}, oppure, indifferentemente la sola iniziale {r, c, a}; 
- col2: lunghezza dell’elemento [m]; 
- col3: parametro di scala A, oppure raggio di curvatura [m], oppure inserire la lettera f nel caso in cui si debba specificare che si tratta di un rettifilo tra due curve di flesso, così da sostituire la verifica della lunghezza minima con quella della lunghezza massima di flesso; 
- col4: parametro di scala A, oppure raggio di curvatura [m], eventualmente se la terza colonna è vuota. La presenza di questa colonna è voluta al fine di facilitare l’inserimento dei dati: questa è, infatti, analoga in tutto per tutto alla precedente per cui, ad esempio, inserendo nella colonna 3 il parametro di scala A tramite semplice copia-incolla, si può effettuare la medesima operazione con il raggio di curvatura nella colonna 4. 

### lim.txt: (un tratto per riga a tre o quattro colonne) 

col1: progressiva iniziale [m] del tratto in cui si vuole imporre una velocità massima locale diversa da quella del tracciato (oppure inserire la lettera i se nella seconda colonna viene specificata la distanza [m] dalla progressiva iniziale del tracciato per la quale va applicato il limite locale); 
col2: progressiva finale [m] del  tratto in cui si vuole imporre una velocità massima locale diversa da quella del tracciato (oppure inserire la lettera f se nella prima colonna viene specificata la distanza [m] dalla progressiva finale del tracciato per la quale va applicato il limite locale); 
col3: velocità massima locale che si vuole imporre nel tratto [km/h]; 
col4: accelerazione/ decelerazione [m/s2] (opzionale, nel caso in cui non si inserisca nessun valore il codice, di default, inserisce il valore di normativa pari a 0.80 m/s2). 

### alt.txt: (un elemento per riga a tre o, eventualmente, quattro colonne) 

Modo I: (inserimento degli elementi altimetrici) 
- col1: tipologia di elemento specificando la parola completa {livelletta, raccordo}, oppure, indifferentemente la sola iniziale {l, r}; 
- col2: lunghezza dell’elemento [m]; 
- col3: pendenza della livelletta [%], oppure raggio del raccordo altimetrico [m]; 
- col4: pendenza della livelletta [%], oppure raggio del raccordo altimetrico [m], eventualmente se la terza colonna è vuota. La presenza di questa colonna è voluta al fine di facilitare l’inserimento dei dati: questa è, infatti, analoga in tutto per tutto alla precedente per cui, ad esempio, inserendo nella colonna 3 i dati relativi alla pendenza della livelletta tramite semplice copia-incolla, si può effettuare la medesima operazione con il raggio del raccordo altimetrico nella colonna 4. 


Modo II: (inserimento dei vertici altimetrici) 
- col1: progressiva del vertice [m] (la progressiva del primo vertice deve coincidere con quella iniziale del tracciato); 
- col2: quota del vertice [m]; 
- col3: raggio del raccordo verticale [m]. 

# Cosa produce? 

Se vengono importati correttamente i dati planimetrici verranno creati i seguenti file testo tabulati: 

### dati generali.txt 
contiene: riferimenti normativi, tipologia stradale §3.1, distanza B fra asse rotazione e estremità carreggiata, velocità minima di progetto §3.6, velocità massima di progetto §3.6, progressiva iniziale, progressiva finale e lunghezza tracciato. 

### velocità prima fase.txt 
contiene: coordinate (progressiva, velocità) del diagramma di velocità prima fase in corrispondenza delle curve circolari §5.4. 

### velocità fase finale.txt 
contiene: coordinate (progressiva, velocità) del diagramma di velocità fase finale §5.4. 

### elementi planimetrici.txt 
contiene: numero dell’elemento, tipologia elemento, lunghezza, raggio, parametro di scala A, progressiva iniziale, progressiva finale, velocità dal diagramma di velocità prima fase, velocità massima dal diagramma di velocità fase finale, pendenza trasversale massima §5.2.4 e allargamento per ogni corsia per iscrizione del veicolo in curva §5.2.7. 

### elementi altimetrici.txt (se vengono importati correttamente i dati altimetrici) 
contiene: numero dell’elemento, tipologia elemento, lunghezza, pendenza longitudinale, raggio, progressiva iniziale, progressiva finale, andamento altimetrico e velocità massima dal diagramma di velocità fase finale. 

### verifiche planimetriche.txt 
contiene: numero dell’elemento e parametri geometrici degli elementi planimetrici confrontati con i valori limite normativi come segue: 

per un rettifilo: 
- lunghezza minima §5.2.2 
- lunghezza massima §5.2.2 
- lunghezza massima di flesso §5.2.5 

per una clotoide: 
- parametro A minimo esatto e approssimato da limitazione del contraccolpo §5.2.5 
- parametro A minimo da sovrapendenza longitudinale dei cigli §5.2.5, §5.2.6 
- parametro A minimo da criterio ottico §5.2.5 
- rapporto parametri A minimo da clotoide precedente e/o successiva §5.2.5	 
- parametro A minimo da clotoide precedente e/o successiva §5.2.5 
- parametro A massimo da criterio ottico §5.2.5 
- rapporto parametri A massimo da clotoide precedente e/o successiva §5.2.5 
- parametro A massimo da clotoide precedente e/o successiva §5.2.5 
- pendenza longitudinale minima dei cigli per il deflusso dell'acqua §5.2.6 

per un arco: 
- sviluppo minimo per corretta percezione §5.2.2 
- differenza di velocità da Vpmax §5.4.4 
- differenza di velocità da curva precedente e/o successiva §5.4.4 
- raggio minimo da differenza di velocità da curva precedente e/o successiva §5.4.4 
- raggio minimo da Vpmin §5.2.4 
- raggio minimo da rettifilo precedente e/o successivo §5.2.2 

L’esito di ciascun confronto viene evidenziato nella prima colonna come 0 se è negativo oppure 1 se è positivo, al fine di facilitare l’applicazione della formattazione condizionale in Excel in base al valore numerico.  

### verifiche altimetriche.txt (se vengono importati correttamente i dati altimetrici) 
contiene: numero dell’elemento e parametri geometrici degli elementi altimetrici confrontati con i valori limite normativi come segue: 

per una livelletta: 
- pendenza massima §5.3.1 

per un raccordo: 
- raggio minimo da distanza di visibilità per l'arresto §5.1.2, §5.3.3, §5.3.4 
- raggio minimo da distanza di visibilità per il sorpasso §5.1.3, §5.3.3, §5.3.4 
- raggio minimo per evitare contatto con la superficie §5.3.2 
- raggio minimo da comfort utenza §5.3.2 
- accelerazione verticale massima da comfort utenza §5.3.2 

L’esito di ciascun confronto viene evidenziato nella prima colonna come 0 se è negativo oppure 1 se è positivo, al fine di facilitare l’applicazione della formattazione condizionale in Excel in base al valore numerico.  

### visibilità arresto.txt (se vengono importati correttamente i dati altimetrici) 
contiene: coordinate (progressiva a passo di un metro, distanza) del diagramma di visibilità richiesta per l’arresto §5.1.2 

### visibilità sorpasso.txt (se la strada è ad unica carreggiata) 
contiene: coordinate (progressiva, distanza) del diagramma di visibilità richiesta per il sorpasso §5.1.3 

### visibilità cambio corsia.txt (se la carreggiata è a più corsie per senso di marcia) 
contiene: coordinate (progressiva, distanza) del diagramma di visibilità richiesta per il cambiamento di corsia §5.1.4 

 

### eventi.txt 

contiene: eventuali file non trovati, oppure dati errati, data e ora di stampa e contatti 
 

# Come funziona? 

Il codice esegue la sequenza di operazioni riportate in basso, ripetibile a richiesta dell’utente nel caso in cui vengono modificati uno o più parametri e si vogliano effettuare nuovamente le verifiche: 
- Specifica del percorso della cartella contenente i file dei dati del tracciato; 
- Importazione dei dati planimetrici da pla.txt, controllo della validità dei dati e segnalazione degli eventuali errori; in tal caso, si ritorna al passo precedente con la richiesta  di confermare o modificare l’ultimo percorso inserito; 
- Importazione dei dati di impostazione del tracciato da imp.txt, controllo della validità dei dati e segnalazione degli eventuali errori; in tal caso, si procede con l’inserimento delle impostazioni del tracciato dato per dato memorizzando come valori di default, da confermare o modificare, gli ultimi dati validi importati; 
- Importazione dei dati dei limiti di velocità locali da lim.txt, controllo della validità dei dati e segnalazione degli eventuali errori; in tal caso, si tralascia l’applicazione dei limiti di velocità locali; 
- Calcolo delle progressive e delle velocità del diagramma di velocità prima fase; 
- Calcolo del diagramma di velocità fase finale a passo di un millimetro e successiva determinazione dei punti critici e delle corrispondenti velocità; 
- Eventuale aggiornamento del diagramma di velocità fase finale con i limiti di velocità locali; 
- Esecuzione delle verifiche sui parametri geometrici degli elementi planimetrici importati; 
- Importazione dei dati altimetrici da alt.txt, controllo della validità dei dati e segnalazione degli eventuali errori; in tal caso, si tralascia l’esecuzione delle verifiche altimetriche; 
- Eventuale esecuzione delle verifiche sui parametri geometrici degli elementi altimetrici importati; 
- Stampa dei risultati in file testo tabulati nello stesso percorso dei dati sovrascrivendo gli eventuali file precedentemente creati. 

## N.B.

- Eventuali file non trovati e dati errati verranno evidenziati sulla schermata dei comandi preceduti da asterisco. Anche l’esito finale delle verifiche di ogni elemento planimetrico ed altimetrico, se è negativo, verrà evidenziato indicando il valore limite da rispettare.
- L’inserimento dei dati planimetrici ed altimetrici è possibile mediante la modalità copia-incolla delle colonne interessate dall’editor geometria in Autodesk Civil 3D, anche includendo l’unita m nelle lunghezze e il segno + nel formato km+m delle progressive. 
- I dati di input vengono preliminarmente validati secondo il tipo di dato come segue: 

numero della categoria stradale: numero intero positivo.
distanza B fra asse rotazione e estremità carreggiata, limite inferiore/ superiore dell’intervallo di velocità di progetto e velocità massima locale: numero decimale positivo (verrà approssimato alla seconda cifra decimale).
accelerazione/ decelerazione: numero decimale indifferentemente positivo o negativo (verrà approssimato alla seconda cifra decimale).
progressiva iniziale del tracciato, progressiva e quota del vertice altimetrico: numero decimale (verrà approssimato alla terza cifra decimale).
progressiva iniziale/ finale del tratto a limite massimo locale: numero decimale (verrà approssimato alla terza cifra decimale) o, eventualmente, stringa indifferentemente in maiuscolo o minuscolo.
tipologia dell’elemento planimetrico/ altimetrico: stringa indifferentemente in maiuscolo o minuscolo.
lunghezza dell’elemento planimetrico/ altimetrico: numero decimale non negativo (verrà approssimato alla terza cifra decimale).
raggio del raccordo planimetrico/ altimetrico e parametro di scala A: numero decimale positivo (verrà approssimato alla terza cifra decimale).
pendenza percentuale della livelletta: numero decimale (verrà approssimato alla seconda cifra decimale) 

Eslam Anter | 26.08.2024 
eslam.anter@outlook.com 

P.S. 
L’idoneità del codice e l’utilizzo dei risultati da esso ottenuti sono onere e responsabilità esclusiva dell’utente. 
