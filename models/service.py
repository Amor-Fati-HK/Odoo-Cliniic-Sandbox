"""
File: service.py
Author: HK
Public service contacts for the clinic management module
"""

from odoo import models,fields,api,_
from odoo.exceptions import ValidationError
import re

class service(models.Model):
    _name="clinic.service"
    _description="Service publique"

    name=fields.Char(string="Nom de l'organisme", required=True, tracking=True)
    code=fields.Char(string="Code/Matricule Officiel")
    service_type=fields.Selection([
        ('dsp', 'Direction de la Santé (DSP)'),
        ('ministry', 'Ministère de la Santé'),
        ('social_security', 'Sécurité Sociale (CNAS / CASNOS)'),
        ('civil_protection', 'Protection Civile / Secours'),
        ('etat_civil', 'État Civil (APC / Mairie)'),
        ('inspection', 'Hygiène & Inspection du Travail'),
        ('other', 'Autre Organisme'), 
    ], string="Type d'organisme", required=True, default='dsp', tracking=True)
    contact_person=fields.Char(string="Responsable / Interlocuteur principal")
    phone=fields.Char(string="Telephone officiel")
    email=fields.Char(string="Email officiel")
    address=fields.Text(string="Adresse de l'institution")

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

    