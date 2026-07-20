"""
File: medecin.py
Author: Hani Katti
Doctor model for the clinic management
"""

from odoo import models,fields,api,_
from odoo.exceptions import ValidationError
from datetime import date, timedelta

class medecin(models.Model):
    _name="clinic.medecin"
    _description="Medecin soignant"

    name=fields.Char(string="Nom", required=True)
    consultation_ids=fields.One2many('clinic.consultation', 'medecin_id',
                                     string="Consultations effectuees")
    surname=fields.Char(string="Prenom", required=True)
    description=fields.Text(string="Description")
    age=fields.Integer(string="Age", compute="_compute_age", store=True, tracking=True)
    sexe=fields.Selection([('man','Homme'),
                           ('woman','Femme')], default='man', string="Genre", required=True)
    birthday=fields.Date(string="Date de Naissance", required=True)
    birthday_place=fields.Char(string="Lieu de Naissance", required=False, default="Algerie")
    service = fields.Selection([
                                ('a', 'Anesthésie-Réanimation'),
                                ('b', 'Cardiologie'),
                                ('c', 'Chirurgie Générale'),
                                ('d', 'Chirurgie Orthopédique'),
                                ('e', 'Dermatologie'),
                                ('f', 'Endocrinologie-Diabétologie'),
                                ('g', 'Gastro-entérologie'),
                                ('h', 'Gériatrie'),
                                ('i', 'Gynécologie-Obstétrique'),
                                ('j', 'Hématologie'),
                                ('k', 'Maternité'),
                                ('l', 'Neurologie'),
                                ('m', 'Oncologie (Cancérologie)'),
                                ('n', 'Ophtalmologie'),
                                ('o', 'ORL (Oto-Rhino-Laryngologie)'),
                                ('p', 'Pédiatrie'),
                                ('q', 'Pneumologie'),
                                ('r', 'Radiologie (Imagerie Médicale)'),
                                ('s', 'Réanimation'),
                                ('t', 'Urgences'),
                            ], string="Service", required=True)
    service_chef=fields.Boolean(string="Chef de service ", default=False)
    recruit_date=fields.Date(string="Date de recrut", required=True)
    salary=fields.Float(string="Salaire", required=False, compute="_compute_salary", store=True)
    experience_here=fields.Integer(string="Experience dans cette clinique", compute="_compute_exp")

    medecin_count=fields.Integer(string="Medecins",compute="_compute_medecin_count", store=True)

   
    @api.depends('birthday')
    def _compute_age(self):
        """Compute method to calculate age"""
        today=date.today()
        for s in self:
            if s.birthday:
                s.age=today.year - s.birthday.year - (
                    (today.month, today.day) < (s.birthday.month,s.birthday.day))
            else:
                s.age=0

    @api.depends('service','service_chef')
    def _compute_salary(self):
        """Compute method to calculate doctors salaries"""
        base_salaries={
            'a': 180000, 'b': 220000, 'c': 250000, 'd': 240000, 'e': 140000,
            'f': 130000, 'g': 160000, 'h': 110000, 'i': 200000, 'j': 150000,
            'k': 120000, 'l': 170000, 'm': 200000, 'n': 190000, 'o': 180000,
            'p': 140000, 'q': 130000, 'r': 210000, 's': 230000, 't': 160000,
        }
        management_bonus=50000
        for s in self:
            base=base_salaries.get(s.service,0)
            bonus=management_bonus if s.service_chef else 0
            s.salary=base+bonus

    @api.depends('recruit_date')
    def _compute_exp(self):
        """Compute method to calculate experience in the clinic"""
        today=date.today()
        for s in self:
            if s.recruit_date:
                s.experience_here=today.year - s.recruit_date.year - (
                    (today.month, today.day) < (s.recruit_date.month,s.recruit_date.day))
            else:
                s.experience_here=0

    @api.depends('name')
    def _compute_medecin_count(self):
        total_medecins=self.search_count([]) or 1
        for s in self:
            s.medecin_count=(1.0/total_medecins)*100

    @api.constrains('service','service_chef')
    def _check_unique_chef_per_service(self):
        """Checks that there is only one chef"""
        for s in self:
            if s.service_chef:
                already_exists=self.search([
                    ('service','=',s.service),
                    ('service_chef','=',True),
                    ('id','!=',s.id)
                ])

                if already_exists:
                    current_chef=already_exists[0].name
                    service_name= dict(self._fields['service'].selection).get(s.service)
                    raise ValidationError(_(
                        "Impossible de nommer un nouveau chef. "
                        "Le service '%s' a deja un chef : %s."
                    ) % (service_name,current_chef))