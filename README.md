
# SI - Tema 1
### Postu Codrin

## Cerinta

>Implementati o infrastructura de comunicatie ce foloseste criptosistemul AES pentru
criptarea traficului intre doua noduri A si B cu urmatoarele caracteristici:
1. Se considera un nod KM (key manager) care detine doua chei pe 128 de biţi K si
K’. Cheia K este asociata cu un mod de operare ECB sau CFB. Cheia K’ este
utilizata pentru criptarea cheii K. Se considera ca vectorul de initializare are o
valoare fixata cunoscuta din start atat de A cat si de B. De asemenea cheia K’ este
detinuta din start si de A si de B.
2. Pentru a initia o sesiune de comunicare securizata nodul A trimite un mesaj catre B
in care comunica modul de operare (ECB sau CFB), cerand in acelasi timp nodului
KM cheia de criptare. Acesta genereaza cheia K in mod random, cu ajutorul unei
librarii criptografice, si apoi o cripteaza ca un singur bloc cu AES folosind cheia K’,
dupa care o trimite nodului A. Dupa ce A primeste cheia criptata de la KM, acesta o
trimite mai departe nodului B. A si B vor decripta cheia K pentru a incepe
comunicarea. De asemenea nodul B va trimite catre A un mesaj de incepere a
comunicarii.
3. Dupa primirea mesajului de confirmare de la B (referitor la inceperea
comunicarii), A incepe sa trimita catre B continutul unui fisier criptat pe blocuri
folosind modul selectat. Nodul B va decripta blocurile primite si va afisa rezultatul
obtinut.

## Exemple de cod

Ma folosesc de AES din libraria pycryprodomex pentru algoritmul de criptare. In aceste cazuri ma folosesc de ECB deoarece nu necesita decat o cheie si procesarea este independenta de celelalte blocuri 

 ###Modul ECB


    aes = AES.new(key_2, AES.MODE_ECB)
            text_curr_block = provided_text[16 * curr_block:16 * (curr_block + 1)]

    if enc_mode == 'ECB':
            cipher_curr_block = aes.encrypt(text_curr_block)


### Modul CFB
    
    aes = AES.new(key_2, AES.MODE_ECB)
    text_curr_block = provided_text[block_size * curr_block:block_size * (curr_block + 1)]
         ...    
    elif enc_mode == 'CFB':
            cipher_curr_block = aes.encrypt(iv)
            cipher_curr_block = xor(cipher_curr_block, text_curr_block)
            iv = cipher_curr_block  # the current ciphertext becomes the iv for next block
            node_b_socket.sendall(cipher_curr_block)

## Pasi instalare
Asigurati-va ca aveti instalat Python 3.5+
https://www.python.org/


1. Clone la proiect pe calculatorul propriu.
2. Proiectul contine 3 fisiere python. 
	- Daca aveti PyCharm, doar deschideti directorul cu proiectul in aplicatie si compilati fisierele in ordinea urmatoare: 
	    - KeyManager.py
	    - NodeB.py
	    - NodeA.py
    - Din linia de comanda puteti sa intrati in directorul unde sunt cele 3 fisiere si scrieti `python [filename.py]` in aceeasi ordine prezentata mai sus
  3. In cazul in care nu functioneaza pycryptodomex, puteti urmari pasii de aici pentru a (re)instala libraria https://pycryptodome.readthedocs.io/en/latest/src/installation.html
	

## Bibliografie

1. https://pycryptodome.readthedocs.io/en/
2. https://profs.info.uaic.ro/~liliana.cojocaru/
3. https://www.programiz.com/python-programming/methods/built-in/bytearray
4. https://www.dlitz.net/software/pycrypto/api/2.6/Crypto.Cipher.AES-module.html

## Erori cunoscute

1. Pentru a trimite textul complet, adaug folosind ljust spatii la finalul acestuia. Textul decodat va ramane cu spatiile de la final.