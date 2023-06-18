#
#
# Der lange Weg zu den Sterbewahrscheinlichkeiten,
# siehe "2018-01-24_DAV-Richtlinie_Herleitung_DAV2004R" unter Dokumente.
#
#
#------------------------------------------------------------------
#------------------------------------------------------------------
# Bibliotheken:

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd             # Auch für pd.read_csv
import csv                      # Einlesen und Umwandlung von csv-Dateien

from scipy.stats import uniform, norm
from pandas_datareader import data
from scipy.fftpack import rfft, irfft, fft, rfft, dct, idct
from scipy.cluster.vq import kmeans2 as kmeans
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import scale as scale_this

#------------------------------------------------------------------
#------------------------------------------------------------------
# Datenpfad und Grafikpfad:

DATAPATH ='C:/Users/Blenki7/PycharmProjects/pythonProject/CodePython/2022_06_03/Tabellen/'
GRAPHPATH = 'C:/Users/Blenki7/PycharmProjects/pythonProject/CodePython/2022_06_03/Grafiken/'

#------------------------------------------------------------------
#------------------------------------------------------------------
# Integer-Konstanten und String-Konstanten:
def f_constm01(): return int(-1)
def f_constm06(): return int(-6)
def f_constp00(): return int(0)
def f_constp01(): return int(1)
def f_constp02(): return int(2)
def f_constp03(): return int(3)
def f_constp05(): return int(5)
def f_constp06(): return int(6)
def f_constp309(): return int(309)

def f_conststr2016(): return str(2016)
def f_conststr2017(): return str(2017)
def f_conststr2018(): return str(2018)
def f_conststr2019(): return str(2019)
def f_conststr2020(): return str(2020)

sex_m = 'männlich'
sex_w = 'weiblich'
sex_I = 'Insgesamt'

sex2_m = 'm'
sex2_w = 'w'

#------------------------------------------------------------------
#------------------------------------------------------------------
# Funktionen:

def f_EmptyRows():
    for i in [0, f_constp03()]:
        print(f"")
    return None

#------------------------------------------------------------------
#------------------------------------------------------------------
# Hauptprogramm:

f_EmptyRows()

# Kohorten-Sterbetafel bis zum Endalter 100 fuer die Jahre 2016-2020
# vom Statistischen Bundesamt vom 06.06.2022 :

#------------------------------------------------------------------
# Von der Datei zu den entsprechenden Listen mit Spaltenüberschriften:

l_Kohorte  = []    # Zu erstellende Liste für die Kohortensterbetafel
l_KohorteM = []    # Zu erstellende Liste für die Kohortensterbetafel Maenner
l_KohorteW = []    # Zu erstellende Liste für die Kohortensterbetafel Frauen
l_KohorteI = []    # Zu erstellende Liste für die Kohortensterbetafel Keine Geschlechtertrennung

with open(DATAPATH+"StatistikDerSterbefaelle_2016_2020.csv", newline="") as d_f:
    csv_reader = csv.reader(d_f, delimiter=';', escapechar="'")
    line_count = f_constm06()
    m_count = 0
    w_count = 0
    i_count = 0
    for row in csv_reader:
        if line_count == f_constm01():
            Titelzeile =row
            print(f"\tSpaltenüberschriften sind: {', '.join(row).title()}")
            f_EmptyRows()
            l_Kohorte.append(Titelzeile)
            l_KohorteM.append(Titelzeile)
            l_KohorteW.append(Titelzeile)
            l_KohorteI.append(Titelzeile)

        elif f_constp309() > line_count > f_constm01():
            print(line_count, row)
            print(f'\tSex: {row[0].strip()}, Age:{row[1].strip()}, Qx2016:{row[2].strip()},'
                  f' Qx2017:{row[3].strip()}, Qx2018:{row[4].strip()}, Qx2019:{row[5].strip()},'
                  f' Qx2020:{row[6].strip()}')
            l_Kohorte.append(row)
            if row[0] == sex_m:
                l_KohorteM.append(row)
                l_KohorteM[m_count+1].insert(2, m_count)
                for teilfolge in range(len(l_KohorteM[m_count+1])):
                    if teilfolge > f_constp02():
                        if l_KohorteM[m_count + 1][int(teilfolge)] != '-':
                              l_KohorteM[m_count + 1][int(teilfolge)] = int(l_KohorteM[m_count + 1][int(teilfolge)])
                        else:
                            pass
                else:
                    pass
                m_count += 1

            elif row[0] == sex_w:
                l_KohorteW.append(row)
                l_KohorteW[w_count + 1].insert(2, w_count)
                for teilfolge in range(len(l_KohorteW[w_count+1])):
                    if teilfolge > f_constp02():
                        if l_KohorteW[w_count + 1][int(teilfolge)] != '-':
                              l_KohorteW[w_count + 1][int(teilfolge)] = int(l_KohorteW[w_count + 1][int(teilfolge)])
                        else:
                            pass
                else:
                    pass
                w_count += 1

            elif row[0] == sex_I:
                l_KohorteI.append(row)
                l_KohorteI[i_count + 1].insert(2, i_count)
                for teilfolge in range(len(l_KohorteI[i_count+1])):
                    if teilfolge > f_constp02():
                        if l_KohorteI[i_count + 1][int(teilfolge)] != '-':
                              l_KohorteI[i_count + 1][int(teilfolge)] = int(l_KohorteI[i_count + 1][int(teilfolge)])
                        else:
                            pass
                else:
                    pass
                i_count += 1
            else:
                pass
        else:
            pass
        line_count += 1
