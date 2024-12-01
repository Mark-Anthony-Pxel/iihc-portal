from django.conf import settings

def default_context(request):
    return {
        'description': (
            '🌟 Start Your Academic Journey at IIH College! 🌟\n\n'
            'Are you a Grade 10 student from a public school graduating in 2024? '
            'IIH College is here to support your transition to Senior High School with an incredible opportunity: '
            'enroll with ZERO PAYMENT through the DepEd SHS Voucher Program!\n\n'
            'Here’s what you can look forward to when you enroll with us:\n\n'
            '✅ No Entrance Exam Required\n'
            '✅ No Maintaining Grade Requirement\n'
            '✅ No Registration Fees\n'
            '✅ No Examination Fees\n'
            '✅ No Monthly Tuition Fees\n'
            '✅ No Hidden Charges\n\n'
            'Plus, enjoy these fantastic FREE items:\n'
            '🎽 FREE Daily Uniform (1 set)\n'
            '🎽 FREE PE Uniform (1 set)\n'
            '📛 FREE Student ID & Lace\n\n'
            'Whether you prefer Face-to-Face or Full Modular Learning, we have you covered!\n\n'
            "Seize this opportunity to embark on your path to academic success. ENROLL NOW!"
        ),
        'keywords': (
            'New Student Enrollment, Senior High School, Zero Payment Education, '
            'DepEd SHS Voucher Program, Free School Uniforms, IIH College Enrollment, Enroll Now'
        ),
        'og_description': (
            'Enroll at IIH College for Senior High School with ZERO PAYMENT for Grade 10 public school graduates in 2024! '
            'Enjoy a seamless enrollment experience with no entrance exams and no fees.'
        ),
        'canonical_url': 'https://www.yourwebsite.com/college-portal',
        'page_description': (
            'IIH College offers senior high school enrollment with zero payment for grade 10 public school graduates in 2024.'
        ),
        'page_url': 'https://www.yourwebsite.com/college-portal',
        'year': '2024',
        'school': 'Integrated Innovation and Hospitality Colleges',
        'location': 'Blk 4 Lot 6 La Forteza Subdivision Camarin Brgy. 175 District 1, Caloocan, Philippines',
        'number': '0967 892 9232',
        'email': 'iihclaforteza@gmail.com',
    }
    
