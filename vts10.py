import math

# vts10 [260824]

titolo = 'Verifica Tracciati Stradali 1.0 | Eslam Anter'
mail = 'eslam.anter@outlook.com'

percorso, vrfp, vrfa, gen, log = '', '', '', '', ''
datpla, elmp = [[], [], []], []
datalt, elma = [[], [], []], []
datimp, datlim = [], [[], [], [], []]
vel1, velf, velr = [[], []], [[], []], [[], []]
dva, dvar, dvc, dvs = [[], []], [[], []], [[], []], [[], []]
n, b, vpmin, vpmax, pi, pf = 0, 0.00, 0, 0, 0.000, 0.000
imp_ok, lim_ok = False, False

nrm = (
    ('[0] CatStrada', '[1] B/Corsia', '[2] Vpmin', '[3] Vpmax', '[4] Rmin', '[5] R*', '[6] R2.5', "[7] R'",
     '[8] qmax', '[9] c', '[10] imax', '[11] Sensi'),
    ('[A]\tAutostrada extraurbana\t\t(Strada principale)', 3.75, 90, 140, 339, 964, 4820, 10250, 0.070, 1.74, 0.05, 1),
    ('[A]\tAutostrada extraurbana\t\t(Strada di servizio)', 3.50, 40, 100, 45, 437, 2187, 5250, 0.070, 1.23, 0.05, 1),
    ('[A]\tAutostrada urbana\t\t(Strada principale)', 3.75, 80, 140, 252, 964, 4820, 10250, 0.070, 1.74, 0.06, 1),
    ('[A]\tAutostrada urbana\t\t(Strada di servizio)', 3.00, 40, 60, 45, 121, 204, 1150, 0.035, -0.244, 0.06, 1),
    ('[B]\tStrada extraurbana principale\t(Strada principale)', 3.75, 70, 120, 178, 667, 3334, 7500, 0.070, 1.50, 0.06, 1),
    ('[B]\tStrada extraurbana principale\t(Strada di servizio)', 3.50, 40, 100, 45, 437, 2187, 5250, 0.070, 1.23, 0.06, 1),
    ('[C1]\tStrada extraurbana secondaria', 3.75, 60, 100, 118, 437, 2187, 5250, 0.070, 1.23, 0.07, 2),
    ('[C2]\tStrada extraurbana secondaria', 3.50, 60, 100, 118, 437, 2187, 5250, 0.070, 1.23, 0.07, 2),
    ('[D]\tStrada urbana di scorrimento\t(Strada principale)', 3.25, 50, 80, 77, 240, 708, 2000, 0.050, 0.51, 0.06, 1),
    ('[D]\tStrada urbana di scorrimento\t(Strada di servizio)', 2.75, 25, 60, 19, 121, 204, 1150, 0.035, -0.244, 0.06, 1),
    ('[E]\tStrada urbana di quartiere', 3.00, 40, 60, 51, 121, 204, 1150, 0.035, -0.244, 0.08, 2),
    ('[F1]\tStrada extraurbana locale', 3.50, 40, 100, 45, 437, 2187, 5250, 0.070, 1.23, 0.10, 2),
    ('[F2]\tStrada extraurbana locale', 3.25, 40, 100, 45, 437, 2187, 5250, 0.070, 1.23, 0.10, 2),
    ('[F]\tStrada urbana locale', 2.75, 25, 60, 19, 121, 204, 1150, 0.035, -0.244, 0.10, 2)
)


def reset():
    global vrfp, vrfa, datpla, datalt, elmp, elma, vel1, velf, velr, pi, pf, datimp, datlim, dva, dvar, dvc, dvs, imp_ok, lim_ok, gen, log
    vrfp, vrfa, gen, log= '', '', '', ''
    datpla, elmp = [[], [], []], []
    vel1, velf, velr = [[], []], [[], []], [[], []]
    datalt, elma = [[], [], []], []
    datimp, datlim= [], [[], [], [], []]
    dva, dvar, dvc, dvs = [[], []], [[], []], [[], []], [[], []]
    imp_ok, lim_ok = False, False
    init()


def elim_tab(testo):
    tab = ['\t\t\t', '\t\t', '\t']
    for t in tab:
        testo = testo.replace(t, ' ')
    return testo


def pk(p):
    s = '-' if p < 0 else ''
    p = abs(p)
    km = int(p / 1000)
    m = int(p - km * 1000)
    mm = int(round(p - km * 1000 - m, 3) * 1000)
    return f'{s}{km}+{m:03d}.{mm}'


def pm(p):
    if '+' in str(p):
        m = p.replace('+', '')
    else:
        m = p
    return m


def correg():
    global pi, pf, elmp, elma
    pi = pi / 1000
    pf = pf / 1000

    for i in range(len(elmp)):
        if elmp[i][0] == 'r':
            elmp[i][0] = 'Rettifilo'
            elmp[i][7] = f'{round(elmp[i][7] * 100, 2)}'
            if elmp[i][2] == 'f':
                elmp[i][2] = 'Flesso'
        if elmp[i][0] == 'c':
            elmp[i][0] = 'Clotoide'
        if elmp[i][0] == 'a':
            elmp[i][0] = 'Arco'
            elmp[i][7] = f'{round(elmp[i][7] * 100, 2)}'
        elmp[i][3] = pk(elmp[i][3] / 1000)
        elmp[i][4] = pk(elmp[i][4] / 1000)

    for i in range(len(elma)):
        if elma[i][0] == 'l':
            elma[i][0] = 'Livelletta'
            elma[i][2] = f'{round(elma[i][2] * 100, 2)}'
        if elma[i][0] == 'r':
            elma[i][0] = 'Raccordo'
        elma[i][3] = pk(elma[i][3] / 1000)
        elma[i][4] = pk(elma[i][4] / 1000)


def msg(testo):
    global log
    print(testo)
    log += f'{testo}\n'