f_EmptyRows()

print(f'Von der csv-Datei zu den Listen, Int-Alter eingefügt, Einteilung in String- und Integer-Werte:')
print(l_Kohorte)
print(l_KohorteM)
print(l_KohorteW)
print(l_KohorteI)
f_EmptyRows()

#------------------------------------------------------------------
# Entsprechende Listen l_KohorteM, l_KohorteW und l_KohorteI
# "ohne die Spaltenüberschriften".
# Anschließend werden die beiden letzten Einträge in den Listen gelöscht,
# da man diese zur Gewinnung von Sterblichkeiten nicht benötigt werden.

# Here "Call by Value" (Wertübergabe) and
# NOT "Call by reference" (pointer, Zeiger) => andere Identität wird hier benötigt !!!
l_KohorteM1 = l_KohorteM[:]
l_KohorteW1 = l_KohorteW[:]
l_KohorteI1 = l_KohorteI[:]

l_KohorteM1.pop(f_constp00())
l_KohorteW1.pop(f_constp00())
l_KohorteI1.pop(f_constp00())

for zaehler in range(f_constp00(), f_constp02()):
    l_KohorteM1.pop()
    l_KohorteW1.pop()
    l_KohorteI1.pop()

print(f'Hier die Listen ohne die Spaltenüberschrift und die beiden letzten Elemente:')
print(l_KohorteM1)
print(l_KohorteW1)
print(l_KohorteI1)
f_EmptyRows()

#------------------------------------------------------------------
# Listen ohne die Altersbeschreibung und mit Kürzung der Geschlechtsangabe.
#

for listenplatz1 in range(len(l_KohorteM)):
    for listenplatz2 in range(len(l_KohorteM[listenplatz1])):
        if listenplatz2 == f_constp00():
            l_KohorteM[listenplatz1][listenplatz2] = 'm'
        elif listenplatz2 == f_constp01():
            del l_KohorteM[listenplatz1][listenplatz2]
            #l_KohorteM[listenplatz1].pop(listenplatz2)
        else:
            pass

for listenplatz1 in range(len(l_KohorteW)):
    for listenplatz2 in range(len(l_KohorteW[listenplatz1])):
        if listenplatz2 == f_constp00():
            l_KohorteW[listenplatz1][listenplatz2] = 'w'
        elif listenplatz2 == f_constp01():
            del l_KohorteW[listenplatz1][listenplatz2]
            #l_KohorteW[listenplatz1].pop(listenplatz2)
        else:
            pass

for listenplatz1 in range(len(l_KohorteI)):
    for listenplatz2 in range(len(l_KohorteI[listenplatz1])):
        if listenplatz2 == f_constp00():
            l_KohorteI[listenplatz1][listenplatz2] = 'I'
        elif listenplatz2 == f_constp01():
            del l_KohorteI[listenplatz1][listenplatz2]
            #l_KohorteI[listenplatz1].pop(listenplatz2)
        else:
            pass


print(f'Mit diesen folgenden Listen wird weiter gearbeitet:')
print(l_KohorteM1)
print(l_KohorteW1)
print(l_KohorteI1)
f_EmptyRows()
#------------------------------------------------------------------
# Listen ohne Geschlechtsangabe und ohne Altersangabe.
# Wir beschränken uns auf das wesentliche.

for listenplatz1 in range(len(l_KohorteM1)):
    for listenplatz2 in range(len(l_KohorteM1[listenplatz1])):
        if listenplatz2 == f_constp00():
            del l_KohorteM1[listenplatz1][listenplatz2:listenplatz2+2]
        else:
            pass

for listenplatz1 in range(len(l_KohorteW1)):
    for listenplatz2 in range(len(l_KohorteW1[listenplatz1])):
        if listenplatz2 == f_constp00():
            del l_KohorteW1[listenplatz1][listenplatz2:listenplatz2+2]
        else:
            pass

for listenplatz1 in range(len(l_KohorteI1)):
    for listenplatz2 in range(len(l_KohorteI1[listenplatz1])):
        if listenplatz2 == f_constp00():
            del l_KohorteI1[listenplatz1][listenplatz2:listenplatz2+2]
        else:
            pass

