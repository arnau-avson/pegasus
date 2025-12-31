from backend.app import db

# Example model
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Data {self.name} - {self.value}>"

# Create all tables
def init_db():
    db.create_all()

if __name__ == "__main__":
    init_db()