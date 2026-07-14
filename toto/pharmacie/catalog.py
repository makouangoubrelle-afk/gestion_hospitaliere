"""
Catalogue pharmaceutique SGHL — médicaments par pathologie / indication.
Chaque entrée : (code, nom, forme, dosage, indication, stock_initial, seuil_alerte)
"""

MEDICAMENT_CATALOG = [
    # --- Infections bactériennes ---
    ('AMOX500', 'Amoxicilline', 'Comprimé', '500 mg', 'Infections bactériennes, angine, otite, sinusite, pneumonie', 300, 60),
    ('AMCL625', 'Amoxicilline-Acide clavulanique', 'Comprimé', '625 mg', 'Infections résistantes, sinusite, pneumonie, infections urinaires', 200, 40),
    ('AZIT500', 'Azithromycine', 'Comprimé', '500 mg', 'Pneumonie, bronchite, infections ORL, MST (chlamydia)', 180, 35),
    ('CIPRO500', 'Ciprofloxacine', 'Comprimé', '500 mg', 'Infections urinaires, prostatite, diarrhée infectieuse, typhoïde', 150, 30),
    ('DOXY100', 'Doxycycline', 'Comprimé', '100 mg', 'Acné, infections respiratoires, maladie de Lyme, paludisme prophylaxie', 120, 25),
    ('METRO500', 'Métronidazole', 'Comprimé', '500 mg', 'Infections anaérobies, parasitoses (giardiase), vaginose', 160, 30),
    ('CEFTR1G', 'Ceftriaxone', 'Poudre injectable', '1 g', 'Méningite, septicémie, pneumonie sévère, gonorrhée', 80, 15),
    ('GENTA80', 'Gentamicine', 'Ampoule', '80 mg/2 ml', 'Infections sévères, septicémie, infections urinaires', 60, 12),
    ('CLIND300', 'Clindamycine', 'Gélule', '300 mg', 'Infections osseuses, dentaires, peau (acné)', 100, 20),
    ('ERYTH500', 'Érythromycine', 'Comprimé', '500 mg', 'Infections ORL, pneumonie (allergie pénicilline), coqueluche', 90, 18),
    ('BACT800', 'Sulfaméthoxazole-Triméthoprime', 'Comprimé', '800/160 mg', 'Infections urinaires, pneumocystose, diarrhées', 140, 28),
    ('VANCO500', 'Vancomycine', 'Poudre injectable', '500 mg', 'Infections à S. aureus résistant, endocardite', 40, 8),
    ('CLAR500', 'Clarithromycine', 'Comprimé', '500 mg', 'Helicobacter pylori, bronchite, pneumonie', 110, 22),
    ('PHENO1G', 'Phénoxyméthylpénicilline', 'Comprimé', '1 M UI', 'Angine streptococcique, prophylaxie rhumatismale', 130, 25),

    # --- Infections virales ---
    ('ACYC200', 'Aciclovir', 'Comprimé', '200 mg', 'Herpès, zona, varicelle, encéphalite herpétique', 100, 20),
    ('VALAC500', 'Valaciclovir', 'Comprimé', '500 mg', 'Herpès génital, zona, prophylaxie CMV', 70, 14),
    ('OSLT75', 'Oseltamivir', 'Gélule', '75 mg', 'Grippe saisonnière (influenza A et B)', 90, 18),
    ('RIBA200', 'Ribavirine', 'Comprimé', '200 mg', 'Hépatite C (association), infections virales sévères', 30, 6),

    # --- Infections fongiques ---
    ('FLUCO150', 'Fluconazole', 'Gélule', '150 mg', 'Candidoses, cryptococcose, teigne', 120, 24),
    ('NYST100', 'Nystatine', 'Comprimé', '100 000 UI', 'Candidose buccale, mycoses digestives', 150, 30),
    ('KETO200', 'Kétoconazole', 'Comprimé', '200 mg', 'Mycoses cutanées et systémiques, teigne', 80, 16),
    ('AMPHB50', 'Amphotéricine B', 'Poudre injectable', '50 mg', 'Mycoses systémiques sévères, leishmaniose', 25, 5),

    # --- Paludisme et parasitoses ---
    ('ARTLUM', 'Artéméther-Luméfantrine', 'Comprimé', '20/120 mg', 'Paludisme à Plasmodium falciparum (non compliqué)', 400, 80),
    ('QUIN300', 'Quinine', 'Comprimé', '300 mg', 'Paludisme sévère, crise de paludisme', 200, 40),
    ('PRIMA15', 'Primaquine', 'Comprimé', '15 mg', 'Paludisme à P. vivax (radical cure)', 100, 20),
    ('ALB400', 'Albendazole', 'Comprimé', '400 mg', 'Ascaridiose, oxyurose, ankylostomiase, neurocysticercose', 350, 70),
    ('MEB100', 'Mébendazole', 'Comprimé', '100 mg', 'Vers intestinaux (ascaris, oxyures)', 300, 60),
    ('PRAZ600', 'Praziquantel', 'Comprimé', '600 mg', 'Schistosomiase, téniasis, distomatose', 180, 36),
    ('IVER3', 'Ivermectine', 'Comprimé', '3 mg', 'Onchocercose, filariose, gale, strongyloïdose', 250, 50),
    ('METR250', 'Métronidazole sirop', 'Sirop', '250 mg/5 ml', 'Amibiase, giardiase, trichomonase', 80, 16),

    # --- Tuberculose ---
    ('INH300', 'Isoniazide', 'Comprimé', '300 mg', 'Tuberculose pulmonaire et extra-pulmonaire', 120, 24),
    ('RIF600', 'Rifampicine', 'Comprimé', '600 mg', 'Tuberculose, prophylaxie méningococcique', 120, 24),
    ('ETHA400', 'Éthambutol', 'Comprimé', '400 mg', 'Tuberculose (schéma RIPE)', 100, 20),
    ('PYRA500', 'Pyrazinamide', 'Comprimé', '500 mg', 'Tuberculose (phase intensive)', 100, 20),

    # --- VIH / SIDA ---
    ('TDF300', 'Ténofovir', 'Comprimé', '300 mg', 'VIH (antirétroviral), hépatite B', 90, 18),
    ('3TC300', 'Lamivudine', 'Comprimé', '300 mg', 'VIH, hépatite B', 90, 18),
    ('EFV600', 'Éfavirenz', 'Comprimé', '600 mg', 'VIH (trithérapie première ligne)', 80, 16),
    ('DTG50', 'Dolutégravir', 'Comprimé', '50 mg', 'VIH (traitement moderne, résistances)', 70, 14),
    ('COTRI', 'Cotrimoxazole prophylactique', 'Comprimé', '960 mg', 'Prophylaxie pneumocystose (patients VIH)', 150, 30),

    # --- Hypertension artérielle ---
    ('AMLO5', 'Amlodipine', 'Comprimé', '5 mg', 'Hypertension artérielle, angine de poitrine', 250, 50),
    ('AMLO10', 'Amlodipine', 'Comprimé', '10 mg', 'Hypertension sévère, angor réfractaire', 180, 36),
    ('ENAL10', 'Énalapril', 'Comprimé', '10 mg', 'Hypertension, insuffisance cardiaque, néphropathie', 200, 40),
    ('LISI10', 'Lisinopril', 'Comprimé', '10 mg', 'Hypertension, post-infarctus, insuffisance cardiaque', 190, 38),
    ('LOSA50', 'Losartan', 'Comprimé', '50 mg', 'Hypertension, néphropathie diabétique', 170, 34),
    ('HCTZ25', 'Hydrochlorothiazide', 'Comprimé', '25 mg', 'Hypertension, œdèmes, insuffisance cardiaque', 220, 44),
    ('ATEN50', 'Aténolol', 'Comprimé', '50 mg', 'Hypertension, angor, arythmies, migraine', 160, 32),
    ('METO50', 'Métoprolol', 'Comprimé', '50 mg', 'Hypertension, infarctus, insuffisance cardiaque', 150, 30),
    ('NIFE20', 'Nifédipine LP', 'Comprimé', '20 mg', 'Hypertension, angor vasospastique', 140, 28),
    ('RAMI5', 'Ramipril', 'Comprimé', '5 mg', 'Hypertension, insuffisance cardiaque, prévention CV', 130, 26),

    # --- Insuffisance cardiaque / œdèmes ---
    ('FURO40', 'Furosémide', 'Comprimé', '40 mg', 'Œdèmes, insuffisance cardiaque, hypertension', 200, 40),
    ('SPIRO25', 'Spironolactone', 'Comprimé', '25 mg', 'Insuffisance cardiaque, cirrhose, hyperaldostéronisme', 120, 24),
    ('DIGO25', 'Digoxine', 'Comprimé', '0,25 mg', 'Fibrillation auriculaire, insuffisance cardiaque', 80, 16),
    ('BISO5', 'Bisoprolol', 'Comprimé', '5 mg', 'Insuffisance cardiaque chronique, hypertension', 110, 22),

    # --- Maladies cardiovasculaires / cholestérol ---
    ('ASP100', 'Aspirine', 'Comprimé', '100 mg', 'Prévention infarctus, AVC, angor', 500, 100),
    ('CLOP75', 'Clopidogrel', 'Comprimé', '75 mg', 'Post-stent, prévention AVC/infarctus', 180, 36),
    ('ATOR20', 'Atorvastatine', 'Comprimé', '20 mg', 'Hypercholestérolémie, prévention cardiovasculaire', 200, 40),
    ('SIMV20', 'Simvastatine', 'Comprimé', '20 mg', 'Hypercholestérolémie, prévention CV', 170, 34),
    ('GTN05', 'Trinitrine sublinguale', 'Comprimé', '0,5 mg', 'Crise d\'angor, insuffisance cardiaque aiguë', 100, 20),
    ('ISDN10', 'Dinitrate d\'isosorbide', 'Comprimé', '10 mg', 'Angor chronique, insuffisance cardiaque', 90, 18),
    ('HEPA5000', 'Héparine', 'Ampoule', '5000 UI', 'Thrombose veineuse, embolie pulmonaire, AVC', 60, 12),
    ('ENOX40', 'Énoxaparine', 'Seringle', '40 mg', 'Thrombose, prophylaxie post-opératoire', 70, 14),
    ('WARF5', 'Warfarine', 'Comprimé', '5 mg', 'Fibrillation auriculaire, thrombose, prothèses valvulaires', 90, 18),

    # --- Diabète ---
    ('METF850', 'Metformine', 'Comprimé', '850 mg', 'Diabète type 2, syndrome des ovaires polykystiques', 300, 60),
    ('GLIB5', 'Glibenclamide', 'Comprimé', '5 mg', 'Diabète type 2', 150, 30),
    ('GLIC80', 'Gliclazide', 'Comprimé', '80 mg', 'Diabète type 2', 140, 28),
    ('INSGLAR', 'Insuline glargine', 'Stylo', '100 UI/ml', 'Diabète type 1 et 2, contrôle glycémique prolongé', 50, 10),
    ('INSRAP', 'Insuline rapide', 'Stylo', '100 UI/ml', 'Diabète, acidocétose, hyperglycémie aiguë', 50, 10),
    ('SITA100', 'Sitagliptine', 'Comprimé', '100 mg', 'Diabète type 2 (inhibiteur DPP-4)', 80, 16),
    ('GLUC40', 'Glucose 40%', 'Ampoule', '40 %', 'Hypoglycémie sévère, urgence', 120, 24),

    # --- Asthme / BPCO / respiratoire ---
    ('SALB100', 'Salbutamol', 'Aérosol', '100 mcg/dose', 'Asthme, bronchospasme, BPCO', 200, 40),
    ('BECO100', 'Béclométasone', 'Aérosol', '100 mcg/dose', 'Asthme persistant, rhinite allergique', 150, 30),
    ('BUDE200', 'Budésonide', 'Aérosol', '200 mcg/dose', 'Asthme, BPCO, rhinite', 140, 28),
    ('IPRA20', 'Ipratropium', 'Aérosol', '20 mcg/dose', 'BPCO, bronchospasme, asthme', 130, 26),
    ('MONT10', 'Montélukast', 'Comprimé', '10 mg', 'Asthme, rhinite allergique', 120, 24),
    ('THEO300', 'Théophylline', 'Comprimé', '300 mg', 'Asthme, BPCO sévère', 70, 14),
    ('AMOXCLAV', 'Amoxicilline sirop', 'Sirop', '250 mg/5 ml', 'Infections respiratoires pédiatriques', 100, 20),

    # --- Douleur / fièvre / inflammation ---
    ('PARA500', 'Paracétamol', 'Comprimé', '500 mg', 'Douleur, fièvre, céphalées, arthralgies', 600, 120),
    ('PARA1G', 'Paracétamol', 'Comprimé', '1 g', 'Douleur modérée à sévère, fièvre', 400, 80),
    ('IBU400', 'Ibuprofène', 'Comprimé', '400 mg', 'Douleur, inflammation, fièvre, dysménorrhée', 350, 70),
    ('DICLO50', 'Diclofénac', 'Comprimé', '50 mg', 'Douleur inflammatoire, arthrite, entorses', 280, 56),
    ('TRAM50', 'Tramadol', 'Gélule', '50 mg', 'Douleur modérée à sévère', 150, 30),
    ('MORPH10', 'Morphine', 'Ampoule', '10 mg/ml', 'Douleur cancéreuse, post-opératoire sévère', 40, 8),
    ('CODE30', 'Codéine', 'Comprimé', '30 mg', 'Toux sèche, douleur légère à modérée', 100, 20),
    ('PARASIR', 'Paracétamol sirop', 'Sirop', '120 mg/5 ml', 'Fièvre et douleur pédiatriques', 200, 40),

    # --- Gastro-intestinal ---
    ('OMEP20', 'Oméprazole', 'Gélule', '20 mg', 'Ulcère, reflux gastro-œsophagien, gastrite', 250, 50),
    ('PANT40', 'Pantoprazole', 'Comprimé', '40 mg', 'RGO, ulcère, protection gastrique', 200, 40),
    ('RANI150', 'Ranitidine', 'Comprimé', '150 mg', 'Ulcère, brûlures d\'estomac, RGO', 120, 24),
    ('METOC10', 'Métoclopramide', 'Comprimé', '10 mg', 'Nausées, vomissements, reflux', 180, 36),
    ('ONDA8', 'Ondansétron', 'Comprimé', '8 mg', 'Nausées chimiothérapie, post-opératoire', 100, 20),
    ('LOPE2', 'Lopéramide', 'Gélule', '2 mg', 'Diarrhée aiguë et chronique', 200, 40),
    ('SRO', 'Sels de réhydratation orale', 'Sachet', '20,5 g', 'Déshydratation, diarrhée, choléra', 500, 100),
    ('MESAL500', 'Mésalazine', 'Comprimé', '500 mg', 'Maladie de Crohn, rectocolite hémorragique', 80, 16),
    ('LACTUL', 'Lactulose', 'Sirop', '10 g/15 ml', 'Constipation, encéphalopathie hépatique', 90, 18),

    # --- Neurologie / épilepsie ---
    ('CARBA200', 'Carbamazépine', 'Comprimé', '200 mg', 'Épilepsie, trouble bipolaire, névralgie du trijumeau', 100, 20),
    ('PHEN100', 'Phénytoïne', 'Comprimé', '100 mg', 'Épilepsie, crises tonico-cloniques', 90, 18),
    ('VALP500', 'Acide valproïque', 'Comprimé', '500 mg', 'Épilepsie généralisée, manie, migraine', 110, 22),
    ('LEVE500', 'Lévétiracétam', 'Comprimé', '500 mg', 'Épilepsie partielle et généralisée', 80, 16),
    ('SUMI50', 'Sumatriptan', 'Comprimé', '50 mg', 'Migraine avec ou sans aura', 70, 14),
    ('AMIT25', 'Amitriptyline', 'Comprimé', '25 mg', 'Douleur neuropathique, migraine prophylaxie, dépression', 100, 20),

    # --- Psychiatrie ---
    ('FLUO20', 'Fluoxétine', 'Gélule', '20 mg', 'Dépression, trouble anxieux, TOC', 120, 24),
    ('SERTR50', 'Sertraline', 'Comprimé', '50 mg', 'Dépression, anxiété, PTSD', 110, 22),
    ('HALO5', 'Halopéridol', 'Comprimé', '5 mg', 'Schizophrénie, agitation psychotique', 60, 12),
    ('RISP2', 'Rispéridone', 'Comprimé', '2 mg', 'Schizophrénie, trouble bipolaire', 70, 14),
    ('DIAZ5', 'Diazépam', 'Comprimé', '5 mg', 'Anxiété, spasmes, épilepsie, sevrage alcool', 80, 16),
    ('LORA1', 'Lorazépam', 'Comprimé', '1 mg', 'Anxiété, insomnie, agitation', 70, 14),
    ('OLANZ10', 'Olanzapine', 'Comprimé', '10 mg', 'Schizophrénie, trouble bipolaire', 65, 13),

    # --- Thyroïde / endocrinien ---
    ('LEVO50', 'Lévothyroxine', 'Comprimé', '50 mcg', 'Hypothyroïdie, goitre', 200, 40),
    ('LEVO100', 'Lévothyroxine', 'Comprimé', '100 mcg', 'Hypothyroïdie sévère', 150, 30),
    ('CARBI20', 'Carbimazole', 'Comprimé', '20 mg', 'Hyperthyroïdie (maladie de Basedow)', 60, 12),
    ('PRED5', 'Prednisolone', 'Comprimé', '5 mg', 'Inflammation, asthme, maladies auto-immunes', 180, 36),
    ('DEXA4', 'Dexaméthasone', 'Comprimé', '4 mg', 'Inflammation sévère, œdème cérébral, COVID sévère', 100, 20),
    ('HYDRO20', 'Hydrocortisone', 'Comprimé', '20 mg', 'Insuffisance surrénalienne, choc', 70, 14),

    # --- Anémie / hématologie ---
    ('FER80', 'Sulfate ferreux', 'Comprimé', '80 mg', 'Anémie ferriprive, grossesse', 300, 60),
    ('ACFOL5', 'Acide folique', 'Comprimé', '5 mg', 'Anémie mégaloblastique, grossesse, MTX', 250, 50),
    ('B121', 'Vitamine B12', 'Ampoule', '1 mg', 'Anémie pernicieuse, neuropathie B12', 80, 16),
    ('EPO4000', 'Érythropoïétine', 'Seringle', '4000 UI', 'Anémie insuffisance rénale, chimiothérapie', 30, 6),

    # --- Allergie / immunologie ---
    ('CETI10', 'Cétirizine', 'Comprimé', '10 mg', 'Rhinite allergique, urticaire, prurit', 220, 44),
    ('LORA10', 'Loratadine', 'Comprimé', '10 mg', 'Allergies saisonnières, urticaire', 200, 40),
    ('PROM25', 'Prométhazine', 'Comprimé', '25 mg', 'Allergies, nausées, sédatif', 100, 20),
    ('EPI1', 'Adrénaline auto-injecteur', 'Stylo', '0,3 mg', 'Choc anaphylactique urgence', 40, 8),

    # --- Dermatologie ---
    ('HYDRC1', 'Hydrocortisone crème', 'Crème', '1 %', 'Eczéma, dermite, démangeaisons', 150, 30),
    ('CLOT1', 'Clotrimazole crème', 'Crème', '1 %', 'Mycoses cutanées, candidose, pied d\'athlète', 140, 28),
    ('MUPI2', 'Mupirocine pommade', 'Pommade', '2 %', 'Impétigo, infections cutanées bactériennes', 100, 20),
    ('BENZ5', 'Peroxyde de benzoyle', 'Gel', '5 %', 'Acné vulgaire', 90, 18),
    ('SILV1', 'Sulfadiazine argentique', 'Crème', '1 %', 'Brûlures, plaies infectées', 80, 16),

    # --- Urologie / néphrologie ---
    ('TAMS04', 'Tamsulosine', 'Gélule', '0,4 mg', 'Hypertrophie bénigne prostate, lithiase', 110, 22),
    ('FIN5', 'Finastéride', 'Comprimé', '5 mg', 'Hypertrophie prostate, alopécie androgénique', 70, 14),
    ('NITRO100', 'Nitrofurantoïne', 'Gélule', '100 mg', 'Infection urinaire basse, prophylaxie', 130, 26),
    ('ALLO100', 'Allopurinol', 'Comprimé', '100 mg', 'Goutte, hyperuricémie', 100, 20),
    ('COLCH1', 'Colchicine', 'Comprimé', '1 mg', 'Crise de goutte aiguë', 80, 16),

    # --- Gynécologie / obstétrique ---
    ('MISO200', 'Misoprostol', 'Comprimé', '200 mcg', 'Induction travail, avortement thérapeutique, ulcère', 50, 10),
    ('OXY10', 'Ocytocine', 'Ampoule', '10 UI/ml', 'Accouchement, hémorragie post-partum', 60, 12),
    ('MIF200', 'Mifépristone', 'Comprimé', '200 mg', 'IVG médicamenteuse (cadre légal)', 30, 6),
    ('FERGYN', 'Fer injectable', 'Ampoule', '100 mg', 'Anémie ferriprive sévère grossesse', 70, 14),

    # --- Ophtalmologie ---
    ('TIMO05', 'Timolol collyre', 'Collyre', '0,5 %', 'Glaucome à angle ouvert', 60, 12),
    ('LATAN', 'Latanoprost collyre', 'Collyre', '0,005 %', 'Glaucome, hypertension oculaire', 50, 10),
    ('LARM', 'Larmes artificielles', 'Collyre', '10 ml', 'Sécheresse oculaire, conjonctivite', 100, 20),
    ('TOBRA', 'Tobramycine collyre', 'Collyre', '0,3 %', 'Conjonctivite bactérienne', 80, 16),

    # --- ORL ---
    ('OFLO', 'Ofloxacine collyre', 'Collyre', '0,3 %', 'Otite externe, conjonctivite', 70, 14),
    ('XYLO', 'Xylométazoline spray', 'Spray nasal', '0,1 %', 'Rhinite, congestion nasale', 120, 24),
    ('CERU', 'Céruménolytique', 'Gouttes auriculaires', '5 ml', 'Bouchon de cérumen', 90, 18),

    # --- Oncologie (traitements courants) ---
    ('TAMOX20', 'Tamoxifène', 'Comprimé', '20 mg', 'Cancer du sein hormono-dépendant', 40, 8),
    ('MTX25', 'Méthotrexate', 'Comprimé', '2,5 mg', 'Cancer, polyarthrite rhumatoïde, psoriasis', 35, 7),
    ('CYCLO50', 'Cyclophosphamide', 'Comprimé', '50 mg', 'Cancers, maladies auto-immunes', 25, 5),
    ('CISPL50', 'Cisplatine', 'Poudre injectable', '50 mg', 'Cancers solides (testicule, ovaire, poumon)', 20, 4),

    # --- Rhumatologie ---
    ('MTX10', 'Méthotrexate', 'Comprimé', '10 mg', 'Polyarthrite rhumatoïde, psoriasis', 50, 10),
    ('HCQ200', 'Hydroxychloroquine', 'Comprimé', '200 mg', 'Lupus, polyarthrite, paludisme prophylaxie', 80, 16),
    ('PRED20', 'Prednisone', 'Comprimé', '20 mg', 'Polyarthrite, lupus, inflammation sévère', 90, 18),

    # --- Vitamines et suppléments ---
    ('VITD1000', 'Vitamine D3', 'Comprimé', '1000 UI', 'Carence vitamine D, ostéoporose', 300, 60),
    ('VITC500', 'Vitamine C', 'Comprimé', '500 mg', 'Carence, immunité, scorbut', 250, 50),
    ('CALC500', 'Calcium carbonate', 'Comprimé', '500 mg', 'Ostéoporose, carence calcique', 200, 40),
    ('MULTIVIT', 'Multivitamines', 'Comprimé', '—', 'Carences nutritionnelles, convalescence', 180, 36),
    ('ZINC20', 'Zinc', 'Comprimé', '20 mg', 'Diarrhée enfant, carence, cicatrisation', 150, 30),

    # --- Urgences / réanimation ---
    ('ADRE1', 'Adrénaline', 'Ampoule', '1 mg/ml', 'Arrêt cardiaque, anaphylaxie, choc', 80, 16),
    ('ATRO1', 'Atropine', 'Ampoule', '1 mg', 'Bradycardie, intoxication organophosphorés', 50, 10),
    ('NALO04', 'Naloxone', 'Ampoule', '0,4 mg', 'Surdosage opioïdes', 40, 8),
    ('FLUMA', 'Flumazénil', 'Ampoule', '0,5 mg', 'Surdosage benzodiazépines', 30, 6),
    ('DIAZ10', 'Diazépam rectal', 'Gel', '10 mg', 'État de mal épileptique urgence', 35, 7),
    ('SALBAMP', 'Salbutamol nébulisation', 'Ampoule', '5 mg', 'Asthme aigu sévère, détresse respiratoire', 100, 20),

    # --- Maladies tropicales / endémiques Afrique ---
    ('ARTES120', 'Artésunate injectable', 'Ampoule', '120 mg', 'Paludisme grave, choc septique', 60, 12),
    ('SCHIST', 'Praziquantel (bilharziose)', 'Comprimé', '600 mg', 'Schistosomiase (bilharziose)', 120, 24),
    ('LEISH', 'Antimoine méglumine', 'Ampoule', '850 mg', 'Leishmaniose viscérale et cutanée', 25, 5),
    ('TRYP', 'Suramine', 'Poudre injectable', '1 g', 'Trypanosomiase (maladie du sommeil)', 15, 3),
    ('CHOLERA', 'Vaccin choléra oral', 'Flacon', '1 dose', 'Prévention choléra (zones à risque)', 40, 8),

    # --- Troubles métaboliques / autres ---
    ('ALLO300', 'Allopurinol', 'Comprimé', '300 mg', 'Goutte chronique, lithiase urique', 80, 16),
    ('ORLIST', 'Orlistat', 'Gélule', '120 mg', 'Obésité, prise de poids excessive', 60, 12),
    ('LEVOC500', 'Lévocarnitine', 'Comprimé', '500 mg', 'Carence carnitine, fatigue musculaire', 50, 10),
    ('PPIVIT', 'Pyridoxine (B6)', 'Comprimé', '100 mg', 'Carence B6, nausées grossesse', 100, 20),
    ('THIA100', 'Thiamine (B1)', 'Ampoule', '100 mg', 'Encéphalopathie de Wernicke, alcoolisme', 70, 14),

    # --- Antiparasitaires cutanés ---
    ('PERM5', 'Perméthrine crème', 'Crème', '5 %', 'Gale, poux', 120, 24),
    ('LIND1', 'Lindane lotion', 'Lotion', '1 %', 'Gale, poux (si résistance)', 60, 12),

    # --- Système nerveux central (Parkinson, Alzheimer) ---
    ('LEVO-DOPA', 'Lévodopa-Bensérazide', 'Comprimé', '100/25 mg', 'Maladie de Parkinson', 50, 10),
    ('RIVA5', 'Rivastigmine', 'Patch', '4,6 mg', 'Maladie d\'Alzheimer, démence', 35, 7),
    ('DONP10', 'Donépézil', 'Comprimé', '10 mg', 'Maladie d\'Alzheimer légère à modérée', 40, 8),

    # --- Infections pédiatriques courantes ---
    ('AMOX125', 'Amoxicilline sirop', 'Sirop', '125 mg/5 ml', 'Otite, angine, pneumonie enfant', 150, 30),
    ('ZINC10', 'Zinc sirop', 'Sirop', '10 mg/5 ml', 'Diarrhée aiguë enfant, malnutrition', 180, 36),
    ('VITAPED', 'Vitamine A', 'Gélule', '100 000 UI', 'Carence vitamine A, xérophtalmie', 100, 20),
]
