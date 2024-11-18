from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _sql_constraints = [
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "Selling price must be positive!",
        ),
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "Expected price must be strictly positive!",
        ),
    ]
    _order = "id desc"

    @staticmethod
    def _default_availability_date():
        # Lấy ngày hiện tại
        today = datetime.today()
        # Tính toán ngày trong 3 tháng tới
        three_months_later = today + timedelta(days=90)  # 3 tháng = 90 ngày
        return three_months_later.date()

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            offer_prices = record.offer_ids.mapped("price")
            record.best_price = max(offer_prices, default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "N"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("You can not sell canceled properties")
            else:
                record.state = "sold"
        return True

    def action_canceled(self):
        for record in self:
            if record.state not in ("new", "offer_received"):
                raise UserError("You can only cancel new or offer received properties")
            else:
                record.state = "canceled"
        return True

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if (
                float_compare(
                    record.selling_price,
                    0.9 * record.expected_price,
                    precision_rounding=0.01,
                )
                < 0
                and record.state == "sold"
            ):
                raise ValidationError(
                    "Selling price must be at least 90% of the expected price!"
                )

    @api.ondelete(at_uninstall=False)
    def _check_property_state_on_delete(self):
        for record in self:
            if record.state not in ["new", "canceled"]:
                raise UserError(
                    "You can only delete properties that are 'New' or 'Canceled'."
                )

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: self._default_availability_date(),
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedroom = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        [("N", "North"), ("S", "South"), ("E", "East"), ("W", "West")],
        string="Garden Orientation",
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        default="new",
        string="State",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    salesman_id = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", readonly=True, copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(string="Total Area", compute="_compute_total_area")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")
