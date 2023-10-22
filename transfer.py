#!/usr/bin/env python3

import os
import time
import pyfiglet
import re
import sys
from termcolor import colored
from InquirerPy import inquirer
from InquirerPy.validator import PathValidator
from InquirerPy import get_style
from tqdm import tqdm
from datetime import datetime
from apple import Apple
from exporter.export_loader import load_exporter

errors = []


def render_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = pyfiglet.figlet_format('APPLE USER TRANSFER!', font='slant')
    colored_banner = colored(banner, 'blue')
    print(colored_banner)


def answer_options():
    team_key_id_format_regex = r'^[A-Z0-9]{10}$'
    client_id_format_regex = r'^[a-z_][a-z0-9_]*(?:\.[a-z_][a-z0-9_]*)*$'

    private_key_file = inquirer.filepath(
        default='./',
        message='Please select or type Apple private key(p8) file.',
        validate=PathValidator(is_file=True, message='This is not a valid apple private key file.'),
        only_files=True
    ).execute()

    source_sub_file = inquirer.filepath(
        default='./',
        message='Select or enter the file containing the list of subs you want to transfer.',
        validate=PathValidator(is_file=True, message='Invalid source sub list file.'),
        only_files=True
    ).execute()

    team_id = inquirer.text(
        message='What was your team ID before transferring you Apple account?',
        validate=lambda input_team_id: bool(re.match(team_key_id_format_regex, input_team_id)),
        invalid_message='Invalid team id (10 characters of uppercase alphabets and numbers)'
    ).execute()

    key_id = inquirer.secret(
        message='Please enter your key ID',
        validate=lambda input_key_id: bool(re.match(team_key_id_format_regex, input_key_id)),
        invalid_message='Invalid key id (10 characters of uppercase alphabets and numbers)'
    ).execute()

    client_id = inquirer.text(
        message='Please enter your client ID. (ex: me.modorigoon.app.exam)',
        validate=lambda input_client_id: bool(re.match(client_id_format_regex, input_client_id)),
        invalid_message='Invalid client id (ex: me.modorigoon.app.exam)'
    ).execute()

    target_team_id = inquirer.text(
        message='What is the target team ID to transfer to?',
        validate=lambda input_target_team_id: bool(re.match(team_key_id_format_regex, input_target_team_id)),
        invalid_message='Invalid target team id (10 characters of uppercase alphabets and numbers)'
    ).execute()

    style = get_style({'pointer': '#FFC0CB bold', 'questionmark': '#FFFF00 bold'}, style_override=False)

    export_type = inquirer.select(
        message='What type of file do you want to save as?',
        choices=['json', 'CSV', 'XML', 'SQL'],
        style=style,
        default='json'
    ).execute()

    sql_table_name = ''
    sql_column_name = ''
    if export_type == 'SQL':
        sql_table_name = inquirer.text(
            message="What is the table name where the Apple sub file is stored? (default: subs)",
            default='subs'
        ).execute()
        sql_column_name = inquirer.text(
            message="What is the column name where the sub is stored? (default: sub)",
            default='sub'
        ).execute()

    file_name = inquirer.text(
        message='Enter a name for the file where you want to save the results. (optional)'
    ).execute()

    return {
        'private_key_file': private_key_file,
        'source_sub_file': source_sub_file,
        'team_id': team_id,
        'key_id': key_id,
        'client_id': client_id,
        'target_team_id': target_team_id,
        'export_type': export_type,
        'if_export_sql_table_name': sql_table_name,
        'if_export_sql_column_name': sql_column_name,
        'file_name': file_name
    }


def get_transfer_target_subs(source_subs_file):
    source_subs = []
    subs = open(source_subs_file, 'r')
    for sub in subs:
        source_subs.append(sub.strip())
    return source_subs


def error_result_handle(result):
    if 'error' in result:
        row = f'error: {result["error"]}'
        if 'error_description' in result:
            row += f', description: {result["error_description"]}'
        errors.append(f'{row}\n')


def save_error_logs():
    log_file_name = f'transfer_failed_{datetime.now().strftime("%Y%m%d%H%M")}.err'
    with open(log_file_name, 'w') as err_file:
        err_file.writelines(errors)
    print(colored(f'{len(errors)} sub transfer failed (log file: {log_file_name})', 'red'))


def transfer(apple: Apple, options: dict):
    target_subs = get_transfer_target_subs(options['source_sub_file'])
    target_length = len(target_subs)

    results = []
    with tqdm(total=target_length) as tbar:
        for sub in target_subs:
            try:
                time.sleep(200 / 1000)
                transfer_result = apple.transfer_sub(sub)
                if 'transfer_sub' in transfer_result:
                    result = {'source': sub, 'to': transfer_result['transfer_sub']}
                    results.append(result)
                    desc = f'😃 Transfer user {sub} '
                else:
                    error_result_handle(transfer_result)
                    desc = f'😵 Transfer failed user: {sub}'
            except Exception:
                desc = f'😵 Transfer failed user: {sub}'

            tbar.set_description(desc)
            tbar.update(1)

    return results


def export(export_type: str, file_name: str, export_target_result: list, table_name=None, column_name=None):
    exporter = load_exporter(export_type, file_name)
    if export_type.lower() == 'sql':
        exporter.set_table_name(table_name)
        exporter.set_column_name(column_name)
    exporter.export(export_target_result)
    print(colored(f'\nExport file name: {exporter.file_name} (Transfer {len(export_target_result)} subs)', 'yellow'))


def main():
    render_banner()
    options = answer_options()

    proceed_confirm = inquirer \
        .confirm(message='Proceed?', default=True, confirm_letter='y', reject_letter='n').execute()

    if proceed_confirm:
        apple = Apple(private_key_file=options['private_key_file'], team_id=options['team_id'],
                      key_id=options['key_id'],
                      client_id=options['client_id'], target_team_id=options['target_team_id'])
        auth_result = apple.authorize()
        if not auth_result:
            sys.exit()
        transfer_result = transfer(apple, options)
        export(options['export_type'], options['file_name'], transfer_result,
               options['if_export_sql_table_name'], options['if_export_sql_column_name'])
        if len(errors) > 0:
            save_error_logs()
    elif not proceed_confirm:
        print(colored('👋 Bye ~', 'yellow'))


if __name__ == '__main__':
    main()
    print('\n\n')
