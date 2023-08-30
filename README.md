# Storefront

This is an imagainary web store backend built in Django and DRF entirely for educational purposes.

### How to run it?

It is fairly simple thanks to docker. Simply run this command after **cloning the repository**.

```
docker-compose up --build -d
```

If you want to seed the database with sample data you can also run this command.

```
docker exec -t storefront-backend-1 python manage.py seed_db
```

That's all! Now simply hit [http://localhost:8000/store](http://localhost:8000/store) and explore available endpoints.
