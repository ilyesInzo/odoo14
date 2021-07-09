from odoo import api, SUPERUSER_ID
import logging
_logger = logging.getLogger(__name__)

def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    print('/******************** Hello Friends *****************///')
    cr.execute('update project_project pr set department_primary_id = (select Distinct(emp.department_id) from hr_employee as emp where emp.user_id is not null and pr.user_id = emp.user_id )')
