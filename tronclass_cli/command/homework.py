from tabulate import tabulate

from tronclass_cli.command import Command
from tronclass_cli.middleware.api import ApiMiddleware
from tronclass_cli.utils import dict_select, process_table_data


class HomeworkCommand(Command):
    name = 'courses'
    middleware_classes = [ApiMiddleware]

    def _init_parser(self):
        self._parser.add_argument('course_id')

        fields = 'accepting_submission,assign_group_ids,assign_student_ids,can_make_up_homework,completion_criterion,' \
                 'completion_criterion_key,completion_criterion_value,created_at,data.announce_score_type,' \
                 'data.description,data.has_assign_target,data.homework_score_percentage.instructor_score_percentage,' \
                 'data.homework_type,data.other_resources,data.score_percentage,data.show_rubric,' \
                 'data.submit_closed_time,data.submit_times,deadline,end_time,group_set_id,group_set_name,' \
                 'has_assign_group,has_assign_student,id,inter_score_map.end_time,inter_score_map.id,' \
                 'inter_score_map.is_closed,inter_score_map.is_started,inter_score_map.pieces_cnt,' \
                 'inter_score_map.start_time,intra_rubric_id,intra_rubric_instance.conditions,' \
                 'intra_rubric_instance.id,intra_rubric_instance.name,intra_rubric_instance.rubric.conditions,' \
                 'intra_rubric_instance.rubric.created_at,intra_rubric_instance.rubric.created_by.id,' \
                 'intra_rubric_instance.rubric.created_by.name,intra_rubric_instance.rubric.engage_number,' \
                 'intra_rubric_instance.rubric.id,intra_rubric_instance.rubric.name,' \
                 'intra_rubric_instance.rubric.updated_at,intra_rubric_instance_id,intra_score_map.end_time,' \
                 'intra_score_map.id,intra_score_map.is_closed,intra_score_map.start_time,' \
                 'is_announce_score_time_passed,is_assigned_to_all,is_inter_review_by_submitter,make_up_closed_time,' \
                 'module_id,need_make_up,non_submit_times,prerequisites,rubric_id,rubric_instance.conditions,' \
                 'rubric_instance.id,rubric_instance.name,rubric_instance.rubric.conditions,' \
                 'rubric_instance.rubric.created_at,rubric_instance.rubric.created_by.id,' \
                 'rubric_instance.rubric.created_by.name,rubric_instance.rubric.engage_number,' \
                 'rubric_instance.rubric.id,rubric_instance.rubric.name,rubric_instance.rubric.updated_at,' \
                 'rubric_instance_id,score_percentage,score_published,sort,start_time,submission_closed,' \
                 'submission_started,submit_by_group,submit_times,submitted,submitted_status,syllabus_id,' \
                 'teaching_unit_id,title,type,updated_at,uploads,user_submit_count '
        default_fields = 'id,title,deadline'
        self._parser.add_argument('--fields', default=default_fields,
                                  help=f'fields to display, default fields: {default_fields}, supported fields: {fields}')

    def _exec(self, args):
        fields = args.fields.split(',')
        homework = list(self._ctx.api.get_homework(args.course_id))
        if len(homework) == 0:
            print('No homework.')
        else:
            homework = [process_table_data(hw, fields) for hw in homework]
            print(tabulate(homework, headers='keys'))
