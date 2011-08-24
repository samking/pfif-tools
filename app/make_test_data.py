#!/usr/bin/env python
# Initial version from From Ka-Ping Yee (kpy@google.com)

# pylint: disable=C0301
"""Makes test PFIF XML files for interoperability tests.

Full details about the test data set is available in the PFIF Conformance Test
Plan:
https://docs.google.com/a/google.com/document/d/1HoCtiKjmp6j2d4d2U9QBJtehuVoANcWc6ggxthacPRY/edit?hl=en_US&authkey=CMaK1qsI"""
# pylint: enable=C0301

import datetime
import personfinder_pfif
import optparse
import utils

COUNTRY_CODES = '''
    zero
    AF AX AL DZ AS AD AO AI AQ AG AR AM AW AU AT AZ BS BH BD BB BY BE BZ BJ BM
    BT BO BQ BA BW BV BR IO BN BG BF BI KH CM CA CV KY CF TD CL CN CX CC CO KM
    CG CD CK CR CI HR CU CW CY CZ DK DJ DM DO EC EG SV GQ ER EE ET FK FO FJ FI
    FR GF PF TF GA GM GE DE GH GI GR GL GD GP GU GT GG GN GW GY HT HM VA HN HK
    HU IS IN ID IR IQ IE IM IL IT JM JP JE JO KZ KE KI KP KR KW KG LA LV LB LS
    LR LY LI LT LU MO MK MG MW MY MV ML MT MH MQ MR MU YT MX FM MD MC MN ME MS
    MA MZ MM NA NR NP NL NC NZ NI NE NG NU NF MP NO OM PK PW PS PA PG PY PE PH
    PN PL PT PR QA RE RO RU RW BL SH KN LC MF PM VC WS SM ST SA SN RS SC SL SG
    SX SK SI SB SO ZA GS ES LK SD SR SJ SZ SE CH SY TW TJ TZ TH TL TG TK TO TT
    TN TR TM TC TV UG UA AE GB US UM UY UZ VU VE VN VG VI WF EH YE ZM ZW
'''.split()

