SELECT idProduct, Name, ActualQuantity, FixationDate, ReservedProduct, ReservationDate
FROM product
WHERE ActualQuantity <= $quantityProduct
