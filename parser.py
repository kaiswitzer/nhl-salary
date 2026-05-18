import pandas as pd
import re

raw_text = """
1Zucker, Jason
34LYr 1 of 2
2$4,750,000M-NTC2025-26UFA2026-27UFAEustace King
Kevyn Adams
62242145$106k0.7350.00.01.132.262Zuccarello, Mats
38RYr 2 of 2
2$4,125,000NMC2024-25UFA2025-26UFACraig Oster
Bill Guerin
59153954$76k0.9254.02.00.492.163Zub, Artyom
30DYr 3 of 4
4$4,600,000M-NTC2023-24UFA2026-27UFADaniel Milstein
Pierre Dorion
8152530$153k0.3754.0-1.00.221.134Zibanejad, Mika
33CYr 4 of 8
8$8,500,000NMC2022-23UFA2029-30UFAMonir Kalgoum
Chris Drury
81344478$109k0.9651.03.00.811.835Zetterlund, Fabian
26LYr 1 of 3
3$4,275,0002025-26RFA+ARB2027-28UFAClaude Lemieux
Steve Staios
82171633$130k0.4055.00.00.771.596Zellweger, Olen
22DYr 3 of 3
3$844,1672023-242025-26RFADave Cowan
Bob Murray
7671522$38k0.2953.01.00.270.907Zegras, Trevor
25CYr 3 of 3
3$5,750,0002023-24RFA2025-26RFA+ARBPat Brisson
Pat Verbeek
81264167$86k0.8355.06.00.691.878Zary, Connor
24CYr 1 of 3
3$3,775,0002025-26RFA2027-28RFA+ARBMichael Kaye
Craig Conroy
74121325$151k0.3448.00.00.601.139Zamula, Yegor
26DYr 1 of 1
1$1,000,0002025-26RFA+ARB2025-26RFA+ARBDaniel Milstein
Don Waddell
33033$333k0.0947.0-6.00.000.4410Zadorov, Nikita
31DYr 2 of 6
6$5,000,000NTC2024-25UFA2029-30UFADaniel Milstein
Don Sweeney
8122022$227k0.2745.0-2.00.090.8111Zacha, Pavel
29CYr 3 of 4
4$4,750,000M-NTC2023-24UFA2026-27UFAPaul Capizzano
Don Sweeney
78303565$73k0.8346.0-1.00.942.3112Yurov, Danila
22RYr 1 of 3
3$950,0002025-262027-28RFARick Komarow
Bill Guerin
73121527$35k0.3748.0-2.00.741.6013York, Cameron
25DYr 1 of 5
5$5,150,0002025-26RFA+ARB2029-30UFAPat Brisson
Daniel Briere
7442226$198k0.3547.0-4.00.140.7514Yamamoto, Kailer
27RYr 1 of 1
1$775,0002025-26UFA no QO2025-26UFAJ.P. Barry
Bill Armstrong
59131023$34k0.3955.04.01.182.0915Yakemchuk, Carter
20DYr 0 of 3
3$942,5002026-272028-29RFAVlad Shushkovsky
Steve Staios
4112$471k0.5041.0-8.01.191.1916Yager, Brayden
21CYr 1 of 3
3$918,3332025-262027-28RFAGerry Johannson
Kyle Dubas
30000.0054.019.00.000.0017Xhekaj, Arber
25DYr 2 of 2
2$1,300,0002024-25RFA2025-26RFA+ARBBrian & Scott Bartlett
Kent Hughes
65134$325k0.0643.0-5.00.080.3418Wright, Shane
22CYr 2 of 3
3$886,6662024-252026-27RFAKurt Overhardt
Ron Francis
74121527$33k0.3653.08.00.551.2419Wright, Jared
23RYr 1 of 2
2$867,5002025-262026-27RFADean Grillo
Rob Blake
23044$217k0.1761.07.00.000.9220Wotherspoon, Parker
28DYr 1 of 2
2$1,000,0002025-26UFA2026-27UFACraig Oster
Kyle Dubas
8032730$33k0.3850.0-2.00.091.0821Wood, Miles
30LYr 3 of 6
6$2,500,000M-NTC2023-24UFA2028-29UFAPeter Fish
Chris MacFarland
548614$179k0.2647.0-4.00.731.2522Wood, Matthew
21LYr 2 of 3
3$950,0002024-252026-27RFASean Coffey
Barry Trotz
71171330$32k0.4247.0-3.00.981.7123Winterton, Ryan
22CYr 3 of 3
3$828,3332023-242025-26RFAJohn Walters
Ron Francis
6841418$46k0.2651.06.00.331.4824Wilson, Garrett
35LYr 1 of 1
1$775,0002025-26UFA2025-26UFA
Daniel Briere
30000.0059.06.00.000.0025Wilson, Tom
32RYr 2 of 7
7$6,500,000M-NTC2024-25UFA2030-31UFAPatrick Morris
Brian MacLellan
72303262$105k0.8655.05.01.062.3026Wilsby, Adam
25DYr 1 of 2
2$775,0002025-26RFA+ARB2026-27RFA+ARBJoakim Persson
Barry Trotz
5811516$48k0.2848.0-2.00.000.8127Willander, Tom
21DYr 1 of 3
3$950,0002025-262027-28RFAMark Gandler & Todd Diamond
Patrik Allvin
7051621$45k0.3040.0-5.00.180.7028Wiesblatt, Ozzy
24CYr 1 of 2
2$775,0002025-26RFA2026-27RFA+ARBDave Cowan
Barry Trotz
40145$155k0.1347.0-2.00.160.8229Wiebe, Abram
22DYr 1 of 2
2$950,0002025-262026-27RFADaren Hermiston
Craig Conroy
40000.0038.0-10.00.000.0030Whitecloud, Zach
29DYr 4 of 6
6$2,750,0002022-23RFA+ARB2027-28UFADean Grillo
Kelly McCrimmon
7821517$162k0.2246.0-5.00.090.6231Werenski, Zach
28DYr 4 of 6
6$9,583,333NMC2022-23RFA+ARB2027-28UFAJudd Moldaver
Jarmo Kekalainen
75225981$118k1.0855.06.00.651.7932Wennberg, Alexander
31CYr 2 of 2
2$5,000,000NTC2024-25UFA2025-26UFAPat Brisson
Mike Grier
80183755$91k0.6948.00.00.431.6133Weegar, MacKenzie
32DYr 3 of 8
8$6,250,000NTC2023-24UFA2030-31UFAMatthew Ebbs
Brad Treliving
7942428$223k0.3546.0-3.00.170.8934Weber, Shea
40DYr 14 of 14
14$7,857,1432012-13RFA2025-26UFAJarrett Bousquet
David Poile
00000.000.00.00.000.0035Washe, Tim
24CYr 1 of 2
2$812,5002025-26RFA2026-27RFA+ARBRichard Evans
Pat Verbeek
39235$163k0.1347.0-6.00.310.7736Ward, Taylor
28RYr 1 of 1
1$775,0002025-26UFA2025-26UFAJustin Duberman
Ken Holland
36347$111k0.1953.0-1.00.571.3237Walman, Jake
30DYr 3 of 3
3$3,400,000NMC2023-24UFA2025-26UFAWade Arnott
Steve Yzerman
5381220$170k0.3845.0-8.00.341.0238Walker, Nathan
32LYr 2 of 2
2$775,0002024-25UFA2025-26UFAAllan Walsh
Doug Armstrong
464711$70k0.2447.0-2.00.501.3739Walker, Sean
31DYr 2 of 5
5$3,600,000M-NTC2024-25UFA2028-29UFAKurt Overhardt (KO)
Eric Tulsky
8192231$116k0.3857.02.00.280.9340Voronkov, Dmitri
25LYr 1 of 2
2$4,175,0002025-26RFA+ARB2026-27RFA+ARBRick Komarow
Don Waddell
63171532$130k0.5156.06.00.741.8241Vlasic, Alex
24DYr 2 of 6
6$4,600,0002024-25RFA+ARB2029-30UFABrian & Scott Bartlett
Kyle Davidson
8121921$219k0.2640.0-3.00.090.7742Villeneuve, William
24DYr 1 of 1
1$775,0002025-26RFA2025-26RFA+ARBDavid Gagner
Brad Treliving
30000.0040.0-4.00.000.0043Vilardi, Gabriel
26CYr 1 of 6
6$7,500,0002025-26RFA+ARB2030-31UFAAndy Scott
Kevin Cheveldayoff
82303969$109k0.8450.03.00.802.1644Viel, Jeffrey
29LYr 2 of 2
2$775,0002024-25UFA2025-26UFAAllain Roy
Don Sweeney
453710$78k0.2252.00.00.351.0445Verhaeghe, Carter
30CYr 1 of 8
8$7,000,000NMC2025-26UFA2032-33UFAIan Pulver
Bill Zito
77253055$127k0.7151.01.00.892.1246Veleno, Joseph
26CYr 1 of 1
1$900,0002025-26RFA+ARB2025-26RFA+ARBPhilippe Lecavalier
Kent Hughes
61235$180k0.0846.0-1.00.190.4847Vatrano, Frank
32CYr 1 of 3
3$4,571,189M-NTC2025-26UFA2027-28UFAPeter Fish
Pat Verbeek
50549$508k0.1842.0-10.00.480.8548van Riemsdyk, James
37LYr 1 of 1
1$1,000,0002025-26UFA2025-26UFAJudd Moldaver
Steve Yzerman
72151631$32k0.4348.00.00.711.7849van Riemsdyk, Trevor
34DYr 3 of 3
3$3,000,0002023-24UFA2025-26UFAJudd Moldaver
Brian MacLellan
6831114$214k0.2151.00.00.190.8250Vaakanainen, Urho
27DYr 1 of 2
2$1,550,0002025-26RFA+ARB2026-27UFAMika Rautakallio
Chris Drury
34066$258k0.1847.0-1.00.000.8351Ufko, Ryan
23DYr 2 of 3
3$925,0002024-252026-27RFAJohn Kofi Osei-Tutu & Bobby Gauthier
Barry Trotz
182911$84k0.6137.0-6.00.552.2052Tverberg, Ryan
24CYr 3 of 3
3$851,6672023-242025-26RFA+ARBJohn Walters
Kyle Dubas
20000.0041.01.00.000.0053Turcotte, Alex
25CYr 2 of 3
3$775,0002024-25RFA2026-27RFA+ARBPat Brisson
Rob Blake
6231114$55k0.2356.06.00.281.3054Tucker, Tyler
26DYr 1 of 2
2$925,0002025-26RFA+ARB2026-27UFARyan Barnes
Doug Armstrong
6931417$54k0.2551.03.00.201.1555Tuch, Alex
30RYr 7 of 7
7$4,750,000M-NTC2019-20RFA2025-26UFABrian & Scott Bartlett
George McPhee
79333366$72k0.8451.01.01.082.5456Tsyplakov, Maxim
27RYr 1 of 2
2$2,250,0002025-26RFA+ARB2026-27UFARyan Barnes
Mathieu Darche
49224$563k0.0848.0-1.00.280.5757Trouba, Jacob
32DYr 7 of 7
7$8,000,000M-NTC2019-20RFA2025-26UFAKurt Overhardt
Jeff Gorton
81102535$229k0.4350.0-2.00.321.0558Trocheck, Vincent
32CYr 4 of 7
7$5,625,000M-NTC2022-23UFA2028-29UFAMatthew Oates
Chris Drury
67163753$106k0.7943.0-5.00.681.6759Trenin, Yakov
29CYr 2 of 4
4$3,500,0002024-25UFA2027-28UFARenat Mamashev
Bill Guerin
8261723$152k0.2851.00.00.381.4460Toropchenko, Alexei
26RYr 1 of 1
1$1,700,0002025-26RFA+ARB2025-26UFAPatrick Morris
Doug Armstrong
654711$155k0.1742.0-9.00.280.7461Toninato, Dominic
32CYr 1 of 2
2$850,0002025-26UFA2026-27UFA
Kyle Davidson
8011$850k0.1353.010.00.000.9662Tolvanen, Eeli
27RYr 2 of 2
2$3,475,0002024-25RFA+ARB2025-26UFAMichael Curran
Ron Francis
78122436$97k0.4640.0-8.00.300.9763Toffoli, Tyler
34RYr 2 of 4
4$6,000,000NTC2024-25UFA2027-28UFAPat Brisson
Mike Grier
79193049$122k0.6249.02.00.732.0564Toews, Jonathan
38CYr 1 of 1
1$2,000,000NMC2025-26UFA2025-26UFAPat Brisson
Kevin Cheveldayoff
82111829$69k0.3547.00.00.311.2065Toews, Devon
32DYr 2 of 7
7$7,250,000NMC2024-25UFA2030-31UFARoss Gurney
Chris MacFarland
6832124$302k0.3557.00.00.101.0466Tkachuk, Matthew
28LYr 4 of 8
8$9,500,000NMC2022-23RFA+ARB2029-30UFACraig Oster
Brad Treliving
31132134$279k1.1054.09.01.032.0667Tkachuk, Brady
26LYr 5 of 7
7$8,205,714NMC2021-22RFA2027-28UFACraig Oster
Pierre Dorion
60223759$139k0.9862.07.00.872.4568Tippett, Owen
27RYr 2 of 8
8$6,200,0002024-25RFA+ARB2031-32UFAMurray Koontz
Daniel Briere
81282351$122k0.6355.05.01.052.0469Timmins, Conor
27DYr 1 of 2
2$2,200,0002025-26RFA+ARB2026-27UFAPaul Capizzano
Kevyn Adams
39088$275k0.2147.0-7.00.000.8170Thomson, Lassi
25DYr 1 of 1
1$775,0002025-26RFA2025-26UFA-Group6Craig Oster
Steve Staios
11033$258k0.2762.09.00.000.8571Thompson, Tage
28CYr 3 of 7
7$7,142,857M-NTC2023-24RFA+ARB2029-30UFAJerry Buckley
Kevyn Adams
81404181$88k1.0050.00.01.552.3072Thomas, Robert
26CYr 3 of 8
8$8,125,000NTC2023-24RFA+ARB2030-31UFACraig Oster
Doug Armstrong
64253964$127k1.0055.07.00.932.5973Theodore, Shea
30DYr 1 of 7
7$7,425,000NTC2025-26UFA2031-32UFACraig Oster
Kelly McCrimmon
70102939$190k0.5656.02.00.321.2774Texier, Alexandre
26LYr 1 of 1
1$1,000,0002025-26RFA+ARB2025-26RFA+ARBDaniel Milstein
Kent Hughes
5181321$48k0.4150.01.00.771.8375Terry, Troy
28CYr 3 of 7
7$7,000,000M-NTC2023-24RFA+ARB2029-30UFAKurt Overhardt
Pat Verbeek
61193857$123k0.9355.03.00.802.2576Teravainen, Teuvo
31CYr 2 of 3
3$5,400,000M-NTC2024-25UFA2026-27UFAMarkus Lehto
Kyle Davidson
75142135$154k0.4741.0-2.00.400.8777Tavares, John
35CYr 1 of 4
4$4,389,280NMC2025-26UFA2028-29UFAPat Brisson
Brad Treliving
82314071$62k0.8750.06.00.772.0078Tarasenko, Vladimir
34RYr 2 of 2
2$4,750,000M-NTC2024-25UFA2025-26UFAPat Brisson
Steve Yzerman
75232447$101k0.6349.0-3.01.051.9179Tanev, Christopher
36DYr 2 of 6
6$4,500,000NMC2024-25UFA2029-30UFAWade Arnott
Brad Treliving
11022$2.25M0.1844.0-10.00.000.8280Tanev, Brandon
34LYr 1 of 3
3$2,500,000M-NTC2025-26UFA2027-28UFAWade Arnott
Bill Armstrong
56033$833k0.0544.0-9.00.000.3581Sýkora, Adam
21LYr 2 of 3
3$806,6662024-252026-27RFAGerry Johannson
Chris Drury
11314$202k0.3642.0-17.01.612.1482Svechnikov, Andrei
26RYr 5 of 8
8$7,750,000M-NTC2021-22RFA2028-29UFAMark Gandler & Todd Diamond
Don Waddell
79313970$111k0.8955.0-1.00.861.8983Svechkov, Fyodor
23CYr 3 of 3
3$925,0002023-242025-26RFADaniel Milstein
David Poile
7041317$54k0.2449.00.00.231.2484Suzuki, Nick
26CYr 4 of 8
8$7,875,0002022-23RFA2029-30UFADavid Gagner
Marc Bergevin
822972101$78k1.2353.06.00.582.1685Suter, Pius
29CYr 1 of 2
2$4,125,0002025-26UFA2026-27UFAGeorges Mueller
Doug Armstrong
64131629$142k0.4550.00.00.681.4386Suniev, Aydar
21LYr 2 of 3
3$923,3332024-252026-27RFAWade Arnott
Craig Conroy
6011$923k0.1742.02.00.001.0087Sundqvist, Oskar
32CYr 2 of 2
2$1,500,0002024-25UFA2025-26UFAClaude Lemieux
Doug Armstrong
5251217$88k0.3338.0-13.00.461.7388Stutzle, Tim
24LYr 3 of 8
8$8,350,0002023-24RFA2030-31UFABen Hankinson
Pierre Dorion
80344983$101k1.0453.0-4.00.922.2789Sturm, Nico
31CYr 1 of 2
2$2,000,0002025-26UFA2026-27UFAMatt Keator
Bill Guerin
495611$182k0.2251.00.00.410.9590Struble, Jayden
24DYr 1 of 2
2$1,412,5002025-26RFA+ARB2026-27RFA+ARBPhilippe Lecavalier
Kent Hughes
5921012$118k0.2048.0-1.00.150.8291Strome, Ryan
32CYr 4 of 5
5$5,000,0002022-23UFA2026-27UFAPatrick Morris
Pat Verbeek
5281321$238k0.4051.01.00.601.7192Strome, Dylan
29CYr 3 of 5
5$5,000,0002023-24RFA+ARB2027-28UFAPatrick Morris
Brian MacLellan
80193958$86k0.7350.00.00.601.5893Stone, Mark
34RYr 7 of 8
8$9,500,000NMC2019-20UFA2026-27UFACraig Oster
George McPhee
60284573$130k1.2259.06.01.022.4094Stephenson, Chandler
32CYr 2 of 7
7$6,250,000NMC2024-25UFA2030-31UFAJason Davidson & Blake Evans
Ron Francis
80163349$128k0.6136.0-14.00.431.3595Stenlund, Kevin
29CYr 2 of 2
2$2,000,0002024-25UFA2025-26UFAJarrett Bousquet
Bill Armstrong
8041418$111k0.2342.0-12.00.140.6296Steeves, Alex
26CYr 1 of 1
1$850,0002025-26UFA-Group62025-26UFA-Group6Allain Roy
Don Sweeney
439716$53k0.3750.04.00.811.4897Steel, Sam
28CYr 1 of 2
2$2,100,0002025-26UFA2026-27UFAGerry Johannson
Jim Nill
73122133$64k0.4550.0-1.00.561.6898Stecher, Troy
32DYr 2 of 2
2$787,5002024-25UFA2025-26UFAEustace King
Jeff Jackson
6431114$56k0.2245.01.00.110.7499Stastney, Spencer
26DYr 2 of 2
2$825,0002024-25RFA+ARB2025-26RFA+ARBPete Rutili
Barry Trotz
662810$83k0.1549.0-4.00.130.60100Stanley, Logan
27DYr 2 of 2
2$1,250,0002024-25RFA+ARB2025-26UFAPatrick Morris
Kevin Cheveldayoff
7691726$48k0.3443.0-6.00.431.03
"""

