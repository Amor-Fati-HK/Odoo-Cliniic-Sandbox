"""
File: vehicule.py
Author: Hani KATTI
Car model for the clinic management module

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
    purchase_year=fields.Integer(string="Annee d'achat", compute="_compute_purchase_year")
    purchase_place=fields.Char(string="Lieu d'achat", compute="_compute_purchase_place")
    price=fields.Float(string="Prix d'achat")
    state=fields.Selection([
        ('available','Disponible'),
        ('in_use','En cours dutilisation'),
        ('repair', 'En Reparation'),
        ('broken', 'Hors service'),
    ], string="Etat", default='available')


    deplacement_ids=fields.One2many('clinic.deplacement','vehicule_id',string="Historique des deplacements")
    

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
                raise ValidationError(_("Matricule Invalide"))

       
    @api.depends('matricule')
    def _compute_purchase_year(self):
        for s in self:
            if s.matricule:
                clean_m=''.join(c for c in s.matricule if c.isdigit())
                if len(clean_m)>=4:
                    m=int(clean_m)%10000
                    year_digits=m//100
                    if year_digits<27:
                        s.purchase_year=2000+year_digits
                    else:
                        s.purchase_year=1900+year_digits
                else:
                    s.purchase_year=0
            else:
                s.purchase_year=0

    
    @api.depends('matricule')
    def _compute_purchase_place(self):
        wilayas = {1: "Adrar", 2: "Chlef", 3: "Laghouat", 4: "Oum El Bouaghi", 5: "Batna", 6: "Béjaïa", 7: "Biskra", 8: "Béchar", 9: "Blida", 10: "Bouira", 
                    11: "Tamanrasset", 12: "Tébessa", 13: "Tlemcen", 14: "Tiaret", 15: "Tizi Ouzou", 16: "Alger", 17: "Djelfa", 18: "Jijel", 19: "Sétif", 20: "Saïda", 
                    21: "Skikda", 22: "Sidi Bel Abbès", 23: "Annaba", 24: "Guelma", 25: "Constantine", 26: "Médéa", 27: "Mostaganem", 28: "M'Sila", 29: "Mascara", 30: "Ouargla", 
                    31: "Oran", 32: "El Bayadh", 33: "Illizi", 34: "Bordj Bou Arréridj", 35: "Boumerdès", 36: "El Tarf", 37: "Tindouf", 38: "Tissemsilt", 39: "El Oued", 40: "Khenchela", 
                    41: "Souk Ahras", 42: "Tipaza", 43: "Mila", 44: "Aïn Defla", 45: "Naâma", 46: "Aïn Témouchent", 47: "Ghardaïa", 48: "Relizane", 49: "El M'Ghair", 50: "El Meniaa", 
                    51: "Ouled Djellal", 52: "Bordj Badji Mokhtar", 53: "In Salah", 54: "In Guezzam", 55: "Touggourt", 56: "Djanet", 57: "Les M'Ghair", 58: "Béni Abbès", 59: "Aflou", 60: "Barika", 
                    61: "El Kantara", 62: "Bir El Ater", 63: "El Aricha", 64: "Ksar Chellala", 65: "Aïn Oussera", 66: "Messaad", 67: "Ksar El Boukhari", 68: "Bou Saâda", 69: "El Abiodh Sidi Cheikh"}

        for s in self:
            if s.matricule:
                clean_m=''.join(c for c in s.matricule if c.isdigit())
                if len(clean_m)>=2:
                    m=int(clean_m)%100
                    if m in wilayas:
                        s.purchase_place=wilayas[m]
                    else:
                        s.purchase_place="Inconnu"
                else:
                    s.purchase_place="Inconnu"
            else:
                s.purchase_place="Inconnu"