def stampa():
    import datetime
    global titolo, nrm, n, b, vpmin, vpmax, pi, pf, percorso, vel1, velr, elmp, vrfp, elma, vrfa, dvar, dvc, dvs, gen, log, mail
    nome_vel1 = 'velocità prima fase'
    nome_velr = 'velocità fase finale'
    nome_elmp = 'elementi planimetrici'
    nome_vrfp = 'verifiche planimetriche'
    nome_elma = 'elementi altimetrici'
    nome_vrfa = 'verifiche altimetriche'
    nome_gen = 'dati generali'
    nome_dvar = 'visibilità arresto'
    nome_dvc = 'visibilità cambio corsia'
    nome_dvs = 'visibilità sorpasso'
    nome_log = 'eventi'

    try:
        if elmp != []:
            with open(f'{percorso}\\{nome_vel1}.txt', 'w') as file:
                file.write('')
            with open(f'{percorso}\\{nome_vel1}.txt', 'a') as file:
                for i in range(len(vel1[0])):
                    file.write(f'{vel1[0][i]}\t{vel1[1][i]}\n')
            with open(f'{percorso}\\{nome_velr}.txt', 'w') as file:
                file.write('')
            with open(f'{percorso}\\{nome_velr}.txt', 'a') as file:
                for i in range(len(velr[0])):
                    file.write(f'{velr[0][i]}\t{velr[1][i]}\n')
            print(f"File '{nome_vel1}.txt', '{nome_velr}.txt' creati.")

            with open(f'{percorso}\\{nome_elmp}.txt', 'w') as file:
                file.write(f'N.\tElemento\tLunghezza [m]\tRaggio [m]\tParametro A\tProg. iniziale [km]\tProg. finale [km]'
                           f'\tVel. prima fase [km/h]\tVmax [km/h]\tqmax [%]\tAllargamento [m]\n')
            with open(f'{percorso}\\{nome_elmp}.txt', 'a') as file:
                txt = ''
                for i in range(len(elmp)):
                    if elmp[i][0] == 'Rettifilo':
                        txt += f'{i +1}\t{elmp[i][0]}\t{elmp[i][1]}\t\t{elmp[i][2]}\t{elmp[i][3]}\t{elmp[i][4]}\t{elmp[i][5]}\t{elmp[i][6]}\t{elmp[i][7]}\t{elmp[i][8]}\n'
                    if elmp[i][0] == 'Clotoide':
                        txt += f'{i +1}\t{elmp[i][0]}\t{elmp[i][1]}\t\t{elmp[i][2]}\t{elmp[i][3]}\t{elmp[i][4]}\t{elmp[i][5]}\t{elmp[i][6]}\t{elmp[i][7]}\t{elmp[i][8]}\n'
                    if elmp[i][0] == 'Arco':
                        txt += f'{i +1}\t{elmp[i][0]}\t{elmp[i][1]}\t{elmp[i][2]}\t\t{elmp[i][3]}\t{elmp[i][4]}\t{elmp[i][5]}\t{elmp[i][6]}\t{elmp[i][7]}\t{elmp[i][8]}\n'
                file.write(txt)
            with open(f'{percorso}\\{nome_vrfp}.txt', 'w') as file:
                file.write('')
            with open(f'{percorso}\\{nome_vrfp}.txt', 'a') as file:
                file.write(f'{vrfp}\n')
            print(f"File '{nome_elmp}.txt', '{nome_vrfp}.txt' creati.")

        if dvc != [[], []]:
            with open(f'{percorso}\\{nome_dvc}.txt', 'w') as file:
                file.write('')
            with open(f'{percorso}\\{nome_dvc}.txt', 'a') as file:
                for i in range(len(dvc[0])):
                    file.write(f'{dvc[0][i]}\t{dvc[1][i]}\n')
            print(f"File '{nome_dvc}.txt' creato.")

        if dvs != [[], []]:
            with open(f'{percorso}\\{nome_dvs}.txt', 'w') as file:
                file.write('')
            with open(f'{percorso}\\{nome_dvs}.txt', 'a') as file:
                for i in range(len(dvs[0])):
                    file.write(f'{dvs[0][i]}\t{dvs[1][i]}\n')
            print(f"File '{nome_dvs}.txt' creato.")

        if elma != []:
            with open(f'{percorso}\\{nome_elma}.txt', 'w') as file:
                file.write(f'N.\tElemento\tLunghezza [m]\tPendenza [%]\tRaggio [m]\tProg. iniziale [km]\tProg. finale [km]\tAndamento\t'
                           f'Vmax [km/h]\n')
            with open(f'{percorso}\\{nome_elma}.txt', 'a') as file:
                txt = ''
                for i in range(len(elma)):
                    if elma[i][0] == 'Livelletta':
                        txt += f'{i +1}\t{elma[i][0]}\t{elma[i][1]}\t{elma[i][2]}\t\t{elma[i][3]}\t{elma[i][4]}\t{elma[i][5]}\t{elma[i][6]}\n'
                    if elma[i][0] == 'Raccordo':
                        txt += f'{i +1}\t{elma[i][0]}\t{elma[i][1]}\t\t{elma[i][2]}\t{elma[i][3]}\t{elma[i][4]}\t{elma[i][5]}\t{elma[i][6]}\n'
                file.write(txt)
            with open(f'{percorso}\\{nome_vrfa}.txt', 'w') as file:
                file.write('')
            with open(f'{percorso}\\{nome_vrfa}.txt', 'a') as file:
                file.write(f'{vrfa}\n')
            print(f"File '{nome_elma}.txt', '{nome_vrfa}.txt' creati.")

            with open(f'{percorso}\\{nome_dvar}.txt', 'w') as file:
                file.write('')
            with open(f'{percorso}\\{nome_dvar}.txt', 'a') as file:
                for i in range(len(dvar[0])):
                    file.write(f'{dvar[0][i]}\t{dvar[1][i]}\n')
            print(f"File '{nome_dvar}.txt' creato.")

        if elmp != []:
            with open(f'{percorso}\\{nome_gen}.txt', 'w') as file:
                txt = f'{titolo}\n\n'
                txt += f'Riferimenti normativi:\tD.M. 6792 del 05/11/2001\n'
                txt += f'Tipo strada:\t{elim_tab(nrm[n][0])}\n'
                txt += f'Tipo piattaforma:\t'
                if nrm[n][11] == 1:
                    txt += f'Carreggiata separata ad unico senso di marcia\n'
                if nrm[n][11] == 2:
                    txt += f'Carreggiata singola a due sensi di marcia\n'
                txt += f'Distanza B fra asse rotazione e estremità carreggiata:\t{b} m\n'
                txt += f'Velocità minima di progetto:\t{vpmin} km/h\n'
                txt += f'Velocità massima di progetto:\t{vpmax} km/h\n'
                txt += f'Progressiva iniziale:\t{pk(pi)} m\n'
                txt += f'Progressiva finale:\t{pk(pf)} m\n'
                txt += f'Lunghezza tracciato:\t{pf - pi} m\n\n'
                file.write(txt)
            print(f"File '{nome_gen}.txt' creato.")

        with open(f'{percorso}\\{nome_log}.txt', 'w') as file:
            ora = datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")
            txt = f'{titolo}'
            txt += f'\n...\n'
            if log == '':
                txt += 'Nessun evento.\n'
            else:
                txt += log
            txt += f'...\n'
            txt += f'Data e ora di stampa: {ora}\n'
            txt += f'Segnalare problemi a: {mail}'
            file.write(txt)
        print(f"File '{nome_log}.txt' creato.")

    except PermissionError:
        msg('*Accesso negato. File output non creati. Avviare come amministratore o cambiare percorso cartella.')


def ok(crt, elm, rif):
    if crt == 'min':
        if elm < rif:
            return 0
        else:
            return 1
    if crt == 'max':
        if elm > rif:
            return 0
        else:
            return 1


def vmax(i, f):
    global velf, pi
    v = max(velf[1][i - pi:f - pi + 1])
    return round(v, 2)


def trova_pend(p):
    global elma
    for i in range(len(elma)):
        if p <= elma[i][4]:
            if elma[i][0] == 'l':
                pend = elma[i][2]
            if elma[i][0] == 'r':
                pend = elma[i - 1][2] + ((p - elma[i][3]) / (elma[i][1] * 1000)) * (elma[i + 1][2] - elma[i - 1][2])
            break
    return round(pend, 4)


def trova_fe(v):
    global n
    grp_fe = ((1, 3), (2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14))
    tab_fe1 = ((80, 90, 100, 110, 120, 130, 140), (0.51, 0.49, 0.47, 0.46, 0.45, 0.44, 0.43))
    tab_fe2 = ((30, 40, 50, 60, 70, 80, 90, 100, 110, 120), (0.51, 0.48, 0.46, 0.43, 0.40, 0.38, 0.36, 0.35, 0.33, 0.31))
    if n in grp_fe[0]:
        fe = tab_fe1[1][0]
        if v > tab_fe1[0][0]:
            fe = tab_fe1[1][-1]
            for s in tab_fe1[0][1:]:
                if v < s:
                    j = tab_fe1[0].index(s)
                    vinf = tab_fe1[0][j - 1]
                    vsup = s
                    fe = tab_fe1[1][j - 1] + ((v - vinf) / (vsup - vinf)) * (tab_fe1[1][j] - tab_fe1[1][j - 1])
                    break
    if n in grp_fe[1]:
        fe = tab_fe2[1][0]
        if v > tab_fe2[0][0]:
            fe = tab_fe2[1][-1]
            for s in tab_fe2[0][1:]:
                if v < s:
                    j = tab_fe2[0].index(s)
                    vinf = tab_fe2[0][j - 1]
                    vsup = s
                    fe = tab_fe2[1][j - 1] + ((v - vinf) / (vsup - vinf)) * (tab_fe2[1][j] - tab_fe2[1][j - 1])
                    break
    return round(fe, 3)


def trova_ft(v):
    global n
    grp_ft = ((1, 2, 3, 4, 5, 6, 7, 8, 12, 13), (9, 10, 11, 14))
    tab_ft1 = ((40, 60, 80, 100, 120, 140), (0.21, 0.17, 0.13, 0.11, 0.10, 0.09))
    tab_ft2 = ((25, 40, 60, 80), (0.22, 0.21, 0.20, 0.16))
    if n in grp_ft[0]:
        ft = tab_ft1[1][0]
        if v > tab_ft1[0][0]:
            ft = tab_ft1[1][-1]
            for s in tab_ft1[0][1:]:
                if v < s:
                    j = tab_ft1[0].index(s)
                    vinf = tab_ft1[0][j - 1]
                    vsup = s
                    ft = tab_ft1[1][j - 1] + ((v - vinf) / (vsup - vinf)) * (tab_ft1[1][j] - tab_ft1[1][j - 1])
                    break
    if n in grp_ft[1]:
        ft = tab_ft2[1][0]
        if v > tab_ft2[0][0]:
            ft = tab_ft2[1][-1]
            for s in tab_ft2[0][1:]:
                if v < s:
                    j = tab_ft2[0].index(s)
                    vinf = tab_ft2[0][j - 1]
                    vsup = s
                    ft = tab_ft2[1][j - 1] + ((v - vinf) / (vsup - vinf)) * (tab_ft2[1][j] - tab_ft2[1][j - 1])
                    break
    return round(ft, 3)


def visa(v, i):
    a = 0.78 * v - 0.0028 * (v ** 2) + ((v ** 2) / (254 * (trova_fe(v) + i)))
    return round(a, 3)


def visc(v):
    c = 2.6 * v
    return round(c, 3)


def viss(v):
    s = 5.5 * v
    return round(s, 3)