print(f'o.B.d.A. und o.B.a.d.A. sind dies unsere Ausgangslisten:')
print(l_KohorteM1)
print(l_KohorteW1)
print(l_KohorteI1)
f_EmptyRows()

#------------------------------------------------------------------
# Wir erzeugen eine Matrix auf R^2, mit den Spaltenüberschriften der Jahre 2016 bis 2020 (=DataFrame):

COLUMNS = [str(year) for year in range(2016, 2021)]
ROWS = [int(zaehler) for zaehler in range(len(l_KohorteM1))]

df_l_KohorteM1 = pd.DataFrame(data=l_KohorteM1, index=ROWS, columns=COLUMNS)    # DataFrame
df_l_KohorteW1 = pd.DataFrame(data=l_KohorteW1, index=ROWS, columns=COLUMNS)    # DataFrame
df_l_KohorteI1 = pd.DataFrame(data=l_KohorteI1, index=ROWS, columns=COLUMNS)    # DataFrame

print(f'Unsere Matrizen:')
print(f'Mann:')
print(df_l_KohorteM1)
f_EmptyRows()
print(f'Frau:')
print(df_l_KohorteW1)
f_EmptyRows()
print(f'Gesamt:')
print(df_l_KohorteI1)
f_EmptyRows()

#print(df_l_KohorteM1.values)
#print(df_l_KohorteW1.values)
#print(df_l_KohorteI1.values)

#------------------------------------------------------------------
print(f"Aber viele Wege führen nach Rom. Also kürzer. Aber diese Matrix hier ist noch nicht ausgreift!!!")

df2_l_KohorteM1 = pd.read_csv(DATAPATH+"StatistikDerSterbefaelle_2016_2020.csv",
                              sep=";", skiprows=f_constp05(), skipfooter=f_constp06(),
                              engine='python', encoding="latin-1")
print('Nur für den Mann exemplarisch:')
print(df2_l_KohorteM1)
f_EmptyRows()

#------------------------------------------------------------------
# Wir machen jetzt nur mit Männern und Frauen weiter.
# dict_Daten ist ein "dictionary", z.B.: mit dem Schlüssel 'm' und als Wert ein "weiteres dictionary".
# Diese "weitere dictionary" hat den Schlüssel 'bez' mit dem Wert 'Männer' und
# den weiteren Schlüssel 'roh' mit dem Wert "df_l_KohorteM1",
# welches unser Dataframe ist, also eine mxn-Matrix ist.
# In dict_Daten werden unsere Ergebnisse als Dataframes gesammelt, im Laufe des Programms.

dict_Daten =\
    {
    'm': {
            'bez': 'Männer',
            'roh': df_l_KohorteM1
         },
    'w': {
            'bez': 'Frauen',
             'roh': df_l_KohorteW1
         }
    }

print(dict_Daten)
f_EmptyRows()

#------------------------------------------------------------------
# Erste Graphische Darstellung der Rohdaten für ein Geschlecht und mehrere Kohortentafeln:
def f_rohdaten(gender):
    graphen = dict_Daten[gender]["roh"].plot(title=f'Statistik der absoluten Todesfälle der Jahre 2016-2020 für die {dict_Daten[gender]["bez"]} ({gender}): ',
                                             figsize=(12, 8),
                                             color=['red', 'yellow', 'magenta', 'springgreen', 'blue']
                                             )
    graphen.set_xlabel('Versicherungstechnisches Alter x in ganzen Jahren')
    graphen.set_ylabel('Anzahl der absoluten Todesfälle y im Zeitintervall ]x-1;x]')
    graphen.grid(visible=True, alpha=0.5, linestyle="dashed", linewidth=1.5)
    plt.xlim(left=0, right=101)
    plt.ylim(bottom=0)
    plt.gca().legend([f'Absolute Todesfaelle der {gender} in 2016',
                      f'Absolute Todesfaelle der {gender} in 2017',
                      f'Absolute Todesfaelle der {gender} in 2018',
                      f'Absolute Todesfaelle der {gender} in 2019',
                      f'Absolute Todesfaelle der {gender} in 2020'], loc="upper left",
                      title=f'Absolute Todesfälle der {dict_Daten[gender]["bez"]} ({gender}) in Deutschland, Kohortentafeln der Jahre 2016-2020:'
                     )
    plt.xticks(np.arange(0, 101, 5))
    plt.yticks(np.arange(0, 21001, 1000))
    plt.tight_layout()
    plt.savefig(GRAPHPATH + f'roh_{gender}.png')
    plt.show()
    return None

f_rohdaten('m')   # Eingeben eines Strings
f_rohdaten('w')