STATE_CODES = '''
    zero
    AE-AJ AE-AZ AE-DU AE-FU AE-RK AE-SH AE-UQ AF-BAL AF-BAM AF-BDG AF-BDS AF-BGL
    AF-FRAU AF-FYB AF-GHA AF-GHO AF-HEL AF-HER AF-JOW AF-KAB AF-KANN AF-KAP
    AF-KDZ AF-KNR AF-LAG AF-LOW AF-NAN AF-NIM AF-ORU AF-PAR AF-PIA AF-PKA AF-SAM
    AF-SAR AF-TAK AF-WAR AF-ZAB AL-BR AL-BU AL-DI AL-DL AL-DR AL-DV AL-EL AL-ER
    AL-FR AL-GJ AL-GR AL-HA AL-KA AL-KB AL-KC AL-KO AL-KR AL-KU AL-LA AL-LB
    AL-LE AL-LU AL-MK AL-MM AL-MR AL-MT AL-PG AL-PQ AL-PR AL-PU AL-SH AL-SK
    AL-SR AL-TE AL-TP AL-TR AL-VL AM-AG AM-AR AM-AV AM-ER AM-GR AM-KT AM-LO
    AM-SH AM-SU AM-TV AM-VD AO-BGO AO-BGU AO-BIE AO-CAB AO-CCU AO-CNN AO-CNO
    AO-CUS AO-HUA AO-HUI AO-LNO AO-LSU AO-LUA AO-MAL AO-MOX AO-NAM AO-UIG AO-ZAI
    AR-A AR-B AR-C AR-D AR-E AR-F AR-G AR-H AR-J AR-K AR-L AR-M AR-N AR-P AR-Q
    AR-R AR-S AR-T AR-U AR-V AR-W AR-X AR-Y AR-Z AT-1 AT-2 AT-3 AT-4 AT-5 AT-6
    AT-7 AT-8 AT-9 AU-CT AU-NS AU-NT AU-QL AU-SA AU-TS AU-VI AU-WA AZ-AB AZ-ABS
    AZ-AGA AZ-AGC AZ-AGM AZ-AGS AZ-AGU AZ-AST AZ-BA AZ-BAB AZ-BAL AZ-BAR AZ-BEY
    AZ-BIL AZ-CAB AZ-CAL AZ-CUL AZ-DAS AZ-DAV AZ-FUZ AZ-GA AZ-GAD AZ-GOR AZ-GOY
    AZ-HAC AZ-IMI AZ-ISM AZ-KAL AZ-KUR AZ-LA AZ-LAC AZ-LAN AZ-LER AZ-MAS AZ-MI
    AZ-MM AZ-NA AZ-NEF AZ-OGU AZ-ORD AZ-QAB AZ-QAX AZ-QAZ AZ-QBA AZ-QBI AZ-QOB
    AZ-QUS AZ-SA AZ-SAB AZ-SAD AZ-SAH AZ-SAK AZ-SAL AZ-SAR AZ-SAT AZ-SIY AZ-SKR
    AZ-SM AZ-SMI AZ-SMX AZ-SS AZ-SUS AZ-TAR AZ-TOV AZ-UCA AZ-XA AZ-XAC AZ-XAN
    AZ-XCI AZ-XIZ AZ-XVD AZ-YAR AZ-YE AZ-YEV AZ-ZAN AZ-ZAQ AZ-ZAR BA-BIH BA-SRP
    BD-01 BD-02 BD-03 BD-04 BD-05 BD-06 BD-07 BD-08 BD-09 BD-1 BD-10 BD-11 BD-12
    BD-13 BD-14 BD-15 BD-16 BD-17 BD-18 BD-19 BD-2 BD-20 BD-21 BD-22 BD-23 BD-24
    BD-25 BD-26 BD-27 BD-28 BD-29 BD-3 BD-30 BD-31 BD-32 BD-33 BD-34 BD-35 BD-36
    BD-37 BD-38 BD-39 BD-4 BD-40 BD-41 BD-42 BD-43 BD-44 BD-45 BD-46 BD-47 BD-48
    BD-49 BD-5 BD-50 BD-51 BD-52 BD-53 BD-54 BD-55 BD-56 BD-57 BD-58 BD-59 BD-6
    BD-60 BD-61 BD-62 BD-63 BD-64 BE-BRU BE-VAN BE-VBR BE-VLG BE-VLI BE-VOV
    BE-VWV BE-WAL BE-WBR BE-WHT BE-WLG BE-WLX BE-WNA BF-BAL BF-BAM BF-BAN BF-BAZ
    BF-BGR BF-BLG BF-BLK BF-COM BF-GAN BF-GNA BF-GOU BF-HOU BF-IOB BF-KAD BF-KEN
    BF-KMD BF-KMP BF-KOP BF-KOS BF-KOT BF-KOW BF-LER BF-LOR BF-MOU BF-NAM BF-NAO
    BF-NAY BF-NOU BF-OUB BF-OUD BF-PAS BF-PON BF-SEN BF-SIS BF-SMT BF-SNG BF-SOM
    BF-SOR BF-TAP BF-TUI BF-YAG BF-YAT BF-ZIR BF-ZON BF-ZOU BG-01 BG-02 BG-03
    BG-04 BG-05 BG-06 BG-07 BG-08 BG-09 BG-10 BG-11 BG-12 BG-13 BG-14 BG-15
    BG-16 BG-17 BG-18 BG-19 BG-20 BG-21 BG-22 BG-23 BG-24 BG-25 BG-26 BG-27
    BG-28 BH-01 BH-02 BH-03 BH-04 BH-05 BH-06 BH-07 BH-08 BH-09 BH-10 BH-11
    BH-12 BI-BB BI-BJ BI-BR BI-CA BI-CI BI-GI BI-KI BI-KR BI-KY BI-MA BI-MU
    BI-MW BI-MY BI-NG BI-RT BI-RY BJ-AK BJ-AL BJ-AQ BJ-BO BJ-CO BJ-DO BJ-KO
    BJ-LI BJ-MO BJ-OU BJ-PL BJ-ZO BN-BE BN-BM BN-TE BN-TU BO-B BO-C BO-H BO-L
    BO-N BO-O BO-P BO-S BO-T BR-AC BR-AL BR-AM BR-AP BR-BA BR-CE BR-DF BR-ES
    BR-GO BR-MA BR-MG BR-MS BR-MT BR-PA BR-PB BR-PE BR-PI BR-PR BR-RJ BR-RN
    BR-RO BR-RR BR-RS BR-SC BR-SE BR-SP BR-TO BS-AC BS-BI BS-CI BS-EX BS-FC
    BS-FP BS-GH BS-GT BS-HI BS-HR BS-IN BS-KB BS-LI BS-MG BS-MH BS-NB BS-NP
    BS-RI BS-RS BS-SP BS-SR BT-11 BT-12 BT-13 BT-14 BT-15 BT-21 BT-22 BT-23
    BT-24 BT-31 BT-32 BT-33 BT-34 BT-41 BT-42 BT-43 BT-44 BT-45 BT-GA BT-TY
    BW-CE BW-CH BW-GH BW-KG BW-KL BW-KW BW-NE BW-NG BW-SE BW-SO BY-BR BY-HO
    BY-HR BY-MA BY-MI BY-VI BZ-BZ BZ-CY BZ-CZL BZ-OW BZ-SC BZ-TOL CA-AB CA-BC
    CA-MB CA-NB CA-NL CA-NS CA-NT CA-NU CA-ON CA-PE CA-QC CA-SK CA-YT CD-BC
    CD-BN CD-EQ CD-KA CD-KE CD-KN CD-KW CD-MA CD-NK CD-OR CD-SK CF-AC CF-BB
    CF-BGF CF-BK CF-HK CF-HM CF-HS CF-KB CF-KG CF-LB CF-MB CF-MP CF-NM CF-OP
    CF-SE CF-UK CF-VK CG-11 CG-12 CG-13 CG-14 CG-15 CG-2 CG-5 CG-7 CG-8 CG-9
    CG-BZV CH-AG CH-AI CH-AR CH-BE CH-BL CH-BS CH-FR CH-GE CH-GL CH-GR CH-JU
    CH-LU CH-NE CH-NW CH-OW CH-SG CH-SH CH-SO CH-SZ CH-TG CH-TI CH-UR CH-VD
    CH-VS CH-ZG CH-ZH CI-01 CI-02 CI-03 CI-04 CI-05 CI-06 CI-07 CI-08 CI-09
    CI-10 CI-11 CI-12 CI-13 CI-14 CI-15 CI-16 CL-AI CL-AN CL-AR CL-AT CL-BI
    CL-CO CL-LI CL-LL CL-MA CL-ML CL-RM CL-TA CL-VS CM-AD CM-CE CM-EN CM-ES
    CM-LT CM-NO CM-NW CM-OU CM-SU CM-SW CN-11 CN-12 CN-13 CN-14 CN-15 CN-21
    CN-22 CN-23 CN-31 CN-32 CN-33 CN-34 CN-35 CN-36 CN-37 CN-41 CN-42 CN-43
    CN-44 CN-45 CN-46 CN-50 CN-51 CN-52 CN-53 CN-54 CN-61 CN-62 CN-63 CN-64
    CN-65 CN-71 CN-91 CN-92 CO-AMA CO-ANT CO-ARA CO-ATL CO-BOL CO-BOY CO-CAL
    CO-CAQ CO-CAS CO-CAU CO-CES CO-CHO CO-COR CO-CUN CO-DC CO-GUA CO-GUV CO-HUI
    CO-LAG CO-MAG CO-MET CO-NAR CO-NSA CO-PUT CO-QUI CO-RIS CO-SAN CO-SAP CO-SUC
    CO-TOL CO-VAC CO-VAU CO-VID CR-A CR-C CR-G CR-H CR-L CR-P CR-SJ CU-01 CU-02
    CU-03 CU-04 CU-05 CU-06 CU-07 CU-08 CU-09 CU-10 CU-11 CU-12 CU-13 CU-14
    CU-99 CV-B CV-BR CV-BV CV-CA CV-CR CV-CS CV-FO CV-MA CV-MO CV-PA CV-PN CV-PR
    CV-RG CV-S CV-SF CV-SL CV-SN CV-SV CV-TA CY-01 CY-02 CY-03 CY-04 CY-05 CY-06
    CZ-JC CZ-JM CZ-KA CZ-KR CZ-LI CZ-MO CZ-OL CZ-PA CZ-PL CZ-PR CZ-ST CZ-US
    CZ-VY CZ-ZL DE-BB DE-BE DE-BW DE-BY DE-HB DE-HE DE-HH DE-MV DE-NI DE-NW
    DE-RP DE-SH DE-SL DE-SN DE-ST DE-TH DJ-AS DJ-DI DJ-DJ DJ-OB DJ-TA DK-015
    DK-020 DK-025 DK-030 DK-035 DK-040 DK-042 DK-050 DK-055 DK-060 DK-065 DK-070
    DK-076 DK-080 DK-101 DK-147 DO-01 DO-02 DO-03 DO-04 DO-05 DO-06 DO-07 DO-08
    DO-09 DO-10 DO-11 DO-12 DO-13 DO-14 DO-15 DO-16 DO-17 DO-18 DO-19 DO-20
    DO-21 DO-22 DO-23 DO-24 DO-25 DO-26 DO-27 DO-28 DO-29 DO-30 DZ-01 DZ-02
    DZ-03 DZ-04 DZ-05 DZ-06 DZ-07 DZ-08 DZ-09 DZ-10 DZ-11 DZ-12 DZ-13 DZ-14
    DZ-15 DZ-16 DZ-17 DZ-18 DZ-19 DZ-20 DZ-21 DZ-22 DZ-23 DZ-24 DZ-25 DZ-26
    DZ-27 DZ-28 DZ-29 DZ-30 DZ-31 DZ-32 DZ-33 DZ-34 DZ-35 DZ-36 DZ-37 DZ-38
    DZ-39 DZ-40 DZ-41 DZ-42 DZ-43 DZ-44 DZ-45 DZ-46 DZ-47 DZ-48 EC-A EC-B EC-C
    EC-D EC-E EC-F EC-G EC-H EC-I EC-L EC-M EC-N EC-O EC-P EC-R EC-S EC-T EC-U
    EC-W EC-X EC-Y EC-Z EE-37 EE-39 EE-44 EE-49 EE-51 EE-57 EE-59 EE-65 EE-67
    EE-70 EE-74 EE-78 EE-82 EE-84 EE-86 EG-ALX EG-ASN EG-AST EG-BA EG-BH EG-BNS
    EG-C EG-DK EG-DT EG-FYM EG-GH EG-GZ EG-IS EG-JS EG-KB EG-KFS EG-KN EG-MN
    EG-MNF EG-MT EG-PTS EG-SHG EG-SHR EG-SIN EG-SUZ EG-WAD ER-AN ER-DK ER-DU
    ER-GB ER-MA ER-SK ES-A ES-AB ES-AL ES-AN ES-AR ES-AV ES-B ES-BA ES-BI ES-BU
    ES-C ES-CA ES-CC ES-CE ES-CL ES-CM ES-CN ES-CO ES-CR ES-CS ES-CT ES-CU ES-EX
    ES-GA ES-GC ES-GI ES-GR ES-GU ES-H ES-HU ES-J ES-L ES-LE ES-LO ES-LU ES-M
    ES-MA ES-ML ES-MU ES-NA ES-O ES-OR ES-P ES-PM ES-PO ES-PV ES-S ES-SA ES-SE
    ES-SG ES-SO ES-SS ES-T ES-TE ES-TF ES-TO ES-V ES-VA ES-VC ES-VI ES-Z ES-ZA
    ET-AA ET-AF ET-AM ET-BE ET-DD ET-GA ET-HA ET-OR ET-SN ET-SO ET-TI FI-AL
    FI-ES FI-IS FI-LL FI-LS FI-OL FJ-C FJ-E FJ-N FJ-R FJ-W FM-KSA FM-PNI FM-TRK
    FM-YAP FR-01 FR-02 FR-03 FR-04 FR-05 FR-06 FR-07 FR-08 FR-09 FR-10 FR-11
    FR-12 FR-13 FR-14 FR-15 FR-16 FR-17 FR-18 FR-19 FR-21 FR-22 FR-23 FR-24
    FR-25 FR-26 FR-27 FR-28 FR-29 FR-2A FR-2B FR-30 FR-31 FR-32 FR-33 FR-34
    FR-35 FR-36 FR-37 FR-38 FR-39 FR-40 FR-41 FR-42 FR-43 FR-44 FR-45 FR-46
    FR-47 FR-48 FR-49 FR-50 FR-51 FR-52 FR-53 FR-54 FR-55 FR-56 FR-57 FR-58
    FR-59 FR-60 FR-61 FR-62 FR-63 FR-64 FR-65 FR-66 FR-67 FR-68 FR-69 FR-70
    FR-71 FR-72 FR-73 FR-74 FR-75 FR-76 FR-77 FR-78 FR-79 FR-80 FR-81 FR-82
    FR-83 FR-84 FR-85 FR-86 FR-87 FR-88 FR-89 FR-90 FR-91 FR-92 FR-93 FR-94
    FR-95 FR-A FR-B FR-C FR-D FR-E FR-F FR-G FR-GF FR-GP FR-H FR-I FR-J FR-K
    FR-L FR-M FR-MQ FR-N FR-NC FR-O FR-P FR-PF FR-PM FR-Q FR-R FR-RE FR-S FR-T
    FR-TF FR-U FR-V FR-WF FR-YT GA-1 GA-2 GA-3 GA-4 GA-5 GA-6 GA-7 GA-8 GA-9
    GB-ABD GB-ABE GB-AGB GB-AGY GB-ANS GB-ANT GB-ARD GB-ARM GB-BAS GB-BBD GB-BDF
    GB-BDG GB-BEN GB-BEX GB-BFS GB-BGE GB-BGW GB-BIR GB-BKM GB-BLA GB-BLY GB-BMH
    GB-BNB GB-BNE GB-BNH GB-BNS GB-BOL GB-BPL GB-BRC GB-BRD GB-BRY GB-BST GB-BUR
    GB-CAM GB-CAY GB-CGN GB-CGV GB-CHA GB-CHS GB-CKF GB-CKT GB-CLD GB-CLK GB-CLR
    GB-CMA GB-CMD GB-CMN GB-CON GB-COV GB-CRF GB-CRY GB-CSR GB-CWY GB-DAL GB-DBY
    GB-DEN GB-DER GB-DEV GB-DGN GB-DGY GB-DNC GB-DND GB-DOR GB-DOW GB-DRY GB-DUD
    GB-DUR GB-EAL GB-EAW GB-EAY GB-EDH GB-EDU GB-ELN GB-ELS GB-ENF GB-ENG GB-ERW
    GB-ERY GB-ESS GB-ESX GB-FAL GB-FER GB-FIF GB-FLN GB-GAT GB-GBN GB-GLG GB-GLS
    GB-GRE GB-GSY GB-GWN GB-HAL GB-HAM GB-HAV GB-HCK GB-HEF GB-HIL GB-HLD GB-HMF
    GB-HNS GB-HPL GB-HRT GB-HRW GB-HRY GB-IOM GB-IOS GB-IOW GB-ISL GB-IVC GB-JSY
    GB-KEC GB-KEN GB-KHL GB-KIR GB-KTT GB-KWL GB-LAN GB-LBH GB-LCE GB-LDS GB-LEC
    GB-LEW GB-LIN GB-LIV GB-LMV GB-LND GB-LRN GB-LSB GB-LUT GB-MAN GB-MDB GB-MDW
    GB-MFT GB-MIK GB-MLN GB-MON GB-MRT GB-MRY GB-MTY GB-MYL GB-NAY GB-NBL GB-NDN
    GB-NEL GB-NET GB-NFK GB-NGM GB-NIR GB-NLK GB-NLN GB-NSM GB-NTA GB-NTH GB-NTL
    GB-NTT GB-NTY GB-NWM GB-NWP GB-NYK GB-NYM GB-OLD GB-OMH GB-ORK GB-OXF GB-PEM
    GB-PKN GB-PLY GB-POL GB-POR GB-POW GB-PTE GB-RCC GB-RCH GB-RCT GB-RDB GB-RDG
    GB-RFW GB-RIC GB-ROT GB-RUT GB-SAW
'''.split()

