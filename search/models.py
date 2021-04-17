from django.core.validators import RegexValidator, EmailValidator
from django.db import models
from django.contrib.postgres.fields import JSONField, IntegerRangeField


class Address(models.Model):
    city = models.CharField(max_length=100)
    postcode = models.CharField(
        max_length=6, validators=[RegexValidator(regex="^\\d\\d-\\d\\d\\d$")]
    )
    district = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    building_nr = models.CharField(max_length=20)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)

    def __str__(self):
        return ",".join([self.city, self.district, self.street, self.building_nr])


class ContactData(models.Model):
    website = models.CharField(max_length=100, blank=True, default="")
    phone = models.CharField(max_length=20, blank=True, default="")
    email = models.CharField(EmailValidator(), max_length=100, blank=True, default="")

    def __str__(self):
        return ",".join([self.website, self.phone, self.email])


class PublicInstitutionData(models.Model):
    """
    Institution (pl. placówka) – a bigger entity which school is a part of eg. "Zespół Szkół Zawodowych..."
    """

    institution_name = models.CharField(max_length=200, blank=True)
    institution_short_name = models.CharField(max_length=20, blank=True)
    institution_type = models.CharField(max_length=100, blank=True)
    institution_nr = models.CharField(max_length=20, blank=True)
    institution_RSPO = models.CharField(max_length=20, blank=True)
    institution_regon = models.CharField(max_length=14, blank=True)
    short_name = models.CharField(max_length=20, blank=True)
    RSPO = models.CharField(max_length=20, blank=True)
    regon = models.CharField(max_length=14, blank=True)
    data = JSONField(default=dict)

    def __str__(self):
        return self.institution_name


class PrivateInstitutionData(models.Model):
    registration_nr = models.CharField(max_length=20)


class SchoolType(models.TextChoices):
    LO = "liceum ogólnokształcące"
    TECH = "technikum"
    BRAN = "szkoła branżowa I stopnia"
    SPEC = "szkoła specjalna przysposabiająca do pracy"
    PRZED = "przedszkole"
    SP = "szkoła podstawowa"
    SPART = "szkoła podstawowa artystyczna"
    POLIC = "szkoła policealna"


class School(models.Model):
    school_name = models.CharField(max_length=200)
    # eg. "Batory", "Poniatówka"
    nickname = models.CharField(max_length=50, blank=True, default="")
    school_type = models.CharField(max_length=100, choices=SchoolType.choices)
    student_type = models.CharField(max_length=100, blank=True)
    is_special_needs_school = models.BooleanField(default=False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    contact = models.ForeignKey(ContactData, on_delete=models.CASCADE, null=True)
    is_public = models.BooleanField()
    public_institution_data = models.ForeignKey(
        PublicInstitutionData, on_delete=models.SET_NULL, null=True
    )
    private_institution_data = models.ForeignKey(
        PrivateInstitutionData, on_delete=models.SET_NULL, null=True
    )
    data = JSONField(default=dict)

    def __str__(self):
        return self.school_name


class HighSchoolClass(models.Model):
    # O - ogólnokształcące, MS - mistrzostwa sportowego
    type = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    year = IntegerRangeField()

    def __str__(self):
        return f"{self.type}, {self.name}"


class LanguageName(models.TextChoices):
    ANG = "ang", "język angielski"
    FRA = "fra", "język francuski"
    HISZ = "hisz", "język hiszpański"
    NIEM = "niem", "język niemiecki"
    POR = "por", "język portugalski"
    ROS = "ros", "język rosyjski"
    WLO = "wlo", "język włoski"
    LAT = "antyk", "język łaciński i kultura antyczna"
    BIA = "język białoruski", "język białoruski"
    LIT = "język litewski", "język litewski"
    UKR = "język ukraiński", "język ukraiński"
    LEM = "język łemkowski", "język łemkowski"
    KAS = "język kaszubski", "język kaszubski"


class Language(models.Model):
    languages = [
        ("ang", "język angielski"),
        ("fra", "język francuski"),
        ("franc", "język francuski"),
        ("hisz", "język hiszpański"),
        ("hiszp", "język hiszpański"),
        ("niem", "język niemiecki"),
        ("por", "język portugalski"),
        ("ros", "język rosyjski"),
        ("wlo", "język włoski"),
        ("wło", "język włoski"),
        ("antyk", "język łaciński i kultura antyczna"),
        ("język białoruski", "język białoruski"),
        ("język litewski", "język litewski"),
        ("język ukraiński", "język ukraiński"),
        ("język łemkowski", "język łemkowski"),
        ("język kaszubski", "język kaszubski"),
    ]
    high_school_class = models.ForeignKey(HighSchoolClass, on_delete=models.CASCADE)
    name = models.CharField(choices=languages, max_length=40)
    # pierwszy język obcy/drugi język obcy
    nr = models.IntegerField(choices=[(1, "pierwszy"), (2, "drugi")])
    is_bilingual = models.BooleanField(default=False)
    multiple_levels = models.BooleanField(default=False)

    def __str__(self):
        return ",".join([self.name, self.high_school_class.school.school_name])


class SubjectName(models.TextChoices):
    BIOL = "biol", "biologia"
    CHEM = "chem", "chemia"
    FILOZ = "filoz", "filozofia"
    FIZ = "fiz", "fizyka"
    GEOGR = "geogr", "geografia"
    HIST = "hist", "historia"
    HMUZ = "h.muz.", "historia muzyki"
    HSZT = "h.szt.", "historia sztuki"
    INF = "inf", "informatyka"
    POL = "pol", "język polski"
    MAT = "mat", "matematyka"
    WOS = "wos", "wiedza o społeczeństwie"
    OBCY = "obcy", "język obcy"


class ExtendedSubject(models.Model):
    subjects = [
        ("biol", "biologia"),
        ("chem", "chemia"),
        ("filoz", "filozofia"),
        ("fiz", "fizyka"),
        ("geogr", "geografia"),
        ("hist", "historia"),
        ("h.muz.", "historia muzyki"),
        ("h.szt.", "historia sztuki"),
        ("inf", "informatyka"),
        ("pol", "język polski"),
        ("mat", "matematyka"),
        ("wos", "wiedza o społeczeństwie"),
        ("obcy", "obcy"),
    ]

    high_school_class = models.ForeignKey(HighSchoolClass, on_delete=models.CASCADE)
    name = models.CharField(choices=subjects + Language.languages, max_length=40)

    def __str__(self):
        return ",".join([self.name, self.high_school_class.school.school_name])


class Statistics(models.Model):
    LAUREAT = -1.0
    high_school_class = models.ForeignKey(HighSchoolClass, on_delete=models.CASCADE)
    # tura rekrutacji
    round = models.IntegerField()
    # aka próg
    points_min = models.FloatField()
    points_max = models.FloatField()
    points_avg = models.FloatField()
    with_competency_test = models.BooleanField(default=False)
    only_sports_test = models.BooleanField(default=False)


# TODO technika, szkoły sportowe, prywatne
