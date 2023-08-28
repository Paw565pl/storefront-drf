BEGIN;
SELECT setval(
        pg_get_serial_sequence('"store_collection"', 'id'),
        coalesce(max("id"), 1),
        max("id") IS NOT null
    )
FROM "store_collection";
SELECT setval(
        pg_get_serial_sequence('"store_promotion"', 'id'),
        coalesce(max("id"), 1),
        max("id") IS NOT null
    )
FROM "store_promotion";
SELECT setval(
        pg_get_serial_sequence('"store_product_promotions"', 'id'),
        coalesce(max("id"), 1),
        max("id") IS NOT null
    )
FROM "store_product_promotions";
SELECT setval(
        pg_get_serial_sequence('"store_product"', 'id'),
        coalesce(max("id"), 1),
        max("id") IS NOT null
    )
FROM "store_product";
SELECT setval(
        pg_get_serial_sequence('"store_customer"', 'id'),
        coalesce(max("id"), 1),
        max("id") IS NOT null
    )
FROM "store_customer";
SELECT setval(
        pg_get_serial_sequence('"store_order"', 'id'),
        coalesce(max("id"), 1),
        max("id") IS NOT null
    )
FROM "store_order";
SELECT setval(
        pg_get_serial_sequence('"store_address"', 'id'),
        coalesce(max("id"), 1),
        max("id") IS NOT null
    )
FROM "store_address";
SELECT setval(
        pg_get_serial_sequence('"store_orderitem"', 'id'),
        coalesce(max("id"), 1),
        max("id") IS NOT null
    )
FROM "store_orderitem";
SELECT setval(
        pg_get_serial_sequence('"store_cartitem"', 'id'),
        coalesce(max("id"), 1),
        max("id") IS NOT null
    )
FROM "store_cartitem";
SELECT setval(
        pg_get_serial_sequence('"store_review"', 'id'),
        coalesce(max("id"), 1),
        max("id") IS NOT null
    )
FROM "store_review";
COMMIT;