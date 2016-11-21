import sys, codecs
import street
import postcode
import phone
import website

if __name__ == '__main__':
    audit_option = sys.argv[1]
    audit_filename = sys.argv[2]
    UTF8Writer = codecs.getwriter('utf8')
    sys.stdout = UTF8Writer(sys.stdout)
    if audit_option == "street":
        street_types = street.audit_street(audit_filename)
        for street_type in street_types.keys():
            print(street_type)
            for street_name in street_types[street_type]:
                print("\t" + street_name)
    elif audit_option == "postcode":
        post_codes = postcode.audit_postcode(audit_filename)
        for code, count in post_codes.items():
            print(code + " | " + str(count))
    elif audit_option == "phone":
        phones = phone.audit_phone(audit_filename)
        for phone in phones:
            print(phone)
    elif audit_option == "website":
        websites = website.audit_website(audit_filename)
        for website in websites:
            print(website)
    else:
        print "Incorrect audit option. Choose from: street, postcode, phone, website."
