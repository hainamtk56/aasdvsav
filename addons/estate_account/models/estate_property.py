from odoo import models, fields, Command

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        # Gọi phương thức gốc từ lớp cơ sở
        super(EstateProperty, self).action_sold()

        # Tạo hóa đơn mới
        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,  # Lấy partner_id từ tài sản hiện tại
            'move_type': 'out_invoice',  # Chọn loại hóa đơn là hóa đơn khách hàng
            'invoice_line_ids': [
                Command.create({
                    'name': '6% của giá bán',  # Mô tả cho dòng hóa đơn đầu tiên
                    'quantity': 1,  # Số lượng
                    'price_unit': self.selling_price * 0.06,  # Giá đơn vị (6% của giá bán)
                }),
                Command.create({
                    'name': 'Phí hành chính',  # Mô tả cho dòng hóa đơn thứ hai
                    'quantity': 1,  # Số lượng
                    'price_unit': 100.00,  # Giá đơn vị (100.00 phí hành chính)
                }),
            ],
        })