def vrf_racc(v, l, i1, i2):
    global nrm, n
    im = (i1 + i2) / 2
    da, ds = visa(v, im), viss(v)
    di = abs(i2 - i1)
    rvmins = 0
    # Caso raccordo convesso (dosso)
    h1 = 1.1
    if i1 > i2:
        rvminr = 20

        # D = Da
        h2 = 0.1
        if da <= l:
            rvmina = round((da ** 2) / (2 * (h1 + h2 + 2 * (h1 * h2) ** 0.5)), 3)
        if da > l:
            rvmina = round((2 / di) * (da - (h1 + h2 + 2 * (h1 * h2) ** 0.5) / di), 3)

        # D = Ds
        if nrm[n][11] == 2:
            h2 = 1.1
            if ds <= l:
                rvmins = round((ds ** 2) / (2 * (h1 + h2 + 2 * (h1 * h2) ** 0.5)), 3)
            if ds > l:
                rvmins = round((2 / di) * (ds - (h1 + h2 + 2 * (h1 * h2) ** 0.5) / di), 3)

    # Caso raccordo concavo (sacca)
    h = 0.5
    t = 1 * math.pi / 180
    if i2 > i1:
        rvminr = 40

        # D = Da
        if da <= l:
            rvmina = round((da ** 2) / (2 * (h + da * t)), 3)
        if da > l:
            rvmina = round((2 / di) * (da - (h + da * t) / di), 3)

    rvminc = round((v / 3.6) ** 2 / 0.6, 3)
    avmax = 0.6

    rvmin = [rvmina, rvmins, rvminr, rvminc, avmax]
    return rvmin


def vrf_livl():
    global nrm, n
    imax = nrm[n][10]
    return imax


def r_curva(v):
    global nrm, n
    r = round(v ** 2 / (127 * (nrm[n][8] + trova_ft(v))), 3)

    return r


def vrf_curv(v, l1, l2):
    global nrm, n, vpmin

    if vpmin == nrm[n][2]:
        rmin = nrm[n][4]
    else:
        rmin = r_curva(vpmin)

    if l1 < 300:
        rminl1 = l1
    else:
        rminl1 = 400
    if l2 < 300:
        rminl2 = l2
    else:
        rminl2 = 400
    lmin = round(0.7 * v, 3)

    return [lmin, rmin, rminl1, rminl2]


def vrf_clot(v, a1, a2, r1, r2, q1, q2):
    global nrm, n, b
    dimax = 18 * b / v
    cmax = 50.4 / v
    g = 9.81

    if r1 == 0:
        rfitt = r2
    elif r2 == 0:
        rfitt = -r1
    else:
        rfitt = r1 * r2 / (r1 - r2)

    if abs(abs(q2) - q1) < abs(q2 - abs(q1)):
        q = abs(q2) - q1
    else:
        q = q2 - abs(q1)

    d = (v / 3.6) ** 3 / cmax
    e = (g * (v / 3.6) * rfitt * q) / cmax
    f = d - e
    if f > 0:
        amin1e = round(f ** 0.5, 3)
    else:
        amin1e = 0

    amin1a = round(0.021 * v ** 2, 3)
    amin2 = round(((abs(rfitt) / dimax) * 100 * b * abs(q2 - q1)) ** 0.5, 3)

    if r1 == 0 or r2 == 0:
        r = r1 + r2
        amin3 = round(r / 3, 3)
        amax = r
    else:
        amin3 = round(max(r1, r2) / 3, 3)
        amax = min(r1, r2)

    aminc1 = round((2 / 3) * a1, 3)
    aminc2 = round((2 / 3) * a2, 3)
    amaxc1 = round((3 / 2) * a1, 3)
    amaxc2 = round((3 / 2) * a2, 3)

    return [amin1e, amin1a, amin2, amin3, aminc1, aminc2, amax, amaxc1, amaxc2]


def vrf_rett(v, a1, a2):
    global vpmax
    tab_lmin = ((40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140), (30, 40, 50, 65, 90, 115, 150, 190, 250, 300, 360))
    if v > tab_lmin[0][0]:
        lmin = tab_lmin[1][-1]
        for s in tab_lmin[0]:
            if v < s:
                i = tab_lmin[0].index(s)
                vinf = tab_lmin[0][i - 1]
                vsup = s
                lmin = round(tab_lmin[1][i - 1] + ((v - vinf) / (vsup - vinf)) * (tab_lmin[1][i] - tab_lmin[1][i - 1]), 3)
                break
    else:
        lmin = tab_lmin[1][0]
    lmax = round(22 * vpmax, 3)
    lmaxf = round((a1 + a2) / 12.5, 3)

    return [lmin, lmax, lmaxf]


def q_curva(r):
    global nrm, n
    import math
    q = nrm[n][8]
    if nrm[n][5] <= r < nrm[n][6]:
        a, c = -0.64, nrm[n][9]
        q = math.exp(a * math.log(r) + c)
    if nrm[n][6] <= r < nrm[n][7]:
        q = 0.025
    if r >= nrm[n][7]:
        q = -0.025
    return round(q, 4)


def v_curva(r):
    global nrm, n, vpmax
    v = 0
    while 127 * (nrm[n][8] + trova_ft(v)) * r - v ** 2 > 0:
        if v < vpmax:
            v += 0.01
        else:
            v = vpmax
            break
    return round(v, 2)


def vrf_dati_lim():
    global datlim, pi, pf, vpmax
    lim_ok = True

    for i in range(len(datlim[0])):

        try:
            datlim[0][i] = int(round(float(pm(datlim[0][i])), 3) * 1000) # px1000
            if str(datlim[1][i]).lower() != 'f':
                if datlim[0][i] < pi or datlim[0][i] > pf:
                    lim_ok = False
                    msg(f'*Progressiva iniziale tratto n.{i + 1} fuori tracciato.')
                    break
        except ValueError:
            if str(datlim[0][i]).lower() != 'i' or str(datlim[1][i]).lower() == 'f':
                lim_ok = False
                msg(f'*Progressiva iniziale tratto n.{i + 1} non valida.')
                break

        try:
            datlim[1][i] = int(round(float(pm(datlim[1][i])), 3) * 1000) # px1000
            try:
                if datlim[1][i] < datlim[0][i]:
                    lim_ok = False
                    msg(f'*Progressiva finale tratto n.{i + 1} non deve essere antecedente a quella iniziale.')
                    break
                if str(datlim[0][i]).lower() != 'i':
                    if datlim[1][i] > pf:
                        lim_ok = False
                        msg(f'*Progressiva finale tratto n.{i + 1} fuori tracciato.')
                        break
            except TypeError:
                pass
        except ValueError:
            if str(datlim[1][i]).lower() != 'f' or str(datlim[0][i]).lower() == 'i':
                lim_ok = False
                msg(f'*Progressiva finale tratto n.{i + 1} non valida.')
                break

        try:
            datlim[2][i] = round(float(datlim[2][i]), 2)
            if datlim[2][i] > vpmax:
                lim_ok = False
                msg(f'*Velocità massima locale tratto n.{i + 1} non deve essere superiore a quella del tracciato.')
                break
        except ValueError:
            lim_ok = False
            msg(f'*Velocità massima locale tratto n.{i + 1} non valida.')
            break

        try:
            datlim[3][i] = abs(round(float(datlim[3][i]), 2))
        except ValueError:
            lim_ok = False
            msg(f'*Accelerazione riga n.{i + 1} non valida.')
            break

    # Creazione tabella limiti massimi locali
    if lim_ok:
        tmp = [['' for col in range(4)] for row in range(len(datlim[0]))]
        for i in range(len(datlim[0])):
            for j in range(4):
                tmp[i][j] = datlim[j][i]

        datlim = tmp
    return lim_ok


