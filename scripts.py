import argparse
import os
import random
import sys

import django
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist


def fix_marks(schoolkid):
    marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    for mark in marks:
        mark.points = 5
        mark.save()


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid, subject):
    praises = [
        'Молодец!', 'Отлично!', 'Хорошо!', 'Сказано здорово – просто и ясно!',
        'Очень хороший ответ!', 'Талантливо!', 'Уже существенно лучше!',
        'Потрясающе!', 'Замечательно!', 'Прекрасное начало!', 'Так держать!'
    ]
    lessons = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject
    ).order_by('-date')
    if not lessons:
        raise ObjectDoesNotExist
    lesson = lessons.first()
    Commendation.objects.create(
        text=random.choice(praises),
        schoolkid=schoolkid,
        subject=lesson.subject,
        created=lesson.date,
        teacher=lesson.teacher
    )


def create_parser():
    parser = argparse.ArgumentParser(
        prog='Be A-student',
        description=f'Исправь плохие оценки, '
                    f'удали замечания и добавь похвалы от учителей'
    )
    subparsers = parser.add_subparsers(
        dest='command',
        title='Возможные команды',
        description=f'Команды, которые должны быть переданы '
                    f'в качестве первого параметра %(prog)s'
    )
    mark_parser = subparsers.add_parser(
        'mark',
        help='Исправить плохие оценки',
        description='Находит плохие оценки и исправляет на 5ки'
    )
    mark_parser.add_argument(
        '-n',
        '--name',
        nargs='+',
        required=True,
        help='Фамилия Имя'
    )
    amnesty_parser = subparsers.add_parser(
        'amnesty',
        help='Удалить замечания',
        description='Удаляет плохие замечания учителей'
    )
    amnesty_parser.add_argument(
        '-n',
        '--name',
        nargs='+',
        required=True,
        help='Фамилия Имя'
    )
    praise_parser = subparsers.add_parser(
        'praise',
        help='Похвалить себя',
        description='Добавить хвалебную запись по указанному предмету'
    )
    praise_parser.add_argument(
        '-n',
        '--name',
        nargs='+',
        required=True,
        help='Фамилия Имя'
    )
    praise_parser.add_argument(
        '-s',
        '--subject',
        required=True
    )
    return parser


def main():
    parser = create_parser()
    namespace = parser.parse_args()
    name = ' '.join(namespace.name)
    try:
        child = Schoolkid.objects.get(full_name__contains=name)
    except ObjectDoesNotExist:
        print(f'Студент с именем {name} не найден. '
              f'Проверь правильность имени.')
        sys.exit()
    except MultipleObjectsReturned:
        print(f'Найдено несколько студентов с именем {name}. Уточни запрос')
        sys.exit()

    if namespace.command == 'mark':
        fix_marks(child)
    elif namespace.command == 'amnesty':
        remove_chastisements(child)
    else:
        subject = namespace.subject
        try:
            create_commendation(child, subject.title())
        except ObjectDoesNotExist:
            print(f'Предмет "{subject}" не найден. '
                  f'Проверь правильность названия предмета')


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    django.setup()
    from datacenter.models import (Chastisement, Commendation, Lesson, Mark,
                                   Schoolkid)
    main()
