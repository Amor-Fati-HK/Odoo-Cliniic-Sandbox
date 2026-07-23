"""
File: consultation.py
Author: Hani Katti
Consultation
"""

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class consultation(models.Model):
    _name="clinic.consultation"
    _description="Consultations"

    patient_id=fields.Many2one('clinic.patient', ondelete="cascade", string="Patient", required=True)
    medecin_id=fields.Many2one('clinic.medecin', ondelete="cascade",string="Medecin", required=True)
    material_ids=fields.Many2many('clinic.material', string="Materiel Utilise")
    material_count=fields.Integer(compute="_compute_material_count")
    date_consultation=fields.Datetime(string="Date et Heure",
                                     default=fields.Datetime.now)
    symptoms=fields.Text(string="Symptomes constates")
    diagnostic=fields.Text(string="Diagnostique")
    ordonnance=fields.Text(string="Prescription / Ordonnance")

    temperature=fields.Float(string="Temperature", required=False)
    tension=fields.Char(string="Tension arterielle")
    prix_consultation=fields.Float(string="Prix (DZD)", default=2000.0)
    salle_consultation=fields.Integer(string="Salle", required=True)


    state=fields.Selection([
        ('draft','Brouillon'),
        ('confirmed','Confirmé / En cours'),
        ('done','Terminé'),
        ('cancel','Annulé'),
    ], string="Statut", default='draft', traking=True)

    @api.depends('material_ids')
    def _compute_material_count(self):
        for s in self:
            s.material_count=len(s.material_ids)

    def action_confirm(self):
        """Swithc the consultaion to 'Confirmed' and blocks the material used """
        for s in self:
            s.state='confirmed'
            for material in s.material_ids:
                if material.state == "available":
                    material.state = 'in_use'
        return True
    
    def action_done(self):
        """Switch to 'Finished' and free the material used"""
        for s in self:
            s.state='done'
            for material in s.material_ids:
                if material.state=='in_use':
                    material.state='available'
        return True

    @api.constrains('prix_consultation')
    def _check_prix_consult(self):
        """Check price validation"""
        for s in self:
            if s.prix_consultation<0:
                raise ValidationError(_("Prix invalide"))

    @api.constrains('date_consultation','medecin_id','salle_consultation')
    def _check_consultation_overlap(self):
        for rec in self:
            if rec.date_consultation:
                duplicate_doctor=self.search([
                    ('date_consultation','=',rec.date_consultation),
                    ('medecin_id','=',rec.medecin_id.id),
                    ('id','!=',rec.id)
                ])
                if duplicate_doctor:
                    raise ValidationError(_("Le medecin %s est deja occupe par une autre consultation le %s !") %(rec.medecin_id.name, rec.date_consultation))

                if rec.salle_consultation:
                    duplicate_room=self.search([
                        ('date_consultation','=',rec.date_consultation),
                        ('salle_consultation','=',rec.salle_consultation),
                        ('id','!=',rec.id)
                    ])
                    if duplicate_room:
                        raise ValidationError(_("La salle numero %s est deja reservee pour une autre consultation le %s !") % (rec.salle_consultation, rec.date_consultation))
                    