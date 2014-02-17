def load_box( DIM_X , DIM_Y , map_input_path ):
    with open(map_input_path, 'r') as map_input:
        map_input = map_input.readlines()
        map_input = [ e.strip() for e in map_input ]
        map_output = []
        #wywalanie komentarzy
        for e in map_input:
            if '#' not in e:
                comma = e.index(",")
                map_output.append(int(e[:comma]))
                map_output.append(int(e[comma+1:]))
        map_len = len(map_output)
        #sprawdzamy czy mamy krotnosc 8 linii poza komentarzami
        if map_len % 8 != 0:
            print "map input format error"
            raise ValueError
        
        matrix = numpy.zeros(shape=(DIM_X,DIM_Y))
        for i in range(0,len(map_output),8):
            print i
            a = (map_output[i], map_output[i+1])
            b = (map_output[i+2], map_output[i+3])
            c = (map_output[i+4], map_output[i+5])
            d = (map_output[i+6], map_output[i+7])
            points = (a, b, c, d)
            matrix = create_box
            
        return matrix