def calc_pla():
    global nrm, n, b, lim_ok, datpla, datlim, elmp, vpmax, pi, pf, vrfp, vel1, velf, velr, dvc, dvs

    # Creazione tabella tracciato planimetrico da dati importati
    elmp = [['' for col in range(9)] for row in range(len(datpla[0]))]
    '''
    elmp[i][0] = elemento
    elmp[i][1] = lunghezza
    elmp[i][2] = raggio/parametro A
    elmp[i][3] = progressiva inizio
    elmp[i][4] = progressiva fine
    elmp[i][5] = v1
    elmp[i][6] = vfmax
    elmp[i][7] = qmax
    elmp[i][8] = allargamento
    '''
    for i in range(len(datpla[0])):
        for j in range(3):
            elmp[i][j] = datpla[j][i]

    # Calcolo progressive iniziali e finali elementi planimetrici px1000
    pi = int(pi * 1000)
    for i in range(len(elmp)):
        if i == 0:
            elmp[i][3] = pi
        else:
            elmp[i][3] = elmp[i - 1][4]
        elmp[i][4] = int(elmp[i][3] + elmp[i][1] * 1000)
    pf = elmp[len(elmp) - 1][4]

    # Creazione diagramma velocita' prima fase px1 e fase finale px1000
    vel1, velf = [[], []], [[], []]
    p = pi
    while p <= pf:
        velf[0].append(p)
        velf[1].append(vpmax)
        p += 1

    for i in range(len(elmp)):
        if elmp[i][0] == 'a':
            elmp[i][5] = v_curva(elmp[i][2])

            vel1[0].append(elmp[i][3] / 1000)
            vel1[1].append(elmp[i][5])
            vel1[0].append(elmp[i][4] / 1000)
            vel1[1].append(elmp[i][5])

            p = elmp[i][3]
            while p <= elmp[i][4]:
                velf[1][p - pi] = elmp[i][5]
                p += 1
        else:
            elmp[i][5] = vpmax

    print("Diagramma delle velocità prima fase calcolato.")

    # Calcolo diagramma velocita' fase finale px1000
    for i in range(len(elmp)):
        if elmp[i][0] == 'a':
            p = elmp[i][3] - 1
            v1 = velf[1][p - pi]
            v2 = (((velf[1][p - pi + 1] / 3.6) ** 2 + 2 * 0.8 * 0.001) ** 0.5) * 3.6
            while v2 < v1 and p >= pi:
                v1 = velf[1][p - pi]
                v2 = (((velf[1][p - pi + 1] / 3.6) ** 2 + 2 * 0.8 * 0.001) ** 0.5) * 3.6
                if v2 < v1:
                    velf[1][p - pi] = v2
                p -= 1

            p = elmp[i][4] + 1
            v1 = velf[1][p - pi]
            v2 = (((velf[1][p - pi - 1] / 3.6) ** 2 + 2 * 0.8 * 0.001) ** 0.5) * 3.6
            while v2 < v1 and p <= pf:
                v1 = velf[1][p - pi]
                v2 = (((velf[1][p - pi - 1] / 3.6) ** 2 + 2 * 0.8 * 0.001) ** 0.5) * 3.6
                if v2 < v1:
                    velf[1][p - pi] = v2
                p += 1

    print("Diagramma delle velocità fase finale calcolato.")

    # Importazione dati limiti massimi locali
    try:
        with open(f'{percorso}\\lim.txt') as file:
            testo = file.readlines()
            for riga in testo:
                tmp = riga.split('\t')
                try:
                    datlim[0].append(tmp[0].replace('\n', ''))
                except IndexError:
                    datlim[0].append('')
                try:
                    datlim[1].append(tmp[1].replace('\n', ''))
                except IndexError:
                    datlim[1].append('')
                try:
                    datlim[2].append(tmp[2].replace('\n', ''))
                except IndexError:
                    datlim[2].append('')
                try:
                    datlim[3].append(tmp[3].replace('\n', ''))
                except IndexError:
                    datlim[3].append(0.8)
        print("File limiti di velocità locali 'lim.txt' trovato.")
        if vrf_dati_lim():
            lim_ok = True
            print("Limiti di velocità locali caricati.")
        else:
            msg("*Limiti di velocità locali non applicati.")
    except FileNotFoundError:
        msg("*File limiti di velocità locali 'lim.txt' non trovato. Limiti di velocità locali non applicati.")

    # Aggiornamento diagramma velocita' fase finale con limiti massimi locali
    if lim_ok:
        for i in range(len(datlim)):

            # Correzione pi e pf
            if datlim[i][0] == 'i':
                datlim[i][0] = pi
                if datlim[i][1] <= pf - pi:
                    datlim[i][1] = pi + abs(datlim[i][1])
                else:
                    datlim[i][1] = pf
            if datlim[i][1] == 'f':
                datlim[i][1] = pf
                if datlim[i][0] <= pf - pi:
                    datlim[i][0] = pf - abs(datlim[i][0])
                else:
                    datlim[i][0] = pi

            p = datlim[i][0]
            while p <= datlim[i][1] and datlim[i][2] < velf[1][p - pi]:
                velf[1][p - pi] = datlim[i][2]
                p += 1

            p = datlim[i][0] - 1
            if p >= pi:
                if datlim[i][2] < velf[1][p - pi]:
                    v1 = velf[1][p - pi]
                    v2 = (((velf[1][p - pi + 1] / 3.6) ** 2 + 2 * datlim[i][3] * 0.001) ** 0.5) * 3.6
                    while v2 < v1 and p >= pi:
                        v1 = velf[1][p - pi]
                        v2 = (((velf[1][p - pi + 1] / 3.6) ** 2 + 2 * datlim[i][3] * 0.001) ** 0.5) * 3.6
                        if v2 < v1:
                            velf[1][p - pi] = v2
                        p -= 1

            p = datlim[i][1] + 1
            if p <= pf:
                if datlim[i][2] < velf[1][p - pi]:
                    v1 = velf[1][p - pi]
                    v2 = (((velf[1][p - pi - 1] / 3.6) ** 2 + 2 * datlim[i][3] * 0.001) ** 0.5) * 3.6
                    while v2 < v1 and p <= pf:
                        v1 = velf[1][p - pi]
                        v2 = (((velf[1][p - pi - 1] / 3.6) ** 2 + 2 * datlim[i][3] * 0.001) ** 0.5) * 3.6
                        if v2 < v1:
                            velf[1][p - pi] = v2
                        p += 1

        print("Limiti di velocità locali applicati al diagramma delle velocità.")

    # Calcolo vmax curva da diagramma velocita' fase finale
    for i in range(len(elmp)):
        elmp[i][6] = vmax(elmp[i][3], elmp[i][4])

    # Calcolo q curva e allargamento in curva per corsia
    for i in range(len(elmp)):
        if elmp[i][0] == 'a':
            elmp[i][7] = q_curva(elmp[i][2])
            if elmp[i][2] < 225:
                elmp[i][8] = round(45 / elmp[i][2], 3)
            else:
                elmp[i][8] = 0.000
        if elmp[i][0] == 'r':
            elmp[i][7] = -0.025

    # Creazione diagramma velocita' finale ridotta px1
    velr = [[velf[0][0] / 1000], [round(velf[1][0], 2)]]
    d = 0

    for i in range(len(velf[0]) - 2):
        j = i + 1
        if velf[1][j] == velf[1][i]:
            if d == -1 or d == 1:
                velr[0].append(velf[0][i] / 1000)
                velr[1].append(round(velf[1][i], 2))
                d = 0
        elif velf[1][j] > velf[1][i]:
            if d == 0 or d == -1:
                if i != 0:
                    velr[0].append(velf[0][i] / 1000)
                    velr[1].append(round(velf[1][i], 2))
                d = 1
        elif velf[1][j] < velf[1][i]:
            if d == 0 or d == 1:
                if i != 0:
                    velr[0].append(velf[0][i] / 1000)
                    velr[1].append(round(velf[1][i], 2))
                d = -1
    velr[0].append(velf[0][j + 1] / 1000)
    velr[1].append(round(velf[1][j + 1], 2))

    # Controlli norma planimetrica
    print('...')
    nr, nc, na = 0, 0, 0
    for i in range(len(elmp)):

        # Verifiche rettifili...
        if elmp[i][0] == 'r':
            nr += 1
            a1, a2 = 0, 0
            if elmp[i][2] == 'f':
                a1 = elmp[i - 1][2]
                a2 = elmp[i + 1][2]

            vrf = vrf_rett(elmp[i][6], a1, a2)

            elm_min, elm_max = [], []
            vrfp += f'\n\t{i + 1}. Rettifilo N.{nr}:\tElemento\tRiferimento\n'
            vrfp += f'{ok('min', elmp[i][1], vrf[0])}\tLunghezza minima\t{elmp[i][1]}\t{vrf[0]}\n'
            elm_min.append(vrf[0])
            vrfp += f'{ok('max', elmp[i][1], vrf[1])}\tLunghezza massima\t{elmp[i][1]}\t{vrf[1]}\n'
            elm_max.append(vrf[1])
            if elmp[i][2] == 'f':
                vrfp += f'{ok('max', elmp[i][1], vrf[2])}\tLunghezza massima di flesso\t{elmp[i][1]}\t{vrf[2]}\n'
                elm_min = [0]
                elm_max.append(vrf[2])

            if elm_min != []:
                if elmp[i][1] < max(elm_min):
                    print(f'*Elemento N.{i + 1} (Rettifilo N.{nr}): Lunghezza {elmp[i][1]} m inferiore al minimo {max(elm_min)} m')
            if elm_max != []:
                if elmp[i][1] > min(elm_max):
                    print(f'*Elemento N.{i + 1} (Rettifilo N.{nr}): Lunghezza {elmp[i][1]} m superiore al massimo {min(elm_max)} m')

        # Verifiche clotoidi...
        if elmp[i][0] == 'c':
            nc += 1
            a, a1, a2, r1, r2, q1, q2, lf, qf = elmp[i][2], 0, 0, 0, 0, -0.025, -0.025, 0, 0

            if i - 1 >= 0:
                if elmp[i - 1][0] == 'r' and elmp[i - 1][2] == 'f':
                    a1 = elmp[i - 2][2]
                    if i - 3 >= 0:
                        lf = elmp[i - 2][1] + elmp[i - 1][1] + elmp[i][1]
                        qf = elmp[i - 3][7] + elmp[i + 1][7]
                elif elmp[i - 1][0] == 'c':
                    a1 = elmp[i - 1][2]
                    q1 = 0.000
                    if i - 3 >= 0:
                        lf = elmp[i - 1][1] + elmp[i][1]
                        qf = elmp[i - 2][7] + elmp[i + 1][7]
                elif elmp[i - 1][0] == 'a':
                    r1 = elmp[i - 1][2]
                    q1 = elmp[i - 1][7]
                    if i - 2 >= 0:
                        if elmp[i - 2][0] == 'c':
                            a1 = elmp[i - 2][2]

            if i + 1 < len(elmp):
                if elmp[i + 1][0] == 'r' and elmp[i + 1][2] == 'f':
                    a2 = elmp[i + 2][2]
                    if i + 3 < len(elmp):
                        lf = elmp[i + 2][1] + elmp[i + 1][1] + elmp[i][1]
                        qf = elmp[i + 3][7] + elmp[i - 1][7]
                elif elmp[i + 1][0] == 'c':
                    a2 = elmp[i + 1][2]
                    q2 = 0.000
                    if i + 3 < len(elmp):
                        lf = elmp[i + 1][1] + elmp[i][1]
                        qf = elmp[i + 2][7] + elmp[i - 1][7]
                elif elmp[i + 1][0] == 'a':
                    r2 = elmp[i + 1][2]
                    q2 = elmp[i + 1][7]
                    if i + 2 < len(elmp):
                        if elmp[i + 2][0] == 'c':
                            a2 = elmp[i + 2][2]

            vrf = vrf_clot(elmp[i][6], a1, a2, r1, r2, q1, q2)

            if elmp[i][1] > 0:
                if lf > 0:
                    di = round(abs(qf) * b * 100 / lf, 2)
                else:
                    di = round(abs(q2 - q1) * b * 100 / elmp[i][1], 2)
            else:
                di = 0
            dimin = round(0.1 * b, 2)

            elm_min, elm_max = [], []
            vrfp += f'\n\t{i + 1}. Clotoide N.{nc}:\tElemento\tRiferimento\n'
            if vrf[0] > 0:
                vrfp += f'{ok('min', elmp[i][2], vrf[0])}\tParametro A minimo esatto da limitazione del contraccolpo\t{elmp[i][2]}\t{vrf[0]}\n'
                elm_min.append(vrf[0])
            if vrf[1] > 0:
                vrfp += f'{ok('min', elmp[i][2], vrf[1])}\tParametro A minimo approssimato da limitazione del contraccolpo\t{elmp[i][2]}\t{vrf[1]}\n'
                elm_min.append(vrf[1])
            if vrf[2] > 0:
                vrfp += f'{ok('min', elmp[i][2], vrf[2])}\tParametro A minimo da sovrapendenza longitudinale dei cigli\t{elmp[i][2]}\t{vrf[2]}\n'
                elm_min.append(vrf[2])
            if vrf[3] > 0:
                vrfp += f'{ok('min', elmp[i][2], vrf[3])}\tParametro A minimo da criterio ottico\t{elmp[i][2]}\t{vrf[3]}\n'
                elm_min.append(vrf[3])
            if vrf[4] > 0:
                vrfp += f'{ok('min', a / a1, 2/3)}\tRapporto parametri A minimo da clotoide precedente\t{round(a / a1, 3)}\t{0.667}\n'
            if vrf[4] > 0:
                vrfp += f'{ok('min', elmp[i][2], vrf[4])}\tParametro A minimo da clotoide precedente\t{elmp[i][2]}\t{vrf[4]}\n'
                elm_min.append(vrf[4])
            if vrf[5] > 0:
                vrfp += f'{ok('min', a / a2, 2/3)}\tRapporto parametri A minimo da clotoide successiva\t{round(a / a2, 3)}\t{0.667}\n'
            if vrf[5] > 0:
                vrfp += f'{ok('min', elmp[i][2], vrf[5])}\tParametro A minimo da clotoide successiva\t{elmp[i][2]}\t{vrf[5]}\n'
                elm_min.append(vrf[5])
            if vrf[6] > 0:
                vrfp += f'{ok('max', elmp[i][2], vrf[6])}\tParametro A massimo da criterio ottico\t{elmp[i][2]}\t{vrf[6]}\n'
                elm_max.append(vrf[6])
            if vrf[7] > 0:
                vrfp += f'{ok('max', a / a1, 3/2)}\tRapporto parametri A massimo da clotoide precedente\t{round(a / a1, 3)}\t{1.500}\n'
            if vrf[7] > 0:
                vrfp += f'{ok('max', elmp[i][2], vrf[7])}\tParametro A massimo da clotoide precedente\t{elmp[i][2]}\t{vrf[7]}\n'
                elm_max.append(vrf[7])
            if vrf[8] > 0:
                vrfp += f'{ok('max', a / a2, 3/2)}\tRapporto parametri A massimo da clotoide successiva\t{round(a / a2, 3)}\t{1.500}\n'
            if vrf[8] > 0:
                vrfp += f'{ok('max', elmp[i][2], vrf[8])}\tParametro A massimo da clotoide successiva\t{elmp[i][2]}\t{vrf[8]}\n'
                elm_max.append(vrf[8])
            if di > 0:
                vrfp += f"{ok('min', di, dimin)}\tPendenza longitudinale minima dei cigli per il deflusso dell'acqua\t{di}%\t{dimin}%\n"

            if elm_min != []:
                if elmp[i][2] < max(elm_min):
                    print(f'*Elemento N.{i + 1} (Clotoide N.{nc}): Parametro A {elmp[i][2]} inferiore al minimo {max(elm_min)}')
            if elm_max != []:
                if elmp[i][2] > min(elm_max):
                    print(f'*Elemento N.{i + 1} (Clotoide N.{nc}): Parametro A {elmp[i][2]} superiore al massimo {min(elm_max)}')

        # Verifiche curve circolari...
        if elmp[i][0] == 'a':
            na += 1
            l1, l2 = 0, 0
            j1 = i
            while j1 > 0 and abs(i - j1) < 2:
                j1 -= 1
                if elmp[j1][0] == 'r':
                    l1 = elmp[j1][1]
                    break
            j2 = i
            while j2 < len(elmp) - 1 and abs(i - j2) < 2:
                j2 += 1
                if elmp[j2][0] == 'r':
                    l2 = elmp[j2][1]
                    break

            dvmax1 = 0
            dvmax2 = 0
            dvmax2c = 0
            if nrm[n][3] >= 100:
                dvmax1 = 10
                dvmax2 = 20
                dvmax2c = 15
            if nrm[n][3] <= 80:
                dvmax1 = 5
                dvmax2 = 20
                dvmax2c = 10

            dv1, dv2c1, dv2c2 = -1, -1, -1

            k = i
            if k > 0:
                k -= 1
                if elmp[k][6] == vpmax:
                    dv1 = round(abs(elmp[i][6] - elmp[k][6]), 2)
                    vminr = vpmax - dvmax1
                    rminr = r_curva(vminr)
            kc1 = i
            while kc1 > 0:
                kc1 -= 1
                if elmp[kc1][0] == 'a':
                    dv2c1 = round(abs(elmp[i][6] - elmp[kc1][6]), 2)
                    vminc1 = elmp[kc1][6] - dvmax2
                    rminc1 = r_curva(vminc1)
                    break
            kc2 = i
            while kc2 < len(elmp) - 1:
                kc2 += 1
                if elmp[kc2][0] == 'a':
                    dv2c2 = round(abs(elmp[i][6] - elmp[kc2][6]), 2)
                    vminc2 = elmp[kc2][6] - dvmax2
                    rminc2 = r_curva(vminc2)
                    break

            vrf = vrf_curv(elmp[i][6], l1, l2)

            elm_min, elm_max = [[], []], []
            vrfp += f'\n\t{i + 1}. Arco N.{na}:\tElemento\tRiferimento\n'
            if vrf[0] > 0:
                vrfp += f'{ok('min', elmp[i][1], vrf[0])}\tSviluppo minimo per corretta percezione\t{elmp[i][1]}\t{vrf[0]}\n'
                elm_min[0].append(vrf[0])
            if dv1 > -1:
                vrfp += f"{ok('max', dv1, dvmax1)}\tDifferenza di velocità da Vpmax\t{dv1}\t{dvmax1}\n"
            if dv2c1 > -1:
                vrfp += f"{ok('max', dv2c1, dvmax2)}\tDifferenza di velocità da curva precedente\t{dv2c1}\t{dvmax2} ({dvmax2c})\n"
            if dv2c2 > -1:
                vrfp += f"{ok('max', dv2c2, dvmax2)}\tDifferenza di velocità da curva successiva\t{dv2c2}\t{dvmax2} ({dvmax2c})\n"
            if dv1 > 0:
                vrfp += f"{ok('min', elmp[i][2], rminr)}\tRaggio minimo da differenza di velocità da Vpmax\t{elmp[i][2]}\t{rminr}\n"
                elm_min[1].append(rminr)
            if dv2c1 > -1:
                vrfp += f"{ok('min', elmp[i][2], rminc1)}\tRaggio minimo da differenza di velocità da curva precedente\t{elmp[i][2]}\t{rminc1}\n"
                elm_min[1].append(rminc1)
            if dv2c2 > -1:
                vrfp += f"{ok('min', elmp[i][2], rminc2)}\tRaggio minimo da differenza di velocità da curva successiva\t{elmp[i][2]}\t{rminc2}\n"
                elm_min[1].append(rminc2)
            vrfp += f"{ok('min', elmp[i][2], vrf[1])}\tRaggio minimo da Vpmin\t{elmp[i][2]}\t{vrf[1]}\n"
            elm_min[1].append(vrf[1])
            if vrf[2] > 0:
                vrfp += f'{ok('min', elmp[i][2], vrf[2])}\tRaggio minimo da rettifilo precedente\t{elmp[i][2]}\t{vrf[2]}\n'
                elm_min[1].append(vrf[2])
            if vrf[3] > 0:
                vrfp += f'{ok('min', elmp[i][2], vrf[3])}\tRaggio minimo da rettifilo successivo\t{elmp[i][2]}\t{vrf[3]}\n'
                elm_min[1].append(vrf[3])

            if elm_min[0] != []:
                if elmp[i][1] < max(elm_min[0]):
                    print(f'*Elemento N.{i + 1} (Arco N.{na}): Sviluppo {elmp[i][1]} m inferiore al minimo {max(elm_min[0])} m')
            if elm_min[1] != []:
                if elmp[i][2] < max(elm_min[1]):
                    print(f'*Elemento N.{i + 1} (Arco N.{na}): Raggio {elmp[i][2]} m inferiore al minimo {max(elm_min[1])} m')

    print('...\nVerifiche planimetriche effettuate.')

    if nrm[n][11] == 1:
        dvc[0] = velr[0]
        for i in range(len(velr[1])):
            dvc[1].append(visc(velr[1][i]))
        print("Distanze di visibilità per il cambio di corsia calcolate.")

    if nrm[n][11] == 2:
        dvs[0] = velr[0]
        for i in range(len(velr[1])):
            dvs[1].append(viss(velr[1][i]))
        print("Distanze di visibilità per il sorpasso calcolate.")


