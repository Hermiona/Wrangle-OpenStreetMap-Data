import sys, codecs
import street
import postcode
import phone
import website

if __name__ == '__main__':
    data_option = sys.argv[1]
    filename = sys.argv[2]
    UTF8Writer = codecs.getwriter('utf8')
    sys.stdout = UTF8Writer(sys.stdout)
    if data_option == "street":
        streets = street.audit_street(filename)
        for street in streets:
            print(street)
    elif data_option == "postcode":
        postcodes = postcode.audit_postcode(filename)
        for code, count in postcodes.items():
            print(code + " | " + str(count))
    elif data_option == "phone":
        phones = phone.audit_phone(filename)
        for phone in phones:
            print(phone)
    elif data_option == "website":
        websites = website.audit_website(filename)
        for website in websites:
            print(website)
    else:
        print("Incorrect data option. Choose from: street, postcode, phone, website.")
