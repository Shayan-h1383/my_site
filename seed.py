from app import create_app
from app.models import User, Book  # Import Book model
from werkzeug.security import generate_password_hash
from app import db

# Create the application context
app = create_app()

with app.app_context():
    # Check if the user "shayan" already exists
    user = User.query.filter_by(username="shayan").first()

    if not user:
        # If the user does not exist, create a new one
        new_user = User(username="shayan", password=generate_password_hash("1234"))
        db.session.add(new_user)
        db.session.commit()
        print("User 'shayan' added to the database!")
    else:
        print("User 'shayan' already exists.")

    # Remove duplicate books by checking their title
    existing_books = Book.query.all()
    seen_books = set()  # To track titles we have seen
    for book in existing_books:
        if book.title in seen_books:
            # If we've seen this book title already, delete it
            db.session.delete(book)
            print(f"Duplicate book '{book.title}' removed from the database.")
        else:
            seen_books.add(book.title)

    db.session.commit()  # Commit after deleting duplicates

    # Adding books to the database if they don't exist
    books = [
        {"title": "Cirque du Freak", "description": "Follow the spine-chilling journey of Darren Shan, a regular schoolboy drawn into the vampire underworld. The Saga of Darren Shan, Book 1: Darren and his best friend, Steve, attend a forbidden freak show, the eerie Cirque Du Freak, featuring bizarre half-human, half-animal performers who interact frighteningly with the crowd."},
        {"title": "The Vampire's Assistant", "description": "Turned into a half-vampire by Mr. Crepsley, Darren discovers the Cirque Du Freak holds more grim revelations for him. The Saga of Darren Shan, Book 2: Darren accompanies Mr. Crepsley as his assistant, returning to the mysterious world of the Cirque."},
        {"title": "Tunnels of Blood", "description": "Darren Shan and Evra Von follow a series of gruesome murders, encountering a sinister creature of the night. The Saga of Darren Shan, Book 3: When Mr. Crepsley is summoned by the Vampire Generals, Darren and Evra leave the Cirque Du Freak for a perilous trip to the city."},
        {"title": "Vampire Mountain", "description": "Darren, now Mr. Crepsley’s assistant, faces a dangerous journey to Vampire Mountain, where the Vampire Princes will decide his fate. The Saga of Darren Shan, Book 4: The treacherous trek to the vampires’ mountain stronghold tests Darren and his mentor."},
        {"title": "Trials of Death", "description": "The fifth installment in Darren Shan's saga introduces the harrowing trials he must face to prove his loyalty to the vampire clan. The Saga of Darren Shan, Book 5: Darren undertakes life-threatening challenges, driven by his devotion to Mr. Crepsley and the vampire way."},
        {"title": "The Vampire Prince", "description": "Darren Shan must clear his name and avenge Gavner Purl’s death while evading a ruthless Vampire Prince. The Saga of Darren Shan, Book 6: Betrayed by Kurda and reeling from Gavner’s murder, Darren, now a fugitive, is pursued by his own kind."},
        {"title": "Hunters of the Dusk", "description": "Darren Shan, Mr. Crepsley, and Vancha Marsch take on the quest to find the Vampaneze Lord, facing unexpected challenges. The Saga of Darren Shan, Book 7: Six years after becoming a Vampire Prince, Darren is part of a prophecy predicting the rise of the Vampaneze Lord."},
        {"title": "Allies of the Night", "description": "Darren’s pursuit of the Vampaneze Lord leads him back to school, where his past collides with his present. The Saga of Darren Shan, Book 8: Despite his appearance as a teenager, Darren’s maturity surpasses his years as he juggles his human and vampire lives."},
        {"title": "Killers of the Dawn", "description": "As the final showdown looms, Darren and his allies face unforeseen dangers in their confrontation with the Vampaneze Lord. The Saga of Darren Shan, Book 9: Darren evolves from human to half-vampire to Vampire Prince while navigating the bloodiest battle yet."},
        {"title": "The Lake of Souls", "description": "In this tenth chapter of Darren Shan’s saga, the protagonist embarks on a dangerous journey beyond life itself. The Saga of Darren Shan, Book 10: Following Harkat into the unknown, Darren risks everything in a world he might never escape."},
        {"title": "Lord of the Shadows", "description": "In the penultimate installment, Darren's destiny becomes clearer as he moves closer to ruling the night and facing ultimate destruction. The Saga of Darren Shan, Book 11: A dark prophecy reveals Darren’s power to shape or shatter the world."},
        {"title": "Sons of Destiny", "description": "The saga’s epic conclusion pits Darren against his nemesis, Steve Leopard, in a battle for fate itself. The Saga of Darren Shan, Book 12: The climactic final confrontation challenges Darren to outwit destiny or uncover an unexpected way out."}
    ]

    for book in books:
        # Check if the book already exists
        existing_book = Book.query.filter_by(title=book["title"]).first()
        if not existing_book:
            new_book = Book(title=book["title"], description=book["description"])
            db.session.add(new_book)
            print(f"Book '{book['title']}' added to the database!")
        else:
            print(f"Book '{book['title']}' already exists.")

    db.session.commit()  # Commit after adding new books