#------------------------------------------------------------------
# Zweite Graphische Darstellung der Rohdaten für verschiedene Geschlechter pro Kohortentafel:

def f_rohdaten2(m_year,w_year):

    if m_year == f_conststr2016(): m_y=0
    elif m_year == f_conststr2017(): m_y=1
    elif m_year == f_conststr2018(): m_y=2
    elif m_year == f_conststr2019(): m_y=3
    elif m_year == f_conststr2020(): m_y=4
    else:
        pass

    if w_year == f_conststr2016(): w_y = 0
    elif w_year == f_conststr2017(): w_y = 1
    elif w_year == f_conststr2018(): w_y = 2
    elif w_year == f_conststr2019(): w_y = 3
    elif w_year == f_conststr2020(): w_y = 4
    else:
        pass

    graphen = dict_Daten['m']["roh"].plot(
                                title=f'Absolute Todesfälle der Männer {dict_Daten["m"]["roh"].columns[m_y]} und der Frauen {dict_Daten["w"]["roh"].columns[w_y]}',
                                figsize=(12, 8),
                                color=['blue'],
                                kind='line',
                                y=m_year,
                                ax=plt.gca(),
                                label=f'Absolute Todesfaelle der Maenner im Jahr {dict_Daten["m"]["roh"].columns[m_y]}'
                                )

    graphen2 = dict_Daten['w']["roh"].plot(color=['red'],
                                           kind='line',
                                           y=w_year,
                                           ax=plt.gca(),
                                           label=f'Absolute Todesfaelle der Frauen im Jahr {dict_Daten["w"]["roh"].columns[w_y]}'
                                          )

    graphen.set_xlabel('Versicherungstechnisches Alter x in ganzen Jahren')
    graphen.set_ylabel('Anzahl der absoluten Todesfälle y im Zeitintervall ]x-1;x]')
    graphen.grid(visible=True, alpha=0.5, linestyle="dashed", linewidth=1.5)
    plt.xlim(left=0, right=101)
    plt.ylim(bottom=0)
    plt.gca().legend(loc="upper left",
                     title=f'Absolute Todesfälle des Mannes von {dict_Daten["m"]["roh"].columns[m_y]} und absolute Todesfälle der Frau von {dict_Daten["w"]["roh"].columns[w_y]}'
                     )
    plt.xticks(np.arange(0, 101, 5))
    plt.yticks(np.arange(0, 21001, 1000))
    plt.tight_layout()
    plt.savefig(GRAPHPATH + f'roh_{m_year}_{w_year}.png')
    return None

def f_rohdaten3(x, y):
        f_rohdaten2(x, y)
        plt.show()
        return None

f_rohdaten3('2018', '2018')    # Eingeben eines Strings
f_rohdaten3('2020', '2020')
f_rohdaten3('2016', '2020')
f_rohdaten3('2020', '2016')
# Rein "optisch": Bis zum Pensionsalter wenig Unterschiede, danach anscheinend "Verschiebung" der "lokalen Maxima" nach "oben rechts".

#------------------------------------------------------------------
# Erzeugen der Differenzen der ersten Ordnung und Abspeicherung dieser Daten als Dataframe
# in unserem Ergebnis-Dictionary (Das Differenzieren verstärkt Schwankungen):

# Here "Call by Value" (Wertübergabe) and
# NOT "Call by reference" (pointer, Zeiger) => andere Identität wird hier benötigt !!!
l_KohorteM2 = l_KohorteM1[:]
l_KohorteW2 = l_KohorteW1[:]

for listenplatz1 in range(len(l_KohorteM2)-1):
    for listenplatz2 in range(len(l_KohorteM2[listenplatz1])):
        l_KohorteM2[listenplatz1][listenplatz2]=l_KohorteM2[listenplatz1+1][listenplatz2] - l_KohorteM2[listenplatz1][listenplatz2]

for listenplatz1 in range(len(l_KohorteW2)-1):
    for listenplatz2 in range(len(l_KohorteW2[listenplatz1])):
        l_KohorteW2[listenplatz1][listenplatz2]=l_KohorteW2[listenplatz1+1][listenplatz2] - l_KohorteW2[listenplatz1][listenplatz2]

COLUMNS_2 = [str(year) for year in range(2016, 2021)]
ROWS_2 = [int(zaehler) for zaehler in range(len(l_KohorteM2))]

df_l_KohorteDiffM1 = pd.DataFrame(data=l_KohorteM2, index=ROWS_2, columns=COLUMNS_2)
df_l_KohorteDiffW1 = pd.DataFrame(data=l_KohorteW2, index=ROWS_2, columns=COLUMNS_2)

# dict_Daten ist eine abzählbare Folge von DataFrames, welche sich wiederum in einem dictionary befindet:
dict_Daten['m']['diff'] = df_l_KohorteDiffM1
dict_Daten['w']['diff'] = df_l_KohorteDiffW1

