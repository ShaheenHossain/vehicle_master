from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # your_ref = fields.Char(string="Your Ref")
    # our_ref = fields.Char(string="Our Ref")
    inquiry_date = fields.Date(string="Inquiry Date")
    deadline_date = fields.Date(string="Deadline")

    # your_ref = fields.Char(string="Your Ref", related="res.partner.partner_id.your_ref", store=True, readonly=False)
    # our_ref = fields.Char(string="Our Ref", related="res.partner.partner_id.our_ref", store=True, readonly=False)

    your_ref = fields.Many2one('res.partner', string='Your Ref', required=True)
    our_ref = fields.Many2one('res.partner', string='Our Ref', required=True)



    vehicle_ids = fields.One2many(
        'vehicle.master',
        'partner_id',
        string='Vehicles'
    )


    # vehicle_ids = fields.Many2many(
    #     'vehicle.master',
    #     string='Vehicles'
    # )

    @api.onchange('partner_id')
    def _onchange_partner_id_vehicle_ids(self):
        for order in self:
            if order.partner_id:
                # Dynamically set domain: only vehicles of this partner
                return {
                    'domain': {
                        'vehicle_ids': [('partner_id', '=', order.partner_id.id)]
                    },
                    'value': {
                        'vehicle_ids': [],  # reset selection if partner changes
                    }
                }
            else:
                return {
                    'domain': {'vehicle_ids': []},
                    'value': {'vehicle_ids': []},
                }


    # vehicle_id = fields.Many2one('vehicle.master', string="Vehicle")


    # @api.onchange('partner_id')
    # def _onchange_partner_id_vehicle(self):
    #     for order in self:
    #         if order.partner_id:
    #             order.vehicle_id = False
    #             return {'domain': {'vehicle_id': [('partner_id', '=', order.partner_id.id)]}}
    #         else:
    #             return {'domain': {'vehicle_id': []}}