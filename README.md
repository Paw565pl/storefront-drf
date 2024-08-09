# Storefront

This is an imaginary web store backend built in Django and DRF entirely for educational purposes.

### How to run it locally?

It is fairly simple thanks to docker. Simply run this command after **cloning the repository**.

```sh
docker compose -f docker-compose.dev.yml up --build --watch
```

If you want to seed the database with sample data you can also run this command.

```sh
docker compose -f docker-compose.dev.yml exec backend python manage.py seed_db
```

That's all! Now simply hit [http://localhost:8000](http://localhost:8000) and explore available endpoints. API is
documented on this URL [http://localhost:8000/schema/swagger-ui/](http://localhost:8000/schema/swagger-ui/).