print(f'Nach Bildung der ersten Differenzen, ergibt sich folgende Datensammlung:')
f_EmptyRows()
print(dict_Daten)
f_EmptyRows()

#------------------------------------------------------------------
# Dritte Graphische Darstellung der Differenzen ersten Ordnung für ein Geschlecht und mehrere Kohortentafeln:
def f_diffrohdaten(gender):
    graphen = dict_Daten[gender]["diff"].plot(title=f'1. Differenzen der absoluten Todesfälle der Jahre 2016-2020 für die {dict_Daten[gender]["bez"]} ({gender}): ',
                                                figsize=(12, 8),
                                                color=['red', 'yellow', 'magenta', 'springgreen', 'blue']
                                                )
    graphen.set_xlabel('Versicherungstechnisches Alter x in ganzen Jahren')
    graphen.set_ylabel('Delta der absoluten Todesfälle [f(x)-f(x-1)] im Zeitintervall ]x-1;x]')
    graphen.grid(visible=True, alpha=0.5, linestyle="dashed", linewidth=1.5)
    plt.xlim(left=0, right=101)
    plt.ylim(bottom=0)
    plt.gca().legend([f'Delta-Todesfaelle der {gender} in 2016',
                      f'Delta-Todesfaelle der {gender} in 2017',
                      f'Delta-Todesfaelle der {gender} in 2018',
                      f'Delta-Todesfaelle der {gender} in 2019',
                      f'Delta-Todesfaelle der {gender} in 2020'], loc="upper left",
                      title=f'Delta-Todesfälle der {dict_Daten[gender]["bez"]} ({gender}) in Deutschland, Kohortentafeln der Jahre 2016-2020:'
                     )
    plt.xticks(np.arange(0, 101, 5))

    if gender   == sex2_m: plt.yticks(np.arange(-3400, 2800, 200))
    elif gender == sex2_w: plt.yticks(np.arange(-5600, 6400, 400))
    else:
        pass

    plt.tight_layout()
    plt.savefig(GRAPHPATH + f'diffroh_{gender}.png')
    plt.show()
    return None

f_diffrohdaten('m')   # Eingeben eines Strings
f_diffrohdaten('w')
f_EmptyRows()
print(f'Die Differenzen zeigen ab dem Alter 65 pro Geschlecht etwa deutliches Schwankungsverhalten.')
f_EmptyRows()

#------------------------------------------------------------------
# Vierte Graphische Darstellung der Differenzen ersten Ordnung für verschiedene Geschlechter pro Kohortentafel:

def f_diffrohdaten2(m_year,w_year):

    if m_year == f_conststr2016(): m_y=0
    elif m_year == f_conststr2017(): m_y=1
    elif m_year == f_conststr2018(): m_y=2
    elif m_year == f_conststr2019(): m_y=3
    elif m_year == f_conststr2020(): m_y=4
    else:
        pass

    if w_year == f_conststr2016(): w_y = 0
    elif w_year == f_conststr2017(): w_y = 1
    elif w_year == f_conststr2018(): w_y = 2
    elif w_year == f_conststr2019(): w_y = 3
    elif w_year == f_conststr2020(): w_y = 4
    else:
        pass

    graphen = dict_Daten['m']["diff"].plot(
                                title=f'1. Differenzen der absoluten Todesfälle der Männer {dict_Daten["m"]["diff"].columns[m_y]} und der Frauen {dict_Daten["w"]["diff"].columns[w_y]}',
                                figsize=(12, 8),
                                color=['blue'],
                                kind='line',
                                y=m_year,
                                ax=plt.gca(),
                                label=f'Delta-Todesfälle der Maenner im Jahr {dict_Daten["m"]["diff"].columns[m_y]}'
                                )

    graphen2 = dict_Daten['w']["diff"].plot(color=['red'],
                                           kind='line',
                                           y=w_year,
                                           ax=plt.gca(),
                                           label=f'Delta-Todesfälle der Frauen im Jahr {dict_Daten["w"]["diff"].columns[w_y]}'
                                          )

    graphen.set_xlabel('Versicherungstechnisches Alter x in ganzen Jahren')
    graphen.set_ylabel('Delta der absoluten Todesfälle [f(x)-f(x-1)] im Zeitintervall ]x-1;x]')
    graphen.grid(visible=True, alpha=0.5, linestyle="dashed", linewidth=1.5)
    plt.xlim(left=0, right=101)
    plt.ylim(bottom=0)
    plt.gca().legend(loc="upper left",
                     title=f'Delta-Todesfälle des Mannes von {dict_Daten["m"]["diff"].columns[m_y]} und Delta-Todesfälle der Frau von {dict_Daten["w"]["diff"].columns[w_y]}'
                    )
    plt.xticks(np.arange(0, 101, 5))
    plt.yticks(np.arange(-5500, +5000, 400))
    plt.tight_layout()
    plt.savefig(GRAPHPATH + f'diffroh_{m_year}_{w_year}.png')
    return None

