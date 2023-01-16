import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import models as m


with open('user_info.json', 'r') as user_file, open('fixtures/tests_data.json', 'r') as data_file:
    db_type, login, password, hostname, db_port, db_name = json.load(user_file).values()
    book_data = json.load(data_file)

DSN = f'{db_type}://{login}:{password}@{hostname}:{db_port}/{db_name}'
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
                        res = session.query(m.Book.book_title, m.Shop.shop_name, m.Sale.book_price, m.Sale.date_sale).\
                                    join(m.Publisher, m.Book.publisher_id==m.Publisher.publisher_id).\
                                    join(m.Stock, m.Stock.book_id==m.Book.book_id).\
                                    join(m.Sale, m.Sale.stock_id==m.Stock.stock_id).\
                                    join(m.Shop, m.Shop.shop_id==m.Stock.shop_id).\
                                    filter(m.Publisher.publisher_id==user_choice)
                        break
                    else:
                        print('Ответ введен некорректно. id должен состоять только из цифр.')
                break
            elif user_choice == '2':
                while (True):
                    user_choice = str(input('Введите фамилию:\n')).strip()
                    if user_choice != '':
                        res = session.query(m.Book.book_title, m.Shop.shop_name, m.Sale.book_price, m.Sale.date_sale).\
                                    join(m.Publisher, m.Book.publisher_id==m.Publisher.publisher_id).\
                                    join(m.Stock, m.Stock.book_id==m.Book.book_id).\
                                    join(m.Sale, m.Sale.stock_id==m.Stock.stock_id).\
                                    join(m.Shop, m.Shop.shop_id==m.Stock.shop_id).\
                                    filter(m.Publisher.publisher_name==user_choice)
                        break
                    else:
                        print('Введите что-нибудь.')
                break
            else:
                print('Ответ введен некорректно. Попробуйте ещё раз.')

        print()
        print('Название книги' + ' ' * 36, '|', 'Магазин' + ' ' * 8, '|', 'Цена' + ' ' * 4, '|', 'Дата продажи')
        for book, shop, price, date in res:
            print(f'{book: <50} | {shop: <15} | {price: <8} | {date: <13}')
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
