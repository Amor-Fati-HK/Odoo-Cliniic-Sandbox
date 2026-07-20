"""
File: materiel.py
Author: Hani Katti
Material model for the clinic management module

"""
from odoo import models,fields,api,_
from odoo.exceptions import ValidationError

class MaterialType(models.Model):
    _name="clinic.material.type"
    _description="Type de Materiel"

    name=fields.Char(string="Nom du type", required=True)
    _sql_constraints=[
        ('name_unique','UNIQUE(name)','Ce type de materiel existe deja !')
    ]

class Material(models.Model):
    _name="clinic.material"
    _description="Gestion du Materiel"

    name=fields.Char(string="Nom / Modele", required=True)
    serial_number=fields.Char(string="Numero de Serie")
    type_id=fields.Many2one('clinic.material.type',string="Categorie", required=True)

    purchase_date=fields.Date(string="Date d'achat")
    price=fields.Float(string="Prix d'achat")
    state=fields.Selection([
        ('available','Disponible'),
        ('in_use','En cours dutilisation'),
        ('repair', 'En maintenance'),
        ('broken', 'Hors service')
    ], string="Etat", default='available')
    

    @api.constrains('price')
    def _check_price(self):
        for s in self:
            if s.price<0 :
                raise ValidationError(_("Prix invalide"))
        
    