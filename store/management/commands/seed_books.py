from django.core.management.base import BaseCommand
from store.models import Category, Book

class Command(BaseCommand):
    help = 'Seeds the database with book categories and high-quality initial books'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database categories and books...')

        # 1. Seed Categories
        categories_to_seed = ["Fiction", "Non-fiction", "Education", "Technology", "Science", "Biography"]
        category_objects = {}
        
        for cat_name in categories_to_seed:
            cat_obj, created = Category.objects.get_or_create(name=cat_name)
            category_objects[cat_name] = cat_obj
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {cat_name}"))

        # 2. Seed Books
        books_data = [
            {
                "title": "The Pragmatic Programmer",
                "author": "David Thomas & Andrew Hunt",
                "category": "Technology",
                "price": 39.99,
                "description": "One of the most significant books in software development. Filled with classic advice on writing clean, modular, and reusable code, personal responsibility, career development, and structural techniques for maintaining code quality.",
                "image_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&q=80&w=400",
                "is_featured": True,
                "is_bestseller": True,
                "is_new_arrival": False
            },
            {
                "title": "Clean Code",
                "author": "Robert C. Martin",
                "category": "Technology",
                "price": 37.50,
                "description": "Even bad code can function. But if code isn't clean, it can bring a development organization to its knees. This book is a must-read for any developer who wants to write better, highly maintainable code using rigorous craftsmanship.",
                "image_url": "https://images.unsplash.com/photo-1629654297299-c8506221ca97?auto=format&fit=crop&q=80&w=400",
                "is_featured": True,
                "is_bestseller": False,
                "is_new_arrival": False
            },
            {
                "title": "A Brief History of Time",
                "author": "Stephen Hawking",
                "category": "Science",
                "price": 14.99,
                "description": "A landmark volume in science writing by one of the world's great minds. Hawking explains the complex models of cosmology, black holes, the big bang, gravity, and the universe for the general non-specialist reader.",
                "image_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&q=80&w=400",
                "is_featured": True,
                "is_bestseller": False,
                "is_new_arrival": False
            },
            {
                "title": "Dune",
                "author": "Frank Herbert",
                "category": "Fiction",
                "price": 12.99,
                "description": "Set on the desert planet Arrakis, Dune is the story of the boy Paul Atreides, who would become the mysterious man known as Muad'Dib. It explores politics, religion, ecology, and technology in a vast, multi-layered galactic empire.",
                "image_url": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?auto=format&fit=crop&q=80&w=400",
                "is_featured": False,
                "is_bestseller": True,
                "is_new_arrival": False
            },
            {
                "title": "Steve Jobs",
                "author": "Walter Isaacson",
                "category": "Biography",
                "price": 18.99,
                "description": "Based on more than forty interviews with Steve Jobs conducted over two years—as well as interviews with more than a hundred family members, friends, adversaries, competitors, and colleagues—this is the definitive biography of a creative visionary.",
                "image_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=400",
                "is_featured": False,
                "is_bestseller": False,
                "is_new_arrival": True
            },
            {
                "title": "The Hobbit",
                "author": "J.R.R. Tolkien",
                "category": "Fiction",
                "price": 10.99,
                "description": "Written for J.R.R. Tolkien's own children, The Hobbit met with instant critical acclaim when it was first published. It is a timeless modern classic about the adventures of Bilbo Baggins in Middle-earth.",
                "image_url": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?auto=format&fit=crop&q=80&w=400",
                "is_featured": False,
                "is_bestseller": False,
                "is_new_arrival": True
            },
            {
                "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
                "author": "Erich Gamma, Richard Helm, Ralph Johnson & John Vlissides",
                "category": "Technology",
                "price": 49.99,
                "description": "A landmark software engineering book that cataloged 23 classic design patterns in object-oriented software design. A fundamental guide for software architects and senior programmers worldwide.",
                "image_url": "https://images.unsplash.com/photo-1605379399642-870262d3d051?auto=format&fit=crop&q=80&w=400",
                "is_featured": False,
                "is_bestseller": False,
                "is_new_arrival": False
            },
            {
                "title": "Sapiens: A Brief History of Humankind",
                "author": "Yuval Noah Harari",
                "category": "Non-fiction",
                "price": 16.99,
                "description": "Harari spans the whole of human history, from the very first humans to walk the earth to the radical breakthroughs of the Cognitive, Agricultural, and Scientific Revolutions, exploring how our societies were built.",
                "image_url": "https://images.unsplash.com/photo-1463320306483-b407ebea7ecb?auto=format&fit=crop&q=80&w=400",
                "is_featured": False,
                "is_bestseller": True,
                "is_new_arrival": False
            },
            {
                "title": "Cosmos",
                "author": "Carl Sagan",
                "category": "Science",
                "price": 15.99,
                "description": "Sagan explores 15 billion years of cosmic evolution and the development of science and civilization. Beautifully written, Cosmos covers space exploration, astronomy, philosophy, and the future of humankind.",
                "image_url": "https://images.unsplash.com/photo-1506703719100-a0f3a48c0f86?auto=format&fit=crop&q=80&w=400",
                "is_featured": False,
                "is_bestseller": False,
                "is_new_arrival": True
            },
            {
                "title": "Educated: A Memoir",
                "author": "Tara Westover",
                "category": "Biography",
                "price": 13.50,
                "description": "An unforgettable memoir about a young girl who, kept out of school by survivalist parents in rural Idaho, leaves her isolated family to teach herself enough mathematics and grammar to enter college and earn a PhD from Cambridge University.",
                "image_url": "https://images.unsplash.com/photo-1531988042231-d39a9cc12a9a?auto=format&fit=crop&q=80&w=400",
                "is_featured": False,
                "is_bestseller": True,
                "is_new_arrival": False
            },
            {
                "title": "Introduction to Algorithms",
                "author": "Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest & Clifford Stein",
                "category": "Education",
                "price": 89.99,
                "description": "Commonly known as CLRS, this is the definitive, rigorous textbook covering all aspects of modern computer algorithms. It offers a comprehensive design and analysis framework for students and engineers.",
                "image_url": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&q=80&w=400",
                "is_featured": True,
                "is_bestseller": False,
                "is_new_arrival": False
            },
            {
                "title": "Zero to One: Notes on Startups, or How to Build the Future",
                "author": "Peter Thiel",
                "category": "Non-fiction",
                "price": 14.50,
                "description": "Legendary entrepreneur and investor Peter Thiel shows how we can find singular ways to create new things, moving our technology and business landscapes from zero to one rather than incrementally copying others.",
                "image_url": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&q=80&w=400",
                "is_featured": False,
                "is_bestseller": True,
                "is_new_arrival": False
            },
            {
                "title": "Grokking Algorithms",
                "author": "Aditya Bhargava",
                "category": "Education",
                "price": 29.99,
                "description": "An illustrated, friendly guide that teaches you how to apply common algorithms to practical problems in computer science. Written with cartoon sketches and simplified mathematical breakdowns, it is the perfect introduction for visual learners.",
                "image_url": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&q=80&w=400",
                "is_featured": False,
                "is_bestseller": False,
                "is_new_arrival": True
            }
        ]

        for b_info in books_data:
            cat_obj = category_objects.get(b_info["category"])
            if not cat_obj:
                continue
                
            book_obj, created = Book.objects.get_or_create(
                title=b_info["title"],
                defaults={
                    "author": b_info["author"],
                    "category": cat_obj,
                    "price": b_info["price"],
                    "description": b_info["description"],
                    "image_url": b_info["image_url"],
                    "is_featured": b_info["is_featured"],
                    "is_bestseller": b_info["is_bestseller"],
                    "is_new_arrival": b_info["is_new_arrival"],
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created book: {b_info['title']}"))
            else:
                # Update existing records to match seed data
                book_obj.author = b_info["author"]
                book_obj.category = cat_obj
                book_obj.price = b_info["price"]
                book_obj.description = b_info["description"]
                book_obj.image_url = b_info["image_url"]
                book_obj.is_featured = b_info["is_featured"]
                book_obj.is_bestseller = b_info["is_bestseller"]
                book_obj.is_new_arrival = b_info["is_new_arrival"]
                book_obj.save()
                self.stdout.write(f"Updated book: {b_info['title']}")

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
