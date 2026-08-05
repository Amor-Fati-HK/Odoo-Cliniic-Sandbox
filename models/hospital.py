"""
File: hospital.py
Author: HK
Hospital model for the contact section in the clinic management module

"""

from odoo import models,fields,api,_
from odoo.exceptions import ValidationError
import re

class hospital(models.Model):
    _name="clinic.hospital"
    _description="Hopitaux / CHU "

    name=fields.Char(string="Nom de l'etablissement", required=True)
    hospital_type = fields.Selection([
        ('chu', 'CHU (Centre Hospitalier Universitaire)'),
        ('eph', 'EPH (Établissement Public Hospitalier)'),
        ('ehs', 'EHS (Établissement Hospitalier Spécialisé)'),
        ('private', 'Clinique Privée Partenaire'),
        ('military', 'Hôpital Militaire'),
    ], string="Type d'établissement", required=True, default='chu')

    wilaya=fields.Char(string="Wilaya", 
                       default="Alger")
    contact_person=fields.Char(string="Directeur de l'hopital ")
    phone=fields.Char(string="Telephone officiel")
    email=fields.Char(string="Email officiel")
    address=fields.Text(string="Adresse exacte")

    description=fields.Text(string="Description")

    @api.constrains('phone')
    def _check_phone_validation(self):
        """Checks the phone number validation"""
        for r in self:
            if r.phone:
                if not r.phone.startswith('+213'):
                    raise ValidationError(_("Le numero doit commencer avec +213 !"))

                clean_phone=''.join(c for c in r.phone if c.isdigit())
                if len(clean_phone)!=12:
                    raise ValidationError(_("Numero Invalide !"))

    @api.constrains('email')
    def _check_email_validation(self):
        """Checks the email syntax validation"""
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        for r in self:
            if not re.match(pattern, r.email):
                raise ValidationError(_("Email Invalide"))

        

