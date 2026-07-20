"""
File: intervention.py
Author: Hani Katti
Intervention model for the clinic module

"""

from odoo import models,fields,api,_
from odoo.exceptions import ValidationError

class intervention_type(models.Model):
    _name="clinic.intervention.type"
    _description="Type d'intervention clinique"

    name=fields.Char(string="Nom du type", required=True)
    _sql_constraints=[
        ('name_unique','UNIQUE(name)','Ce type d intervention existe deja !')
    ]

class intervention(models.Model):
    _name="clinic.intervention"
    _description="Intervention Clinique"

    patient_id=fields.Many2one('clinic.patient', ondelete="cascade", string="Patient", required=True)
    medecin_id=fields.Many2one('clinic.medecin', ondelete="cascade",string="Medecin", required=True)
    material_ids=fields.Many2many('clinic.material', string="Materiel Utilise")

    type_id=fields.Many2one('clinic.intervention.type',string="Type d'intervention",required=True)
    date_intervention=fields.Datetime(string="Date et Heure", required=True)    
    description=fields.Text(string="Description")
    patient_state=fields.Selection([
        ('dead','Decede'),
        ('critic','Critique'),
        ('stable','Stable'),
        ('healed','Guerri'),
    ])

    @api.model
    def create(self, vals):
        record = super(intervention, self).create(vals)
        if 'patient_state' in vals:
            record._sync_patient_state(vals['patient_state'])
        return record

    def write(self, vals):
        res = super(intervention, self).write(vals)
        if 'patient_state' in vals:
            for record in self:
                record._sync_patient_state(vals['patient_state'])
        return res
    
    def _sync_patient_state(self, state):
        
        if state == 'dead' and self.patient_id:
            self.patient_id.write({'decease': True})

    @api.model
    def _register_hook(self):
        self._cr.execute("UPDATE clinic_intervention SET patient_state = 'dead' WHERE patient_state='Dead';")
        return super(intervention, self)._register_hook()
    