# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 15:13:18 2016

@author: michielstock

Create alignment independent features for proteins
"""

import numpy as np

# amino acid descriptors

Z_1 = {'A': 0.07, 'V' : -2.69, 'L' : -4.19, 'I' : -4.44, 'P' : -1.22,
       'F' : -4.92, 'W': -4.75, 'M':-2.49, 'K': 2.84, 'R' : 2.88, 'H': 2.41,
       'G' :2.23, 'S': 1.96, 'T' : 0.92, 'C' : 0.71, 'Y' : -1.39, 'N' : 3.22,
       'Q' : 2.18, 'D' : 3.64, 'E' : 3.08}

Z_2 = {'A': -1.73, 'V' : -2.53, 'L' : -1.03, 'I' : -1.68, 'P' : 0.88,
       'F' : 1.3, 'W': 3.65, 'M':-.27, 'K': 1.41, 'R' : 2.52, 'H': 1.74,
       'G' :-5.36, 'S': -1.63, 'T' : -2.09, 'C' : 0.71, 'Y' : 2.32,
       'N' : 0.01, 'Q' : 0.53, 'D' : 1.13, 'E' : 0.39}

Z_3 = {'A': 0.09, 'V' : -1.29, 'L' : -0.98, 'I' : -1.03, 'P' : 2.23,
       'F' : 0.45, 'W': 0.85, 'M':-.41, 'K': -3.14, 'R' : -3.44, 'H': 1.11,
       'G' :0.30, 'S': 0.57, 'T' : -1.4, 'C' :4.13 , 'Y' : 0.01, 'N' : 0.84,
       'Q' : -1.14, 'D' : 2.36, 'E' : -0.07}

def calc_AC( seq, lag, Za, Zb = None ):
    if Zb is None:
        Zb = Za
    AC = 0
    n = len(seq)
    for i in range( n - lag ):
        if Za.has_key(seq[ i ]) and Zb.has_key(seq[ i + lag ]):
            AC += ( Za[ seq[ i ] ] * Zb[ seq[ i + lag ] ] )/( n - lag )
    return AC


def ProteinFeatures(sequence, lagRange = range(1, 25),
                    discriptors = [Z_1, Z_2, Z_3]):
    """
    Calculates features of protein sequences based on lagged correlation
    of physicochemical properties of the amino acids
    """
    k = len(lagRange)
    p = len(discriptors)
    n_features = (p + (p*(p-1))/2)*k
    x = np.zeros(n_features)
    ind = 0
    for lag in lagRange:
        for Z in discriptors:
           x[ind] =  calc_AC(sequence, lag, Z)
           ind += 1
        for i in range(p-1):
            for j in range(i+1, p):
                x[ind] =  calc_AC(sequence, lag, discriptors[i], discriptors[j])
                ind += 1
    return x


if __name__ == '__main__':
    
    # example on
    # RNA-dependent RNA polymerase [Sudan ebolavirus]
    
    sequence = '''MMATQHTQYPDARLSSPIVLDQCDLVTRACGLYSEYSLNPKLRTCRLPKHIYRLKYDAIVLRFISDVPVATIPIDYIAPMLINVLADSKNAPLEPPCLSFLDEIVNYTVQDAAFLNYYMNQIKTQEGVITDQLKQNIRRVIHKNRYLSALFFWHDLSILTRRGRMNRGNVRSTWFVTNEVVDILGYGDYIFWKIPIALLPMNSANVPHASTDWYQPNIFKEAIQGHTHIISVSTAEVLIMCKDLVTSRFNTLLIAELARLEDPVSADYPLVDDIQSLYNA
GDYLLSILGSEGYQIIKYLEPLCLAKIQLCSQYTERKGRFLTQMHLAVIQTLRELLLNRGLKKSQLSKIR
EFHQLLLRLRSTPQQLCELFSIQKHWGHPVLHSEKAIQKVKNHATVLKALRPIIIFETYCVFKYSVAKHF
FDSQGTWYSVISDRCLTPGLNSYIRRNQFPPLPMIKDLLWEFYHLDHPPLFSTKIISDLSIFIKDRATAV
EQTCWDAVFEPNVLGYSPPYRFNTKRVPEQFLEQEDFSIESVLQYAQELRYLLPQNRNFSFSLKEKELNV
GRTFGKLPYLTRNVQTLCEALLADGLAKAFPSNMMVVTEREQKESLLHQASWHHTSDDFGEHATVRGSSF
VTDLEKYNLAFRYEFTAPFIKYCNQCYGVRNVFDWMHFLIPQCYMHVSDYYNPPHNVTLENREYPPEGPS
AYRGHLGGIEGLQQKLWTSISCAQISLVEIKTGFKLRSAVMGDNQCITVLSVFPLESSPNEQERCAEDNA
ARVAASLAKVTSACGIFLKPDETFVHSGFIYFGPKQYLNGIQLPQSLKTAARMAPLSDAIFDDLQGTLAS
IGTAFERSISETRHILPSRVAAAFHTYFSVRILQHHHLGFHKGSDLGQLAINKPLDFGTIALSLAVPQVL
GGLSFLNPEKCLYRNLGDPVTSGLFQLKHYLSMVGMSDIFHALVAKSPGNCSAIDFVLNPGGLNVPGSQD
LTSFLRQIVRRSITLSARNKLINTLFHASADLEDELVCKWLLSSTPVMSRFAADIFSRTPSGKRLQILGY
LEGTRTLLASKMISNNAETPILERLRKITLQRWNLWFSYLDHCDSALMEAIQPIRCTVDIAQILREYSWA
HILGGRQLIGATLPCIPEQFQTTWLKPYEQCVECSSTNNSSPYVSVALKRNVVSAWPDASRLGWTIGDGI
PYIGSRTEDKIGQPAIKPRCPSAALREAIELTSRLTWVTQGSANSDQLIRPFLEARVNLSVQEILQMTPS
HYSGNIVHRYNDQYSPHSFMANRMSNTATRLMVSTNTLGEFSGGGQAARDSNIIFQNVINFAVALYDIRF
RNTCTSSIQYHRAHIHLTDCCTREVPAQYLTYTTTLNLDLSKYRNNELIYDSEPLRGGLNCNLSIDSPLM
KGPRLNIIEDDLIRLPHLSGWELAKTVLQSIISDSSNSSTDPISSGETRSFTTHFLTYPKIGLLYSFGAL
ISFYLGNTILCTKKIGLTEFLYYLQNQIHNLSHRSLRIFKPTFRHSSVMSRLMDIDPNFSIYIGGTAGDR
GLSDAARLFLRIAISTFLSFVEEWVIFRKANIPLWVVYPLEGQRPDPPGEFLNRVKSLIVGIEDDKNKGS
ILSRSEEKCSSNLVYNCKSTASNFFHASLAYWRGRHRPKKTIGATKATTAPHIILPLGNSDRPPGLDLNQ
SNDTFIPTRIKQIVQGDSRNDRTTTTRLPPQSRSTPTSATEPPTKIYEGSTTYRGKSTDTHLDEGHNAKE
FPFNPHRLVVPFFKLTKDGEYSIEPSPEESRSNIKGLLQHLRTMVDTTIYCRFTGIVSSMHYKLDEVLWE
YNKFESAVTLAEGEGSGALLLIQKYGVKKLFLNTLATEHSIESEVISGYTTPRMLLSVMPRTHRGELEVI
LNNSASQITDITHRDWFSNQKNRIPNDVDIITMDAETTENLDRSRLYEAVYTIICNHINPKTLKVVILKV
FLSDLDGMCWINNYLAPMFGSGYLIKPITSSARSSEWYLCLSNLLSTLRTTQHQTQANCLHVVQCALQQQ
VQRGSYWLSHLTKYTTSRLHNSYIAFGFPSLEKVLYHRYNLVDSRNGPLVSITRHLALLQTEIRELVTDY
NQLRQSRTQTYHFIKTSKGRITKLVNDYLRFELVIRALKNNSTWHHELYLLPELIGVCHRFNHTRNCTCS
ERFLVQTLYLHRMSDAEIKLMDRLTSLVNMFPEGFRSSSV'''

sequence = sequence.replace('\n', '')

features = ProteinFeatures(sequence)