from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "Offer price must be strictly positive!")
    ]
    _order = "price desc"

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date and record.validity:
                record.date_deadline = record.create_date + timedelta(
                    days=record.validity
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                delta = record.date_deadline - record.create_date
                record.validity = delta.days

    def action_accept(self):
        for record in self:
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
    
    @api.model
    def create(self, vals):
        # Fetch the property associated with the offer
        property_id = vals.get('property_id')
        if property_id:
            property_record = self.env['estate.property'].browse(property_id)

            # Ensure the offer price is higher than any existing offer
            if vals.get('price', 0) < property_record.best_price:
                raise ValidationError("The offer price must be higher than the current best offer.")

            # Change property state to 'Offer Received' when an offer is created
            if property_record.state == 'new':
                property_record.state = 'offer_received'

        return super(EstatePropertyOffer, self).create(vals)
    
    

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False, string="Status"
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    create_date = fields.Date(string="Create Date", default=fields.Date.today)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    property_type_id = fields.Many2one(related="property_id.property_type_id", string="Property Type", store=True)
