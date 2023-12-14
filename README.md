# advdaba_tp2
On utilise curl et sed pour télécharger et transformer les données en streaming.
Les données streamées sont données au script import.py qui utilise ijson pour lire les objets après 10000 objets lu un background process va envoyer en une fois les 10000 objets à la base de données.