from sqlalchemy import create_engine, String, Float, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy.orm import DeclarativeBase


engine = create_engine(f"postgresql+psycopg2://postgres:'Your_username'@localhost:'Your_host'/'Your_Table_nam'e", echo=True)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    def create_db(self):
        Base.metadata.create_all(engine)

    def drop_db(self):
        Base.metadata.drop_all(engine)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String(15))
    address: Mapped[str] = mapped_column(String(50))
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="product")



class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'),nullable = False)
    product: Mapped["Product"] = relationship("Product", back_populates="orders")
    user: Mapped['User'] = relationship("User", back_populates='orders')


def init_db():
    base = Base()
    base.create_db() 

    with Session() as session:
        products = [
            Product(name="Nike Air Max", description="Класичні кросівки для бігу", price=4300,
                    image="https://s3.eu-north-1.amazonaws.com/lms.goiteens-files/b0a4323b-a7a6-4da7-94f8-7fb6b3012a57nike_air_max.png"),
            Product(name="Adidas Ultraboost", description="Легкі та комфортні кросівки", price=3100,
                    image="https://s3.eu-north-1.amazonaws.com/lms.goiteens-files/cbced02e-673e-4f6f-9557-51d99938fe8badidas_ultraboost.png"),
            Product(name="Puma RS-X", description="Стильні кросівки для міста", price=3750,
                    image="https://s3.eu-north-1.amazonaws.com/lms.goiteens-files/be789244-fd99-451b-83ea-33f06ea53d6dpuma_rsx.png"),
        ]
        session.add_all(products)
        session.commit()

# init_db()



def get_products():
    with Session() as session:
            products = session.query(Product).all()
    return products


def get_product(id):
    with Session() as session:
            product = session.query(Product).filter_by(id=id).first()
            # product = session.query(Product).get(id)
    return product

def add_user(name, phone, address):
    with Session() as session:
        new_user = User(
            name=name,
            phone=phone,
            address=address
        )
        session.add(new_user)
        session.commit()


def add_order(product_id, user_id):
    with Session() as session:
        new_order = Order(
            product_id = product_id,
            user_id = user_id
        )
        session.add(new_order)
        session.commit()

    

def get_users():
    with Session() as session:
            users = session.query(User).all()
    return len(users)

print(get_users())



def get_user(phone):
    with Session() as session:
            user = session.query(User).filter_by(phone=phone).first()
    return user




def get_orders(user_id):
    with Session() as session:
            orders = session.query(Order).filter_by(user_id=user_id).all()
            products = []
            for order in orders:
                 if order.product:
                      products.append({'id':order.product.id,'name':order.product.name, 
                                       'price':order.product.price ,'desc':order.product.description,
                                       'img':order.product.image})
                    
    return orders, products