SOURCE_DATE = datetime.datetime(2011, 1, 1, 1, 1, 1)
ENTRY_START = datetime.datetime(2011, 2, 3, 4, 5, 6)
PERSON_INTERVAL = datetime.timedelta(0, 60*60)  # 60 minutes between persons
NOTE_INTERVAL = datetime.timedelta(0, 30*60)  # 30 minutes between notes
EXPIRY_START = datetime.datetime(2011, 4, 1, 0, 0, 0)
EXPIRY_INTERVAL = datetime.timedelta(0, 30*60)
FIRST_PERSON_WITH_NOTES = 1
LAST_PERSON_WITH_NOTES = 99
FIRST_PERSON = 1
LAST_PERSON = 1357
FIRST_NOTE = 1
LAST_NOTE_PLACEHOLDER = 0
PERSON_RECORD_ID_BASE = 'example.org/p'
NOTE_RECORD_ID_BASE = 'example.org/n'

def make_person_id(person_num):
  """Turns the specified person_num into a person_record_id in the format
  example.org/p####."""
  return PERSON_RECORD_ID_BASE + '%04d' % person_num

def make_note_id(person_num, note_num):
  """Turns the specified person_num and note_num into a note_record_id in the
  format example.org/nPPNN."""
  return NOTE_RECORD_ID_BASE + '%02d%02d' % (person_num, note_num)