def f_diffrohdaten3(x, y):
        f_diffrohdaten2(x, y)
        plt.show()
        return None

f_diffrohdaten3('2018', '2018')    # Eingeben eines Strings
f_diffrohdaten3('2020', '2020')
f_diffrohdaten3('2016', '2020')
f_diffrohdaten3('2020', '2016')
print(f'Bei Frauen und Männer zeigen die Differenzen wenig Gemeinsamkeiten.')
f_EmptyRows()


#------------------------------------------------------------------
# Durchführung der Glättung der Zeitreihe durch Verwendung der Fast-Fourier-Transformierten:
# Die Integration glättet Schwankungen  mittels FFT aus.
# Im speziellen wird die Entwicklung eines Vektors nach einem vollständigen Orthonormalsystem
# in einem Hilbertraum durchgeführt.

# Fünfte graphische Darstellung der der ersten Differenzen
# der  Todesfall-Rohdaten für Männer ('m') oder Frauen ('w') pro Kohortentafel:

def diff_fourier_plot(gender, year, start, k):
    # Parameter und Elemente in Mengenschreibweise:
    # gender = {'m','w'}
    # year = {2016,2017,2018,2019,2020}
    # start = Eintrittsalter des Versicherten {18,...,70}
    # k =  Anzahl der Orthogonalbasis-Funktionen ist k, k aus den natürlichen Zahlen.
    # bzw. auch als Fourier-Filter bezeichnet.

    data = dict_Daten[gender]['diff'][year][start:]

    # Gläten der Zeitreihe mit der Fourier-Transformation
    # (eigentliche Verwendung in der Signalverarbeitung, insbesondere
    # bei periodischen Funktionen:

    fcoeffs = rfft(data)            # Fourier-Transformation
    fcoeffs[k + 1:] = 0.0           # Entfernen der hohen Frequenzen
    fitted_data = irfft(fcoeffs)    # Inverse Fourier-Transformation

    # Graphik-Formatierung:
    fig, ax = plt.subplots(figsize=(12, 8))

    ax.set_title(f'1. Differenzen von Todesfällen mit Fourier-Filter der {dict_Daten[gender]["bez"]} im Jahr {year}, ab dem Eintrittsalter {start}', color='C0')
    ax.set_xlabel(f'Versicherungstechnisches Alter x in ganzen Jahren, ab Eintrittsalter {start}')
    ax.set_ylabel(f'Delta Todesfälle (Erste Differenzen) {dict_Daten[gender]["bez"]}')
    ax.plot(data.values, label=f'Delta-1-Rohdaten ({dict_Daten[gender]["bez"]}), {year}, EA {start}')
    ax.plot(fitted_data, label=f'Fourier-Filter (k = {k})')
    ax.grid(visible=True, alpha=0.5, linestyle="dashed", linewidth=1.5)
    ax.color = ['red', 'yellow']

    legend = ax.legend(loc='lower left', shadow=True, fontsize='x-large')
    xticks_range = np.arange(0, 100 - start + 1, 5)
    labels = plt.xticks(xticks_range, xticks_range + start)

    if gender == sex2_m:
        plt.yticks(np.arange(-3400, 2800, 200))
    elif gender == sex2_w:
        plt.yticks(np.arange(-5600, 6400, 400))
    else:
        pass

    plt.tight_layout()
    plt.savefig(GRAPHPATH + f'ff_{gender}_{year}_{start}_{k}.png')
    plt.show()
    return fcoeffs[:k]     # Rückgabe der Fourierkoeffizienten der Orthogonalbasis-Funktionen

def diff_fourier_plot2(gender, year, start, k):
    print(f'FFT (Fast-Fourier-Transformierte) und ihre Koeffizienten:')
    fourierkoeffizienten=diff_fourier_plot(gender, year, start, k)
    print(f'{fourierkoeffizienten}')
    f_EmptyRows()
    return None


diff_fourier_plot2('m', '2018', 50, 22)

diff_fourier_plot2('m', '2019', 65, 15)

diff_fourier_plot2('m', '2018', 20, 36)
f_EmptyRows()

#------------------------------------------------------------------
# Von den Rohdaten zu den Sterbewahrscheinlichkeiten, aber ohne
# Berücksichtigung der "zeitlichen Entwicklung der Kohorten"
# Es kann aber der Mittelwert der Todesfälle
# für das x-te Lebensjahr der neuesten Kohortenjahre 2016-2020 betrachtet werden:


df_aggregiert = pd.DataFrame(
                           np.array([list(df_l_KohorteM1.mean(axis=1).values),
                                     list(df_l_KohorteW1.mean(axis=1).values)]).T,
                                     columns=['Männer', 'Frauen']
                            )

