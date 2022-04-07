SELECT idOrder,
       OrderSum,
       OrderDate,
       OrderStatus,
       OrderStatusDate
FROM customerorder
WHERE idCustomer = $customerName OR $allOrders