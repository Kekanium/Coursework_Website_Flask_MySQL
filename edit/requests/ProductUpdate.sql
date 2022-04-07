UPDATE product
SET Name       = '$Name',
    Material   = '$Material',
    UnitOfMeasurement = '$UnitOfMeasurement',
    PricePerUnit=$PricePerUnit,
    ActualQuantity=$ActualQuantity,
    FixationDate='$FixationDate',
    ReservedProduct=$ReservedProduct,
    ReservationDate='$ReservationDate'

WHERE idProduct = $idProduct