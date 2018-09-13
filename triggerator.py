##############################################################################
## Triggerator triggera stringhe inserite via console dall'utente
## attualmente con 3 modalità (+ 1 in sequenza opzionale):
##
## MEGA trigger: aggiunge x tag trigger sull'intera stringa, utile per immagi-
## ni, quote, o in generale un effetto di trigger più ampio
##
## CHAIN trigger:
##  CRESCENDO: effetto frusta, con la coda a destra
##  DECRESCENDO: effetto frusta, con la coda a sinistra
##  ARMONICA: la vostra cazzo di sinusoide
##      nota: è possibile raggruppare più di una singola lettera in modalità
##          chain.
##
##                                                  - Nobsyde
##############################################################################


string = input('Inserire la stringa da triggerare e premere invio!\n')
mega_trig = int(input('Quanto vuoi MEGA triggerare? (0 = No)\n'))
char_per_trig = int(input(
    'Ogni quante lettere usare il CHAIN trig? (0 = No)\n'))

def mega_triggerer():
    mega_triggered_string = ('[triggered]' * mega_trig + string + 
        '[/triggered]' * mega_trig)
    return mega_triggered_string

def c_crescendo(string, char_t, n_armonica=0):
    """triggera in modalità chain crescendo"""
    triggered_string = '[triggered]'
    if char_t == 1:
        triggered_string += '[triggered]'.join(string[:])
    else:
        # calculate how many [/triggered] I have to add
        triggered_string += ('[triggered]'.join(string[i:i+char_t] 
            for i in range(0, len(string), char_t)) )

    # se non sono in modalità armonica, aggiungo le tag conclusive
    if n_armonica == 0:
        # calcolo quante tag devo inserire
        suffix = int(len(string)/char_t)
        if len(string) % char_t != 0:
            suffix += 1
        triggered_string += '[/triggered]' * suffix

    return triggered_string

def c_descrendo(string, char_t, n_armonica=0):
    """triggera in modalità chain decrescendo"""
    if char_t == 1:
        triggered_string = '[/triggered]'.join(string[:]) + '[/triggered]'
    else:
        # calculate how many [triggered] I have to add
        triggered_string = ('[/triggered]'.join(string[i:i+char_t]
                for i in range(0, len(string), char_t)) + '[/triggered]')

    # se non sono in modalità armonica, aggiungo le tag conclusive
    if n_armonica == 0:
        # calcolo quante tag devo inserire
        prefix = int(len(string)/char_t)
        if len(string) % char_t != 0:
            prefix += 1
        triggered_string = ('[triggered]' * prefix) + triggered_string

    return triggered_string

def c_armonica(string, char_t):
    """triggera in modalità chain armonica"""
    # divide string in 2
    char_string = int(len(string)/2)
    strings = [string[:char_string], string[char_string:]]

    # controllo se le due stringhe sono diverse, nel caso aggiungo uno spazio
    # alla stringa più corta
    if len(strings[0]) > len(strings[1]):
        strings[1] += ' '
    elif len(strings[0]) < len(strings[1]):
        strings[0] += ' '

    armonized_string = c_crescendo(strings[0], char_t, 1)
    armonized_string += c_descrendo(strings[1], char_t, 1)
    return armonized_string

def multi_armonica(string, char_t, n_armonica):
    """divide la stringa in n parti da passare a c_armonica"""
    char_string = int(len(string)/n_armonica)
    armonized_string = ''
    for i in range(n_armonica):
        # controllo se è l'ultimo ciclo, nel caso aggiungo i resti
        if i < n_armonica-1:
            partial_string = string[i*char_string:(i+1)*char_string]
        else:
            partial_string = string[i*char_string:]
        print(partial_string)
        # invio la stringa parziale a c_armonica, e la aggiungo a ar_str
        armonized_string += c_armonica(partial_string, char_t)

    return armonized_string


def chain_triggerer(string, char_t=1, chain_mode=0):
    """triggera un testo ogni char_t lettere"""
    # mndalità crescendo
    if chain_mode == 0:
        triggered_string = c_crescendo(string, char_t)

    # modalità decrescendo
    elif chain_mode == 1:
        triggered_string = c_descrendo(string, char_t)

    elif chain_mode == 2:
        n_armonica = int(input('Quante armoniche? (default: 1)\n'))
        if n_armonica > 1:
            triggered_string = multi_armonica(string, char_t, n_armonica)
        else:
            triggered_string = c_armonica(string, char_t)
        
    return triggered_string

if char_per_trig:
    chain_mode = int(input('Che modalità usare per il CHAIN trig?\n\
        0: chain crescendo (DEFAULT)\n\
        1: chain decrescendo\n\
        2: chain armonica\n'))
    if not chain_mode < 3:
        chain_mode = 0
    string = chain_triggerer(string, char_per_trig, chain_mode)
if mega_trig:
    string = mega_triggerer()

print(string)
