from tabulate import tabulate

from tronclass_cli.command import Command
from tronclass_cli.middleware.api import ApiMiddleware
from tronclass_cli.utils import flatten_dict, unflatten_fields, dict_select, process_table_data


class CoursesCommand(Command):
    name = 'courses'
    middleware_classes = [ApiMiddleware]

    def _init_parser(self):
        fields = 'id,name,course_code,department(id,name),grade(id,name),klass(id,name),course_type,cover,' \
                 'small_cover,start_date,end_date,is_started,is_closed,academic_year_id,semester_id,credit,' \
                 'compulsory,second_name,display_name,created_user(id,name),org(is_enterprise_or_organization),' \
                 'org_id,instructors(id,name,email,avatar_small_url),public_scope,course_attributes(' \
                 'teaching_class_name,copy_status),audit_status,audit_remark,can_withdraw_course,imported_from,' \
                 'instructor_assistants(id),allow_clone,team_teachings(id,name,email) '
        default_fields = 'id,name,instructors.name'
        self._parser.add_argument('--fields', default=default_fields,
                                  help=f'fields to display, default fields: {default_fields}, supported fields: {fields}')

    def _exec(self, args):
        fields = args.fields.split(',')
        courses = list(self._ctx.api.get_courses(fields=unflatten_fields(fields)))
        if len(courses) == 0:
            print('No courses.')
        else:
            courses = [process_table_data(course, fields) for course in courses]
            print(tabulate(courses, headers='keys'))
