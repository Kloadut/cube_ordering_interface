from datetime import datetime

from django.db import models


COUNTRIES = (
    ('be', 'Belgium'),
    ('nl', 'Netherlands'),
    ('lu', 'Luxembourg'),
)

class Order(models.Model):
    made_on = models.DateTimeField(auto_now_add=True)

    nick = models.CharField(max_length=255, null=True, blank=True, verbose_name="Nickname (optional)", help_text="We may know you better by your nickname than your civil name :-)")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    email = models.EmailField(help_text="We will never send you unwanted emails. You will only receive a copy of your order, and further information about it.")

    wants_vpn = models.BooleanField(default=False, verbose_name="I want to subscribe to the Neutrinet's VPN service and become a member of Neutrinet ASBL/VZW")
    wants_to_install_everything_himself = models.BooleanField(default=False, verbose_name="Do not configure my Cube for me, I want to do it by myself")

    # domain
    wants_neutrinet_to_renew_the_domain = models.BooleanField(default=False, verbose_name="I want my domain to be renewed automatically every year.", help_text="It is a common mistake to forget to renew a domain name every year. Check this box if you want Neutrinet to do it for you.")
    domain_name = models.URLField(blank=True, null=False, verbose_name="Domain name")

    # needed if the user wants the vpn
    street = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    town = models.CharField(max_length=255, null=True, blank=True)
    birthplace = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=2, choices=COUNTRIES, null=True, blank=True, help_text="If you do not see your country of living on this list, please <a href='http://db.ffdn.org'>find another ISP closer to you</a>. If you want to choose Neutrinet anyway, please indicate your country of living in the comment section below.")
    birth_date = models.DateField(null=True, blank=True, help_text="Format: dd/mm/yyyy")

    # private
    has_payed = models.BooleanField(default=False)
    we_have_received_the_order = models.BooleanField(default=False)
    member_has_been_give_order = models.BooleanField(default=False)
    private_comment = models.TextField(null=True, blank=True)

    components = models.ManyToManyField('Component', through='ComponentOrder')

    estimated_price = models.DecimalField(max_digits=10, decimal_places=2)
    real_price = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    # member is invited to add more if he wants to
    price_payed = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)

    comment = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "order #%s for %s made %s days ago" % (self.id, "%s %s" % (self.first_name, self.last_name) if not self.nick else "%s %s (%s)" % (self.first_name, self.last_name, self.nick), (datetime.now() - self.made_on.replace(tzinfo=None)).days)


class Component(models.Model):
    reference = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)  # price costing right now (default is for ordering >= 10)
    url = models.URLField()
    estimated_shipment_time = models.PositiveSmallIntegerField(null=True, blank=True, help_text="in days")
    in_default_pack = models.BooleanField(default=False)

    def __unicode__(self):
        return self.reference if not self.full_name else u"%s (%s)" % (self.full_name, self.reference)


class ComponentOrder(models.Model):
    order = models.ForeignKey(Order)
    component = models.ForeignKey(Component)
    number = models.PositiveIntegerField(default=1)
    paid_price = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)  # effectivly paid price
    received = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return "%s '%s' for %s" % (self.number, self.component, self.order)
