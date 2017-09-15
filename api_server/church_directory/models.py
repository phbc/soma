
from django.db import models
from PIL import Image
from django_resized import ResizedImageField
from soma.settings import SOMA_HOME

def _crop_image(path, cw, ch):
    img = Image.open(path)
    w, h = img.size
    if cw < w:
        mult = cw / w
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

NON_MEMBER = 0
ACTIVE_MEMBER = 1
HOMEBOUND_MEMBER = 2
OUTOFAREA_MEMBER = 3
FORMER_MEMBER = 4
DECEASED = 5

MEMBERSHIP_STATUS = (
    (NON_MEMBER, 'Non-member'),
    (ACTIVE_MEMBER, 'Active Member'),
    (HOMEBOUND_MEMBER, 'Homebound Member'),
    (OUTOFAREA_MEMBER, 'Out-of-area Member'),
    (FORMER_MEMBER, 'Former Member'),
    (DECEASED, 'Deceased'),
)
MEMBERSHIP_STATUS_REV = _create_reverse_lookup(MEMBERSHIP_STATUS)

def membership_status_int(status):
    return MEMBERSHIP_STATUS_REV[status]

def membership_status_str(status):
    return MEMBERSHIP_STATUS[status][1]

def is_member(status):
    if status == ACTIVE_MEMBER:
        return True
    elif status == HOMEBOUND_MEMBER:
        return True
    elif status == OUTOFAREA_MEMBER:
        return True
    else:
        return False

MALE = 0
FEMALE = 1

SEXES = (
    (MALE, 'Male'),
    (FEMALE, 'Female'),
)

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
    if sex == 'Male':
        return MALE
    elif sex == 'Female':
        return FEMALE


# Create your models here.

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
    membership_status = models.IntegerField(choices=MEMBERSHIP_STATUS)
    father = models.ForeignKey('Person', on_delete=models.SET_NULL, related_name='father_child', null=True, blank=True)
    mother = models.ForeignKey('Person', on_delete=models.SET_NULL, related_name='mother_child', null=True, blank=True)
    spouse = models.ForeignKey('Person', on_delete=models.SET_NULL, related_name='person_spouse', null=True, blank=True)
    notes = models.TextField('notes', null=True, blank=True)
    picture = ResizedImageField(size=[PERSON_PICTURE_WIDTH, PERSON_PICTURE_HEIGHT], crop=['middle', 'center'], upload_to=PERSON_PICTURE_DIR, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'People'

    def is_member(self):
        return is_member(MEMBERSHIP_STATUS_REV[self.membership_status])

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class MembershipStatusChange(models.Model):
    person = models.IntegerField(primary_key=True)
    begin_date = models.DateField()
    end_date = models.DateField(null=True)