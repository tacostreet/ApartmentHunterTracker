from django.db import models

# Create your models here.

class HoustonListings(models.Model):
    apt = models.TextField(db_column='APT', blank=True, null=True)  # Field name made lowercase.
    ad_code = models.FloatField(db_column='Ad Code', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ads_link = models.TextField(db_column='Ads Link', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    apartment_type = models.TextField(db_column='Apartment Type', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    building_address = models.TextField(db_column='Building Address', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    building_complex = models.TextField(db_column='Building/Complex', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cl = models.TextField(db_column='CL', blank=True, null=True)  # Field name made lowercase.
    cl_0 = models.FloatField(db_column='Cl', blank=True, null=True)  # Field name made lowercase. Field renamed because of name conflict.
    contact_name = models.TextField(db_column='Contact Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    email = models.TextField(db_column='Email', blank=True, null=True)  # Field name made lowercase.
    postal_code = models.TextField(db_column='Postal Code', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rlx = models.TextField(db_column='RLX', blank=True, null=True)  # Field name made lowercase.
    ry = models.TextField(db_column='RY', blank=True, null=True)  # Field name made lowercase.
    rent = models.TextField(db_column='Rent', blank=True, null=True)  # Field name made lowercase.
    specific_locations = models.TextField(db_column='Specific Locations', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    #zil = models.TextField(db_column='ZIL', blank=True, null=True)  # Field name made lowercase.
    zu = models.TextField(db_column='ZU', blank=True, null=True)  # Field name made lowercase.
    available_on = models.TextField(db_column='available on', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    bathrooms = models.TextField(blank=True, null=True)
    bedrooms = models.TextField(blank=True, null=True)
    housing_type = models.TextField(db_column='housing type', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    laundry = models.TextField(blank=True, null=True)
    parking = models.TextField(blank=True, null=True)
    phone_number = models.TextField(db_column='phone number', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    posting_title = models.TextField(db_column='posting title', blank=True, null=True)  # Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'houston_listings'

