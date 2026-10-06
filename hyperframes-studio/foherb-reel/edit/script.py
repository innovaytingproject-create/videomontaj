"""Russian subtitles (translation of the Uzbek speech) and graphic cues, in SOURCE seconds.

*word* marks a word highlighted in brand orange.
"""

# kind "title" lines are shown as big kinetic titles instead of a subtitle.
CAPTIONS = [
    (0.00, 2.90, "title", "Massajni sevasizmi?"),
    (3.00, 5.10, "cap", "Men massajni *juda sevaman*"),
    (5.20, 8.45, "cap", "Shuning uchun assotsiatsiyada o’zimga"),
    (8.50, 11.25, "cap", "mana shunday pribor — *biomassajyor* xarid qildim"),
    (11.30, 13.15, "title", "Bu shunchaki mo’jiza"),
    (13.50, 17.40, "cap", "Buni *uyingiz uchun* ham xarid qilsangiz bo’ladi"),
    (18.80, 21.40, "cap", "O’zingiz bilan *olib yurish* mumkin"),
    (21.50, 25.30, "cap", "Mana, qarang: *remenchalari* bor"),
    (25.40, 27.20, "cap", "taqdingiz — yelkaga osdingiz"),
    (27.25, 29.25, "cap", "qo’lda ushlab yursangiz ham bo’ladi"),
    (29.30, 33.95, "cap", "remenlari *mana bunday* taqiladi"),
    (34.05, 38.00, "cap", "u tomondan ham, bu tomondan ham"),
    (38.30, 40.80, "cap", "Xuddi *kosmetichkaga* o’xshaydi"),
    (40.85, 44.30, "cap", "grimyorlar sumkasini shunday taqib yuradi"),
    (44.45, 47.10, "cap", "taqib oldingiz — *yurish qulay*"),
    (47.30, 50.00, "cap", "Endi — *ichidagi mo’jiza*"),
    (52.40, 55.95, "cap", "Qarang, bu yerda nima bor:"),
    (56.00, 60.30, "cap", "tolalariga *kumush* o’tkazilgan"),
    (60.35, 63.30, "cap", "massaj uchun *kumushli qo’lqop*"),
    (68.10, 72.85, "cap", "Bular — *ulash uchun* provodlar"),
    (72.90, 76.70, "cap", "biomassajyor *bir nechta funksiyaga* ega"),
    (78.00, 84.80, "cap", "*kumush qo’lqoplar* qo’lga taqiladi"),
    (86.40, 93.20, "cap", "bu — *elektr quvvati*, rozetkaga ulanadi"),
    (97.60, 100.45, "cap", "Mana o’zi — *biomassajyor*"),
    (100.50, 104.15, "cap", "ajoyib, kichkinagina pribor"),
    (104.20, 106.35, "cap", "uni *«qovoqcha»* deb ham atashadi"),
    (106.60, 108.30, "cap", "Uni *mana bunday* o’rnatamiz"),
    (109.10, 111.60, "cap", "va hammasini birga ulaymiz"),
    (112.30, 114.10, "cap", "U funksiyasini *o’zi bajaradi*"),
    (114.15, 115.50, "cap", "funksiyalari — *beshta*"),
    (115.60, 120.00, "cap", "massajni *o’zi qilib beradi*"),
    (120.90, 124.95, "cap", "Qo’lqop taqilsa — *impuls massaj*"),
    (125.00, 127.70, "cap", "*guasha* massaji"),
    (127.75, 129.95, "cap", "va hatto *quruq hijoma*"),
    (130.20, 135.80, "cap", "Yana mana bu *kichkina nasadkasi* bor"),
    (136.10, 139.95, "cap", "*Quloq* og’risa, *burun* bitib qolsa"),
    (140.00, 144.10, "cap", "uni ham davolashda ishlatiladi"),
    (144.20, 149.25, "skip", ""),
    (149.30, 154.50, "cap", "Qo’l massajida *charchab qolish* mumkin"),
    (155.00, 159.80, "cap", "bu massajyor bilan esa *hammasini o’zingiz*"),
    (159.85, 164.60, "cap", "bemalol, kuch sarflamasdan qilasiz"),
    (165.20, 167.60, "cap", "Men uni *juda sevib qoldim*"),
    (167.70, 171.25, "cap", "onamning oyoq tomirlari og’riydi"),
    (171.30, 174.30, "cap", "*varikoz* muammosini ketkazadi"),
    (174.35, 176.20, "cap", "oyoq tomirlarini"),
    (176.25, 179.00, "cap", "*ikki qavat ichkariga* kirib ishlaydi"),
    (179.05, 182.90, "cap", "nafaqat teri — *ichki tomirlar* bilan ham"),
    (183.00, 185.80, "cap", "U *kichkina* — sumkada olib yuring"),
    (185.85, 187.70, "cap", "bemalol ishlataverasiz"),
    (187.80, 191.70, "cap", "*Fiziokabinet* ochmoqchi bo’lsangiz —"),
    (191.75, 194.30, "cap", "bu *zo’r imkoniyat*, daromad qiling"),
    (194.35, 195.85, "title", "Tavsiya qilaman!"),
]

# Numbered block cards: (source start, number, label).
CHIPS = [
    (18.80, "01", "O’zingiz bilan oling"),
    (47.30, "02", "Kumush qo’lqoplar"),
    (97.60, "03", "Biomassajyor"),
    (136.10, "04", "Quloq va burun"),
    (165.20, "05", "Tomirlar uchun"),
]

# Function pills appear as she names each one (source seconds), all clear at FUNC_END.
FUNCS = [(123.20, "Impuls massaj"), (126.30, "Guasha"), (127.90, "Quruq hijoma")]
FUNC_END = 129.95

BIG_FIVE = (114.15, 115.50)    # "у него их пять"
STAT = (146.15, 149.25)        # "1 биомассажёр = 10 ручных массажей"
PRODUCT_TAG = (8.50, 11.25)    # name tag when she first names the device
CTA_START = 187.80
END_TAIL = 0.6                 # end card hold past the source end (the take already ends on a pause)
