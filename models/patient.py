"""
File : patient.py
Author: HK
Patient model for the clinic management

"""



from odoo import models,fields,api, _
from odoo.exceptions import ValidationError
from datetime import date, timedelta

class decease_cause(models.Model):
    _name="clinic.patient.decease"
    _description="Mort patient"

    name=fields.Selection([
        ('Diag_error','Erreur de diagnostic'),
        ('medication_incident','Incident de medication'), #
        ('interventionnal_incident','Incident interventionnel'),
        ('IAS','Infection Associes aux Soins'),
        ('Surveil_failure','Defaut de surveillance'),
        ('Communication problem','Probleme de communication'),
    ],string="Cause", required=True)

    surveil_salle=fields.Many2one('clinic.room',string="Salle",required=True)
    medecin_ids=fields.Many2many('clinic.medecin', string="Medecins responsables", required=True)
    description=fields.Text(string="Description", required=True)

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
    age=fields.Integer(string="Age", compute="_compute_age", store=True, tracking=True, group_operator="avg")
    sexe=fields.Selection([('man','Homme'),
                           ('woman','Femme')], default='man', string="Genre", required=True)
    height=fields.Float(string="Taille", help="Taille en centimetre",group_operator="avg")
    weight=fields.Float(string="Poids", help="Taille en kilogrammes",group_operator="avg")
    imc=fields.Float(string="IMC", compute="_compute_imc",help="Indice de Masse Corporelle",group_operator="avg")

    birthday=fields.Date(string="Date de Naissance", required=True)
    birthday_place=fields.Char(string="Lieu de Naissance", required=False, default="Algerie")
    blood=fields.Selection([('o+','O+'),('o-','O-'),('a+','A+'),('a-','A-'),('b+','B+'),('b-','B-'),('ab+','AB+'),('ab-','AB-')],
                          required=False, string="Groupe Sanguin")
    father_name=fields.Char(string="Nom du pere", tracking=True)
    mother_name=fields.Char(string="Nom de la mere", tracking=True)
    profession=fields.Char(string="Profession", required=False)
    sportif=fields.Boolean(string="Sportif")
    sportif_count=fields.Integer(string="Nombre de sportif",
                                 compute="_compute_indicators", store=True)
    sportif_rate=fields.Float(string="Sportif (%)", compute="_compute_clinic_rates", store=True, group_operator="avg")
    decease=fields.Boolean(string="Decede", store=True, default=False, tracking=True)
    decease_cause=fields.Many2one('clinic.patient.decease',string="Cause du deces",required=True)
    decease_count=fields.Integer(string="Nombre de Deces",
                                 compute="_compute_indicators", store=True)
    decease_rate=fields.Float(string="Deces (%)", compute="_compute_clinic_rates", store=True, group_operator="avg")
    medical_antecedant=fields.Text(string="Antecedant Medicaux")
    patient_count=fields.Integer(string="Patients", compute="_compute_patient_count",store=True)
    age_state=fields.Selection([
        ('kid','Enfant'),
        ('teen','Adolescent'),
        ('young_adult','Jeune Adulte'),
        ('adult','Adulte'),
        ('aged','Sujet Agé'),
        ('big_age','Grand Age'),
    ], compute="_compute_age_state", string="Classe d'age", store=True)
    sport_gender=fields.Selection([
        ('m_sport','Homme Sportif'),
        ('m_nosport','Homme Non-Sportif'),
        ('f_sport','Femme Sportive'),
        ('f_nosport','Femme Non-Sportive'),
    ], string="Genre et Sport", compute="_compute_sport_gender",store=True)

    @api.depends('sexe','sportif')
    def _compute_sport_gender(self):
        """Associate each patient at its combined category genre + sport"""
        for r in self:
            if r.sexe=='man':
                r.sport_gender='m_sport' if r.sportif else 'm_nosport'
            elif r.sexe=='woman':
                r.sport_gender='f_sport' if r.sportif else 'f_nosport'
            else:
                r.sport_gender=False


    @api.depends('age')
    def _compute_age_state(self):
        for s in self:
            if s.age:
                if s.age<12:
                    s.age_state='kid'
                elif s.age<18:
                    s.age_state='teen'
                elif s.age<26:
                    s.age_state='young_adult'
                elif s.age<60:
                    s.age_state='adult'
                elif s.age<75:
                    s.age_state='aged'
                else:
                    s.age_state='big_age'

    def _compute_clinic_rates(self):
        """Compute clinic stats"""
        total_patients=self.search_count([]) or 1
        total_sportifs=self.search_count([('sportif','=',True)])
        total_decease=self.search_count([('decease','=',True)])

        for r in self:
            r.sportif_rate=(total_sportifs / total_patients)*100.0
            r.decease_rate=(total_decease / total_patients)*100.0

    @api.depends('name')
    def _compute_patient_count(self):
        for r in self:
            r.patient_count=1
    
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
    
    @api.model
    def _register_hook(self):
        """Force le calcul du champ combiné pour TOUS les patients au démarrage du serveur"""
        patients = self.search([])
        if patients:
            patients._compute_sport_gender()
        return super(Patient, self)._register_hook()


    @api.depends('sportif', 'decease')
    def _compute_indicators(self):

        for r in self:
            r.sportif_count= 1 if r.sportif else 0
            r.decease_count= 1 if r.decease else 0