def get_persons_after_record(persons, notes, record):
  """Returns persons with all elements before and including record removed.
  Also, if a removed person had any notes, removes that from notes and returns
  an updated notes map.  Each person in persons should be a map from field name
  to field value.  notes should be in the format used by
  get_notes_after_record."""
  last_excluded_person_num = int(record[-4:])

  recent_persons = [
      person for person in persons if int(person['person_record_id'][-4:]) >
      last_excluded_person_num]

  # Remove all excluded notes
  if last_excluded_person_num >= LAST_PERSON_WITH_NOTES:
    recent_notes = {}
  else:
    note_id = make_note_id(last_excluded_person_num, last_excluded_person_num)
    recent_notes = get_notes_after_record(notes, note_id)

  return recent_persons, recent_notes

def get_notes_after_record(notes, record):
  """Returns notes with all elements before and including record removed.
  notes is a map from person_record_id to a list of notes.  record is a string
  of the last record_id to reject (for instance, if record is
  example.org/n1201, then this method will return records starting with
  n1202).  notes should be a map from person_record_id to a list of notes
  associated with that person_record_id."""
  last_excluded_note_num = int(record[-2:])
  last_excluded_person_num = int(record[-4:-2])
  first_person_with_notes = last_excluded_person_num
  is_partially_included_person = (last_excluded_note_num !=
                                  last_excluded_person_num)

  # If we delete the last note in a person, delete that person too.
  if not is_partially_included_person:
    first_person_with_notes = last_excluded_person_num + 1

  recent_notes = notes.copy()

  # Delete all notes in persons before the person containing record
  for excluded_person_num in range(1, first_person_with_notes):
    excluded_person_id = make_person_id(excluded_person_num)
    if excluded_person_id in recent_notes:
      del recent_notes[excluded_person_id]

  # 'Delete' (by reassigning) all notes up to and including record in the
  # person containing record (unless the whole person has no notes and is
  # already deleted).  Makes no assumptions about sortedness of the note array
  # or about what the first or last record it includes is.
  if is_partially_included_person:
    partially_included_person = make_person_id(first_person_with_notes)
    recent_notes[partially_included_person] = [
        note for note in recent_notes[partially_included_person] if
        int(note['note_record_id'][-2:]) > last_excluded_note_num]

  return recent_notes

