"""
File: deplacement.py
Author: Hani KATTI
Medical Travel model for the clinic management module

"""

from odoo import models,fields,api,_
from odoo.exceptions import ValidationError
from datetime import date, timedelta



class driver(models.Model):
    _name="clinic.driver"
    _description="Chauffeur du deplacement"

    name=fields.Char(string="Nom complet", required=True)
    surname=fields.Char(string="Prenom", required=True)
    age=fields.Integer(string="Age", compute="_compute_age", store=True, tracking=True)
    sexe=fields.Selection([('man','Homme'),
                           ('woman','Femme')], default='man', string="Genre", required=True)
        
    birthday=fields.Date(string="Date de Naissance", required=True)
    birthday_place=fields.Char(string="Lieu de Naissance", required=False, default="Algerie")
    paper_num=fields.Integer(string="Numero national", required=True)
    
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

    @api.constrains('age')
    def _check_age_validation(self):
        """Checks age validation"""
        for s in self:
            if s.age<18:
                raise ValidationError(_("Le chauffeur ne peut pas etre mineur"))
            


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
    patient_id=fields.Many2one('clinic.patient',string="Patient transporte",required=True)
    driver_id=fields.Many2one('clinic.driver',string="Chauffeur", required=True)

    date_deplacement=fields.Datetime(string="Date et Heure", required=True)
    start_address=fields.Char(string="Addresse de Depart",required=True)
    dest_address=fields.Char(string="Addresse d'Arrivee", required=True)
    state=fields.Boolean(string="Termine", default=False)

    map_iframe=fields.Html(string="Carte du trajet", compute="_compute_map_iframe")

    @api.depends('start_address','dest_address')
    def _compute_map_iframe(self):
        for s in self:
            if s.start_address and s.dest_address:
                start=s.start_address.replace(' ','+')
                dest=s.dest_address.replace(' ','+')
                url= f"https://maps.google.com/maps?saddr={start}&daddr={dest}&output=embed"
                s.map_iframe=f'<iframe width="100%" height="400" frameborder="0" src="{url}" style="border:0; border-radius:8px;"></iframe>'
            else:
                s.map_iframe=False

    @api.model
    def create(self,vals):
        record=super(deplacement,self).create(vals)
        record._update_vehicule_state()
        return record
    
    def write(self,vals):
        res=super(deplacement,self).write(vals)
        if 'state' in vals or 'vehicule_id' in vals:
            for record in self:
                record._update_vehicule_state()
        return res
    
    def _update_vehicule_state(self):
        """Update method for car state"""
        for rec in self:
            if rec.vehicule_id:
                if rec.state:
                    rec.vehicule_id.write({'state': 'available'})
                else:
                    rec.vehicule_id.write({'state': 'in_use'})

    def name_get(self):
        result=[]
        for rec in self:
            patient_name=""
            if rec.patient_id:
                patient_name="%s %s" % (rec.patient_id.surname or '',
                                        rec.patient_id.name or '')
                type_name=rec.type_id if rec.type_id else ""

                date_str=""
                if rec.date_deplacement:
                    date_str=rec.date_deplacement.strftime('%d/%m/%Y %H:%M')

                display_name=_("Deplacement du %s - %s ( %s)") % (date_str,patient_name,type_name)

            result.append((rec.id,display_name))
        return result 

    
    