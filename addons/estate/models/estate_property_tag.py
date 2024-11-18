from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _sql_constraint = [
        ('name_uniq', 'UNIQUE(name)', 'Tag name must be unique!')
    ]
    _order = "name"

    name = fields.Char(string='Property Tag Name', required=True)
    color = fields.Integer(string="Color")