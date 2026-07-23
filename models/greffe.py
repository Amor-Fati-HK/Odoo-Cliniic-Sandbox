"""
File: greffe.py
Author: Hani Katti
Transplantation model for the clinic management module
"""

from odoo import models,fields,api,_
from odoo.exceptions import ValidationError
from datetime import date, timedelta


class organ(models.Model):
    _name="clinic.organ"
    _description="Organe cible"

    name=fields.Char(string="Organe", required=True)
    _sql_constraints=[
        ('name_unique','UNIQUE(name)','Cet organe existe deja dans la liste !')
    ]

class donor(models.Model):
    _name="clinic.donor"
    _description="Donneur d'organe"

    name=fields.Char(string="Nom", required=True)
    description=fields.Text(string="Description")
    surname=fields.Char(string="Prenom", required=True)
    age=fields.Integer(string="Age", compute="_compute_age", store=True, tracking=True)
    sexe=fields.Selection([('man','Homme'),
                           ('woman','Femme')], default='man', string="Genre", required=True)
    height=fields.Float(string="Taille actuelle", help="Taille en centimetre")
    weight=fields.Float(string="Poids actuel", help="Taille en kilogrammes")
    imc=fields.Float(string="IMC", compute="_compute_imc",help="Indice de Masse Corporelle")

    birthday=fields.Date(string="Date de Naissance", required=True)
    birthday_place=fields.Char(string="Lieu de Naissance", required=False, default="Algerie")
    blood=fields.Selection([('o+','O+'),('o-','O-'),('a+','A+'),('a-','A-'),('b+','B+'),('b-','B-'),('ab+','AB+'),('ab-','AB-')],
                          required=True, string="Groupe Sanguin")
    hla_a1 = fields.Char(string="HLA - A (Allèle 1)", help="Exemple: 02:01")
    hla_a2 = fields.Char(string="HLA - A (Allèle 2)", help="Exemple: 11:03")
    hla_b1 = fields.Char(string="HLA - B (Allèle 1)", help="Exemple: 07:02")
    hla_b2 = fields.Char(string="HLA - B (Allèle 2)", help="Exemple: 44:01")
    hla_dr1 = fields.Char(string="HLA - DR (Allèle 1)", help="Exemple: 03:01")
    hla_dr2 = fields.Char(string="HLA - DR (Allèle 2)", help="Exemple: 15:01")



    medical_antecedant=fields.Text(string="Antecedant Medicaux")

    @api.depends('birthday')
    def _compute_age(self):
        today = date.today()
        for s in self:
            if s.birthday:
                s.age = today.year - s.birthday.year - ((today.month, today.day) < (s.birthday.month, s.birthday.day))
            else:
                s.age = 0

    @api.depends('height', 'weight')
    def _compute_imc(self):
        for r in self:
            if r.height > 0:
                r.imc = r.weight / ((r.height / 100) ** 2)
            else:
                r.imc = 0


class greffe(models.Model):
    _name="clinic.greffe"
    _description="Greffe d'organe"

    patient_id=fields.Many2one('clinic.patient', string="Patient", required=True)
    donor_id=fields.Many2one('clinic.donor', string="Donneur",required=True)
    medecin_ids=fields.Many2many('clinic.medecin',string="Chirurgien(s)",required=True)
    material_ids=fields.Many2many('clinic.material', string="Materiel Utilise")

    hla_a1 = fields.Char(string="HLA - A (Allèle 1)", help="Exemple: 02:01")
    hla_a2 = fields.Char(string="HLA - A (Allèle 2)", help="Exemple: 11:03")
    hla_b1 = fields.Char(string="HLA - B (Allèle 1)", help="Exemple: 07:02")
    hla_b2 = fields.Char(string="HLA - B (Allèle 2)", help="Exemple: 44:01")
    hla_dr1 = fields.Char(string="HLA - DR (Allèle 1)", help="Exemple: 03:01")
    hla_dr2 = fields.Char(string="HLA - DR (Allèle 2)", help="Exemple: 15:01")
    compatibility=fields.Char(string="Compatibilite", compute="_compute_compatibility")

    date_greffe=fields.Datetime(string="Date et Heure")
    salle_greffe=fields.Integer(string="Salle")
    patient_state=fields.Selection([
        ('dead','Decede'),
        ('critic','Critique'),
        ('stable','Stable'),
        ('healed','Guerri'),
     ])
    

    @api.depends('patient_id', 'donor_id', 'hla_a1', 'hla_a2', 'hla_b1', 'hla_b2', 'hla_dr1', 'hla_dr2')
    def _compute_compatibility(self):
        """Compute the compatibility"""

        blood_map = {
            'o+': 'O', 'o-': 'O',
            'a+': 'A', 'a-': 'A',
            'b+': 'B', 'b-': 'B',
            'ab+': 'AB', 'ab-': 'AB'
        }
        for rec in self:
            if not rec.patient_id or not rec.donor_id:
                rec.compatibility="Selectionnez un patient et un donneur"
                continue
            donor_blood=blood_map.get(rec.donor_id.blood)
            receiver_blood=blood_map.get(rec.patient_id.blood)

            if not donor_blood or not receiver_blood:
                rec.compatibility="Groupe sanguin manquant"
                continue
            compatible_blood=False
            if donor_blood=='O':
                compatible_blood=True
            elif donor_blood==receiver_blood:
                compatible_blood=True
            elif donor_blood=='A' and receiver_blood=='AB':
                compatible_blood=True
            elif donor_blood=='B' and receiver_blood=='AB':
                compatible_blood=True

            if not compatible_blood:
                rec.compatibility="Incompatible"
                continue

            mismatch=0
            donor_a=[rec.donor_id.hla_a1, rec.donor_id.hla_a2]
            receiver_a=[rec.hla_a1, rec.hla_a2]
            for allele in donor_a:
                if allele and allele not in receiver_a:
                    mismatch+=1

            donor_b=[rec.donor_id.hla_b1, rec.donor_id.hla_b2]
            receiver_b=[rec.hla_b1, rec.hla_b2]
            for allele in donor_b:
                if allele and allele not in receiver_b:
                    mismatch+=1

            donor_dr=[rec.donor_id.hla_dr1, rec.donor_id.hla_dr2]
            receiver_dr=[rec.hla_dr1, rec.hla_dr2]
            for allele in donor_dr:
                if allele and allele not in receiver_dr:
                    mismatch+=1

            if mismatch <=3:
                status="Fortement Compatible"
            elif mismatch <=5:
                status="Compatible sous surveillance"
            else:
                status="Incompatible"
            rec.compatibility=f"{status} (Mismatches HLA: {mismatch}/6)"

