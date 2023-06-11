# End-Points
Ecco la lista di tutti gli end-point disponibili:
- **/register** (per la registrazione di un nuovo utente)
- **/login** (per loggare un utente e controllare se è loggato)
- **/animals** (per ricevere tutti gli animali di un utente)
- **/luoghi** (per ricevere tutti i luoghi)
- **/logout** (per fare il logout e disattivare il cookie della sessione)

# Documentazione singoli end-point
A seguire istruzioni e documentazione per ogni singolo endpoint
## **/register**
### Metodo POST:
Bisogna inviare in un json username, password e email formattati in questo modo:
```
{
  "username": "usernameUtente",
  "password": "passwordUtente",
  "mail": "mailUtente@example.com"
}
```
Se vengono inviati i dati di un utente già esistente non ne verrà creato uno nuovo ma l'utente verrà loggato.

Codici di errore:
- **400** ❌: manca un parametro (username, email o password)

Codici successo:
- **200** ✅: registrazione/login avvenuto con successo

## **/login**
### ***Metodo POST:***
Bisogna inviare un json con username e password formattato in questo modo:
```
{
  "username": "usernameUtente",
  "password": "passwordUtente"
}
```
L'utente verrà loggato e verrano generati e restituiti i cookie della sessione.

Codici di errore:
- **400** ❌: manca un parametro (username o password)
- **401** ❌: username o password non corretti

Codici successo:
- **200** ✅: login avvenuto con successo
### ***Metodo GET:***
Senza bisogno di inviare dati aggiuntivi (oltre ai cookie) restituirà se l'utente è loggato o meno
- **401** ❌: utente non loggato

Codici successo:
- **200** ✅: utente loggato