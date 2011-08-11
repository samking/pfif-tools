#!/usr/bin/env python
# Initial version from From Ka-Ping Yee (kpy@google.com)

import datetime
import pfif

persons = []
notes = []

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

def make_test_data(version, file):
    SOURCE_DATE = datetime.datetime(2011, 1, 1, 1, 1, 1)
    ENTRY_START = datetime.datetime(2011, 2, 3, 4, 5, 6)
    PERSON_INTERVAL = datetime.timedelta(0, 60*60)  # 60 minutes between persons
    NOTE_INTERVAL = datetime.timedelta(0, 30*60)  # 30 minutes between notes
    EXPIRY_START = datetime.datetime(2011, 4, 1, 0, 0, 0)
    EXPIRY_INTERVAL = datetime.timedelta(0, 30*60)

    fields = version.fields['person']
    note_fields = version.fields['note']
    persons = []
    entry_date = ENTRY_START
    expiry_date = EXPIRY_START
    for p in range(1, 1358):
        P = '%04d' % p
        person = dict((field, field + P) for field in fields)
        person['person_record_id'] = 'example.org/p' + P
        person['entry_date'] = pfif.format_utc_datetime(entry_date)
        entry_date += PERSON_INTERVAL
        person['source_date'] = pfif.format_utc_datetime(SOURCE_DATE)
        if 'expiry_date' in fields:
            if p < 1000:
                person['expiry_date'] = pfif.format_utc_datetime(expiry_date)
            else:
                del person['expiry_date']
        expiry_date += EXPIRY_INTERVAL
        person['author_email'] = P + '@example.com'
        person['author_phone'] = '0000' + P
        person['source_url'] = 'http://example.org/' + P
        person['other'] = 'description: ' + P
        person['home_country'] = COUNTRY_CODES[(p % 248) or 248]

        # sex
        person['sex'] = pfif.PERSON_SEX_VALUES[p % 4]
        if p % 4 == 0:
            del person['sex']

        # date_of_birth
        if p < 90:
            del person['date_of_birth']
        elif p == 98:
            person['date_of_birth'] = '1900'
        elif p == 99:
            person['date_of_birth'] = '1900-01'
        else:
            dob = datetime.date(1900, 1, 1) + p*datetime.timedelta(30)
            person['date_of_birth'] = dob.strftime('%Y-%m-%d')

        # age
        if p == 1:
            person['age'] = '34-56'
        elif p < 98:
            person['age'] = str(p)
        elif p in [98, 99]:
            person['age'] = '111'
        else:
            del person['age']

        persons.append(person)

    notes = {}
    entry_date = ENTRY_START
    for p in range(1, 100):
        P = '%02d' % p
        person_record_id = 'example.org/p00' + P
        notes[person_record_id] = []

        for n in range(1, p + 1):
            N = '%02d' % n
            note = dict((field, field + P + N) for field in note_fields)
            note['note_record_id'] = 'example.org/n' + P + N
            note['person_record_id'] = person_record_id
            note['entry_date'] = pfif.format_utc_datetime(entry_date)
            entry_date += NOTE_INTERVAL
            note['source_date'] = pfif.format_utc_datetime(SOURCE_DATE)
            note['author_email'] = P + N + '@example.com'
            note['author_phone'] = '0000' + P + N
            note['found'] = ((p + n) % 2) and 'true' or 'false'
            if note['found']:
                note['email_of_found_person'] = note['author_email']
                note['phone_of_found_person'] = note['author_phone']
            else:
                del note['email_of_found_person']
                del note['phone_of_found_person']
            note['status'] = pfif.NOTE_STATUS_VALUES[n % 6]

            notes[person_record_id].append(note)

    def get_notes_for_person(person):
        return notes.get(person['person_record_id'], [])

    version.write_file(file, persons, get_notes_for_person)

file = open('pfif-1.2-test.xml', 'w')
make_test_data(pfif.PFIF_1_2, file)
file.close()

file = open('pfif-1.3-test.xml', 'w')
make_test_data(pfif.PFIF_1_3, file)
file.close()
