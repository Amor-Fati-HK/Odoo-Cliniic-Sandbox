"""
File: room.py
Author: HK
Room and bloc models for the clinic management module
"""
from odoo import models,fields,api,_
from odoo.exceptions import ValidationError

class bloc_type(models.Model):
    _name="clinic.bloc.type"
    _description="Type de bloc"

    name=fields.Char(string="Type du bloc")
    _sql_constraints=[
            ('name_unique','UNIQUE(name)','Ce type existe deja !')
    ]
    
class bloc(models.Model):
    _name="clinic.bloc"
    _description="Bloc clinique"

    bloc_num=fields.Integer(string="Numero du Bloc", required=True, help="Exp: 1")
    etage=fields.Integer(string="Etage", required=True)
    type_id=fields.Many2one('clinic.bloc.type',string="Type de bloc", required=True)
    role=fields.Selection([
        ('consult','Consultation'),
        ('intervention','Intervention'),
    ], string="Dédié aux ", required=True)

    _sql_constraints=[
            ('bloc_unique','UNIQUE(bloc_num)','Ce bloc existe deja !')
    ]

    def name_get(self):
        result=[]
        for rec in self:
            if rec.bloc_num:
                display_name=_("Bloc %s")%(rec.bloc_num)
            result.append((rec.id,display_name))
        return result

class room_type(models.Model):
    _name="clinic.room.type"
    _description="Type de salle"

    name=fields.Char(string="Type de salle")
    _sql_constraints=[
            ('name_unique','UNIQUE(name)','Ce type existe deja !')
    ]
    
class room(models.Model):
    _name="clinic.room"
    _description="Salle clinique"

    bloc_id=fields.Many2one('clinic.bloc',string="Bloc", required=True)
    room_num=fields.Integer(string="Numero de salle", required=True)
    room_full_num=fields.Integer(string="Salle", compute="_compute_room_full_num")
    type_id=fields.Many2one('clinic.room.type',string="Type de salle", required=True)
    bloc_role=fields.Selection(related="bloc_id.role", string="Role du bloc", readonly=True)
    consultation_ids=fields.One2many('clinic.consultation','room_id',
                                     string="Historique des consultations")
    

    num_bed=fields.Integer(string="Nombre de Lits", required=False)
    patient_ids=fields.Many2many('clinic.patient', string="Patients")
    medecin_ids=fields.Many2many('clinic.medecin', string="Medecin assignes")
    disponibility=fields.Boolean(string="Disponibilite" ,default=True,)

    @api.constrains('num_bed')
    def _check_num_bed(self):
        for s in self:
            if s.num_bed<0:
                raise ValidationError(_("Nombre de lits invalide !"))

    @api.constrains('room_num')
    def _check_room_num(self):
        for s in self:
            if s.room_num >99:
                raise ValidationError(_("Le numero de salle doit etre inferieur a 100 !"))
            elif s.room_num<=0:
                raise ValidationError(_("Numero de salle invalide !"))


    @api.depends('bloc_id','room_num')
    def _compute_room_full_num(self):
        for s in self:
            if s.bloc_id:
                if s.room_num:
                    s.room_full_num=(s.bloc_id.bloc_num*100)+s.room_num
                else:
                    s.room_full_num=0
            else:
                s.room_full_name=0

    def name_get(self):
        result=[]
        for rec in self:
            if rec.room_full_num:
                display_name=_("Salle %s")%(rec.room_full_num)
            result.append((rec.id,display_name))
        return result

    
    