print('Das ist die aggregierte Kohortentafel mit erwartungstreuen Schätzer für die Jahre 2016-2020:')
print(df_aggregiert)
f_EmptyRows()

#------------------------------------------------------------------
# Sechste graphische Darstellung der aggregierten Kohortentafeln 2016-2020:


def f_aggregiert():
    graph = df_aggregiert.plot(title='Todesfälle in Deutschland 2016-2020, aggregiert und gemittelt',
                               figsize=(12, 8),
                               color=['yellow', 'springgreen'])
    graph.set_xlabel('Versicherungstechnisches Alter x in ganzen Jahren')
    graph.set_ylabel('Absolute gemittelte Todesfälle der Jahre 2016-2020 im Zeitintervall ]x-1;x]')
    graph.grid(visible=True, alpha=0.5, linestyle="dashed", linewidth=1.5)
    plt.xlim(left=0, right=101)
    plt.ylim(bottom=0)

    plt.gca().legend([f'Absolute gemittelte Todesfaelle der {df_aggregiert.columns[0]}',
                      f'Absolute gemittelte Todesfaelle der {df_aggregiert.columns[1]}'],
                      loc="upper left",
                      title=f'Erwartungstreu geschätzte absolute Todesfälle der Jahre 2016-2020:'
                     )

    plt.xticks(np.arange(0, 101, 5))
    plt.tight_layout()

    plt.savefig(GRAPHPATH + 'aggregiert.png')
    plt.show()
    return None


f_aggregiert()
f_EmptyRows()

#------------------------------------------------------------------
# Die weitere Entwicklung zur Absterbeordnung und zu den Sterbewahrscheinlichkeiten
# für die aggregierten und gemittelten Jahre 2016-2021 für Männer und Frauen:

# Schätzer für die Wahrscheinlichkeit, daß ein x-jähriger Mann im Versicherungsjahr ]x-1;x] verstirbt:
AbsterbeOrdnungM = np.r_[df_l_KohorteM1.sum(axis=1).values[::-1].cumsum()[::-1], np.zeros(1)]
AbsterbeOrdnungM = 10**6 / AbsterbeOrdnungM[0] * AbsterbeOrdnungM

# Schätzer für die Wahrscheinlichkeit, daß eine x-jährige Frau im Versicherungsjahr ]x-1;x] verstirbt:
AbsterbeOrdnungW = np.r_[df_l_KohorteW1.sum(axis=1).values[::-1].cumsum()[::-1], np.zeros(1)]
AbsterbeOrdnungW = 10**6 / AbsterbeOrdnungW[0] * AbsterbeOrdnungW

df_AbsterbeOrdnung = pd.DataFrame(
                                   np.array([AbsterbeOrdnungM, AbsterbeOrdnungW]).T,
                                             columns=['Männer', 'Frauen']
                                 )

#------------------------------------------------------------------
# Siebte graphische Darstellung der Absterbeordung:

def f_absterben():
    graph = df_AbsterbeOrdnung.plot(title='Geschätzte Absterbeordnung für Deutschland, aggregiert und gemittelt',
                               figsize=(12, 8),
                               color=['yellow', 'springgreen'])
    graph.set_xlabel('Versicherungstechnisches Alter x in ganzen Jahren')
    graph.set_ylabel('Anzahl der Überlebenden zum Alterszeitpunkt x')
    graph.grid(visible=True, alpha=0.5, linestyle="dashed", linewidth=1.5)
    plt.xlim(left=0, right=101)
    plt.ylim(bottom=0)

    plt.gca().legend([f'Absterbeordnung der {df_aggregiert.columns[0]}',
                      f'Absterbeordnung der {df_aggregiert.columns[1]}'],
                      loc="lower left",
                      title=f'Absterbeordnung ausgehend von 1 Mio versicherter Personen:'
                     )

    plt.xticks(np.arange(0, 101, 5))
    plt.yticks(np.arange(0, 1100000, 100000))
    plt.tight_layout()

    plt.savefig(GRAPHPATH + 'absterben.png')
    plt.show()
    return None

f_absterben()
f_EmptyRows()

#------------------------------------------------------------------
# Absterbeordungen der einzelnen Kohortenjahre 2016-2020:

df_l_KohorteM1sum = dict(zip(df_l_KohorteM1.columns, [df_l_KohorteM1[column].sum() for column in df_l_KohorteM1.columns]))
df_l_KohorteW1sum = dict(zip(df_l_KohorteW1.columns, [df_l_KohorteW1[column].sum() for column in df_l_KohorteW1.columns]))