def calc_alt():
    global datalt, elma, pi, pf, vrfa, dva, dvar

    # Creazione tabella tracciato altimetrico da dati importati
    elma = [['' for col in range(7)] for row in range(len(datalt[0]))]
    '''
    elma[i][0] = elemento
    elma[i][1] = lunghezza
    elma[i][2] = pendenza longitudinale / raggio
    elma[i][3] = progressiva inizio
    elma[i][4] = progressiva fine
    elma[i][5] = tipo livelletta / raccordo
    elma[i][6] = vmax
    '''
    for i in range(len(datalt[0])):
        for j in range(3):
            elma[i][j] = datalt[j][i]

    # Calcolo progressive iniziali e finali elementi altimetrici px1000
    pfpro = pi
    for i in range(len(elma)):
        if i == 0:
            elma[i][3] = pi
        else:
            elma[i][3] = elma[i - 1][4]
        elma[i][4] = int(elma[i][3] + elma[i][1] * 1000)
        pfpro += int(elma[i][1] * 1000)

    # Controlli norma altimetrica
    print('...')
    nl, nr = 0, 0
    for i in range(len(elma)):

        # Verifiche livellette
        if elma[i][0] == 'l':
            nl += 1
            if elma[i][2] == 0:
                elma[i][5] = 'Orizzontale'
            elif elma[i][2] > 0:
                elma[i][5] = 'Salita'
            elif elma[i][2] < 0:
                elma[i][5] = 'Discesa'
            if elma[i][4] > pf:
                if elma[i][3] > pf:
                    elma[i][6] = 0
                else:
                    elma[i][6] = vmax(elma[i][3], pf)
            else:
                elma[i][6] = vmax(elma[i][3], elma[i][4])
            vrf = vrf_livl()

            elm_min, elm_max = [], []
            vrfa += f'\n\t{i + 1}. Livelletta N.{nl}:\tElemento\tRiferimento\n'
            vrfa += f'{ok('max', abs(elma[i][2]), vrf)}\tPendenza massima\t{round(elma[i][2] * 100, 2)}%\t{round(vrf * 100, 2)}%\n'
            elm_max.append(vrf)

            if elm_max != []:
                if abs(elma[i][2]) > min(elm_max):
                    print(f'*Elemento N.{i + 1} (Livelletta N.{nl}): Pendenza {round(elma[i][2] * 100, 2)}% superiore al massimo {round(min(elm_max) * 100, 2)}%')

        # Verifiche raccordi verticali
        if elma[i][0] == 'r':
            nr += 1
            l = elma[i][1]
            r = elma[i][2]
            i1 = elma[i - 1][2]
            i2 = elma[i + 1][2]
            if i1 > i2:
                elma[i][5] = 'Dosso'
            if i1 < i2:
                elma[i][5] = 'Sacca'
            if elma[i][4] > pf:
                if elma[i][3] > pf:
                    elma[i][6] = 0
                else:
                    elma[i][6] = vmax(elma[i][3], pf)
            else:
                elma[i][6] = vmax(elma[i][3], elma[i][4])
            a = round((elma[i][6] / 3.6) ** 2 / r, 3)
            vrf = vrf_racc(elma[i][6], l, i1, i2)

            elm_min, elm_max = [], []
            vrfa += f'\n\t{i + 1}. Raccordo N.{nr}:\tElemento\tRiferimento\n'
            if vrf[0] > 0:
                vrfa += f"{ok('min', r, vrf[0])}\tRaggio minimo da distanza di visibilità per l'arresto\t{r}\t{vrf[0]}\n"
                elm_min.append(vrf[0])
            if vrf[1] > 0:
                vrfa += f"{ok('min', r, vrf[1])}\tRaggio minimo da distanza di visibilità per il sorpasso\t{r}\t{vrf[1]}\n"
            vrfa += f'{ok('min', r, vrf[2])}\tRaggio minimo per evitare contatto con la superficie\t{r}\t{vrf[2]}\n'
            elm_min.append(vrf[2])
            if vrf[3] > 0:
                vrfa += f'{ok('min', r, vrf[3])}\tRaggio minimo da comfort utenza\t{r}\t{vrf[3]}\n'
                elm_min.append(vrf[3])
            if a > 0:
                vrfa += f'{ok('max', a, vrf[4])}\tAccelerazione verticale massima da comfort utenza\t{a}\t{vrf[4]}\n'

            if elm_min != []:
                if r < max(elm_min):
                    print(f'*Elemento N.{i + 1} (Raccordo N.{nr}): Raggio {r} m inferiore al minimo {max(elm_min)} m')

    print('...\nVerifiche altimetriche effettuate.')

    dva[0].append(pi)
    dva[1].append(visa(velf[1][0], trova_pend(pi)))
    p = pi + 1000
    while p < pf:
        if p <= pfpro:
            dva[0].append(p)
            dva[1].append(visa(velf[1][p - pi], trova_pend(p)))
            p += 1000
        else:
            dva[0].append(pfpro)
            dva[1].append(visa(velf[1][pfpro - pi], trova_pend(pfpro)))
            break
    if p <= pfpro:
        dva[0].append(pf)
        dva[1].append(visa(velf[1][pf - pi], trova_pend(pf)))

    # Distanze di visibilita' per l'arresto (ridotte)
    ult = dva[1][0]
    dvar = [[dva[0][0] / 1000], [ult]]
    for i in range(len(dva[0])):
        if dva[1][i] != ult:
            dvar[0].append(dva[0][i] / 1000)
            dvar[1].append(dva[1][i])
            ult = dva[1][i]
    if dva[0][-1] / 1000 != dvar[0][-1]:
        dvar[0].append(dva[0][-1] / 1000)
        dvar[1].append(dva[1][-1])

    print("Distanze di visibilità per l'arresto calcolate.")


