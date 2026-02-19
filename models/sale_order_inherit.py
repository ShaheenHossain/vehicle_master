from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    inquiry_date = fields.Date(string="Inquiry Date")
    deadline_date = fields.Date(string="Deadline")

    your_ref = fields.Many2one('res.partner', string='Your Ref', required=True)
    our_ref = fields.Many2one('res.partner', string='Our Ref', required=True)

    brand_id = fields.Many2one('vehicle.brand', string='Brand')
    model_id = fields.Many2one('vehicle.model', string='Model', domain="[('brand_id','=',brand_id)]")

    year = fields.Selection([(str(y), str(y)) for y in range(1980, 2031)],
        string='Year')

    year_from = fields.Integer(string="Year From")
    year_to = fields.Integer(string="Year To")

    variant_id = fields.Many2one(
        'vehicle.variant',
        string='Variant',
        domain="[('model_id','=',model_id)]"
    )

    license_plate = fields.Char(
        string='License Plate',
        required=True
    )

    vin = fields.Char(string='Chassis Number')
    color = fields.Char(string='Color')
    fuel_type = fields.Char(string='Fuel Type')

    first_registration = fields.Date(string='First Registration')
    mileage = fields.Integer(string='Mileage')

    type_code = fields.Char(string='Type Code')
    # master_number = fields.Char(string='Master Number')
    master_number = fields.Char(string='Master Number', readonly=True, copy=False)
    last_service_date = fields.Date(string='Last Service Date')


    # vehicle_ids = fields.Many2many(
    #     'vehicle.master',
    #     'sale_order_vehicle_rel',  # Relation table name
    #     'order_id',  # Current model column
    #     'vehicle_id',  # Target model column
    #     string='Vehicles'
    # )
    #
    #
    # @api.onchange('partner_id')
    # def _onchange_partner_id_vehicle_ids(self):
    #     # Clear selected vehicles if the partner changes
    #     self.vehicle_ids = [(5, 0, 0)]
    #     if self.partner_id:
    #         return {'domain': {'vehicle_ids': [('partner_id', '=', self.partner_id.id)]}}
    #     return {'domain': {'vehicle_ids': []}}
    #
    # def _prepare_invoice(self):
    #     """ Pass the custom fields to the invoice values dictionary """
    #     invoice_vals = super(SaleOrder, self)._prepare_invoice()
    #     invoice_vals.update({
    #         'inquiry_date': self.inquiry_date,
    #         'deadline_date': self.deadline_date,
    #         # Use .id to avoid the "can't adapt type" error
    #         'your_ref': self.your_ref.id if self.your_ref else False,
    #         'our_ref': self.our_ref.id if self.our_ref else False,
    #         # For Many2many, use the command format [(6, 0, ids)]
    #         'vehicle_ids': [(6, 0, self.vehicle_ids.ids)],
    #     })
    #     return invoice_vals

    vehicle_id = fields.Many2one(
        'vehicle.master',
        string='Vehicle'
    )


    @api.onchange('partner_id')
    def _onchange_partner_id_vehicle_id(self):
        self.vehicle_id = False
        if self.partner_id:
            return {
                'domain': {
                    'vehicle_id': [('partner_id', '=', self.partner_id.id)]
                }
            }
        return {'domain': {'vehicle_id': []}}

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        invoice_vals.update({
            'inquiry_date': self.inquiry_date,
            'deadline_date': self.deadline_date,
            'your_ref': self.your_ref.id if self.your_ref else False,
            'our_ref': self.our_ref.id if self.our_ref else False,
            'vehicle_id': self.vehicle_id.id if self.vehicle_id else False,
        })
        return invoice_vals



class AccountMove(models.Model):
    _inherit = 'account.move'


    inquiry_date = fields.Date(string="Inquiry Date")
    deadline_date = fields.Date(string="Deadline")

    your_ref = fields.Many2one('res.partner', string='Your Ref', required=True)
    our_ref = fields.Many2one('res.partner', string='Our Ref', required=True)

    vehicle_ids = fields.Many2many('vehicle.master', 'account_move_vehicle_rel',
            'move_id', 'vehicle_id', string='Vehicles')

    vehicle_id = fields.Many2one(
        'vehicle.master',
        string='Vehicle'
    )


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    inquiry_date = fields.Date(string="Inquiry Date")
    deadline_date = fields.Date(string="Deadline")

    your_ref = fields.Many2one('res.partner', string='Your Ref', required=True)
    our_ref = fields.Many2one('res.partner', string='Our Ref', required=True)

    # vehicle_ids = fields.Many2many('vehicle.master', 'account_move_vehicle_rel',
    #         'move_id', 'vehicle_id', string='Vehicles')

    vehicle_id = fields.Many2one(
        'vehicle.master',
        string='Vehicle'
    )