df_l_KohorteM1absterben=pd.DataFrame(
    np.array([np.r_[df_l_KohorteM1[column].values[::-1].cumsum()[::-1]/df_l_KohorteM1sum[column]*(10**6), np.zeros(1)] for column in df_l_KohorteM1.columns]).T,
                 columns=df_l_KohorteM1.columns
            )

df_l_KohorteW1absterben=pd.DataFrame(
    np.array([np.r_[df_l_KohorteW1[column].values[::-1].cumsum()[::-1]/df_l_KohorteW1sum[column]*(10**6), np.zeros(1)] for column in df_l_KohorteW1.columns]).T,
                columns = df_l_KohorteW1.columns
            )

dict_Daten['m']['ao'] = df_l_KohorteM1absterben
dict_Daten['w']['ao'] = df_l_KohorteW1absterben

print(dict_Daten)
#------------------------------------------------------------------
# Achte graphische Darstellung der Absterbeordungen der einzelnen Kohortenjahre 2016-2020:



def f_einzelnsterben(gender):
    graph = dict_Daten[gender]['ao'].plot(title=f'Geschätzte Absterbeordnungen: {dict_Daten[gender]["bez"]} in Deutschland, 2016-2021.',
                               figsize=(12, 8),
                               color=['red', 'yellow', 'magenta', 'springgreen', 'blue'])
    graph.set_xlabel('Versicherungstechnisches Alter x in ganzen Jahren')
    graph.set_ylabel('Anzahl der Überlebenden zum Alterszeitpunkt x')
    graph.grid(visible=True, alpha=0.5, linestyle="dashed", linewidth=1.5)
    plt.xlim(left=0, right=101)
    plt.ylim(bottom=0)

    plt.gca().legend([f'Absterbeordnung der {gender} in 2016',
                      f'Absterbeordnung der {gender} in 2017',
                      f'Absterbeordnung der {gender} in 2018',
                      f'Absterbeordnung der {gender} in 2019',
                      f'Absterbeordnung der {gender} in 2020'],
                     loc="lower left",
                     title=f'Absterbeordnung {dict_Daten[gender]["bez"]} ({gender}) ausgehend von 1 Mio versicherter Personen:'
                     )

    plt.xticks(np.arange(0, 101, 5))
    plt.yticks(np.arange(0, 1100000, 100000))
    plt.tight_layout()

    plt.savefig(GRAPHPATH + f'ao_{gender}.png')
    plt.show()
    return None

f_einzelnsterben('m')
f_einzelnsterben('w')
f_EmptyRows()

#------------------------------------------------------------------
# Sensitivitätsanalyse:
# Welche Unterschiede ergeben sich beim
# "Leistungsbarwert einer lebenslänglichen nachschüssigen Leibrente"
# zum versicherungstechnischen Alter x,
# wenn man die einzelnen Absterbeordnungen von 2016-2020 und
# einen vorgegebenen Rechnungszins betrachtet?


def f_lbw_leibrente(x, ao, rz):
    # x ist das Eintrittsalter der versicherten Person
    # ao ist die zu betrachtende Absterbeordnung
    # rz ist der vorzugebende Rechnungszins

    survival_probabilities = ao[x+1:]/ao[x]
    discount_factors = np.array([(1+rz/100) ** (-t) for t in range(1, len(ao) - x)])
    return np.inner(survival_probabilities, discount_factors)


f_lbw_leibrente(20, df_l_KohorteM1absterben['2016'], 1.5)

#------------------------------------------------------------------
# Neunte graphische Darstellung zur Sensitivitätsanalyse:

def f_sensitiv(gender, rz):
    ao = dict_Daten[gender]['ao']

    fig = plt.figure(figsize=(12, 8))

    ax = fig.add_subplot(111, projection='3d')

    for colour, x in zip(['r', 'g', 'b', 'y', 'c', 'magenta'], [20, 30, 40, 50, 60, 70]):
        xs = range(5)
        ys = np.array([f_lbw_leibrente(x, ao[year], rz) for year in COLUMNS])
        ref_value = ys[0]
        ys = (ys - ref_value)/ref_value * 100
        cs = [colour] * len(xs)
        ax.bar(xs, ys, zs=x, zdir='y', color=cs, alpha=0.8)

    ax.set_title(f'Relatives Leistungsbarwert-Delta (in %) zum Jahr 2016,\n{dict_Daten[gender]["bez"]} bei Rechnungszins {rz}%')
    ax.set_ylabel('Versicherungstechnisches Alter x')
    ax.set_zlabel('Delta Leistungsbarwerte in (%)')
    plt.xticks(np.arange(5), COLUMNS)
    plt.savefig(GRAPHPATH+f'sens_{gender}_{rz}.pdf')
    plt.show()

f_sensitiv('m', 1.5)
f_sensitiv('m', 3.5)

f_sensitiv('w', 1.5)
f_sensitiv('w', 3.5)
#------------------------------------------------------------------
#------------------------------------------------------------------