def delete_omitted_fields(record, omitted_fields):
  """Removes every field in omitted_fields from record."""
  for field in omitted_fields:
    if field in record:
      del record[field]

def generate_persons(version=None, omitted_fields=(), # pylint: disable=R0912
                     first_person=FIRST_PERSON, last_person=LAST_PERSON):
  """Returns a list of (last_person - first_person + 1) persons generated per
  the conformance test plan."""
  if version == None:
    version = personfinder_pfif.PFIF_VERSIONS['1.3']
  fields = version.fields['person']

  persons = []
  for person_id_num in range(first_person, last_person + 1):
    person_id_four_digit = '%04d' % person_id_num
    person = dict((field, field + person_id_four_digit) for field in fields)
    person['person_record_id'] = make_person_id(person_id_num)
    entry_date = ENTRY_START + PERSON_INTERVAL * (person_id_num - 1)
    person['entry_date'] = personfinder_pfif.format_utc_datetime(entry_date)
    person['source_date'] = personfinder_pfif.format_utc_datetime(SOURCE_DATE)
    if 'expiry_date' in fields:
      if person_id_num < 1000:
        # Generate the expiry_date directly rather than incrementing it as we go
        # so that it will work even if we only generate a few persons in the
        # middle.
        expiry_date = EXPIRY_START + EXPIRY_INTERVAL * (person_id_num - 1)
        person['expiry_date'] = (
            personfinder_pfif.format_utc_datetime(expiry_date))
      else:
        del person['expiry_date']
    person['author_email'] = person_id_four_digit + '@example.com'
    person['author_phone'] = '0000' + person_id_four_digit
    person['source_url'] = 'http://example.org/' + person_id_four_digit
    person['other'] = 'description: ' + person_id_four_digit
    person['home_country'] = COUNTRY_CODES[(person_id_num % 248) or 248]
    person['home_state'] = STATE_CODES[person_id_num]
    person['photo_url'] = 'http://photo.example.org/' + person_id_four_digit
    person['home_postal_code'] = '0' + person_id_four_digit

    # sex
    person['sex'] = personfinder_pfif.PERSON_SEX_VALUES[person_id_num % 4]
    if person_id_num % 4 == 0:
      del person['sex']

    # date_of_birth
    if person_id_num < 98:
      del person['date_of_birth']
    elif person_id_num == 98:
      person['date_of_birth'] = '1900'
    elif person_id_num == 99:
      person['date_of_birth'] = '1900-01'
    else:
      dob = datetime.date(1900, 1, 1) + person_id_num*datetime.timedelta(30)
      person['date_of_birth'] = dob.strftime('%Y-%m-%d')

    # age
    if person_id_num == 1:
      person['age'] = '34-56'
    elif person_id_num < 98:
      person['age'] = str(person_id_num)
    elif person_id_num in [98, 99]:
      person['age'] = '111'
    else:
      del person['age']

    delete_omitted_fields(person, omitted_fields)

    persons.append(person)

  return persons

