"""
Modul sa funkcijama za proračun O-C dijagrama,
fitovanje trećeg tela i bootstrap analizu grešaka.
"""
import numpy as np
from scipy.optimize import curve_fit

def Epoch(t, P):
    """Računa epohu za dato vreme pomračenja i period dvojnog sistema."""
    t0 = t[0]
    epoch = np.round((t-t0)/P*2)/2
    return epoch

def OC(t,E, P):
    """Računa O-C vrednosti za zadato vreme pomračenja, epohu i period."""
    t0 = t[0]
    C = t0 + P*E
    OC = t - C
    return OC

def OC_trece_telo(t, t03, p3, e, asini, w, shift):
    """Modeluje uticaj trećeg tela na O-C dijagram efektom svetlosnog kašnjenja."""
    M = (2 * np.pi * (t - t03)) / p3
    E = M
    #Ovde rešavam Keplerovu jednačinu da bih dobila pravu anomaliju iz ekscentrične
    #Stavila sam za početak 15 iteracija, možda treba promeniti da uslov bude
    #da se dostigne neka zadata tačnost
    #for _ in range(15):
    #    E = M + e * np.sin(E)

    epsilon = 1e-10
    razlika = 1

    while np.max(razlika) > epsilon:
        E_novo = M + e * np.sin(E)
        razlika = abs(E_novo - E)
        E = E_novo

    v = 2 * np.arctan(np.sqrt((1+e) / (1-e)) * np.tan(E/2) )

    dt = (asini / 2.59e10) * (
        ((1 - np.power(e, 2)) / (1 + e * np.cos(v))) * np.sin(v + w)
        + e * np.sin(w)
        ) + shift

    y = t + dt
    return t - y #Ovde se vraća O-C

def izracunaj_bootstrap_greske(t, oc, bounds, N=200):
    """
    Računa standardne greške parametara nelinearnog fita pomoću Bootstrap metode.
    
    Argumenti:
    t -- niz vremenskih trenutaka pomračenja
    oc -- niz O-C vrednosti
    bounds -- granice za parametre
    N -- broj bootstrap iteracija
    
    Vraća:
    bootstrap_greske -- niz standardnih devijacija za svaki parametar
    """
    n_tacaka = len(t)
    broj_parametara = len(bounds[0])
    
    # Matrica u koju upisujemo fitovane parametre za svaku iteraciju
    popt_bootstrap = np.zeros((N, broj_parametara))
    uspesni_fitovi = 0

    for i in range(N):
        # Nasumični indeksi sa ponavljanjem
        boot_indeksi = np.random.choice(n_tacaka, size=n_tacaka, replace=True)
        
        t_boot = t[boot_indeksi]
        oc_boot = oc[boot_indeksi]
        
        try:
            # Ponavljanje fitovanja na re-uzorkovanim podacima
            # Koristi funkciju OC_trece_telo koja mora biti definisana u notebook-u
            popt_b, _ = curve_fit(
                OC_trece_telo, t_boot, oc_boot,
                bounds=bounds, maxfev=5000
            )
            popt_bootstrap[uspesni_fitovi] = popt_b
            uspesni_fitovi += 1
        except RuntimeError:
            # Ponekad fit može da ne konvergira na lošem uzorku, to preskačemo
            continue

    # Skraćujemo matricu samo na uspešne fitove
    popt_bootstrap = popt_bootstrap[:uspesni_fitovi]

    # Računanje standardne devijacije za svaki parametar
    bootstrap_greske = np.std(popt_bootstrap, axis=0)

    return bootstrap_greske, popt_bootstrap

def izracunaj_masu_treceg_tela(P3, asini):
    """Računa minimalnu masu trećeg tela na osnovu funkcije mase."""
    M12 = 2 * 1.989e30 #2 mase Sunca
    G = 6.67408e-11
    
    T = P3 * 24 * 60 * 60 #period pretvaramo u sekunde iz dana

    asini1 = asini * 1000

    fm = ((4*np.pi**2) / (G*T**2)) * asini1**3 

    coeff = [1, -fm, -2*fm*M12, - fm*(M12**2)]
    rezultat = np.roots(coeff)

    Masa = np.real(rezultat[0])
    #Jer ova funkcija np.roots vraća vrednost u formatu kompleksnog broja
    Masa = Masa / 1.989e30 #Vraćam u mase sunca iz kg
    return Masa

def izracunaj_bootstrap_gresku_mase(popt_bootstrap):
    """
    Prolazi kroz sve bootstrap fitove koji su izlaz iz funkcije 
    izracunaj_bootstrap_greske, računa masu trećeg tela za svaku 
    iteraciju i vraća standardnu grešku (neodređenost) mase.
    
    Argumenti:
    popt_bootstrap -- matrica uspešnih parametara iz bootstrap fita, 
    dimenzija (N_boot, broj_parametara)
    
    Vraća:
    masa_error -- standardna devijacija izračunatih masa
    """
    P3_boot = popt_bootstrap[:, 1]
    asini_boot = popt_bootstrap[:, 3]
    N = len(popt_bootstrap)
    # Niz u koji ću smestiti izračunate mase za svaku iteraciju
    mase_bootstrap = np.zeros(len(popt_bootstrap))

    for i in range(N):
        mase_bootstrap[i] = izracunaj_masu_treceg_tela(P3_boot[i], asini_boot[i])

    # Izbacujemo nan vrednosti ako ih je bilo
    mase_bootstrap = mase_bootstrap[~np.isnan(mase_bootstrap)]

    # Standardna devijacija svih izračunatih masa je direktno greška dobijene mase!
    masa_error = np.std(mase_bootstrap)
    
    return masa_error
