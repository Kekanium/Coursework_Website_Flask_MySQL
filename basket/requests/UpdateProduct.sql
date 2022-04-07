UPDATE product
SET ActualQuantity= $ActualQuantity,
    ReservedProduct=$ReservedProduct,
    ReservationDate=CURDATE()
WHERE idProduct = $idProduct