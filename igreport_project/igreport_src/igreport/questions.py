# Questions in various languages
# the keys of dict translations which correspond to languages should be of max length 6
# the spec: http://www.w3.org/International/articles/language-tags/Overview
# reference:http://www.iana.org/assignments/language-subtag-registry
translations = {
    'eng': dict(
        COMPLAINT_QUESTION = 'Expose Corruption toll free service, what is your complaint?',
        ACCUSED_QUESTION = 'Please answer with ONLY the name of the person and Organisation you are reporting?',
        DISTRICT_QUESTION = 'Please send me ONLY the name of the district where the person works?',
        AMOUNT_QUESTION = 'What was involved (if money, how much)?',
        NAME_QUESTION = 'What is your Name?',
        CONFIRMATION_MESSAGE = 'Your complaint has been recorded. Thank you. Your SMS Complaint # is: <NUMBER>. For further queries please call 0414123456'
    ),
    'lug': dict(
        COMPLAINT_QUESTION = 'Loopa obulyaake kubwerere. Olina kwemulugunya ki?',
        ACCUSED_QUESTION = 'Kitongole ki oba muntu ki gw\'oloopa?',
        DISTRICT_QUESTION = 'Oli mu disitulikiti ki?',
        AMOUNT_QUESTION = 'Ssente meka zebakusabye?',
        NAME_QUESTION = 'Amanya go gwe ani?',
        CONFIRMATION_MESSAGE = 'Okwemulugunya kwo tukufunye. Webale nyo.'
    )
}