def imposta():
    global nrm, n, b, vpmin, vpmax, pi, imp_ok, datimp

    n_mod = False
    if imp_ok:
        n_ok, b_ok, vpmin_ok, vpmax_ok, pi_ok = True, True, True, True, True
    else:
        n_ok, b_ok, vpmin_ok, vpmax_ok, pi_ok = False, False, False, False, False

        print('Inserire impostazioni strada...\n')
        for i in range(1, len(nrm)):
            print(f'{i}.\t{nrm[i][0]}')
        print()

    while not n_ok:
        if n == 0:
            tmp = input('Numero categoria stradale > ')
            if tmp.isnumeric():
                tmp = int(tmp)
                if 1 <= int(tmp) <= 14:
                    n_ok = True
                    n_mod = True
                    n = tmp
        else:
            tmp = input(f'Numero categoria stradale <{n}> ')
            if tmp.isnumeric():
                tmp = int(tmp)
                if 1 <= int(tmp) <= 14:
                    n_ok = True
                    if int(tmp) == n:
                        n = tmp
                    else:
                        n_mod = True
                        n = tmp
            elif tmp == '':
                n_ok = True

    msg = f'Distanza B fra asse rotazione e estremità carreggiata deve essere positiva.'
    while not b_ok:
        if n_mod:
            tmp = input(f'Distanza B fra asse rotazione e estremità carreggiata [m] <{nrm[n][1]}> ')
            try:
                tmp = float(tmp)
                if tmp > 0:
                    b_ok = True
                    b = round(tmp, 2)
                else:
                    print(msg)
            except ValueError:
                if tmp == '':
                    b_ok = True
                    b = nrm[n][1]
        else:
            tmp = input(f'Distanza B fra asse rotazione e estremità carreggiata [m] <{b}> ')
            try:
                tmp = float(tmp)
                if tmp > 0:
                    b_ok = True
                    b = round(tmp, 2)
                else:
                    print(msg)
            except ValueError:
                if tmp == '':
                    b_ok = True

    msg = f"*Il limite inferiore dell'intervallo di velocità di progetto per la categoria stradale deve essere tra {nrm[n][2]} e {nrm[n][3]} km/h."
    while not vpmin_ok:
        if n_mod:
            tmp = input(f"Limite inferiore dell'intervallo di velocità di progetto (Vpmin) [km/h] <{nrm[n][2]}> ")
            if tmp.isnumeric():
                tmp = int(tmp)
                if nrm[n][2] <= tmp <= nrm[n][3]:
                    vpmin_ok = True
                    vpmin = round(tmp, 2)
                else:
                    print(msg)
            else:
                if tmp == '':
                    vpmin_ok = True
                    vpmin = nrm[n][2]
        else:
            tmp = input(f"Limite inferiore dell'intervallo di velocità di progetto (Vpmin) [km/h] <{vpmin}> ")
            if tmp.isnumeric():
                tmp = int(tmp)
                if nrm[n][2] <= tmp <= nrm[n][3]:
                    vpmin_ok = True
                    vpmin = round(tmp, 2)
                else:
                    print(msg)
            else:
                if tmp == '':
                    vpmin_ok = True

    msg1 = f"*Il limite superiore dell'intervallo di velocità di progetto per la categoria stradale non deve essere maggiore di {nrm[n][3]} km/h."
    msg2 = f"*Il limite superiore dell'intervallo di velocità di progetto non deve essere minore del limite inferiore {vpmin} km/h."
    while not vpmax_ok:
        if n_mod:
            tmp = input(f"Limite superiore dell'intervallo di velocità di progetto (Vpmax) [km/h] <{nrm[n][3]}> ")
            if tmp.isnumeric():
                tmp = int(tmp)
                if vpmin <= tmp <= nrm[n][3]:
                    vpmax_ok = True
                    vpmax = round(tmp, 0)
                elif tmp > nrm[n][3]:
                    print(msg1)
                elif vpmin > tmp:
                    print(msg2)
            else:
                if tmp == '':
                    vpmax_ok = True
                    vpmax = nrm[n][3]
        else:
            tmp = input(f"Limite superiore dell'intervallo di velocità di progetto (Vpmax) [km/h] <{vpmax}> ")
            if tmp.isnumeric():
                tmp = int(tmp)
                if vpmin <= tmp <= nrm[n][3]:
                    vpmax_ok = True
                    vpmax = round(tmp, 0)
                elif tmp > nrm[n][3]:
                    print(msg1)
                elif vpmin > tmp:
                    print(msg2)
            else:
                if tmp == '':
                    vpmax_ok = True

    while not pi_ok:
        tmp = input(f'Progressiva inizio tracciato [m] <{pi}> ')
        try:
            tmp = float(tmp)
            pi_ok = True
            pi = round(tmp, 3)
        except ValueError:
            if tmp == '':
                pi_ok = True


