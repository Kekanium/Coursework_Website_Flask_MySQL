INSERT INTO customerorder (idCustomer, OrderDate, OrderSum, OrderStatus, OrderStatusDate)
VALUES ($idCustomer, CURDATE(), $OrderSum, $OrderStatus, CURDATE())