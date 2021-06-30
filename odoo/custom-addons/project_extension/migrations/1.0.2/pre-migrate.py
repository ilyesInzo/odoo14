
def migrate(cr, version):
    print('/******************** Hello Friends *****************///')
    cr.execute('update project_project pr set department_primary_id = (select Distinct(emp.department_id) from hr_employee as emp where emp.user_id is not null and pr.user_id = emp.user_id )')
