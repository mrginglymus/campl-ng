__all__ = ('QUICKLINKS', 'STUDY_DRAWER', 'ABOUT_DRAWER')

QUICKLINKS = (
  ("http://www.cam.ac.uk/for-staff", "For staff"),
  ("http://www.admin.cam.ac.uk/students/gateway", "For current students"),
  ("http://www.alumni.cam.ac.uk/", "For alumni"),
  ("http://www.cam.ac.uk/for-business", "For business"),
  ("http://www.cam.ac.uk/colleges-and-departments", "Colleges & departments"),
  ("http://www.cam.ac.uk/libraries-and-facilities", "Libraries & facilities"),
  ("http://www.cam.ac.uk/museums-and-collections", "Museums & collections"),
  ("http://www.cam.ac.uk/email-and-phone-search", "Email & phone search"),
)

STUDY_DRAWER = {
  'title': ('Study at Cambridge', 'http://www.cam.ac.uk/study-at-cambridge'),
  'links': [
    [
      ('Undergraduate', 'http://www.undergraduate.study.cam.ac.uk', [
        ('Courses', 'http://www.undergraduate.study.cam.ac.uk/courses'),
        ('Applying', 'http://www.undergraduate.study.cam.ac.uk/applying'),
        ('Events and open days', 'http://www.undergraduate.study.cam.ac.uk/events/cambridge-open-days'),
        ('Fees and finance', 'http://www.undergraduate.study.cam.ac.uk/finance'),
        ('Student blogs and videos', 'http://www.becambridge.com'),
      ]),
    ],
    [
      ('Graduate', 'http://www.graduate.study.cam.ac.uk', [
        ('Why Cambridge', 'http://www.graduate.study.cam.ac.uk/why-cambridge/welcome-vice-chancellor'),
        ('Course directory', 'http://www.graduate.study.cam.ac.uk/courses'),
        ('How to apply', 'http://www.graduate.study.cam.ac.uk/how-do-i-apply'),
        ('Fees and funding', 'http://www.admin.cam.ac.uk/students/studentregistry/fees'),
        ('Frequently asked questions', 'http://www.graduate.study.cam.ac.uk/faqs/applicant'),
      ]),
    ],
    [
      ('International Students', 'http://www.internationalstudents.cam.ac.uk', []),
      ('Continuing education', 'http://www.ice.cam.ac.uk', []),
      ('Executive and professional education', 'http://www.epe.admin.cam.ac.uk', []),
      ('Courses in education', 'http://www.epe.admin.cam.ac.uk', []),
    ],
  ],
}

ABOUT_DRAWER = {
  'title': ('About the University', 'http://www.cam.ac.uk/about-the-university'),
  'links': [
    [
      ('How the University and Colleges work', 'http://www.cam.ac.uk/about-the-university/how-the-university-and-colleges-work', []),
      ('History', 'http://www.cam.ac.uk/about-the-university/history', []),
      ('Visiting the University', 'http://www.cam.ac.uk/about-the-university/visiting-the-university', []),
      ('Term dates and calendars', 'http://www.cam.ac.uk/about-the-university/term-dates-and-calendars', []),
      ('Map', 'http://map.cam.ac.uk', []),
    ],
    [
      ('Media relations', 'http://www.cam.ac.uk/media-relations', []),
      ('Video and audio', 'http://www.cam.ac.uk/video-and-audio', []),
      ('Find an expert', 'http://webservices.admin.cam.ac.uk/fae/', []),
      ('Publications', 'http://www.cam.ac.uk/about-the-university/publications', []),
      ('Global Cambridge', 'http://www.cam.ac.uk/global-cambridge', []),
    ],
    [
      ('News', 'http://www.cam.ac.uk/news', []),
      ('Events', 'http://www.admin.cam.ac.uk/whatson', []),
      ('Public engagement', 'http://www.cam.ac.uk/public-engagement', []),
      ('Jobs', 'http://www.jobs.cam.ac.uk', []),
      ('Give to Cambridge', 'https://www.philanthropy.cam.ac.uk', []),
    ],
  ],
}