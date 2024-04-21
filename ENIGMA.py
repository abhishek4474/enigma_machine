# START

import sys

# Fetching and printing information about the Enigma

print("THE ENIGMA MACHINE\n")
with open("EnigmaInfo.txt", "r") as f:
    f1 = f.read()
    print(f1)
ax = 1

# --x--x--x--xMain loop starts--x--x--x--x

while ax == 1:

    # List definition

    rotors = [1, 2, 3, 4, 5, 6, 7, 8]
    l1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
          'W', 'X', 'Y', 'Z']
    l = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
         'W', 'X', 'Y', 'Z']
    temp1 = rotors
    temp2 = l
    rt = []

    # --x--x--x--xStart of setting selector part--x--x--x--x

    # Plugboard settings input

    n = int(input("Enter the number of connections you wish to make (maximum 10): "))
    temp = l1
    di = {}
    if n < 0:
        print("Please enter a positive integer less than or equal to 10.")
    elif n == 0:
        pass
    elif n > 10:
        print("You can make a maximum of 10 connections only.")
    else:
        for i in range(0, n):
            print(temp)
            k = input("Enter the first letter of the connection pair: ")
            k = k.upper()
            v = input("Enter the second letter of the connection pair: ")
            v = v.upper()
            temp.pop(temp.index(k))
            temp.pop(temp.index(v))
            di[k] = v
            di[v] = k

    # Rotor settings input

    for i in range(0, 3):
        p = []
        print(temp1)
        r = int(input("Enter a rotor number from the list above: "))
        temp1.pop(temp1.index(r))
        print(temp2)
        a = input("Enter the starting letter: ")
        a = a.upper()
        if a not in l:
            print("Please enter a valid character")
            sys.exit()
        p.extend([r, a])
        rt.append(p)

    # Reflector settings input

    rfc = ["B", "C", "B thin", "C thin"]
    print(rfc)
    rf = int(input("Enter a number from 0 to 3 to choose a reflector from the following: "))
    if rf > len(rfc):
        print("Please choose a valid number")
        sys.exit()
    else:
        r = rfc[rf]
    print("Your part selection is the following:", di, rt, r, sep="\n")
    o = input("Are you satisfied with your selection? (Y/N): ")
    o = o.upper()
    if o == "Y":
        pass
    else:
        sys.exit()

    # --*--*--*--*End of setting selector part--*--*--*--

    # Connecting MySQL

    import mysql.connector as sqltor

    mycon = sqltor.connect(host="localhost", user="root", passwd="011cr7", database="enigma")
    if mycon.is_connected():
        print("Connection Successful")
    else:
        print("Connection Failed")
    cursor = mycon.cursor()

    # Main string input

    pt1 = input("Enter a string to encode/decode: ")
    pt1 = pt1.upper()
    pt1 = pt1.replace(" ", "")

    # Shift variable declaration

    j = 0
    b = 0
    g = 0
    op = ""

    # --x--x--x--xWorking loop starts--x--x--x--x

    for i in range(0, len(pt1)):

        # Plugboard switching

        pt = ""
        if pt1[i] in di.keys():
            t = di[pt1[i]]
            pt = t
        else:
            pt = pt1[i]

        # Plugboard -> Rotor 1

        n = l.index(pt) + j + l.index(rt[0][1])
        m = n % 26
        k = l[m]
        d = rt[0][0]
        q = "SELECT {} from rotors WHERE rotor= '{}';".format(k, d)
        cursor.execute(q)
        data = cursor.fetchall()
        c = data[0][0]
        

        # Rotor 1 -> Rotor 2

        n1 = l.index(c) + b + l.index(rt[1][1])
        m1 = n1 % 26
        k1 = l[m1]
        d1 = rt[1][0]
        q1 = "SELECT {} from rotors WHERE rotor= '{}';".format(k1, d1)
        cursor.execute(q1)
        data1 = cursor.fetchall()
        c1 = data1[0][0]

        # Rotor 2 -> Rotor 3

        n2 = l.index(c1) + g + l.index(rt[2][1])
        m2 = n2 % 26
        k2 = l[m2]
        d2 = rt[2][0]
        q2 = "SELECT {} from rotors WHERE rotor= '{}';".format(k2, d2)
        cursor.execute(q2)
        data2 = cursor.fetchall()
        c2 = data2[0][0]

        # Rotor 3 -> Reflector

        ct1 = ""
        h = c2
        qrf = "SELECT {} from reflectors WHERE reflectors = '{}';".format(h, r)
        cursor.execute(qrf)
        datarf = cursor.fetchall()
        ct1 = datarf[0][0]

        # Reverse path starts

        # Reflector -> Rotor 3

        n2r = l.index(ct1)
        m2r = n2r % 26
        k2r = l[m2r]
        d2r = rt[2][0]
        q2r = "SELECT * from rotors WHERE rotor= '{}';".format(d2r)
        cursor.execute(q2r)
        data2r = cursor.fetchall()
        ct2r = ""
        for y in range(1, len(data2r[0])):
            if data2r[0][y] == k2r:
                ct2r = l[(y - g - 1 - l.index(rt[2][1])) % 26]
        c2r = ct2r

        # Rotor 3 -> Rotor 2

        n1r = l.index(c2r)
        m1r = n1r % 26
        k1r = l[m1r]
        d1r = rt[1][0]
        q1r = "SELECT * from rotors WHERE rotor= '{}';".format(d1r)
        cursor.execute(q1r)
        data1r = cursor.fetchall()
        ct1r = ""
        for y in range(1, len(data1r[0])):
            if data1r[0][y] == k1r:
                ct1r = l[(y - b - 1 - l.index(rt[1][1])) % 26]
        c1r = ct1r

        # Rotor 2 -> Rotor 1

        nr = l.index(c1r)
        mr = nr % 26
        kr = l[mr]
        dr = rt[0][0]
        qr = "SELECT * from rotors WHERE rotor= '{}';".format(dr)
        cursor.execute(qr)
        datar = cursor.fetchall()
        ctr = ""
        for y in range(1, len(datar[0])):
            if datar[0][y] == kr:
                ctr = l[(y - j - 1 - l.index(rt[0][1])) % 26]
        cr = ctr

        # Rotor 1 -> Plugboard

        ptr = ""
        if cr in di.keys():
            tr = di[cr]
            ptr = tr
        else:
            ptr = cr
        op += ptr

        # Incrementing shift variables

        j += 1
        if j % 26 == 0 and j != 0:
            b += 1
        if b % 26 == 0 and b != 0:
            g += 1

    # --x--x--x--xWorking loop ends--x--x--x--x

    print(op)
    ax = 0

    # Asking user to continue/end the program

    ch1 = input("Do you want to continue? (Y/N): ")
    if ch1 in "yY":
        ax = ax + 1
    elif ch1 in "nN":
        break
    else:
        print("Invalid Choice")

# --x--x--x--xMain loop ends--x--x--x--x

# END