def get_absolute_note_num(person_num, note_num):
  """Note 0201 (person_num=2, note_num=1) is the second absolute note (0101 was
  first).  This function converts a person_num and note_num to the absolute
  number of the note."""
  return sum(range(person_num)) + note_num

def generate_notes(version=None, omitted_fields=(), # pylint: disable=R0914
                   first_person_with_notes=FIRST_PERSON_WITH_NOTES,
                   last_person_with_notes=LAST_PERSON_WITH_NOTES,
                   first_note=FIRST_NOTE,
                   last_note=LAST_NOTE_PLACEHOLDER):
  """Generates a map from person_record_id to a list of that person's notes.
  Each note is generated per the test conformance plan."""
  if version == None:
    version = personfinder_pfif.PFIF_VERSIONS['1.3']
  note_fields = version.fields['note']
  notes = {}
  for person_id_num in range(first_person_with_notes, last_person_with_notes +
                             1):
    person_id_two_digit = '%02d' % person_id_num
    person_record_id = make_person_id(person_id_num)
    notes[person_record_id] = []

    # for unit testing, we may want a specific note
    if last_note == LAST_NOTE_PLACEHOLDER:
      current_last_note = person_id_num
    else:
      current_last_note = min(last_note, person_id_num)

    for note_id in range(first_note, current_last_note + 1):
      note_id_two_digit = '%02d' % note_id
      note = dict((field, field + person_id_two_digit + note_id_two_digit) for
                  field in note_fields)
      note['note_record_id'] = make_note_id(person_id_num, note_id)
      note['person_record_id'] = person_record_id
      entry_date = (ENTRY_START + NOTE_INTERVAL *
                    (get_absolute_note_num(person_id_num, note_id) - 1))
      note['entry_date'] = personfinder_pfif.format_utc_datetime(entry_date)
      note['source_date'] = personfinder_pfif.format_utc_datetime(SOURCE_DATE)
      note['author_email'] = (person_id_two_digit + note_id_two_digit +
                              '@example.com')
      note['author_phone'] = '0000' + person_id_two_digit + note_id_two_digit
      note['found'] = ((person_id_num + note_id) % 2) and 'true' or 'false'
      if note['found'] == 'true':
        note['email_of_found_person'] = note['author_email']
        note['phone_of_found_person'] = note['author_phone']
      else:
        del note['email_of_found_person']
        del note['phone_of_found_person']
      note['status'] = personfinder_pfif.NOTE_STATUS_VALUES[note_id % 6]

      # linked_person_record_id
      if person_id_num > 1 and note_id == 1:
        if person_id_num % 2:
          linked_person_record_id = make_person_id(person_id_num - 1)
        else:
          linked_person_record_id = make_person_id(person_id_num + 1)
        note['linked_person_record_id'] = linked_person_record_id
      else:
        del note['linked_person_record_id']

      delete_omitted_fields(note, omitted_fields)

      notes[person_record_id].append(note)

  return notes

