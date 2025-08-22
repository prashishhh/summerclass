# Islington Marketplace (Django)

A student-first campus marketplace for Islington College. Students can browse categories, discover featured deals, view product detail with variations (size/color), add items to cart, and contact sellers. Admins can approve listings and feature products for the homepage “Great Offer” spotlight.

## Features

### Public (browsing & search)
- Modern homepage with:
  - Banner carousel (admin-managed)
  - Curated category hero cards
  - **Popular Products** (latest approved items)
  - **Great Offer** spotlight (prefers `is_featured=True`, falls back to newest)
- Category listing pages (pagination)
- Full-text search on product name & description
- Product detail page:
  - Product images, description, price and optional `old_price`
  - Stock indicator
  - Variation selectors (Color, Size) – only active variations shown
- Add to Cart (by product + chosen variations)
- Responsive design (Bootstrap + custom CSS)

### Sellers & Profiles
- Product owner field (seller)
- Seller profile page: list of the seller’s active products
- “Message Seller” flow (sends site message + optional email)

### Admin / Content Management
- Approvals: `is_approved` gate for visibility
- Feature switch: `is_featured` for the homepage spotlight
- Optional `old_price` shown struck-through if set
- Categories with optional image (fallback to default image)
- Banners with status toggle

## Tech Stack

- Django 5.x, Python 3.13
- SQLite (default) or your DB of choice
- Bootstrap 4, jQuery (bundled in static files)
- Pillow for image handling

---

## Setup & Run (Local)

> **Prereqs:** Python 3.13, pip, virtualenv

```bash
# 1) Create & activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Environment variables (optional)
# Create a .env or export the following for email, etc. (if used)
# EMAIL_HOST=...
# EMAIL_HOST_USER=...
# EMAIL_HOST_PASSWORD=...

# 4) Migrate database
python manage.py migrate

# 5) Create a superuser for admin access
python manage.py createsuperuser

# 6) (Optional) Load seed data or add via admin
# python manage.py loaddata seed.json

# 7) Run the server
python manage.py runserver
