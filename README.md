# Lois's Herbs Website

A Django-based website for a herbalist practice, featuring a blog system and appointment booking functionality.

## Project Structure

The project consists of two main Django apps:

### Blog App
- Allows posting herbal medicine articles and insights
- Categories include:
  - Herbal Medicine
  - Wellness Tips
  - Herbal Recipes
  - Health Insights
  - Treatment Information
- Features image upload capability for blog posts
- Draft/Published status for content management

### Bookings App
- Appointment scheduling system
- Client management
- Service catalog
- Testimonials system

## Technical Setup

### Database
- PostgreSQL database
- Name: `loiss_herbs`

### Dependencies
- Django
- Pillow (for image handling)
- psycopg2-binary (PostgreSQL adapter)

## Development Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL database:
```bash
createdb loiss_herbs
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

## Current Features
- Blog post management system
- Appointment booking system
- Client information management
- Service catalog
- Testimonials system

## Next Steps
- Frontend development
- User authentication
- Custom blog management interface
- Appointment scheduling interface
- Email notifications
