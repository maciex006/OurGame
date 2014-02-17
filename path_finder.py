__author__ = 'maciex'

line1 = (1, (-1,3),(-2,2))
line2 = (2, (-2,1),(-6,3),(-3,4))
line3 = (3, (-1,1),(-6,2),(-4,4))
line4 = (4, (-4,3),(-3,2),(-5,5))
line5 = (5, (-5,4),(-6,6))
line6 = (6, (-6,5))
data = ( line1, line2, line3, line4, line5 )

def find( currentPosition1, targetPosition1, data ):


    #przeszukanie line1
    def recur( currentPosition , targetPosition ):
        currentPosition = currentPosition -1
        path_ent = [0]
        path_cham = [0]
        for i in range(1, len(data[currentPosition])):

            new_path_ent = data[currentPosition][i][0]
            new_path_cham = data[currentPosition][i][1]

            path_ent = path_ent + [new_path_ent]
            path_cham = path_cham + [new_path_cham]
            #path_ent[i-1] =  data[currentPosition][i][0]
            #path_cham[i-1] = data[currentPosition][i][1]

            if path_cham[i] == targetPosition:
                return ( path_ent[i] , path_cham[i] )
                print("returnelo")
            else:
                pass
                #print path_cham[i]

        return (path_ent, path_cham)



    # DRUGA ITERACJA

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





    def remove(path , remove):

        for i in range(0, len(remove)):
            del path[remove[i]]
            for j in range (0, len(remove)):
                remove[j] = remove[j]-1
        return path

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
            print(remove)
            return remove
        else:
            return -1



    '''
    def removing2(path):
        found = 0
        remove = [-1]
        leng = len(path)
        for i in range(0, leng):
            for j in range(0,len(path[i])-2):
                for k in range(0, leng):
                    print(str(path[i][j]) + " = " + str(path[k][len(path[k])-1]))
                    if path[i][j] == path[k][len(path[k])-1]:
                        print("DEL")
                        remove = remove + [k]

        remove.remove(-1)
        print("REM" + str(remove))
        return remove
    '''

    # PO DRUGIEJ I TRZECIEJ ITERACJI

    path = [0]
    print(path)
    path = druga_iter(path , currentPosition1 , -1)
    print(path)
    print(path[0][1])
    path = druga_iter(path , path[0][1] , 0) + druga_iter(path, path[1][1], 1)
    print(path)
    path = remove(path , removing(path))
    print(path)
    path = druga_iter(path , path[0][2] , 0) + druga_iter(path, path[1][2], 1) + druga_iter(path, path[2][2], 2) + druga_iter(path, path[3][2], 3)
    print(path)
    if ( check(path, 5) != -1):
          print "KONIEC"
    path = remove(path, check(path, 5))
    print(path)


find(1,5,data)
