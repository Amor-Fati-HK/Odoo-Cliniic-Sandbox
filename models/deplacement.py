"""
File: deplacement.py
Author: Hani KATTI
Medical Travel model for the clinic management module

"""

from odoo import models,fields,api,_
from odoo.exceptions import ValidationError


class deplacement(models.Model):
    _name="clinic.deplacement"
    _description="Deplacement Medical"

    type_id=fields.Selection([
        ('urgence','Urgence'),
        ('interhospital','Inter-Hospitalier'),
        ('logistic','Logistique'),
        ('house_care','Soin a domicile'),
        ('routine','Routine'),
    ], string="Type de deplacement", required=True)    
    vehicule_id=fields.Many2one('clinic.vehicule',string="Vehicule utilise",required=True)
    patient_id=fields.Many2one('clinic.vehicule',string="Patient transporte",required=True)

    
    