def vrf_dati_pla():
    global datpla
    pla_ok, elementi = True, ('r', 'rettifilo', 'c', 'clotoide', 'a', 'arco')
    trac = ''
    for i in range(len(datpla[0])):
        if datpla[0][i].lower() not in elementi:
            pla_ok = False
            msg(f"*Tipo elemento planimetrico riga n.{i + 1} non valido. Usare 'rettifilo', 'clotoide' o 'arco'.")
            break
        datpla[0][i] = datpla[0][i][0]
        trac += datpla[0][i]
        try:
            datpla[1][i] = round(float(datpla[1][i].replace('m', '')), 3)
            if datpla[1][i] < 0:
                pla_ok = False
                msg(f'*Lunghezza elemento planimetrico riga n.{i + 1} deve assumere un valore non negativo.')
                break
        except ValueError:
            pla_ok = False
            msg(f'*Lunghezza elemento planimetrico riga n.{i + 1} non valida.')
            break

        if datpla[0][i] == 'r':
            if datpla[2][i] == '' or datpla[2][i].lower() == 'f':
                pass
            else:
                pla_ok = False
                msg(f"*Tipo rettifilo riga n.{i + 1} non valido. Usare 'f' per rettifilo di flesso")
                break

        if datpla[0][i] == 'c':
            try:
                datpla[2][i] = round(float(datpla[2][i].replace('m', '')), 3)
                if datpla[2][i] <= 0:
                    pla_ok = False
                    msg(f'*Parametro A riga n.{i + 1} deve assumere un valore positivo.')
            except ValueError:
                pla_ok = False
                msg(f'*Parametro A riga n.{i + 1} non valido.')
                break

        if datpla[0][i] == 'a':
            try:
                datpla[2][i] = round(float(datpla[2][i].replace('m', '')), 3)
                if datpla[2][i] <= 0:
                    pla_ok = False
                    msg(f'*Raggio arco riga n.{i + 1} deve assumere un valore positivo.')
            except ValueError:
                pla_ok = False
                msg(f'*Raggio arco riga n.{i + 1} non valido.')
                break
    if datpla == [[], [], []]:
        pla_ok = False
        msg(f'*Il tracciato non contiene alcun elemento planimetrico.')
    if 'rr' in trac:
        pla_ok = False
        msg(f'*Il tracciato contiene due o più rettifili consecutivi.')

    return pla_ok


def vrf_dati_imp():
    global nrm, datimp, n, b, vpmin, vpmax, pi
    imp_ok = True

    for i in range(1):

        try:
            tmp = int(datimp[0])
            if 1 <= tmp <= 14:
                n = tmp
            else:
                imp_ok = False
                msg('*Numero categoria stradale non valido.')
                break
        except ValueError:
            imp_ok = False
            msg('*Numero categoria stradale non valido.')
            break
        except IndexError:
            imp_ok = False
            msg('*Numero categoria stradale non inserito.')
            break

        try:
            tmp = float(datimp[1])
            if tmp > 0:
                b = round(tmp, 2)
            else:
                imp_ok = False
                msg(f'*Distanza B fra asse rotazione e estremità carreggiata deve essere positiva.')
                b = nrm[n][1]
        except ValueError:
            b = nrm[n][1]
            if datimp[1] != '':
                imp_ok = False
                msg('*Distanza B fra asse rotazione e estremità carreggiata non valida.')
        except IndexError:
            b = nrm[n][1]

        try:
            tmp = float(datimp[2])
            if nrm[n][2] <= tmp <= nrm[n][3]:
                vpmin = round(tmp, 0)
            else:
                imp_ok = False
                msg(f"*Limite inferiore dell'intervallo di velocità di progetto per la categoria stradale deve essere tra {nrm[n][2]} e {nrm[n][3]} km/h.")
                vpmin = nrm[n][2]
        except ValueError:
            vpmin = nrm[n][2]
            if datimp[2] != '':
                imp_ok = False
                msg("*Limite inferiore dell'intervallo di velocità di progetto non valido.")
        except IndexError:
            vpmin = nrm[n][2]

        try:
            tmp = float(datimp[3])
            if vpmin <= tmp <= nrm[n][3]:
                vpmax = round(tmp, 0)
            elif tmp > nrm[n][3]:
                imp_ok = False
                msg(f"*Limite superiore dell'intervallo di velocità di progetto per la categoria stradale non deve essere maggiore di {nrm[n][3]} km/h.")
                vpmax = nrm[n][3]
            elif vpmin > tmp:
                imp_ok = False
                msg(f"*Limite superiore dell'intervallo di velocità di progetto non deve essere minore del limite inferiore {vpmin} km/h.")
                vpmax = nrm[n][3]
        except ValueError:
            vpmax = nrm[n][3]
            if datimp[3] != '':
                imp_ok = False
                msg("*Limite superiore dell'intervallo di velocità di progetto non valido.")
        except IndexError:
            vpmax = nrm[n][3]

        try:
            pi = round(float(pm(datimp[4])), 3)
        except ValueError:
            pi = 0
            if datimp[4] != '':
                imp_ok = False
                msg('*Progressiva inizio tracciato non valida.')
        except IndexError:
            pi = 0

    return imp_ok