def make_test_data(output_file, version=None, omitted_fields=(),
                   first_person=FIRST_PERSON, last_person=LAST_PERSON,
                   first_person_with_notes=FIRST_PERSON_WITH_NOTES,
                   last_person_with_notes=LAST_PERSON_WITH_NOTES,
                   first_note=FIRST_NOTE, last_note=LAST_NOTE_PLACEHOLDER,
                   embed_notes_in_persons=True):
  """Generates a test data file as per the provided version (from
  personfinder_pfif) and writes it to output_file."""
  persons = generate_persons(version, omitted_fields, first_person, last_person)
  notes = generate_notes(version, omitted_fields, first_person_with_notes,
                         last_person_with_notes, first_note, last_note)
  write_records(version, output_file, persons, notes,
                embed_notes_in_persons=embed_notes_in_persons)

def write_records(version, output_file, persons, notes,
                  embed_notes_in_persons=True):
  """Writes all persons and notes to output_file.  Wrapper for
  version.write_file if embed_notes_in_persons."""
  if embed_notes_in_persons:
    def get_notes_for_person(person):
      """Gets all notes associated with person."""
      return notes.get(person['person_record_id'], [])
    version.write_file(output_file, persons, get_notes_for_person)
  # Doing this work manually is necessary because version.write_file will never
  # emit a note that is not contained inside of a person.
  else:
    output_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output_file.write('<pfif:pfif xmlns:pfif="%s">\n' % version.ns)
    for person in persons:
      version.write_person(output_file, person, indent='  ')
    for _, notes_arr in notes.items():
      for note in notes_arr:
        version.write_note(output_file, note, indent='  ')
    output_file.write('</pfif:pfif>\n')

