from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _sql_constraint = [
        ('name_uniq', 'UNIQUE(name)', 'Property Type name must be unique!')
    ]
    _order = "name"
    
    @api.depends('property_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    name = fields.Char(string='Property Type Name', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    sequence = fields.Integer('Sequence')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    offer_count = fields.Integer(compute='_compute_offer_count')