def vrf_dati_alt():
    global datalt, pi
    alt_ok, elementi = True, ('l', 'livelletta', 'r', 'raccordo')
    prof = ''
    ultpend = None
    pvi = False

    for i in range(len(datalt[0])):
        if datalt[0][i].lower() not in elementi:
            if i == 0:
                try:
                    datalt[0][0] = round(float(pm(datalt[0][0].replace('m', ''))), 3)
                    if len(datalt[0]) < 2:
                        alt_ok = False
                        msg(f'*Il profilo deve avere almeno due vertici.')
                    elif int(datalt[0][0] * 1000) != pi:
                        alt_ok = False
                        msg(f'*Progressiva inizile del profilo non coincide con quella del tracciato.')
                    else:
                        pvi = True
                    break
                except ValueError:
                    alt_ok = False
                    msg(f"*Tipo elemento altimetrico riga n.1 non valido. Usare 'livelletta' o 'raccordo'.")
                    break

            alt_ok = False
            msg(f"*Tipo elemento altimetrico riga n.{i + 1} non valido. Usare 'livelletta' o 'raccordo'.")
            break

        datalt[0][i] = datalt[0][i][0]
        prof += datalt[0][i]
        try:
            datalt[1][i] = round(float(datalt[1][i].replace('m', '')), 3)
            if datalt[1][i] < 0:
                alt_ok = False
                msg(f'*Lunghezza elemento altimetrico riga n.{i + 1} deve assumere un valore non negativo.')
                break
        except ValueError:
            alt_ok = False
            msg(f'*Lunghezza elemento altimetrico riga n.{i + 1} non valida.')
            break

        if datalt[0][i] == 'l':
            try:
                datalt[2][i] = round(float(datalt[2][i].replace('%', '')) / 100, 4)
                if datalt[2][i] == ultpend:
                    alt_ok = False
                    msg(f'*Pendenza livelletta riga n.{i + 1} non deve essere uguale alla precedente.')
                    break
                ultpend = datalt[2][i]
            except ValueError:
                alt_ok = False
                msg(f'*Pendenza livelletta riga n.{i + 1} non valida.')
                break

        if datalt[0][0] == 'r':
            alt_ok = False
            msg(f'*Il profilo altimetrico deve iniziare con un elemento del tipo livelletta.')
        if datalt[0][len(datalt[0]) - 1] == 'r':
            alt_ok = False
            msg(f'*Il profilo altimetrico deve terminare con un elemento del tipo livelletta.')

        if datalt[0][i] == 'r':
            try:
                datalt[2][i] = round(float(datalt[2][i].replace('m', '')), 3)
                if datalt[2][i] <= 0:
                    alt_ok = False
                    msg(f'*Raggio raccordo altimetrico riga n.{i + 1} deve assumere un valore positivo.')
                    break
                if datalt[2][i - 1] == datalt[2][i + 1]:
                    alt_ok = False
                    msg(f'*Pendenze livellette righe n.{i} e {i + 2} non possono assumere lo stesso valore.')
                    break
            except ValueError:
                alt_ok = False
                msg(f'*Raggio raccordo altimetrico riga n.{i + 1} non valido.')
                break
    if datalt == [[], [], []]:
        alt_ok = False
        msg(f'*Il profilo non contiene alcun elemento altimetrico.')
    if 'll' in prof:
        alt_ok = False
        msg(f'*Il profilo contiene due o più livellette consecutive senza raccordi altimetrici.')
    if 'rr' in prof:
        alt_ok = False
        msg(f'*Il profilo contiene due o più raccordi altimetrici consecutivi.')

    if pvi:
        alt_tmp = [[], [], [], []]

        for i in range(len(datalt[0])):
            if i > 0:
                try:
                    datalt[0][i] = round(float(pm(datalt[0][i].replace('m', ''))), 3)
                    if datalt[0][i] <= datalt[0][i - 1]:
                        alt_ok = False
                        msg(f'*Progressiva vertice altimetrico riga n.{i + 1} deve essere maggiore di quella precedente.')
                        break
                except ValueError:
                    alt_ok = False
                    msg(f'*Progressiva vertice altimetrico riga n.{i + 1} non valida.')
                    break

            try:
                datalt[1][i] = round(float(datalt[1][i].replace('m', '')), 3)
            except ValueError:
                alt_ok = False
                msg(f'*Quota vertice altimetrico riga n.{i + 1} non valida.')
                break

            if 0 < i < len(datalt[0]) - 1:
                try:
                    datalt[2][i] = round(float(datalt[2][i].replace('m', '')), 3)
                    if datalt[2][i] <= 0:
                        alt_ok = False
                        msg(f'*Raggio raccordo altimetrico riga n.{i + 1} deve assumere un valore positivo.')
                        break
                except ValueError:
                    alt_ok = False
                    msg(f'*Raggio raccordo altimetrico riga n.{i + 1} non valido.')
                    break

        if alt_ok:

            for i in range(1, len(datalt[0])):
                alt_tmp[0].append(round(datalt[0][i] - datalt[0][i - 1], 3))
                alt_tmp[1].append(round((datalt[1][i] - datalt[1][i - 1]) / (datalt[0][i] - datalt[0][i - 1]), 4))

            for i in range(len(alt_tmp[0])):
                if i > 0:
                    r = datalt[2][i]
                    i1 = alt_tmp[1][i - 1]
                    i2 = alt_tmp[1][i]
                    di = abs(i2 - i1)
                    l = round(r * di, 3)
                    alt_tmp[2].append(l)
                    alt_tmp[3].append(r)

            datalt = [[], [], []]
            for i in range(len(alt_tmp[0])):
                datalt[0].append('l')
                datalt[1].append(alt_tmp[0][i])
                datalt[2].append(alt_tmp[1][i])
                if i < len(alt_tmp[2]):
                    datalt[0].append('r')
                    datalt[1].append(alt_tmp[2][i])
                    datalt[2].append(alt_tmp[3][i])

            for i in range(len(datalt[0])):
                if datalt[0][i] == 'r':
                    datalt[1][i - 1] = round(datalt[1][i - 1] - datalt[1][i] / 2, 3)
                    datalt[1][i + 1] = round(datalt[1][i + 1] - datalt[1][i] / 2, 3)
                    if datalt[1][i - 1] < 0:
                        alt_ok = False
                        msg(f'*Il raggio del raccordo altimetrico riga n.{i} non è geometricamente fattibile.')
                        break
                    if datalt[1][i + 1] < 0:
                        alt_ok = False
                        msg(f'*Il raggio del raccordo altimetrico riga n.{i} non è geometricamente fattibile.')
                        break

    return alt_ok


def importa():
    global percorso, datpla, imp_ok, datimp, datlim, datalt, log
    try:
        with open(f'{percorso}\\pla.txt') as file:
            testo = file.readlines()
            for riga in testo:
                tmp = riga.split('\t')
                try:
                    datpla[0].append(tmp[0].replace('\n', ''))
                except IndexError:
                    datpla[0].append('')
                try:
                    datpla[1].append(tmp[1].replace('\n', ''))
                except IndexError:
                    datpla[1].append('')
                try:
                    datpla[2].append(tmp[2].replace('\n', ''))
                except IndexError:
                    datpla[2].append('')
                if datpla[2][-1] == '':
                    try:
                        datpla[2][-1] = tmp[3].replace('\n', '')
                    except IndexError:
                        pass
        print("File dati planimetrici 'pla.txt' trovato.")

        if vrf_dati_pla():
            print('Dati planimetrici caricati.')

            try:
                with open(f'{percorso}\\imp.txt') as file:
                    testo = file.readlines()
                    datimp = testo[0].split('\t')
                    print("File impostazioni tracciato 'imp.txt' trovato.")
                    if vrf_dati_imp():
                        imp_ok = True
                        print('Impostazioni tracciato caricate.')
                    else:
                        print("Una o più impostazioni non caricate.")
            except FileNotFoundError:
                msg("*File impostazioni tracciato 'imp.txt' non trovato. Impostazioni non caricate.")
            except IndexError:
                msg("*Impostazioni tracciato non trovate. Verificare contenuto 'imp.txt'.")

            imposta()
            calc_pla()

            try:
                with open(f'{percorso}\\alt.txt') as file:
                    testo = file.readlines()
                for riga in testo:
                    tmp = riga.split('\t')
                    try:
                        datalt[0].append(tmp[0].replace('\n', ''))
                    except IndexError:
                        datalt[0].append('')
                    try:
                        datalt[1].append(tmp[1].replace('\n', ''))
                    except IndexError:
                        datalt[1].append('')
                    try:
                        datalt[2].append(tmp[2].replace('\n', ''))
                    except IndexError:
                        datalt[2].append('')
                    if datalt[2][-1] == '':
                        try:
                            datalt[2][-1] = tmp[3].replace('\n', '')
                        except IndexError:
                            pass
                print("File dati altimetrici 'alt.txt' trovato.")
                if vrf_dati_alt():
                    print('Dati altimetrici caricati.')
                    calc_alt()
                else:
                    print("Verifiche altimetriche non effettuate.")
            except FileNotFoundError:
                msg("*File dati altimetrici 'alt.txt' non trovato. Verifiche altimetriche non effettuate.")

            correg()
            stampa()
            reset()
        else:
            print("Verifiche planimetriche non effettuate.")
            stampa()
            reset()
    except FileNotFoundError:
        msg("*File dati planimetrici 'pla.txt' non trovato. Verifiche planimetriche non effettuate.")
        reset()


def init():
    global percorso
    nome_ok = False
    while not nome_ok:
        if percorso == '':
            tmp = input('\nPercorso cartella del tracciato > ')
            if tmp != '':
                nome_ok = True
                percorso = tmp
        else:
            tmp = input(f'\nPercorso cartella del tracciato <{percorso}> ')
            nome_ok = True
            if tmp != '':
                percorso = tmp
    importa()


print(titolo)
try:
    init()
except Exception as e:
    import keyboard
    print(f'*Si è verificato un errore: {e}.')
    print(f"Segnalare l'errore a: {mail}")
    print('...\nPremere un tasto qualsiasi per chiudere.')
    while True:
        if keyboard.is_pressed(keyboard.read_key()):
            raise SystemExit
