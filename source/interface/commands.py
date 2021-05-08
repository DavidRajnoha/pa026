import click
from source.interface.app_logic import schedule_categories


@click.group()
def cli():
    pass


@click.command('schedule_categories')
@click.option('--oris_id')
@click.option('--course_definition')
@click.option('--same_start_req')
@click.option('--specific_time_req')
@click.option('--ignore_categories')
@click.option('--interval')
@click.option('--concurrent_slots')
def schedule_categories_command(oris_id, course_definition, same_start_req, specific_time_req,
                        ignore_categories, interval, concurrent_slots):
    ignore_categories_list = ignore_categories.split(",")
    schedule_categories(oris_id, course_definition, same_start_req, specific_time_req,
                        ignore_categories_list, int(interval), int(concurrent_slots))


cli.add_command(schedule_categories_command)
