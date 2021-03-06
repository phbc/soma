
import datetime

from PIL import Image
from django.db import models
from django_resized import ResizedImageField
from soma.settings import SOMA_HOME

def _crop_image(path, cw, ch):
    img = Image.open(path)
    w, h = img.size
    if cw < w:
        mult = float(cw) / float(w)
        w *= mult
        h *= mult
    img = img.resize((int(w), int(h)), Image.ANTIALIAS)
    # crop if necessary
    x, y = 0, 0
    w, h = img.size
    if w > cw:
        diff = (w - cw) / 2
        x += diff
        w -= diff
    if h > ch:
        diff = (h - ch)
        h -= diff
    img = img.crop((x, y, w, h))
    img.save(path)

def _create_reverse_lookup(s):
    out = {}
    for i in s:
        out[i[1]] = i[0]
    return out

PERSON_PICTURE_DIR = 'images/church_directory/person/pictures'
PERSON_PICTURE_WIDTH = 360
PERSON_PICTURE_HEIGHT = 230

NON_MEMBER = False
MEMBER = True

MEMBERSHIP_STATUS = (
    (NON_MEMBER, 'Non-member'),
    (MEMBER, 'Member'),
)
MEMBERSHIP_STATUS_REV = _create_reverse_lookup(MEMBERSHIP_STATUS)

EVENT_BAPTISM = 'Baptism'
EVENT_DEATH = 'Death'
EVENT_DIVORCE = 'Divorce'
EVENT_JOINED_CHURCH = 'Added to Membership'
EVENT_LEFT_CHURCH = 'Removed from Membership'
EVENT_WEDDING = 'Wedding'
EVENT_WIDOWED = 'Widowed'

LIFE_EVENTS = [
    EVENT_BAPTISM,
    EVENT_DEATH,
    EVENT_DIVORCE,
    EVENT_JOINED_CHURCH,
    EVENT_LEFT_CHURCH,
    EVENT_WEDDING,
    EVENT_WIDOWED,
]

CLEARANCE_BACKGROUND_CHECK = 'Background Check'

CLEARANCE_TYPES = [
    CLEARANCE_BACKGROUND_CHECK,
]

def membership_status_int(status):
    return MEMBERSHIP_STATUS_REV[status]

def membership_status_str(status):
    return MEMBERSHIP_STATUS[status][1]

MALE = 0
FEMALE = 1

SEXES = (
    (MALE, 'Male'),
    (FEMALE, 'Female'),
)
SEXES_REV = _create_reverse_lookup(SEXES)

SINGLE = 1
MARRIED = 2

MARITAL_STATUSES = (
    (0, 'N/A'),
    (SINGLE, 'Single'),
    (MARRIED, 'Married'),
)

def sex_str(sex):
    return SEXES[sex][1]

def sex_int(sex):
    try:
        return SEXES_REV[sex]
    except KeyError:
        pass


# Create your models here.

class ClearanceType(models.Model):
    type_id = models.AutoField('ID', primary_key=True)
    name = models.CharField('Name', max_length=50, unique=True)
    duration = models.DurationField(null=True, blank=True)
    builtin = models.BooleanField()

    class Meta:
        verbose_name = 'Clearance Type'

    def __str__(self):
        return self.name

class Clearance(models.Model):
    clearance_type = models.ForeignKey('ClearanceType', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.clearance_type) + ': ' + str(self.person)

class Role(models.Model):
    type_id = models.AutoField('ID', primary_key=True)
    name = models.CharField('Name', max_length=50, unique=True)

    def __str__(self):
        return self.name

class RoleAssignment(models.Model):
    role_id = models.AutoField('ID', primary_key=True)
    role_type = models.ForeignKey('Role', on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Role Assignment'

    def role_name(self):
        return self.role_type.name

    def ongoing(self):
        return self.end_date == None

    def __str__(self):
        s = str(self.role_type) + ': ' + str(self.person)
        if self.start_date != None or self.end_date != None:
            if self.start_date != None:
                s += ' (' + str(self.start_date.year)
            else:
                s += ' (?'
            if self.end_date != None:
                s += ' - ' + str(self.end_date.year)
            s += ')'
        return s

class EventType(models.Model):
    type_id = models.AutoField('ID', primary_key=True)
    name = models.CharField('Name', max_length=50, unique=True)
    builtin = models.BooleanField()

    class Meta:
        verbose_name = 'Event Type'

    def __str__(self):
        return self.name

class Event(models.Model):
    event_id = models.AutoField('ID', primary_key=True)
    event_type = models.ForeignKey('EventType', on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)

    def event_age(self):
        b = self.date
        if b != None:
            n = datetime.date.today()
            d = n - b
            return (d.days / 365) + (d.days / 365) * (1 / (365 * 4))
        else:
            return -1

    def __str__(self):
        return str(self.event_type) + ': ' + str(self.person)

class Person(models.Model):
    person_id = models.AutoField('ID', primary_key=True)
    first_name = models.CharField('First Name', max_length=50)
    middle_name = models.CharField('Middle Name', max_length=50, null=True, blank=True)
    last_name = models.CharField('Last Name', max_length=50)
    suffix = models.CharField('Suffix', max_length=5, null=True, blank=True)
    marital_status = models.IntegerField(choices=MARITAL_STATUSES)
    sex = models.IntegerField(choices=SEXES)
    birthday = models.DateField(null=True)
    home_phone = models.CharField('Home Number', max_length=10, blank=True, null=True)
    cell_phone = models.CharField('Cell Number', max_length=10, blank=True, null=True)
    email_address = models.CharField('Email Address', max_length=75, blank=True, null=True)
    address_line1 = models.CharField('Address Line 1', max_length=50, blank=True, null=True)
    address_line2 = models.CharField('Address Line 2', max_length=50, null=True, blank=True)
    city = models.CharField('City', max_length=50, null=True, blank=True)
    province = models.CharField('Province', max_length=50, null=True, blank=True)
    zipcode = models.CharField('Zip Code', max_length=10, null=True, blank=True)
    homebound = models.BooleanField()
    out_of_area = models.BooleanField()
    member = models.BooleanField(choices=MEMBERSHIP_STATUS)
    father = models.ForeignKey('Person', on_delete=models.SET_NULL, related_name='father_child', null=True, blank=True)
    mother = models.ForeignKey('Person', on_delete=models.SET_NULL, related_name='mother_child', null=True, blank=True)
    spouse = models.ForeignKey('Person', on_delete=models.SET_NULL, related_name='person_spouse', null=True, blank=True)
    notes = models.TextField('notes', null=True, blank=True)
    picture = ResizedImageField(size=[PERSON_PICTURE_WIDTH, PERSON_PICTURE_HEIGHT], crop=['middle', 'center'], upload_to=PERSON_PICTURE_DIR, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'People'

    def age(self):
        b = self.birthday
        if b != None:
            n = datetime.date.today()
            d = n - b
            return (d.days / 365) + (d.days / 365) * (1 / (365 * 4))
        else:
            return -1

    def date_joined(self):
        et = EventType.objects.get(name=EVENT_JOINED_CHURCH)
        w = Event.objects.get(person=self, event_type=et)
        if w != None:
            return w.date

    def wedding(self):
        et = EventType.objects.get(name=EVENT_WEDDING)
        w = Event.objects.get(person=self, event_type=et)
        if w != None:
            return w.date

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class MembershipStatusChange(models.Model):
    person = models.IntegerField(primary_key=True)
    begin_date = models.DateField()
    end_date = models.DateField(null=True)