def main():
  """Creates test data and outputs it to a file."""
  parser = optparse.OptionParser()
  parser.add_option('--pfif-version', default='1.3',
                    help='Specify the PFIF version.  Defaults to 1.3.  '
                    'Currently supported: 1.2, 1.3.')
  parser.add_option('--omit-field', action='append', default=[],
                    dest='omitted_fields',
                    help='If your repository has issues with one field that '
                    'prevents you from running all of the tests, you can omit '
                    'that field here.  For instance, if your repo tries to '
                    'load photos specified by photo_url rather than just '
                    'storing the link, the repo will timeout on every record, '
                    'so you should pass --omit-field photo_url.  To omit '
                    'multiple fields, pass this argument multiple times.  This '
                    'will not omit mandatory fields.')
  parser.add_option('--output-file', default=None,
                    help='Output will be written to this file.  Defaults to '
                    'pfif-VERSION-test.xml')
  group = optparse.OptionGroup(
      parser, 'Unit Testing Options',
      'These options are used for unit testing different record IDs. The '
      'default values for these options are what is specified in the Test '
      'Conformance document, and changing them could generate insufficient '
      'data to correctly test conformance.  You should not set these options.')
  group.add_option('--first-person', default=FIRST_PERSON)
  group.add_option('--last-person', default=LAST_PERSON)
  group.add_option('--first-person-with-notes', default=FIRST_PERSON_WITH_NOTES)
  group.add_option('--last-person-with-notes', default=LAST_PERSON_WITH_NOTES)
  group.add_option('--first-note', default=FIRST_NOTE)
  group.add_option('--last-note', default=LAST_NOTE_PLACEHOLDER)
  group.add_option('--all-notes-are-top-level', dest='embed_notes_in_persons',
                   action='store_false', default=True)
  parser.add_option_group(group)

  (options, args) = parser.parse_args() # pylint: disable=W0612
  if options.output_file is None:
    options.output_file = 'pfif-' + options.pfif_version + '-test.xml'
  assert options.pfif_version in ['1.2', '1.3'], ('Only versions 1.2 and 1.3 '
                                                  'are supported.')

  output_file = utils.open_file(options.output_file, 'w')
  version_map = personfinder_pfif.PFIF_VERSIONS[options.pfif_version]

  make_test_data(output_file, version=version_map,
                 omitted_fields=options.omitted_fields,
                 first_person=int(options.first_person),
                 last_person=int(options.last_person),
                 first_person_with_notes=int(options.first_person_with_notes),
                 last_person_with_notes=int(options.last_person_with_notes),
                 first_note=int(options.first_note),
                 last_note=int(options.last_note),
                 embed_notes_in_persons=options.embed_notes_in_persons)
  output_file.close()

if __name__ == '__main__':
  main()
