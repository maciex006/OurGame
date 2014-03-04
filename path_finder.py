__author__ = 'maciex'

#line1 = (1, (-1,3),(-2,2))
#line2 = (2, (-2,1),(-6,3),(-3,4))
#line3 = (3, (-1,1),(-6,2),(-4,4))
#line4 = (4, (-4,3),(-3,2),(-5,5))
#line5 = (5, (-5,4),(-6,6))
#line6 = (6, (-6,5))
#data = ( line1, line2, line3, line4, line5, line6 )

line1 = (1, (-1,2))
line2 = (2, (-1,1),(-2,3))
line3 = (3, (-2,2))
data = ( line1, line2, line3 )

# FUNKCJA ZWRACA LISTE PUNKTOW, PRZEZ KTORE TRZEBA PRZEJSC ZEBY DOSTAC SIE DO DOCELOWEGO POMIESZCZENIA


def find_path( currentPosition1, targetPosition1, data ):


    # FUNKCJA ZWRACA WSZYSTKIE POKOJE PRZYLEGACJACE DO CURRENTPOSITION, CHYBA, ZE JEST NIM POSZUKIWANY POKOJ
    # TARGET POSITION, WTEDY ZWRACA TYLKO JEGO NUMER
    def recur( currentPosition , targetPosition ):
        currentPosition = currentPosition -1
        path_ent = [0]
        path_cham = [0]
        for i in range(1, len(data[currentPosition])):

            new_path_ent = data[currentPosition][i][0]
            new_path_cham = data[currentPosition][i][1]

            path_ent = path_ent + [new_path_ent]
            path_cham = path_cham + [new_path_cham]

            if path_cham[i] == targetPosition:
                return ( path_ent[i] , path_cham[i] )
            else:
                pass
                #print path_cham[i]

        return (path_ent, path_cham)



    # FUNKCJA TWORZY STRUKTURE PATH, ZAWIERAJACA WSZYSTKIE MOZLIWE SCIEZKI
    # path - sciezka wczesniej przez nas wygenerowana (dopisuje nowe punkty do sciezki)
    # curPosition - aktualna nasza pozycja
    # nunber - indeks sciezki\

    def druga_iter( path , curPosition , number ):
        if number == -1:
            pathnumber = [curPosition]
        else:
            pathnumber = path[number]

        bufpath = [0]

        recur1 = recur( curPosition, targetPosition1)

        if recur1[1] == (targetPosition1):
            bufpath = pathnumber + [recur1[1]]
            return [bufpath]
        else:
            pass

        recur_len = len(recur1[1])

        path_ent = [0]

        for i in range(1,recur_len):
            path_ent = path_ent + [0]
            path_ent[i] = pathnumber + [recur1[1][i]]
            bufpath = bufpath + [path_ent[i]]

        bufpath.remove(0)
        return bufpath

    # FUNKCJA USUWA POZYCJE W LISCIE PRZEZNACZONE DO USUNIECIA
    def remove(path , remove):

        for i in range(0, len(remove)):
            del path[remove[i]]
            for j in range (0, len(remove)):
                remove[j] = remove[j]-1
        return path

    # FUNKCJA ZWRACA POZYCJE, KTORE NALEZY USUNAC, ZE WZGLEDU NA ZAPETLENIA
    # LOOP PREVENTION
    def removing(path):
        found = 0
        remove = [-1]
        for i in range(0,len(path)):
            for j in range(1,len(path[i])):
                if path[i][0] == path[i][j]:
                    found = 1
            if found == 1:
                remove = remove + [i]
                found = 0
        remove.remove(-1)
        return remove

    # SPRAWDZA CZY DOTARLISMY JUZ DO CELU
    def check(path, target):
        remove = [-1]
        for i in range(0, len(path)):
            if path[i][len(path[i])-1] == target:
                remove = remove + [-2]
            else:
                remove = remove + [i]

        if -2 in remove:
            remove.remove(-1)
            while -2 in remove:
                remove.remove(-2)
            return remove
        else:
            return -1


    # PO DRUGIEJ I TRZECIEJ ITERACJI

    # GLOWNA FUNKCJA ( NASZA AKTUALNA POZYCJA (KTORY POKOJ), CEL (POKOJ DO KTOREGO ZMIERZAMY))
    # ZWRACA SCIEZKE W POSTACI LISTY POKOI
    def main_func( currentPosition1 , targetPosition1 ):

        path = [0]
        path = druga_iter(path , currentPosition1 , -1)
        j = 1
        while ( check(path, targetPosition1) == -1):
            bufpath = [0]
            for i in range(len(path)):
                bufpath = bufpath + druga_iter(path , path[i][j] , i)

            bufpath.remove(0)
            path = bufpath
            path = remove(path , removing(path))
            j = j + 1

        path = remove(path, check(path, targetPosition1))
        #######################################################print(path)
        return path

    # FUNKCJA "TLUMACZACA" SCIEZKE ZAWIERAJACA NUMERY POKOI, NA SCIEZKE ZAWIERAJACA NUMERY DRZWI
    def translate(path):

        new_path = [[0]]
        first_iteration = 1
        for m in range(len(path)):
            if first_iteration == 1:
                first_iteration = 0
            else:
                new_path = new_path + [[0]]
            for j in range(0, len(path[m])-1):
                for i in range(1,len(data[path[m][j]-1])):
                    if data[path[m][j]-1][i][1] == path[m][j+1] :
                        new_path[m] = new_path[m] + [data[path[m][j]-1][i][0]]

            new_path[m].remove(0)

        return new_path


    return translate( main_func( currentPosition1 , targetPosition1 ) )

