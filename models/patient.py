"""
File : patient.py
Author: Hani Katti
Patient model for the clinic management

"""



from odoo import models,fields,api, _
from odoo.exceptions import ValidationError
from datetime import date, timedelta

class Patient(models.Model):
    _name="clinic.patient"
    _description="Clinic Patient"

    name=fields.Char(string="Nom", required=True)
    description=fields.Text(string="Description")

    consultation_ids=fields.One2many('clinic.consultation','patient_id', string="Historique des consultations")
    intervention_ids=fields.One2many('clinic.intervention','patient_id', string="Historique des interventions")
    deplacement_ids=fields.One2many('clinic.deplacement','patient_id',string="Historique des deplacement")
    greffe_ids=fields.One2many('clinic.greffe','patient_id',string="Historique des transplantations")
    
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
                          required=False, string="Groupe Sanguin")
    father_name=fields.Char(string="Nom du pere", tracking=True)
    mother_name=fields.Char(string="Nom de la mere", tracking=True)
    profession=fields.Char(string="Profession", required=False)
    sportif=fields.Boolean(string="Sportif")
    decease=fields.Boolean(string="Decede", store=True, default=False, tracking=True)
    decease_cause=fields.Char(string="Cause du deces", tracking=True)
    medical_antecedant=fields.Text(string="Antecedant Medicaux")
    
    @api.constrains('age')
    def _check_age_validation(self):
        """Check age validation"""
        for re in self:
            if re.age < 0:
                raise ValidationError(_("L'age ne peut pas etre inferieur a 0"))
            elif re.age >199:
                raise ValidationError(_("Le patient doit etre mortel"))
    
    @api.constrains('height','weight')
    def _check_height_weight(self):
        """Check height and weight validation"""
        for re in self:
            if re.height < 0 or re.weight<0:
                raise ValidationError(_("Taille ou poids invalide"))
            
    @api.depends('height', 'weight')
    def _compute_imc(self):
        for r in self:
            if r.height > 0:
                r.imc = r.weight / ((r.height / 100) ** 2)
            else:
                r.imc = 0


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
    
            
    

            