def clean_nhl_text(text):
    players = []
    
    # NEW PATTERN: 
    # 1. Matches Name (Last, First)
    # 2. Skips lines until it finds the Position (C, L, R, D) followed by 'Yr'
    # 3. Skips lines until it finds the $ amount
    pattern = r"([A-Za-z]+,\s[A-Za-z]+).*?\n.*?([CLRD])Yr.*?\n.*?\$([0-9,]+)"
    
    # re.DOTALL is the magic trick here—it lets the '.' match across new lines
    matches = re.finditer(pattern, text, re.DOTALL)
    
    for match in matches:
        name = match.group(1).strip()
        pos = match.group(2)
        salary_str = match.group(3).replace(',', '')
        
        salary = int(salary_str)
        group = "Offense" if pos in ['C', 'L', 'R'] else "Defense"
        
        players.append({
            "Player": name, 
            "Position": pos,
            "Position_Group": group, 
            "Cap_Hit": salary
        })
    
    return pd.DataFrame(players)

# Run the cleaner
df_players = clean_nhl_text(raw_text)

if not df_players.empty:
    df_players.to_csv("cleaned_players.csv", index=False)
    print(f"✅ Success! Extracted {len(df_players)} players to cleaned_players.csv")
    print(df_players.head()) # Shows you the first 5 rows in the terminal
else:
    print("❌ No players found. Check the raw_text format.")