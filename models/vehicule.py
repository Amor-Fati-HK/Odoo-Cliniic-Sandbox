"""
File: vehicule.py
Author: Hani KATTI
Car model for he clinic management module

"""

from odoo import models,fields,api,_
from odoo.exceptions import ValidationError

class vehicule_type(models.Model):
    _name="clinic.vehicule.type"
    _description="Type de vehicule"

    name=fields.Char(string="Nom du Type", required=True)

    _sql_constraints=[
        ('name_unique', 'UNIQUE(name)', 'Ce type de vehicule existe deja !')
    ]

class vehicule(models.Model):
    _name="clinic.vehicule"
    _description="Vehicules de la clinique"

    name=fields.Char(string="Nom / Modele", required=True)
    description=fields.Text(string="Description")
    type_id=fields.Many2one('clinic.vehicule.type', string="Type", required=True)
    matricule=fields.Char(string="Matricule du vehicule", help="xxxxx-xxx-xx")
    purchase_date=fields.Date(string="Date d'achat")
    price=fields.Float(string="Prix d'achat")
    state=fields.Selection([
        ('available','Disponible'),
        ('in_use','En cours dutilisation'),
        ('repair', 'En maintenance'),
        ('broken', 'Hors service'),
    ], string="Etat", default='available')
    

    @api.constrains('price')
    def _check_price(self):
        """Check the price validation"""
        for s in self:
            if s.price<0 :
                raise ValidationError(_("Prix invalide"))
            
    @api.constrains('matricule')
    def _check_matricule(self):
        """Check the matricule validation"""
        for s in self:
            if len(s.matricule)!=10:
                raise ValidationError(_("Matricule non valide"))