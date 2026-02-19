from odoo import models, fields, api, _


class VehicleMaster(models.Model):
    _name = 'vehicle.master'
    _description = 'Vehicle'

    # Owner
    partner_id = fields.Many2one('res.partner', string='Owner', required=True)

    brand_id = fields.Many2one('vehicle.brand', string='Brand')
    model_id = fields.Many2one('vehicle.model', string='Model', domain="[('brand_id','=',brand_id)]")
    year = fields.Selection([(str(y), str(y)) for y in range(1980, 2031)], string='Year')
    year_from = fields.Integer(string="Year From")
    year_to = fields.Integer(string="Year To")
    # variant = fields.Char(string='Variant')
    variant_id = fields.Many2one('vehicle.variant', string='Variant', domain="[('model_id','=',model_id)]")
    license_plate = fields.Char(string='License Plate', required=True)
    vin = fields.Char(string='Chassis Number')
    color = fields.Char(string='Color')
    fuel_type = fields.Char(string='Fuel Type')

    first_registration = fields.Date(string='First Registration')
    mileage = fields.Integer(string='Mileage')

    type_code = fields.Char(string='Type Code')
    # master_number = fields.Char(string='Master Number')
    master_number = fields.Char(string='Master Number', readonly=True, copy=False)
    last_service_date = fields.Date(string='Last Service Date')

    vehicle_id = fields.Many2one('vehicle.master', string="Vehicle")

    name = fields.Char(string='Vehicle Name', compute='_compute_vehicle_name', store=True)

    @api.depends('brand_id', 'model_id', 'year')
    def _compute_vehicle_name(self):
        for vehicle in self:
            brand = vehicle.brand_id.name if vehicle.brand_id else 'Brand'
            model = vehicle.model_id.name if vehicle.model_id else 'Model'
            year = vehicle.year or ''
            vehicle.name = f"{brand} {model} {year}".strip()


    @api.model
    def create(self, vals):
        if not vals.get('master_number'):
            vals['master_number'] = self._generate_master_number()
        return super(VehicleMaster, self).create(vals)


    @api.model
    def _generate_master_number(self):
        last_vehicle = self.search([], order='id desc', limit=1)
        if last_vehicle and last_vehicle.master_number:
            last = last_vehicle.master_number.replace('.', '')
            new = str(int(last) + 1).zfill(9)  # 9 digits
        else:
            new = '000000001'
        return f"{new[:3]}.{new[3:6]}.{new[6:]}"




class ResPartner(models.Model):
    _inherit = 'res.partner'

    vehicle_ids = fields.One2many('vehicle.master', 'partner_id', string='Vehicles')


class VehicleBrand(models.Model):
    _name = 'vehicle.brand'
    _description = 'Vehicle Brand'

    name = fields.Char(string="Brand Name", required=True)
    logo = fields.Image(string="Logo", max_width=256, max_height=256)
    model_ids = fields.One2many('vehicle.model', 'brand_id', string="Models")

    active = fields.Boolean(default=True)

    model_count = fields.Integer(string="Model Count", compute="_compute_model_count")

    @api.depends('model_ids')
    def _compute_model_count(self):
        for record in self:
            record.model_count = len(record.model_ids)

    _sql_constraints = [
        ('brand_name_unique', 'unique(name)', 'Brand name must be unique!')
    ]


class VehicleModel(models.Model):
    _name = 'vehicle.model'
    _description = 'Vehicle Model'

    name = fields.Char(string="Model Name", required=True)
    brand_id = fields.Many2one('vehicle.brand', string="Brand", required=True, ondelete='cascade')

    _sql_constraints = [
        ('model_brand_unique',
         'unique(name, brand_id)',
         'Model already exists for this brand!')
    ]


class VehicleVariant(models.Model):
    _name = 'vehicle.variant'
    _description = 'Vehicle Variant'

    name = fields.Char(required=True)
    model_id = fields.Many2one('vehicle.model', required=True, ondelete='cascade' )

    year_from = fields.Integer(string="Year From")
    year_to = fields.Integer(string="Year To")

    _sql_constraints = [
        ('variant_unique',
         'unique(name, model_id)',
         'Variant already exists for this model!')
    ]