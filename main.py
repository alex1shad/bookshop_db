import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import models as m


with open('user_info.txt', 'rt') as user_file, open('fixtures/tests_data.json', 'r') as data_file:
    db_type = user_file.readline().replace('db_type=', '').strip()
    login = user_file.readline().replace('login=', '').strip()
    password = user_file.readline().replace('password=', '').strip()
    host_name = user_file.readline().replace('hostname=', '').strip()
    db_port = user_file.readline().replace('db_port=', '').strip()
    db_name = user_file.readline().replace('db_name=', '').strip()
    book_data = json.load(data_file)


DSN = f'{db_type}://{login}:{password}@{host_name}:{db_port}/{db_name}'
engine = sqlalchemy.create_engine(DSN)
m.create_table(engine)

Session = sessionmaker(bind=engine)
session = Session()

for el in book_data:
    model_dict = {'publisher': m.Publisher,
                  'book': m.Book,
                  'shop': m.Shop,
                  'stock': m.Stock,
                  'sale': m.Sale
                  }
    model_class = model_dict[el.get('model')]
    session.add(model_class(**el.get('fields')))
session.commit()


def book_info():
    while (True):
        while (True):
            user_choice = str(input('Укажите критерий поиска.\n'
                                    'Если id - введите "1", если фамилия - введите "2":\n')).strip()
            if user_choice == '1':
                while (True):
                    user_choice = str(input('Введите id:\n')).strip()
                    if user_choice.isdigit() and user_choice != '':
                        qw = session.query(m.Publisher.publisher_id, m.Book.book_title, m.Shop.shop_name,
                            m.Sale.book_price, m.Sale.date_sale).\
                            join(m.Book).join(m.Stock).join(m.Shop).join(m.Sale).\
                            filter(m.Publisher.publisher_id == int(user_choice))
                        break
                    else:
                        print('Ответ введен некорректно. id должен состоять только из цифр.')
                break
            elif user_choice == '2':
                while (True):
                    user_choice = str(input('Введите фамилию:\n')).strip()
                    if user_choice != '':
                        qw = session.query(m.Publisher.publisher_name, m.Book.book_title, m.Shop.shop_name,
                            m.Sale.book_price, m.Sale.date_sale).\
                            join(m.Book).join(m.Stock).join(m.Shop).join(m.Sale).\
                            filter(m.Publisher.publisher_name.ilike(user_choice))
                        break
                    else:
                        print('Введите что-нибудь.')
                break
            else:
                print('Ответ введен некорректно. Попробуйте ещё раз.')

        print()
        print('Название книги' + ' ' * 36, '|', 'Магазин' + ' ' * 8, '|', 'Цена' + ' ' * 4, '|', 'Дата продажи')
        print('-' * 50, '|', '-' * 15, '|', '-' * 8, '|', '-' * 13)
        for el in qw:
            if len(el[1]) != 50:
                book_name = el[1] + ' ' * (50 - len(el[1]))
            else:
                book_name = el[1]
            if len(el[2]) != 15:
                shop_name = el[2] + ' ' * (15 - len(el[2]))
            else:
                shop_name = el[2]
            if len(str(el[3])) != 8:
                book_price = str(el[3]) + ' ' * (8 - len(str(el[3])))
            else:
                book_price = str(el[3])
            data_without_time = str(el[4]).split()[0]
            print(f'{book_name} | {shop_name} | {book_price} | {data_without_time}')
        print('-' * 50, '|', '-' * 15, '|', '-' * 8, '|', '-' * 13)
        while (True):
            final_choice = str(input('Введите "1", чтобы продолжить; введите "2", чтобы выйти:\n'))
            if final_choice == '1':
                break
            elif final_choice == '2':
                return
            else:
                print('Ответ введен некорректно. Попробуйте ещё раз.')


book_info()
session.close()
